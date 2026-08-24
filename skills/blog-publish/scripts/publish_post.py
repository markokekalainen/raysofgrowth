#!/usr/bin/env python3
"""Publish a markdown blog draft into HTML and update blog listing/sitemap."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BLOG_DIR = ROOT / "blog"
BLOG_INDEX = BLOG_DIR / "index.html"
SITEMAP_PATH = ROOT / "sitemap.xml"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path, help="Path to markdown draft")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing blog post HTML")
    parser.add_argument("--skip-sitemap", action="store_true", help="Skip sitemap.xml updates")
    return parser.parse_args()


def parse_frontmatter(markdown_text: str) -> tuple[dict[str, str], str]:
    lines = markdown_text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise SystemExit("Draft must start with YAML frontmatter delimited by ---")

    frontmatter: dict[str, str] = {}
    idx = 1
    while idx < len(lines):
        line = lines[idx]
        if line.strip() == "---":
            break
        if ":" not in line:
            raise SystemExit(f"Invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip().strip('"').strip("'")
        idx += 1

    if idx >= len(lines) or lines[idx].strip() != "---":
        raise SystemExit("Frontmatter is not properly closed with ---")

    body = "\n".join(lines[idx + 1 :]).strip()
    return frontmatter, body


def validate_meta(meta: dict[str, str]) -> None:
    required = ["title", "date", "slug", "category", "excerpt", "description"]
    missing = [key for key in required if not meta.get(key)]
    if missing:
        raise SystemExit(f"Missing required frontmatter fields: {', '.join(missing)}")

    try:
        dt.date.fromisoformat(meta["date"])
    except ValueError as exc:
        raise SystemExit("Field 'date' must be in YYYY-MM-DD format") from exc

    if not re.fullmatch(r"[a-z0-9-]+", meta["slug"]):
        raise SystemExit("Field 'slug' must use lowercase letters, numbers, and hyphens")


def render_body(markdown_body: str) -> str:
    blocks = re.split(r"\n\s*\n", markdown_body.strip())
    rendered: list[str] = []

    for block in blocks:
        stripped = block.strip()
        if not stripped:
            continue

        lines = [ln.rstrip() for ln in stripped.splitlines() if ln.strip()]
        if not lines:
            continue

        if lines[0].startswith("# "):
            continue

        if lines[0].startswith("## "):
            rendered.append(f"        <h2>{html.escape(lines[0][3:].strip())}</h2>")
            continue

        if lines[0].startswith("### "):
            rendered.append(f"        <h3>{html.escape(lines[0][4:].strip())}</h3>")
            continue

        if all(re.match(r"^\d+\.\s+", ln) for ln in lines):
            rendered.append("        <ol>")
            for ln in lines:
                item = re.sub(r"^\d+\.\s+", "", ln)
                rendered.append(f"          <li>{html.escape(item)}</li>")
            rendered.append("        </ol>")
            continue

        if all(ln.startswith("- ") for ln in lines):
            rendered.append("        <ul>")
            for ln in lines:
                rendered.append(f"          <li>{html.escape(ln[2:].strip())}</li>")
            rendered.append("        </ul>")
            continue

        if all(ln.startswith(">") for ln in lines):
            rendered.append('        <blockquote class="highlight-quote">')
            for ln in lines:
                quote_line = ln.lstrip(">").strip()
                if quote_line:
                    rendered.append(f"          <p>{html.escape(quote_line)}</p>")
            rendered.append("        </blockquote>")
            continue

        paragraph = " ".join(ln.strip() for ln in lines)
        rendered.append(f"        <p>{html.escape(paragraph)}</p>")

    return "\n".join(rendered)


def render_post_html(meta: dict[str, str], body_html: str) -> str:
    title = html.escape(meta["title"])
    description = html.escape(meta["description"])
    date = html.escape(meta["date"])
    category = html.escape(meta["category"])
    slug = meta["slug"]
    canonical = f"https://raysofgrowth.com/blog/{slug}/"

    return f"""<!doctype html>
