"""Check this documentation bundle without network requests or extra packages."""

from __future__ import annotations

import argparse
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]


def prose(text: str) -> str:
    """Remove examples and comments before inspecting rendered links."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    result = []
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            value = marker[1]
            if fence is None:
                fence = value
                continue
            if value[0] == fence[0] and len(value) >= len(fence):
                fence = None
                continue
        if fence is None:
            result.append(line)
    return "\n".join(result)


class HTMLReferences(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.anchors: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if value is None:
                continue
            if key in {"href", "src"}:
                self.links.append(value)
            if key == "id" or (tag == "a" and key == "name"):
                self.anchors.add(value)


def references(text: str) -> tuple[list[str], set[str]]:
    text = prose(text)
    parser = HTMLReferences()
    without_code = re.sub(r"(`+).*?\1", "", text)
    parser.feed(without_code)
    # shortcut: handles the link forms used by this bundle, not a full GFM parser;
    # use a Markdown parser if future docs rely on escaped or nested URL syntax.
    for match in re.finditer(r'\]\(\s*(?:<([^>\n]+)>|([^\s)]+))(?:\s+"[^"]*")?\s*\)', without_code):
        parser.links.append(html.unescape(match[1] or match[2]))
    for match in re.finditer(r"^\s{0,3}\[[^\]]+\]:\s*<?([^\s>]+)>?", without_code, re.M):
        parser.links.append(html.unescape(match[1]))
    counts: dict[str, int] = {}
    for match in re.finditer(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", text, re.M):
        label = re.sub(r"<[^>]*>", "", match[1])
        label = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", label)
        slug = re.sub(r"[^\w\- ]", "", html.unescape(label).lower()).replace(" ", "-")
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        parser.anchors.add(f"{slug}-{count}" if count else slug)
    return parser.links, parser.anchors


def check(root: Path) -> tuple[int, list[str]]:
    root = root.resolve()
    errors: list[str] = []
    files = []
    for directory, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = [name for name in dirs if not name.startswith(".")
                   and name not in {"preview", "__pycache__"}
                   and not (Path(directory) / name).is_symlink()]
        for name in names:
            path = Path(directory) / name
            if not name.startswith(".") and path.suffix.lower() in {".md", ".json", ".svg"}:
                if not path.resolve().is_relative_to(root):
                    errors.append(f"{path.relative_to(root)}: file resolves outside bundle")
                else:
                    files.append(path)
    markdown: dict[Path, tuple[list[str], set[str]]] = {}
    for path in files:
        try:
            text = path.read_text(encoding="utf-8-sig")
            if path.suffix.lower() == ".md":
                markdown[path.resolve()] = references(text)
            elif path.suffix.lower() == ".json":
                json.loads(text)
            else:
                ET.fromstring(text)
        except (OSError, UnicodeError, ValueError, ET.ParseError) as exc:
            errors.append(f"{path.relative_to(root)}: {exc}")
    for source, (links, _) in markdown.items():
        for link in links:
            try:
                url = urlsplit(link)
                if url.scheme in {"http", "https", "mailto", "tel", "data"} or (not url.scheme and url.netloc):
                    continue
                destination = (source.parent / unquote(url.path)).resolve() if url.path else source
                if url.scheme:
                    problem = "unsupported URL scheme"
                elif not destination.is_relative_to(root):
                    problem = "link escapes bundle"
                elif not destination.exists():
                    problem = "missing target"
                elif url.fragment and destination.suffix.lower() == ".md":
                    anchors = markdown.get(destination, ([], set()))[1]
                    problem = "missing anchor" if unquote(url.fragment) not in anchors else ""
                else:
                    problem = ""
            except ValueError as exc:
                problem = f"invalid URL ({exc})"
            if problem:
                errors.append(f"{source.relative_to(root)}: {problem}: {link}")
    return len(files), errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Documentation bundle root")
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error("root must be an existing directory")
    count, errors = check(args.root)
    if errors:
        print("\n".join(errors))
        print(f"FAILED: {len(errors)} issue(s) in {count} files.")
        return 1
    print(f"OK: {count} Markdown, JSON and SVG files; local links and anchors checked.")
    print("External URLs, live services and full GitHub rendering were not checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
