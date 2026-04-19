#!/usr/bin/env python3
"""Create a new markdown draft under blog/drafts from blog/_template.md."""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TEMPLATE_PATH = ROOT / "blog" / "_template.md"
DRAFTS_DIR = ROOT / "blog" / "drafts"


def slugify(text: str) -> str:
    lowered = text.strip().lower()
    replaced = re.sub(r"[^a-z0-9]+", "-", lowered)
    collapsed = re.sub(r"-+", "-", replaced).strip("-")
    if not collapsed:
        raise ValueError("Could not generate slug from input.")
    return collapsed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("title", help="Post title")
    parser.add_argument("--date", default=dt.date.today().isoformat(), help="Post date (YYYY-MM-DD)")
    parser.add_argument("--slug", help="URL slug (defaults to slugified title)")
    parser.add_argument("--excerpt", default="Lisää lyhyt kuvaus tähän.", help="Short excerpt for blog index")
    parser.add_argument("--description", default="Lisää metakuvaus tähän.", help="Meta description")
    parser.add_argument("--force", action="store_true", help="Overwrite existing draft")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        dt.date.fromisoformat(args.date)
    except ValueError as exc:
        raise SystemExit(f"Invalid --date '{args.date}'. Expected YYYY-MM-DD.") from exc

    slug = args.slug or slugify(args.title)

    if not TEMPLATE_PATH.exists():
        raise SystemExit(f"Template not found: {TEMPLATE_PATH}")

    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = DRAFTS_DIR / f"{args.date}-{slug}.md"

    if output_path.exists() and not args.force:
        raise SystemExit(f"Draft already exists: {output_path}. Use --force to overwrite.")

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    content = (
        template.replace("{{TITLE}}", args.title)
        .replace("{{DATE}}", args.date)
        .replace("{{SLUG}}", slug)
        .replace("{{EXCERPT}}", args.excerpt)
        .replace("{{DESCRIPTION}}", args.description)
    )

    output_path.write_text(content, encoding="utf-8")
    print(f"Created draft: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
