"""Every example plugin must import, load and register what it promises,
without touching the network."""

import io
from pathlib import Path
import queue
import sys
import tempfile
import time
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "Telegram/PluginSDK"))

from ovygram_runtime import Manager, plugin_metadata

EXAMPLES = ROOT / "tools/ovygram/examples"


def example_namespace(name):
    """The module-level code of an example, without running its imports of
    the client-only SDK parts."""
    source = (EXAMPLES / name).read_text(encoding="utf-8")
    namespace = {"__name__": "example"}
    exec(compile(source, name, "exec"), namespace)
    return namespace


def offline(*arguments, **keywords):
    raise OSError("network disabled in tests")


class ExampleTests(unittest.TestCase):
    def test_every_example_has_valid_metadata(self):
        for path in sorted(EXAMPLES.glob("*.ovyplugin")):
            with self.subTest(example=path.name):
                metadata = plugin_metadata(path.read_bytes(), path.name)
                self.assertEqual(metadata["platform"], "desktop")
                compile(path.read_text(encoding="utf-8"), path.name, "exec")

    def test_examples_without_libraries_load_offline(self):
        expected = {
            "currency_rates.ovyplugin": {"ui.menu.add"},
            "wiki_summary.ovyplugin": {"ui.menu.add"},
            "rss_feed.ovyplugin": set(),
            "clean_links.ovyplugin": set(),
            "away_reply.ovyplugin": {"ui.menu.add"},
            "chat_stats.ovyplugin": {"ui.menu.add"},
            "reminders.ovyplugin": {"ui.menu.add"},
        }
        with tempfile.TemporaryDirectory() as directory, \
                mock.patch("urllib.request.urlopen", offline):
            manager = Manager(Path(directory) / "profile")
            commands = queue.Queue()
            manager.runtime.sender = commands.put
            manager.runtime.ready.set()
            try:
                for name, methods in expected.items():
                    with self.subTest(example=name):
                        plugin_id = manager.install(str(EXAMPLES / name))
                        manager.enable(plugin_id)
                        self.assertIn(plugin_id, manager.loaded, manager.errors.get(plugin_id))
                        # The first feed check finishes while the network is
                        # still patched out (timers stay, they never finish).
                        instance = manager.loaded[plugin_id][0]
                        for _ in range(300):
                            if not getattr(instance, "checking", False):
                                break
                            time.sleep(0.01)
                        sent = set()
                        while not commands.empty():
                            sent.add(commands.get_nowait().get("method"))
                        self.assertTrue(methods <= sent, sent)
                        manager.disable(plugin_id)
                        self.assertNotIn(plugin_id, manager.loaded)
            finally:
                manager.shutdown()

    def test_clean_links_keeps_meaningful_parameters(self):
        clean = example_namespace("clean_links.ovyplugin")["clean_text"]
        self.assertEqual(clean("see https://x.com/a?utm_source=tg&id=5."), "see https://x.com/a?id=5.")
        self.assertEqual(clean("https://youtu.be/abc?si=XYZ"), "https://youtu.be/abc")
        self.assertEqual(clean("(https://a.b/c?q=1&fbclid=z)"), "(https://a.b/c?q=1)")
        self.assertEqual(clean("no links here"), "no links here")

    def test_rss_parses_rss_and_atom(self):
        fetch = example_namespace("rss_feed.ovyplugin")["fetch_items"]
        rss = (b"<rss><channel><item><title>One</title><link>https://a/1</link>"
               b"<guid>g1</guid></item></channel></rss>")
        atom = (b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><id>e1</id>'
                b'<title>Two</title><link href="https://a/2"/></entry></feed>')
        for data, item in ((rss, ("g1", "One", "https://a/1")), (atom, ("e1", "Two", "https://a/2"))):
            with mock.patch("urllib.request.urlopen", return_value=io.BytesIO(data)):
                self.assertEqual(fetch("https://feed"), [item])

    def test_chat_stats_chart_scales_bars(self):
        namespace = example_namespace("chat_stats.ovyplugin")
        commands, height = namespace["bar_chart"]([("Аня", 10), ("Боб", 5)])
        bars = [command for command in commands if command["op"] == "rect"]
        self.assertEqual(len(bars), 2)
        self.assertGreater(bars[0]["width"], bars[1]["width"])
        self.assertLessEqual(height, namespace["BARS_HEIGHT"])


if __name__ == "__main__":
    unittest.main()
