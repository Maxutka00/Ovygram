import ast
import asyncio
import base64
from concurrent.futures import CancelledError
import copy
import hashlib
import json
from pathlib import Path
import queue
import struct
import sys
import tempfile
import unittest
from unittest.mock import AsyncMock, patch


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "Telegram/PluginSDK"))
sys.path.insert(0, str(ROOT / "tools/ovygram"))

from desktop import tl
from desktop import client, media
from desktop._runtime import RpcError, context
from desktop.models import Attachment, Chat, Message
from desktop_utils import run_on_ui
from generate_tl import parse_schema, stubs
from hook_utils import CANCEL, MODIFY, MODIFY_FINAL, HookCancelled, HookError, HookResult
from ovygram_runtime import Manager


class CodecTests(unittest.TestCase):
    def test_all_generated_types_match_the_pinned_schema(self):
        schema = ROOT / "Telegram/SourceFiles/mtproto/scheme/api.tl"
        catalogue = json.loads((ROOT / "Telegram/PluginSDK/desktop/tl/schema.json").read_text(encoding="utf-8"))
        self.assertEqual(catalogue["declarations"], parse_schema(schema.read_text(encoding="utf-8")))
        self.assertEqual(catalogue["schema_sha256"], hashlib.sha256(schema.read_text(encoding="utf-8").encode()).hexdigest())
        generated_stubs = stubs(catalogue["declarations"])
        self.assertEqual((ROOT / "Telegram/PluginSDK/desktop/tl/__init__.pyi").read_text(encoding="utf-8"), generated_stubs)
        ast.parse(generated_stubs)
        import keyword
        for declaration in catalogue["declarations"]:
            exported = tl
            for part in declaration["name"].split("."):
                exported = getattr(exported, part + "_" if keyword.iskeyword(part) or part == "self" else part)
            self.assertEqual(exported._tl["id"], declaration["id"])

    def test_known_wire_fixture_and_flags_round_trip(self):
        self.assertEqual(tl.encode(tl.inputPeerSelf()), bytes.fromhex("c97ea07d"))
        request = tl.messages.sendMessage(peer=tl.inputPeerSelf(), message="Привет", random_id=123,
                                          silent=True, no_webpage=True)
        encoded = tl.encode(request)
        self.assertEqual(struct.unpack_from("<I", encoded, 4)[0], (1 << 5) | (1 << 1))
        self.assertEqual(tl.decode(encoded), request)
        self.assertEqual(tl.updates.getState().constructor_name, "updates.getState")

    def test_vectors_bytes_and_response_type_validation(self):
        request = tl.messages.deleteMessages(id=[1, 2, 3], revoke=True)
        self.assertEqual(tl.decode(tl.encode(request)), request)
        part = tl.upload.saveFilePart(file_id=-5, file_part=0, bytes=b"x" * 1000)
        self.assertEqual(tl.decode(tl.encode(part)), part)
        with self.assertRaises(TypeError):
            tl.decode(tl.encode(tl.inputPeerSelf()), "User")
        wrapped = tl.invokeWithoutUpdates(query=tl.users.getUsers(id=[]))
        self.assertEqual(tl.response_type(wrapped), "Vector<User>")
        self.assertEqual(tl.decode(struct.pack("<Ii", 0x1CB5C415, 0), tl.response_type(wrapped)), [])

    def test_malformed_and_trailing_input_are_rejected(self):
        for data in (b"", b"\xff" * 4, tl.encode(tl.inputPeerSelf()) + b"\x00" * 4):
            with self.subTest(data=data), self.assertRaises(ValueError):
                tl.decode(data)
        with self.assertRaises(TypeError):
            tl.messages.sendMessage(peer=tl.inputPeerSelf(), message="text")
        with self.assertRaises(TypeError):
            tl.encode(tl.messages.getHistory(peer=tl.inputUserSelf(), offset_id=0,
                offset_date=0, add_offset=0, limit=10, max_id=0, min_id=0, hash=0))
        with self.assertRaises(TypeError):
            tl.encode(tl.upload.saveFilePart(file_id=1, file_part=0, bytes=12))


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.manager = Manager(self.root / "profile")
        self.addCleanup(self.manager.shutdown)
        self.runtime = self.manager.runtime
        self.commands = queue.Queue()
        self.runtime.sender = self.commands.put
        self.runtime.ready.set()
        self.plugins = {}
        for identity in ("plugin.a", "plugin.b"):
            source = self.root / (identity + ".plugin")
            source.write_text(
                'from base_plugin import BasePlugin\n'
                f'__id__ = {identity!r}\n__name__ = "Test"\n__version__ = "1.0"\n'
                '__author__ = "Test"\n__description__ = "Test"\n'
                '__platform__ = "desktop"\n__desktop_sdk__ = 1\n'
                'class TestPlugin(BasePlugin):\n    pass\n', encoding="utf-8")
            self.manager.install(str(source))
            self.manager.enable(identity)
            self.plugins[identity] = self.manager.loaded[identity][1]

    def hook(self, name="before_rpc", data=None, **extra):
        request = data or tl.messages.sendMessage(peer=tl.inputPeerSelf(), message="original", random_id=1)
        return self.runtime.native_hook({"point": name, "account_id": "42", "request_id": 100,
            "data": base64.b64encode(tl.encode(request)).decode("ascii"), **extra})

    def test_hook_priority_order_final_and_transactional_default(self):
        seen = []

        def change(value):
            seen.append(context().plugin_id)
            value.request.message += " changed"
            return HookResult(MODIFY, value)

        def final(value):
            seen.append("final")
            return HookResult(MODIFY_FINAL, value)

        self.runtime.register(self.plugins["plugin.b"], "before_rpc", change)
        self.runtime.register(self.plugins["plugin.a"], "before_rpc", change)
        self.runtime.register(self.plugins["plugin.a"], "before_rpc", final, priority=-1)
        self.runtime.register(self.plugins["plugin.b"], "before_rpc", change, priority=-2)
        response = self.hook()
        self.assertEqual(seen, ["plugin.a", "plugin.b", "final"])
        self.assertEqual(tl.decode(base64.b64decode(response["data"])).message, "original changed changed")

    def test_exception_and_invalid_result_leave_input_intact(self):
        original = tl.messages.sendMessage(peer=tl.inputPeerSelf(), message="original", random_id=1)

        def invalid(value):
            value.request.message = "partial"
            return value

        self.runtime.register(self.plugins["plugin.a"], "before_rpc", invalid)
        with self.assertRaises(HookError):
            self.hook(data=original)
        self.assertEqual(original.message, "original")
        self.assertIn("plugin.a", self.manager.errors)

    def test_cancel_and_account_or_recipient_changes_are_rejected(self):
        handler = self.runtime.register(self.plugins["plugin.a"], "before_send",
            lambda value: HookResult(CANCEL, reason="test"))
        with self.assertRaises(HookCancelled):
            self.hook()
        handler.cancel()

        def switch(value):
            value.account_id = "99"
            return HookResult(MODIFY, value)

        handler = self.runtime.register(self.plugins["plugin.a"], "before_rpc", switch)
        with self.assertRaises(HookError):
            self.hook()
        handler.cancel()

        def redirect(value):
            value.request.peer = tl.inputPeerChat(chat_id=99)
            return HookResult(MODIFY, value)

        self.runtime.register(self.plugins["plugin.a"], "before_rpc", redirect)
        with self.assertRaises(HookError):
            self.hook()

    def test_own_hook_is_skipped_for_recursive_requests(self):
        seen = []

        def handler(value):
            seen.append("called")
            self.hook(hook_stack=list(("plugin.a",)))
            return HookResult()

        self.runtime.register(self.plugins["plugin.a"], "before_rpc", handler)
        self.hook()
        self.assertEqual(seen, ["called"])

    def test_default_discards_mutation_and_outgoing_text_is_committed(self):
        def ignored(value):
            value.request.message = "discarded"

        handle = self.runtime.register(self.plugins["plugin.a"], "before_rpc", ignored)
        self.assertEqual(tl.decode(base64.b64decode(self.hook()["data"])).message, "original")
        handle.cancel()

        def outgoing(value):
            value.text = "caption"
            return HookResult(MODIFY, value)

        self.runtime.register(self.plugins["plugin.a"], "before_send", outgoing)
        response = self.hook()
        self.assertEqual(tl.decode(base64.b64decode(response["local_texts"][0]["text"])).text, "caption")

    def test_request_uses_explicit_account_and_reports_native_error(self):
        owner = self.plugins["plugin.a"]

        async def operation():
            try:
                await client.rpc("background-account", tl.updates.getState())
            except RpcError as error:
                return error.name

        future = self.runtime.schedule(owner, operation())
        command = self.commands.get(timeout=2)
        self.assertEqual(command["account_id"], "background-account")
        self.runtime.complete({"id": command["id"], "error": {"code": 0, "name": "ACCOUNT_CLOSED"}})
        self.assertEqual(future.result(timeout=2), "ACCOUNT_CLOSED")

    def test_disable_cleans_tasks_hooks_and_subscriptions(self):
        owner = self.plugins["plugin.a"]
        self.runtime.register(owner, "before_rpc", lambda value: None)
        future = self.runtime.schedule(owner, client.rpc("42", tl.updates.getState()))
        command = self.commands.get(timeout=2)
        self.assertTrue(self.runtime.is_pending(command["id"], "plugin.a"))
        response = json.loads(self.manager.dispatch(json.dumps({"action": "client_pending",
            "request_id": command["id"], "plugin_id": "plugin.a"})))
        self.assertTrue(response["result"])
        self.assertFalse(self.runtime.is_pending(command["id"], "plugin.b"))
        self.manager.disable("plugin.a")
        self.assertFalse(self.runtime.is_pending(command["id"], "plugin.a"))
        with self.assertRaises(CancelledError):
            future.result(timeout=2)
        self.assertFalse(self.runtime.registrations)
        self.assertEqual(self.runtime.hook_mask, 0)
        self.runtime.complete({"id": command["id"], "result": {"data": ""}})
        self.manager.enable("plugin.a")
        self.assertFalse(self.runtime.registrations)

    def test_ui_callback_runs_on_owner_thread_and_keeps_python_result(self):
        current_thread = __import__("threading").get_ident()

        async def task():
            return await run_on_ui(lambda: (current_thread, __import__("threading").get_ident()))

        future = self.runtime.schedule(self.plugins["plugin.a"], task())
        command = self.commands.get(timeout=2)
        self.runtime.execute_ui(command["call_id"])
        self.runtime.complete({"id": command["id"], "result": None})
        self.assertEqual(future.result(timeout=2), (current_thread, current_thread))

    def test_event_keeps_background_account_and_deduplicates_updates(self):
        received = []
        self.runtime.register(self.plugins["plugin.a"], "deleted_message", received.append)
        update = tl.updateDeleteMessages(messages=[3, 4], pts=8, pts_count=2)
        event = {"point": "raw_update", "account_id": "background-account",
                 "data": base64.b64encode(tl.encode(update)).decode("ascii")}
        self.runtime.native_event(event)
        self.runtime.native_event(event)
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0].account_id, "background-account")
        self.assertEqual(received[0].message_ids, (3, 4))

    def test_catchup_and_live_events_do_not_deliver_the_same_message_twice(self):
        received = []
        self.runtime.register(self.plugins["plugin.a"], "new_message", received.append)
        message = tl.message(id=11, peer_id=tl.peerUser(user_id=7), date=5, message="catchup")
        self.runtime.native_event({"point": "raw_message", "account_id": "42",
            "data": base64.b64encode(tl.encode(message)).decode()})
        update = tl.updateNewMessage(message=message, pts=6, pts_count=1)
        event = {"point": "raw_update", "account_id": "42",
                 "data": base64.b64encode(tl.encode(update)).decode()}
        self.runtime.native_event(event)
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0].message.text, "catchup")
        self.assertEqual(received[0].chat_id, 7)
        self.runtime.native_event({**event, "account_id": "99"})
        self.assertEqual([value.account_id for value in received], ["42", "99"])

    def test_response_hook_matches_request_and_can_recover_an_error(self):
        state = tl.updates.state(pts=1, qts=0, date=0, seq=0, unread_count=0)
        received = []

        def recover(value):
            received.append(value.request.constructor_name)
            value.error = None
            value.response = tl.encode(state)
            return HookResult(MODIFY, value)

        self.runtime.register(self.plugins["plugin.a"], "after_rpc", recover, request="updates.getState")
        response = self.runtime.native_hook({"point": "after_rpc", "account_id": "42", "request_id": 99,
            "data": "", "request_data": base64.b64encode(tl.encode(tl.updates.getState())).decode(),
            "error": {"code": 500, "name": "INTERNAL", "description": "test"}})
        self.assertIsNone(response["error"])
        self.assertEqual(tl.decode(base64.b64decode(response["data"])), state)
        self.assertEqual(received, ["updates.getState"])

    def test_inherited_stack_skips_own_response_hook(self):
        received = []
        self.runtime.register(self.plugins["plugin.a"], "after_rpc", received.append)
        self.runtime.native_hook({"point": "after_rpc", "account_id": "42", "request_id": 99,
            "data": base64.b64encode(struct.pack("<I", 0x997275B5)).decode(),
            "request_data": base64.b64encode(tl.encode(tl.account.updateStatus(offline=False))).decode(),
            "hook_stack": ["plugin.a"], "error": None})
        self.assertFalse(received)

    def test_response_hook_cannot_change_the_request_type(self):
        def invalid(value):
            value.request = tl.account.updateStatus(offline=False)
            value.error = None
            value.response = struct.pack("<I", 0x997275B5)
            return HookResult(MODIFY, value)

        self.runtime.register(self.plugins["plugin.a"], "after_rpc", invalid)
        with self.assertRaises(HookError):
            self.runtime.native_hook({"point": "after_rpc", "account_id": "42", "request_id": 99,
                "data": "", "request_data": base64.b64encode(tl.encode(tl.updates.getState())).decode(),
                "error": {"code": 500, "name": "INTERNAL"}})

    def test_update_hook_keeps_the_background_account(self):
        observed = []

        def update(value):
            observed.append(value.account_id)
            value.updates.date = 10
            return HookResult(MODIFY, value)

        handle = self.runtime.register(self.plugins["plugin.a"], "before_updates", update)
        response = self.hook(name="before_updates", data=tl.updates(updates=[], users=[], chats=[], date=0, seq=0))
        self.assertEqual(observed, ["42"])
        self.assertEqual(tl.decode(base64.b64decode(response["data"]), "Updates").date, 10)
        handle.cancel()

        def invalid(value):
            value.account_id = "99"
            return HookResult(MODIFY, value)

        self.runtime.register(self.plugins["plugin.a"], "before_updates", invalid)
        with self.assertRaises(HookError):
            self.hook(name="before_updates", data=tl.updatesTooLong())

    def test_hooks_skip_requests_they_do_not_handle(self):
        received = []
        self.runtime.register(self.plugins["plugin.a"], "after_rpc", received.append,
                              request="updates.getState")
        garbage = base64.b64encode(b"\xff\xff\xff\xff").decode()
        # Another request: nothing is decoded, even an unreadable response.
        response = self.runtime.native_hook({"point": "after_rpc", "account_id": "42", "request_id": 99,
            "data": garbage, "request_data": base64.b64encode(
                tl.encode(tl.account.updateStatus(offline=False))).decode(), "error": None})
        self.assertEqual(response["data"], garbage)
        self.assertFalse(received)

    def test_unchanged_response_is_not_decoded(self):
        received = []
        self.runtime.register(self.plugins["plugin.a"], "after_rpc", received.append)
        garbage = base64.b64encode(b"\xff\xff\xff\xff").decode()
        response = self.runtime.native_hook({"point": "after_rpc", "account_id": "42", "request_id": 99,
            "data": garbage, "request_data": base64.b64encode(
                tl.encode(tl.updates.getState())).decode(), "error": None})
        self.assertEqual(response["data"], garbage)
        self.assertEqual(len(received), 1)

    def test_unreadable_updates_are_kept(self):
        received = []
        self.runtime.register(self.plugins["plugin.a"], "before_updates", received.append)
        garbage = base64.b64encode(b"\xff\xff\xff\xff").decode()
        response = self.runtime.native_hook({"point": "before_updates", "account_id": "42",
                                             "data": garbage})
        self.assertEqual(response["data"], garbage)
        self.assertFalse(received)

    def test_no_ui_command_after_unload(self):
        owner = self.plugins["plugin.a"]
        self.manager.disable("plugin.a")
        with self.assertRaises(RuntimeError):
            self.runtime.submit_ui(owner, "ui.clipboard", text="late")

    def test_received_file_names_are_safe(self):
        from desktop.models import safe_file_name
        self.assertEqual(safe_file_name("../../plugins/evil.py", 1), "evil.py")
        self.assertEqual(safe_file_name("a\\..\\b.txt", 1), "b.txt")
        self.assertEqual(safe_file_name("..", 7), "7")
        self.assertEqual(safe_file_name("", 7), "7")
        self.assertEqual(safe_file_name('x:y?.txt', 7), "x_y_.txt")

    def test_account_settings_survive_update_and_rollback(self):
        owner = self.plugins["plugin.a"]
        owner.set("key", "first", "42")
        owner.set("key", "second", "99")
        source = self.root / "plugin.a.plugin"
        source.write_text(source.read_text(encoding="utf-8").replace('"1.0"', '"2.0"'), encoding="utf-8")
        self.manager.install(str(source), "plugin.a")
        self.manager.enable("plugin.a")
        updated = self.manager.loaded["plugin.a"][1]
        self.assertEqual(updated.get("key", None, "42"), "first")
        self.assertEqual(updated.get("key", None, "99"), "second")
        self.manager.rollback("plugin.a")
        self.manager.enable("plugin.a")
        self.assertEqual(self.manager.loaded["plugin.a"][1].get("key", None, "42"), "first")


