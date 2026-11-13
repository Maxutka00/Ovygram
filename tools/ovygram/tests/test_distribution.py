"""Distribution tests use real Ed25519 signatures and an in-memory transport.

No package network access or Telegram profile is needed. The fake registry
speaks the same signed JSON protocol as the server.
"""

import base64
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
import urllib.parse

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "Telegram/PluginSDK"))
from ovygram_registry import Registry, canonical, json_document, protected_author
from ovygram_runtime import Manager

EXAMPLE = ROOT / "tools/ovygram/examples/lifecycle.ovyplugin"


@unittest.skipUnless(shutil.which("openssl"), "OpenSSL CLI needed to sign test answers")
class DistributionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.now = datetime.now(timezone.utc)
        self.private = self.root / "key.der"
        self.private.write_bytes(bytes.fromhex("302e020100300506032b657004220420") + bytes(range(32)))
        public = subprocess.check_output(["openssl", "pkey", "-inform", "DER", "-in", str(self.private),
                                          "-pubout", "-outform", "DER"])[-32:]
        self.key_id = hashlib.sha256(public).hexdigest()[:16]
        self.records = {}
        self.downloads = {}
        self.calls = []
        self.index = {}
        self.chain = []
        self.offline = False
        self.registry = Registry({"server_url": "https://registry.test", "index_url": "https://files.test/index.json",
                                  "public_keys": {self.key_id: base64.b64encode(public).decode()}},
                                 fetch=self.fetch, now=lambda: self.now)
        self.manager = Manager(self.root / "profile", registry=self.registry)
        self.addCleanup(self.manager.shutdown)
        self.manager.runtime.sender = lambda command: None

    def sign(self, answer):
        answer = {"issued_at": self.now.isoformat(), "expires_at": (self.now + timedelta(days=7)).isoformat(),
                  "key_id": self.key_id, **answer}
        path = self.root / "message.json"
        path.write_bytes(canonical(answer))
        signature = subprocess.check_output(["openssl", "pkeyutl", "-sign", "-rawin", "-inkey",
                                              str(self.private), "-keyform", "DER", "-in", str(path)])
        return {**answer, "signature": base64.b64encode(signature).decode()}

    def fetch(self, url, limit):
        self.calls.append(url)
        if self.offline:
            raise OSError("network unavailable")
        if url in self.downloads:
            return self.downloads[url]
        if url == self.registry.index_url:
            return json.dumps({"plugins": self.index}).encode()
        parsed = urllib.parse.urlsplit(url)
        if parsed.path == "/v1/check":
            query = urllib.parse.parse_qs(parsed.query)
            digest = query["sha256"][0]
            record = self.records.get(digest, {"sha256": digest, "plugin_id": query["plugin_id"][0],
                                               "package_type": query["package_type"][0], "status": "unverified"})
            return json.dumps(self.sign(record)).encode()
        if parsed.path.startswith("/v1/chains/"):
            return json.dumps(self.sign({"chain": 7, "plugin_id": "lifecycle", "versions": self.chain})).encode()
        raise ValueError("Unexpected URL: " + url)

    def source(self, version="1.0.0", extra="", release=True):
        text = EXAMPLE.read_text().replace('"1.0.0"', repr(version))
        # The example is deliberately local-only.
        import re
        text = re.sub(r"__release__\s*=\s*(True|False)", "__release__ = " + repr(release), text)
        return (text + "\n" + extra).encode()

    def approve(self, payload, version="1.0.0", sequence=1, status="verified", chain=7, release=True):
        digest = hashlib.sha256(payload).hexdigest()
        self.records[digest] = {"sha256": digest, "plugin_id": "lifecycle", "package_type": "ovyplugin",
                                "version": version, "release_sequence": sequence, "chain": chain,
                                "release": release, "status": status,
                                "publication": "published" if release else None,
                                "url": "https://files.test/published/lifecycle.ovyplugin" if release else None}
        return digest

    def wait(self, token):
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            self.manager.distribution.poll()
            job = self.manager.distribution.jobs.get(token)
            if job is None or job["state"] != "pending":
                return job
            time.sleep(.005)
        self.fail("background job timed out")

    def prepare(self, payload):
        path = self.root / "lifecycle.ovyplugin"
        path.write_bytes(payload)
        token = self.manager.distribution.prepare(str(path))
        self.assertEqual(self.wait(token)["state"], "ready")
        return token, path

    def install(self, payload=None, **kwargs):
        token, _ = self.prepare(payload or self.source())
        return self.manager.distribution.commit(token, **kwargs)

    def check(self):
        self.manager.distribution.start_check(manual=True)
        token = next(token for token, job in self.manager.distribution.jobs.items() if job["operation"] == "check")
        self.wait(token)

    def offer(self, version="1.1", sequence=2, extra="", chain=7):
        payload = self.source(version, extra)
        digest = self.approve(payload, version, sequence, chain=chain)
        url = "https://files.test/lifecycle.ovyplugin"
        self.downloads[url] = payload
        self.index["lifecycle"] = {"latest_version": version, "release_sequence": sequence, "url": url}
        return digest, url

    def test_signed_exact_file_is_trusted_and_persisted(self):
        self.approve(self.source())
        identity = self.install()
        plugin = self.manager.describe(identity)
        self.assertEqual(plugin["trust"]["status"], "verified")
        self.assertEqual(plugin["trust"]["release_sequence"], 1)
        self.assertEqual(json.loads(self.manager.state.read_text())["installations"][identity]["current"]["trust"]["chain"], 7)

    def test_tampered_unknown_or_expired_signatures_never_grant_trust(self):
        self.approve(self.source())
        answer = self.registry.check({"id": "lifecycle", "version": "1.0.0", "release": True},
                                     hashlib.sha256(self.source()).hexdigest(), "ovyplugin")
        self.registry.validate(answer)
        for field, value in (("status", "official"), ("chain", 8), ("key_id", "unknown")):
            with self.subTest(field=field), self.assertRaises(Exception):
                self.registry.validate({**answer, field: value})
        self.now += timedelta(days=8)
        with self.assertRaises(ValueError):
            self.registry.validate(answer)

    def test_mismatched_id_type_or_version_is_unavailable(self):
        digest = self.approve(self.source())
        metadata = {"id": "lifecycle", "version": "1.0.0", "release": True}
        for field, value in (("plugin_id", "other"), ("package_type", "ovyzip"), ("version", "9.0"), ("chain", True)):
            old = self.records[digest][field]
            self.records[digest][field] = value
            self.assertEqual(self.registry.check(metadata, digest, "ovyplugin")["status"], "verification_unavailable")
            self.records[digest][field] = old

    def test_blocked_install_is_refused(self):
        self.approve(self.source(), status="blocked")
        with self.assertRaisesRegex(ValueError, "запрещена"):
            self.install()
        self.assertFalse(self.manager.records)

    def test_offline_requires_separate_confirmation(self):
        self.offline = True
        with self.assertRaisesRegex(ValueError, "подтверждение"):
            self.install()
        identity = self.install(allow_unavailable=True)
        self.assertEqual(self.manager.describe(identity)["trust"]["status"], "verification_unavailable")

    def test_uses_prepared_bytes_after_original_file_changes(self):
        original = self.source()
        self.approve(original)
        token, path = self.prepare(original)
        path.write_bytes(self.source("8.0"))
        identity = self.manager.distribution.commit(token)
        self.assertEqual(Path(self.manager.share_file(identity)).read_bytes(), original)

    def test_separate_trusted_duplicate_is_refused(self):
        self.approve(self.source())
        self.install()
        with self.assertRaisesRegex(ValueError, "Два проверенных"):
            self.install(separate=True)

    def test_trust_loss_requires_confirmation_and_separate_data_is_empty(self):
        self.approve(self.source())
        identity = self.install()
        self.manager.set_setting(identity, "secret", "private")
        unknown = self.source("1.1")
        with self.assertRaisesRegex(ValueError, "потери проверки"):
            self.install(unknown, installation_id=identity)
        separate = self.install(unknown, separate=True)
        self.assertEqual(self.manager.records[separate]["settings"], {})
        self.install(unknown, installation_id=identity, allow_loss=True)
        self.assertEqual(self.manager.describe(identity)["trust"]["status"], "unverified")

    def test_verified_to_blocked_disables_and_latches_during_outage(self):
        digest = self.approve(self.source())
        identity = self.install()
        self.manager.enable(identity)
        self.records[digest]["status"] = "blocked"
        self.check()
        self.assertFalse(self.manager.records[identity]["enabled"])
        self.assertNotIn(identity, self.manager.loaded)
        self.offline = True
        self.check()
        with self.assertRaisesRegex(ValueError, "запрещён"):
            self.manager.enable(identity)
        self.assertEqual(self.manager.describe(identity)["trust"]["status"], "blocked")

    def test_revoked_does_not_automatically_disable(self):
        digest = self.approve(self.source())
        identity = self.install()
        self.manager.enable(identity)
        self.records[digest]["status"] = "revoked"
        self.check()
        self.assertIn(identity, self.manager.loaded)
        self.assertEqual(self.manager.describe(identity)["trust"]["status"], "revoked")

    def test_outage_removes_green_badge_but_retains_chain_for_retry(self):
        self.approve(self.source())
        identity = self.install()
        self.offline = True
        self.check()
        self.assertEqual(self.manager.describe(identity)["trust"]["status"], "verification_unavailable")
        self.assertEqual(self.manager.records[identity]["current"]["trust"]["chain"], 7)
        self.offline = False
        self.check()
        self.assertEqual(self.manager.describe(identity)["trust"]["status"], "verified")

    def test_incompatible_update_leaves_working_code(self):
        self.approve(self.source())
        identity = self.install()
        _, url = self.offer()
        import re
        self.downloads[url] = re.sub(rb"__desktop_sdk__\s*=\s*\d+", b"__desktop_sdk__ = 999", self.downloads[url])
        self.assertIn(b"__desktop_sdk__ = 999", self.downloads[url])
        self.check()
        self.wait(self.manager.distribution.apply_offer(identity))
        self.assertEqual(self.manager.describe(identity)["version"], "1.0.0")

    def test_injected_bytecode_or_module_is_refused(self):
        self.approve(self.source())
        identity = self.install()
        directory = self.manager.directory(self.manager.records[identity]["current"])
        for filename in ("injected.py", "injected.pyc", "native.so"):
            path = directory / filename
            path.write_bytes(b"injected")
            with self.assertRaisesRegex(RuntimeError, "посторонний"):
                self.manager.enable(identity)
            path.unlink()

    def test_index_cannot_authorize_replaced_payload(self):
        self.approve(self.source())
        identity = self.install()
        _, url = self.offer()
        self.downloads[url] = self.source("9.0")
        self.check()
        self.wait(self.manager.distribution.apply_offer(identity))
        self.assertEqual(self.manager.describe(identity)["version"], "1.0.0")

    def test_approved_but_unpublished_update_is_refused(self):
        self.approve(self.source())
        identity = self.install()
        digest, _ = self.offer()
        self.records[digest]["publication"] = "pending"
        self.records[digest]["url"] = None
        self.check()
        self.wait(self.manager.distribution.apply_offer(identity))
        self.assertEqual(self.manager.describe(identity)["version"], "1.0.0")

    def test_sequence_does_not_authorize_an_equivalent_text_version(self):
        self.approve(self.source())
        identity = self.install()
        old = self.manager.records[identity]["current"]["directory"]
        self.offer("1.0.0", 2, extra="# Different bytes, equivalent version")
        self.check()
        self.wait(self.manager.distribution.apply_offer(identity))
        self.assertEqual(self.manager.records[identity]["current"]["directory"], old)

    def test_incompatible_latest_selects_newest_compatible_from_info(self):
        import re
        self.approve(self.source())
        identity = self.install()
        latest = re.sub(rb"__desktop_sdk__\s*=\s*\d+", b"__desktop_sdk__ = 3", self.source("1.3"))
        compatible = self.source("1.2")
        self.approve(latest, "1.3", 3)
        self.approve(compatible, "1.2", 2)
        latest_url = "https://files.test/1.3/lifecycle.ovyplugin"
        compatible_url = "https://files.test/1.2/lifecycle.ovyplugin"
        info_url = "https://files.test/info.json"
        self.downloads.update({latest_url: latest, compatible_url: compatible,
                               info_url: json.dumps({"id": "lifecycle", "versions": [
                                   {"version": "1.2", "release_sequence": 2, "url": compatible_url},
                                   {"version": "1.3", "release_sequence": 3, "url": latest_url}]}).encode()})
        self.index["lifecycle"] = {"latest_version": "1.3", "release_sequence": 3,
                                    "url": latest_url, "info_url": info_url}
        self.check()
        self.wait(self.manager.distribution.apply_offer(identity))
        self.assertEqual(self.manager.describe(identity)["version"], "1.2")
        self.assertEqual(self.calls.count(latest_url), 1)
        self.assertEqual(self.calls.count(compatible_url), 1)
        self.assertEqual(self.calls.count(info_url), 1)

    def test_update_preserves_identity_settings_and_running_state(self):
        self.approve(self.source())
        identity = self.install()
        self.manager.enable(identity)
        self.manager.set_setting(identity, "secret", 42)
        _, url = self.offer("1.10")
        self.check()
        self.wait(self.manager.distribution.apply_offer(identity))
        self.assertEqual(self.manager.describe(identity)["version"], "1.10")
        self.assertEqual(self.manager.records[identity]["settings"]["secret"], 42)
        self.assertIn(identity, self.manager.loaded)
        self.assertEqual(self.calls.count(url), 1)
        self.assertIsNotNone(self.manager.records[identity]["previous"])

    def test_activation_failure_restores_working_code_and_settings(self):
        self.approve(self.source())
        identity = self.install()
        self.manager.enable(identity)
        old = self.manager.records[identity]["current"]["directory"]
        self.offer(extra='raise RuntimeError("broken release")')
        self.check()
        self.wait(self.manager.distribution.apply_offer(identity))
        self.assertEqual(self.manager.records[identity]["current"]["directory"], old)
        self.assertIn(identity, self.manager.loaded)
        self.assertTrue(self.manager.records[identity]["enabled"])
        self.assertFalse(self.manager.pending_updates)

    def test_process_exit_during_activation_restores_durable_previous_state(self):
        self.approve(self.source())
        identity = self.install()
        self.manager.enable(identity)
        self.manager.set_setting(identity, "secret", 42)
        old_directory = self.manager.records[identity]["current"]["directory"]
        profile = self.manager.root
        self.manager.shutdown()
        # Exit after replacing state/code and before activation completes.
        # Only Python runs here: no native compilation or host executable.
        script = '''import os, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from ovygram_runtime import Manager, read_package
manager = Manager(sys.argv[2])
manager.runtime.sender = lambda command: None
payload = Path(sys.argv[3]).read_bytes().replace(b'"1.0.0"', b'"2.0"')
metadata, kind = read_package(payload, 'lifecycle.ovyplugin')
manager.enable = lambda identity: os._exit(73)
manager.activate_update(sys.argv[4], {'payload': payload, 'metadata': metadata,
    'package_type': kind, 'trust': {'status': 'verified'}})
'''
        result = subprocess.run([sys.executable, "-B", "-c", script, str(ROOT / "Telegram/PluginSDK"),
                                 str(profile), str(EXAMPLE), identity], capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 73, result.stderr.decode())
        interrupted = json.loads((profile / "state.json").read_text())
        self.assertTrue(interrupted["pending_updates"])
        self.assertEqual(interrupted["installations"][identity]["current"]["metadata"]["version"], "2.0")
        self.manager = Manager(profile, registry=self.registry)
        self.addCleanup(self.manager.shutdown)
        self.assertEqual(self.manager.records[identity]["current"]["directory"], old_directory)
        self.assertEqual(self.manager.records[identity]["settings"]["secret"], 42)
        self.assertTrue(self.manager.records[identity]["enabled"])
        self.assertFalse(self.manager.pending_updates)
        self.assertFalse(json.loads((profile / "state.json").read_text())["pending_updates"])

    def test_unverified_wrong_chain_or_missing_download_does_not_replace(self):
        self.approve(self.source())
        identity = self.install()
        old = self.manager.records[identity]["current"]["directory"]
        digest, url = self.offer(chain=8)
        self.check()
        self.wait(self.manager.distribution.apply_offer(identity))
        self.assertEqual(self.manager.records[identity]["current"]["directory"], old)
        self.records[digest]["status"] = "unverified"
        self.check()
        self.wait(self.manager.distribution.apply_offer(identity))
        self.assertEqual(self.manager.records[identity]["current"]["directory"], old)
        self.downloads.pop(url)
        self.check()
        self.wait(self.manager.distribution.apply_offer(identity))
        self.assertEqual(self.manager.records[identity]["current"]["directory"], old)

    def test_unverified_id_never_binds_to_public_updates(self):
        identity = self.install()
        self.offer()
        self.check()
        self.assertNotIn(identity, self.manager.distribution.offers)

    def test_private_release_does_not_offer_public_updates(self):
        payload = self.source(release=False)
        self.approve(payload, release=False)
        identity = self.install(payload)
        self.offer()
        self.check()
        self.assertNotIn(identity, self.manager.distribution.offers)

    def test_safe_rollback_is_offered_and_rechecked(self):
        original = self.source()
        digest = self.approve(original)
        identity = self.install()
        target_digest, url = self.offer()
        self.check()
        self.wait(self.manager.distribution.apply_offer(identity))
        self.records[target_digest]["status"] = "blocked"
        old_url = "https://files.test/old/lifecycle.ovyplugin"
        self.downloads[old_url] = original
        self.chain = [{**self.records[digest], "url": old_url, "publication": "published"}]
        self.check()
        self.assertTrue(self.manager.distribution.offers[identity]["rollback"])
        self.wait(self.manager.distribution.apply_offer(identity))
        self.assertEqual(self.manager.describe(identity)["version"], "1.0.0")

    def test_two_local_intervals_survive_restart(self):
        first = datetime(2026, 11, 13, 9, tzinfo=timezone.utc)
        distribution = self.manager.distribution
        self.assertTrue(distribution.start_check(now=first))
        self.wait(next(iter(distribution.jobs)))
        self.assertFalse(distribution.start_check(now=first.replace(hour=11)))
        self.assertTrue(distribution.start_check(now=first.replace(hour=12)))
        self.wait(next(iter(distribution.jobs)))
        self.manager.shutdown()
        # Cleanup was registered for the original instance; shutdown is idempotent.
        self.manager = Manager(self.root / "profile", registry=self.registry)
        self.addCleanup(self.manager.shutdown)
        self.assertFalse(self.manager.distribution.start_check(now=first.replace(hour=13)))

    def test_local_private_previous_version_is_available_for_safe_rollback(self):
        old = self.source(release=False)
        self.approve(old, release=False)
        identity = self.install(old)
        new = self.source("1.1", release=False)
        digest = self.approve(new, "1.1", 2, release=False)
        self.install(new, installation_id=identity)
        self.records[digest]["status"] = "revoked"
        self.check()
        self.assertIn("local_directory", self.manager.distribution.offers[identity])
        self.wait(self.manager.distribution.apply_offer(identity))
        self.assertEqual(self.manager.describe(identity)["version"], "1.0.0")

    def test_remove_can_retain_settings_and_data(self):
        identity = self.install()
        self.manager.set_setting(identity, "keep", 42)
        directory = self.manager.root / "data" / identity
        directory.mkdir(parents=True)
        (directory / "data.txt").write_text("data")
        self.manager.remove(identity, keep_data=True)
        self.assertTrue(directory.exists())
        self.assertEqual(json.loads((self.manager.root / "retained" / identity / "settings.json").read_text())["settings"]["keep"], 42)


