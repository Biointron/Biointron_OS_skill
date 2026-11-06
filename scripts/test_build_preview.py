"""Preview rendering checks; skipped when optional Python Markdown is absent."""

from pathlib import Path
import tempfile
import unittest

from build_preview import build, markdown, render


@unittest.skipIf(markdown is None, "optional Python Markdown package is not installed")
class BuildPreviewTests(unittest.TestCase):
    def test_language_metadata_and_rtl_content(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for locale in ("ar", "fa", "zh-TW", "pt-BR", "ur-Latn", "ml"):
                (root / f"README.{locale}.md").write_text(
                    '<p dir="ltr"><a href="README.md">English</a></p>\n\n'
                    '<div dir="rtl">\n\n# عنوان\n\n**نص**\n\n</div>', encoding="utf-8")
            build(root)
            for locale in ("ar", "fa", "zh-TW", "pt-BR", "ur-Latn", "ml"):
                page = (root / f"preview/README.{locale}.html").read_text(encoding="utf-8")
                direction = "rtl" if locale in {"ar", "fa"} else "ltr"
                self.assertIn(f'<html lang="{locale}" dir="{direction}">', page)
                self.assertIn('<p dir="ltr"><a href="README.html">English</a></p>', page)
                self.assertIn('<strong>نص</strong>', page)
                self.assertIn('<div dir="rtl">', page)

    def test_relative_links_and_centered_markdown(self) -> None:
        page = render('''<div align="center">

# Biointron OS

**[Guide](docs/install.md#start)** · [Remote](https://example.org/README.md)

</div>

<details>
<summary>Details</summary>

Read the [license](LICENSE).

</details>
''')
        self.assertIn('<h1 id="biointron-os">Biointron OS</h1>', page)
        self.assertIn('<strong><a href="docs/install.html#start">Guide</a></strong>', page)
        self.assertIn('href="https://example.org/README.md"', page)
        self.assertIn('href="LICENSE.html"', page)
        self.assertNotIn("[Guide]", page)
        self.assertNotIn('markdown="1"', page)

    def test_preserves_folder_structure_and_copies_assets(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for directory in ("docs", "assets", "examples", "preview", ".hidden"):
                (root / directory).mkdir()
            (root / "README.md").write_text("# Home\n[Guide](docs/guide.md#intro)", encoding="utf-8")
            (root / "docs/guide.md").write_text("# Intro\n[Home](../README.md)", encoding="utf-8")
            (root / "assets/hero.svg").write_text("<svg/>", encoding="utf-8")
            (root / "examples/config.toml").write_text('name = "demo"', encoding="utf-8")
            (root / "LICENSE").write_text("# License\nTerms.", encoding="utf-8")
            (root / "preview/ignored.md").write_text("# Ignore", encoding="utf-8")
            (root / ".hidden/ignored.md").write_text("# Ignore", encoding="utf-8")
            self.assertEqual(build(root), 3)
            self.assertIn('href="../README.html"', (root / "preview/docs/guide.html").read_text(encoding="utf-8"))
            self.assertEqual((root / "preview/assets/hero.svg").read_text(encoding="utf-8"), "<svg/>")
            self.assertTrue((root / "preview/examples/config.toml").exists())
            self.assertTrue((root / "preview/LICENSE").exists())
            self.assertTrue((root / "preview/LICENSE.html").exists())
            self.assertFalse((root / "preview/ignored.html").exists())
            self.assertFalse((root / "preview/.hidden").exists())


if __name__ == "__main__":
    unittest.main()
