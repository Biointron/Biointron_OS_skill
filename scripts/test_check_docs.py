"""Small regression checks for the documentation validator."""

from pathlib import Path
import tempfile
import unittest

from check_docs import check


class CheckDocsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name: str, text: str) -> None:
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_links_anchors_badges_and_examples(self) -> None:
        self.write("README.md", '''# Start here
[Guide](docs/guide.md#中文-title)
<a href="docs/guide.md#explicit">Guide</a>
[![Badge](https://example.invalid/badge.svg)](docs/guide.md#repeat-1)
[Reference][guide]
[guide]: docs/guide.md#repeat
<!-- [Not rendered](absent.md) -->
`[Inline example](absent.md)`
```md
[Example](absent.md)
```
~~~text
<img src="absent.svg">
~~~
[External](https://example.invalid/path)
''')
        self.write("docs/guide.md", '# 中文 `Title`\n<a id="explicit"></a>\n## Repeat\n## Repeat\n')
        self.write("examples/data.json", '{"ok": true}')
        self.write("assets/image.svg", '<svg xmlns="http://www.w3.org/2000/svg"/>')
        self.assertEqual(check(self.root), (4, []))

    def test_reports_missing_file_and_anchor(self) -> None:
        self.write("README.md", '[Missing](missing.md)\n[Wrong anchor](guide.md#wrong)')
        self.write("guide.md", "# Exists")
        _, errors = check(self.root)
        self.assertTrue(any("missing target: missing.md" in error for error in errors))
        self.assertTrue(any("missing anchor: guide.md#wrong" in error for error in errors))

    def test_rejects_path_escape_before_reading(self) -> None:
        self.write("README.md", '[Escape](../private.md)\n[Encoded](%2e%2e/private.md)')
        _, errors = check(self.root)
        self.assertEqual(len(errors), 2)
        self.assertTrue(all("link escapes bundle" in error for error in errors))

    def test_rejects_file_urls(self) -> None:
        self.write("README.md", '[Private](file:///private/data.md)')
        _, errors = check(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("unsupported URL scheme", errors[0])

    def test_invalid_json_and_svg(self) -> None:
        self.write("examples/broken.json", '{"unfinished":')
        self.write("assets/broken.svg", '<svg>')
        _, errors = check(self.root)
        self.assertEqual(len(errors), 2)

    def test_ignores_hidden_and_preview_files(self) -> None:
        self.write("README.md", "# Valid")
        self.write("preview/broken.md", "[Broken](absent.md)")
        self.write(".cache/broken.json", "broken")
        self.write(".hidden.md", "[Broken](absent.md)")
        self.assertEqual(check(self.root), (1, []))


if __name__ == "__main__":
    unittest.main()
