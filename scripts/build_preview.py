"""Render a local README preview; requires the optional Python Markdown package."""

from __future__ import annotations

import argparse
import html
import os
from pathlib import Path
import re
import shutil
from urllib.parse import urlsplit, urlunsplit

try:
    import markdown
except ImportError:
    markdown = None


ROOT = Path(__file__).resolve().parents[1]
CSS = """
:root { color-scheme: light dark; --bg:#f6f8fa; --paper:#fff; --ink:#1f2328;
 --muted:#636c76; --border:#d1d9e0; --link:#0969da; --code:#eff1f3; }
@media(prefers-color-scheme:dark) { :root { --bg:#010409; --paper:#0d1117;
 --ink:#e6edf3; --muted:#9198a1; --border:#3d444d; --link:#4493f8; --code:#151b23; } }
* { box-sizing:border-box; }
body { margin:0; color:var(--ink); background:var(--bg); font:16px/1.6 -apple-system,
 BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,"Microsoft YaHei",sans-serif; }
.preview-note { max-width:1012px; margin:24px auto 10px; padding:0 20px;
 font-size:12px; color:var(--muted); }
article { max-width:1012px; margin:0 auto 48px; padding:40px; background:var(--paper);
 border:1px solid var(--border); border-radius:6px; overflow-wrap:break-word; }
a { color:var(--link); text-decoration:none; } a:hover { text-decoration:underline; }
h1,h2,h3,h4 { font-weight:600; line-height:1.25; margin:24px 0 16px; }
h1 { font-size:32px; } h2 { font-size:24px; } h3 { font-size:20px; }
h1,h2 { padding-bottom:.3em; border-bottom:1px solid var(--border); }
p,table,pre,blockquote,ul,ol { margin:0 0 16px; }
img { max-width:100%; height:auto; vertical-align:middle; }
div[align="center"] { text-align:center; }
div[align="center"] h1 { border:0; padding:0; margin:26px 0 14px; font-size:40px; }
div[align="center"] h3 { font-size:22px; margin-top:0; }
div[align="center"] p { margin-bottom:20px; }
table { display:block; width:max-content; max-width:100%; overflow:auto;
 border-collapse:collapse; font-size:14px; }
th,td { padding:9px 13px; border:1px solid var(--border); text-align:start; vertical-align:top; }
th { font-weight:600; } tr:nth-child(2n) { background:var(--bg); }
code,pre { font:13px/1.55 ui-monospace,SFMono-Regular,Consolas,"Liberation Mono",monospace; }
code { background:var(--code); padding:.2em .4em; border-radius:4px; direction:ltr; unicode-bidi:isolate; }
pre { background:var(--code); padding:16px; border-radius:6px; overflow:auto; }
pre { direction:ltr; text-align:left; }
pre code { padding:0; background:transparent; }
html[dir="rtl"] pre:has(code.language-text), html[dir="rtl"] code.language-text {
 direction:rtl; text-align:right; }
blockquote { color:var(--muted); border-left:4px solid var(--border); padding:0 16px; }
hr { height:1px; border:0; background:var(--border); margin:28px 0; }
details { margin:0 0 16px; } summary { cursor:pointer; margin-bottom:12px; }
li + li { margin-top:4px; } sub { color:var(--muted); }
@media(max-width:640px) { article { padding:24px 18px; margin:0 10px 24px; }
 .preview-note { margin-top:14px; } div[align="center"] h1 { font-size:32px; }
 div[align="center"] h3 { font-size:19px; } }
"""


def rewrite_href(match: re.Match[str]) -> str:
    prefix, quote, value = match.groups()
    url = urlsplit(html.unescape(value))
    if url.scheme or url.netloc:
        return match[0]
    path = url.path
    if path.lower().endswith(".md"):
        path = path[:-3] + ".html"
    elif path.rsplit("/", 1)[-1] == "LICENSE":
        path += ".html"
    value = html.escape(urlunsplit(url._replace(path=path)), quote=True)
    return f"{prefix}{quote}{value}{quote}"


def render(text: str, language: str = "en") -> str:
    if markdown is None:
        raise RuntimeError("Install the optional preview dependency: python -m pip install Markdown")
    # md_in_html leaves ordinary raw HTML opaque unless explicitly enabled.
    text = re.sub(r'<(div\b[^>]*|details)>',
                  lambda match: match[0] if "markdown=" in match[1]
                  else f'<{match[1]} markdown="1">', text)
    body = markdown.markdown(
        text, extensions=["tables", "fenced_code", "toc", "md_in_html"],
        extension_configs={"toc": {"slugify": lambda value, separator:
            re.sub(r"[^\w\- ]", "", html.unescape(value).lower()).replace(" ", separator)}},
    )
    body = re.sub(r'(\bhref\s*=\s*)(["\'])(.*?)\2', rewrite_href, body)
    heading = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
    title = re.sub(r"<[^>]*>", "", heading[1]) if heading else "Biointron OS"
    direction = "rtl" if language in {"ar", "fa"} else "ltr"
    return f'''<!doctype html>
<html lang="{html.escape(language, quote=True)}" dir="{direction}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(html.unescape(title))} · Local preview</title><style>{CSS}</style></head>
<body><div class="preview-note">Local README preview · GitHub rendering may differ.</div>
<article>{body}</article></body></html>
'''


def build(root: Path) -> int:
    root = root.resolve()
    output = root / "preview"
    if output.is_symlink():
        raise ValueError("Preview output cannot be a symbolic link")
    count = 0
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [name for name in dirs if not name.startswith(".")
                   and name not in {"preview", "__pycache__"}
                   and not (Path(directory) / name).is_symlink()]
        for name in files:
            source = Path(directory) / name
            if name.startswith(".") or source.is_symlink() or not source.resolve().is_relative_to(root):
                continue
            relative = source.relative_to(root)
            is_markdown = source.suffix.lower() == ".md"
            is_license = relative.as_posix() == "LICENSE"
            is_asset = relative.parts[0] == "assets" and source.suffix.lower() in {".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif"}
            is_example = relative.parts[0] == "examples" and source.suffix.lower() in {".json", ".toml"}
            if not (is_markdown or is_license or is_asset or is_example):
                continue
            destination = output / relative
            rendered = destination.with_suffix(".html") if is_markdown else destination.with_name("LICENSE.html")
            for path in (destination, rendered):
                if path.is_symlink() or not path.resolve().is_relative_to(output):
                    raise ValueError(f"Unsafe preview destination: {relative}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            if is_markdown or is_license:
                locale = re.fullmatch(r"README\.([a-z]{2}(?:-[A-Za-z]+)?)\.md", name)
                language = locale[1] if locale else "en"
                rendered.write_text(render(source.read_text(encoding="utf-8-sig"), language), encoding="utf-8")
                count += 1
            if is_license or is_asset or is_example:
                shutil.copyfile(source, destination)
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Documentation bundle root")
    args = parser.parse_args()
    if markdown is None:
        parser.exit(1, "Preview needs Python Markdown. Install with: python -m pip install Markdown\n")
    if not args.root.is_dir():
        parser.error("root must be an existing directory")
    try:
        count = build(args.root)
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        parser.exit(1, f"Preview failed: {exc}\n")
    print(f"Built {count} HTML pages in {args.root.resolve() / 'preview'}")
    print("Open preview/README.html or preview/docs/readme/README.zh-CN.html in your browser.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