@unittest.skipUnless(os.environ.get("OVYGRAM_SMOKE_EXE"), "native host not staged")
class EmbeddedDistributionTests(unittest.TestCase):
    def test_prepare_warning_and_commit_through_embedded_host(self):
        import queue
        import threading
        with tempfile.TemporaryDirectory() as temporary:
            process = subprocess.Popen([os.environ["OVYGRAM_SMOKE_EXE"], temporary, "normal"],
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       text=True, encoding="utf-8")
            replies = queue.Queue()
            threading.Thread(target=lambda: [replies.put(line) for line in process.stdout], daemon=True).start()
            try:
                def request(**command):
                    process.stdin.write(json.dumps(command) + "\n")
                    process.stdin.flush()
                    return json.loads(replies.get(timeout=10))
                token = request(action="prepare_install", path=str(EXAMPLE))["result"]
                deadline = time.monotonic() + 10
                while True:
                    info = request(action="prepared_install", token=token)["result"]
                    if info["state"] != "pending":
                        break
                    self.assertLess(time.monotonic(), deadline)
                    time.sleep(.01)
                self.assertEqual(info["state"], "ready")
                self.assertEqual(info["trust"]["status"], "verification_unavailable")
                self.assertIn("error", request(action="commit_install", token=token))
                identity = request(action="commit_install", token=token, allow_unavailable=True)["result"]
                self.assertIn("result", request(action="enable", installation_id=identity))
                plugin = request(action="snapshot")["result"]["plugins"][0]
                self.assertTrue(plugin["loaded"])
                self.assertEqual(plugin["installation_id"], identity)
            finally:
                process.stdin.close()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
                stderr = process.stderr.read()
                process.stdout.close()
                process.stderr.close()
            self.assertEqual(process.returncode, 0, stderr)