<html lang=\"fi\">
  <head>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','GTM-NF2C9WG4');</script>
    <!-- End Google Tag Manager -->
    <title>Rays Of Growth | {title}</title>
    <meta name=\"description\" content=\"{description}\">
    <meta name=\"author\" content=\"Marko Kekäläinen\">
    <meta name=\"robots\" content=\"index, follow\">
    <link rel=\"canonical\" href=\"{canonical}\">
    <meta property=\"og:title\" content=\"Rays Of Growth | {title}\">
    <meta property=\"og:description\" content=\"{description}\">
    <meta property=\"og:type\" content=\"article\">
    <meta property=\"og:url\" content=\"{canonical}\">
    <meta property=\"og:site_name\" content=\"Rays Of Growth\">
    <meta property=\"og:locale\" content=\"fi_FI\">
    <meta property=\"og:image\" content=\"https://raysofgrowth.com/assets/images/chamonix.jpeg\">
    <meta property=\"og:image:alt\" content=\"Näkymä Chamonix'sta vuoristomaisemassa\">
    <meta name=\"twitter:card\" content=\"summary_large_image\">
    <meta name=\"twitter:title\" content=\"Rays Of Growth | {title}\">
    <meta name=\"twitter:description\" content=\"{description}\">
    <meta name=\"twitter:image\" content=\"https://raysofgrowth.com/assets/images/chamonix.jpeg\">
    <link rel=\"icon\" href=\"../../favicon.svg\" type=\"image/svg+xml\">
    <link rel=\"stylesheet\" href=\"../../styles.css?v=79\">
  </head>
  <body>
    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src=\"https://www.googletagmanager.com/ns.html?id=GTM-NF2C9WG4\"
    height=\"0\" width=\"0\" style=\"display:none;visibility:hidden\"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->
    <header aria-label=\"Logo\">
      <div class=\"header-inner\">
        <a class=\"logo-link\" href=\"../../index.html\">
          <img class=\"logo\" src=\"../../assets/logos/logo-lockup-teal.svg\" alt=\"Raysofgrowth wordmark with symbol in teal\">
        </a>
        <nav class=\"site-nav\" aria-label=\"Main\">
          <a class=\"nav-link\" href=\"../../index.html\">Etusivu</a>
          <a class=\"nav-link\" href=\"../../miksi/\">Mitä?</a>
          <a class=\"nav-link\" href=\"../../blog/\">Ajatuksia</a>
          <a class=\"nav-link\" href=\"../../yhteisollisyys/lahteen-yhteisolenkki/\">Lenkille?</a>
        </nav>
      </div>
    </header>
    <main class=\"page\">
      <header class=\"page-hero\">
        <p class=\"post-meta\"><time datetime=\"{date}\">{date}</time> · {category}</p>
        <h1>{title}</h1>
      </header>
      <section class=\"page-content\">
{body_html}
      </section>
    </main>
    <footer class=\"site-footer\">
      <div class=\"footer-inner\">
        <a class=\"contact-link\" href=\"https://signal.me/#p/+358505446182\" target=\"_blank\" rel=\"noopener noreferrer\">Signal</a>
        <a class=\"contact-link\" href=\"https://instagram.com/raysofgrowth\" target=\"_blank\" rel=\"noopener noreferrer\">Instagram</a>
        <a class=\"contact-link\" href=\"https://www.youtube.com/@raysofgrowth\" target=\"_blank\" rel=\"noopener noreferrer\">YouTube</a>
      </div>
      <p class=\"iteration-count\">Version: 82</p>
    </footer>
  </body>
</html>
"""


def post_card(meta: dict[str, str]) -> str:
    title = html.escape(meta["title"])
    date = html.escape(meta["date"])
    category = html.escape(meta["category"])
    excerpt = html.escape(meta["excerpt"])
    slug = meta["slug"]

    return (
        "        <article class=\"post-card\">\n"
        f"          <p class=\"post-meta\"><time datetime=\"{date}\">{date}</time> · {category}</p>\n"
        f"          <h2 class=\"post-title\">{title}</h2>\n"
        f"          <p class=\"post-excerpt\">{excerpt}</p>\n"
        f"          <a class=\"post-link\" href=\"{slug}/\">Lue lisää</a>\n"
        "        </article>"
    )


def update_blog_index(meta: dict[str, str]) -> None:
    content = BLOG_INDEX.read_text(encoding="utf-8")
    slug_marker = f'href="{meta["slug"]}/"'
    if slug_marker in content:
        print(f"Blog index already contains slug '{meta['slug']}', skipping index update.")
        return

    marker = '<section class="post-list" aria-label="Blog posts">\n'
    if marker not in content:
        raise SystemExit("Could not find post list section in blog/index.html")

    updated = content.replace(marker, marker + post_card(meta) + "\n", 1)
    BLOG_INDEX.write_text(updated, encoding="utf-8")
    print("Updated blog/index.html")


def update_sitemap(slug: str) -> None:
    if not SITEMAP_PATH.exists():
        print("sitemap.xml not found; skipping sitemap update.")
        return

    loc = f"https://raysofgrowth.com/blog/{slug}/"
    content = SITEMAP_PATH.read_text(encoding="utf-8")
    if loc in content:
        print("sitemap.xml already contains post URL; skipping sitemap update.")
        return

    insertion = f"  <url>\n    <loc>{loc}</loc>\n  </url>\n"
    closing = "</urlset>"
    if closing not in content:
        raise SystemExit("Could not find closing </urlset> in sitemap.xml")

    updated = content.replace(closing, insertion + closing, 1)
    SITEMAP_PATH.write_text(updated, encoding="utf-8")
    print("Updated sitemap.xml")


def main() -> int:
    args = parse_args()
    draft_path = args.draft.resolve()

    if not draft_path.exists():
        raise SystemExit(f"Draft file not found: {draft_path}")

    markdown_text = draft_path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(markdown_text)
    validate_meta(meta)

    destination_dir = BLOG_DIR / meta["slug"]
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination_file = destination_dir / "index.html"
    if destination_file.exists() and not args.overwrite:
        raise SystemExit(f"Destination already exists: {destination_file}. Use --overwrite.")

    body_html = render_body(body)
    html_output = render_post_html(meta, body_html)
    destination_file.write_text(html_output, encoding="utf-8")
    print(f"Published post HTML: {destination_file}")

    update_blog_index(meta)
    if not args.skip_sitemap:
        update_sitemap(meta["slug"])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