class MediaTests(unittest.IsolatedAsyncioTestCase):
    async def test_expired_file_reference_is_refreshed_in_its_own_account(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "file.bin"
            attachment = Attachment("42", tl.inputDocumentFileLocation(
                id=1, access_hash=2, file_reference=b"old", thumb_size=""),
                4, 3, "file.bin", message_chat_id=7, message_id=8)
            updated = copy.deepcopy(attachment)
            updated.location.file_reference = b"new"
            chat = Chat("42", 7, "Test", tl.inputPeerUser(user_id=7, access_hash=9), "user")
            message = Message("42", 8, 7, "", 0, False, updated)
            request = AsyncMock(side_effect=[RpcError(400, "FILE_REFERENCE_EXPIRED"),
                tl.upload.file(type=tl.storage.fileUnknown(), mtime=0, bytes=b"abc")])
            loaded_chat = AsyncMock(return_value=chat)
            loaded_message = AsyncMock(return_value=message)
            with patch.object(media, "rpc", request), patch.object(media, "get_chat", loaded_chat), \
                    patch.object(media, "get_message", loaded_message):
                await media.download_file(attachment, target)
            loaded_chat.assert_awaited_once_with("42", 7)
            loaded_message.assert_awaited_once_with(chat, 8)
            self.assertEqual(request.await_args_list[1].args[1].location.file_reference, b"new")
            self.assertEqual(target.read_bytes(), b"abc")

    async def test_upload_parts_keep_account_and_progress(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.bin"
            path.write_bytes(b"x" * (media.PART_SIZE + 11))
            chat = Chat("account-2", 7, "Test", tl.inputPeerSelf(), "user")
            calls = []
            progress = []

            async def rpc(account, request, **options):
                calls.append((account, request))
                return True if request.constructor_name.startswith("upload.") else "sent"

            with patch.object(media, "rpc", rpc):
                self.assertEqual(await media.send_file(chat, path, progress=progress.append), "sent")
            self.assertTrue(all(account == "account-2" for account, _ in calls))
            self.assertEqual(len(calls), 3)
            self.assertEqual(progress[-1].transferred, path.stat().st_size)

    async def test_download_failure_keeps_existing_destination_and_removes_partial(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "file.bin"
            target.write_bytes(b"existing")
            attachment = Attachment("account-2", tl.inputDocumentFileLocation(
                id=1, access_hash=2, file_reference=b"ref", thumb_size=""), 4, 10, "file.bin")

            async def failed(*arguments, **keywords):
                raise RpcError(500, "INTERNAL")

            with patch.object(media, "rpc", failed), self.assertRaises(RpcError):
                await media.download_file(attachment, target)
            self.assertEqual(target.read_bytes(), b"existing")
            self.assertEqual(list(Path(directory).glob("*.part-*")), [])

    async def test_download_cancellation_keeps_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "file.bin"
            target.write_bytes(b"existing")
            attachment = Attachment("42", tl.inputDocumentFileLocation(
                id=1, access_hash=2, file_reference=b"ref", thumb_size=""), 4, 10, "file.bin")
            started = asyncio.Event()

            async def waiting(*arguments, **keywords):
                started.set()
                await asyncio.Future()

            with patch.object(media, "rpc", waiting):
                task = asyncio.create_task(media.download_file(attachment, target))
                await started.wait()
                task.cancel()
                with self.assertRaises(asyncio.CancelledError):
                    await task
            self.assertEqual(target.read_bytes(), b"existing")
            self.assertFalse(list(Path(directory).glob("*.part-*")))

    async def test_complete_download_publishes_only_the_complete_file(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "file.bin"
            attachment = Attachment("42", tl.inputDocumentFileLocation(
                id=1, access_hash=2, file_reference=b"ref", thumb_size=""), 4, 3, "file.bin")

            async def response(account, request, **options):
                self.assertEqual(account, "42")
                self.assertEqual(options["dc_id"], 4)
                return tl.upload.file(type=tl.storage.fileUnknown(), mtime=0, bytes=b"abc")

            with patch.object(media, "rpc", response):
                self.assertEqual(await media.download_file(attachment, target), target.resolve())
            self.assertEqual(target.read_bytes(), b"abc")
            self.assertFalse(list(Path(directory).glob("*.part-*")))


if __name__ == "__main__":
    unittest.main()