class RegistryConfigurationTests(unittest.TestCase):
    def test_deployment_environment_overrides_endpoints_but_keeps_pinned_keys(self):
        config = {"server_url": "https://packaged.test", "index_url": "https://packaged.test/index.json",
                  "public_keys": {"pinned": "public-key"}}
        with patch("ovygram_registry.Path.read_bytes", return_value=json.dumps(config).encode()), \
                patch.dict(os.environ, {"OVYGRAM_REGISTRY_URL": "https://deployment.test/",
                                        "OVYGRAM_PLUGIN_INDEX_URL": "https://index.test/index.json"}):
            registry = Registry()
        self.assertEqual(registry.url, "https://deployment.test")
        self.assertEqual(registry.index_url, "https://index.test/index.json")
        self.assertEqual(registry.keys, config["public_keys"])

    def test_empty_environment_preserves_packaged_endpoints(self):
        config = {"server_url": "https://packaged.test", "index_url": "https://packaged.test/index.json"}
        with patch("ovygram_registry.Path.read_bytes", return_value=json.dumps(config).encode()), \
                patch.dict(os.environ, {"OVYGRAM_REGISTRY_URL": "", "OVYGRAM_PLUGIN_INDEX_URL": ""}):
            registry = Registry()
        self.assertEqual(registry.url, config["server_url"])
        self.assertEqual(registry.index_url, config["index_url"])

    def test_explicit_configuration_is_independent_of_environment(self):
        config = {"server_url": "https://explicit.test", "index_url": "https://explicit.test/index.json"}
        with patch.dict(os.environ, {"OVYGRAM_REGISTRY_URL": "https://unexpected.test",
                                    "OVYGRAM_PLUGIN_INDEX_URL": "https://unexpected.test/index.json"}):
            registry = Registry(config)
        self.assertEqual(registry.url, config["server_url"])
        self.assertEqual(registry.index_url, config["index_url"])


class AuthorAndJsonTests(unittest.TestCase):
    def test_reserved_author_confusables_and_invisibles(self):
        for author in ("OVYGRAM", "Оvygrаm", "Ovy\u200bgram", "Ovygrm", "Ovygram Team", "Ovygrarn"):
            self.assertTrue(protected_author(author, "unverified"), author)
            self.assertFalse(protected_author(author, "official"), author)
        for author in ("Alice", "Developer", "Programmer", "John Smith"):
            self.assertFalse(protected_author(author, "unverified"), author)

    def test_duplicate_json_and_nonfinite_numbers_are_refused(self):
        for payload in ('{"status":"blocked","status":"verified"}', '{"x":NaN}', '[]'):
            with self.assertRaises(ValueError):
                json_document(payload)
