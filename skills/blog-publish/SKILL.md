---
name: blog-publish
description: Publish a markdown blog draft into the static HTML blog structure used by this repository. Use when the user asks to turn a draft into a live post page, update blog/index.html cards, and keep sitemap.xml in sync.
---

# Blog Publish

Convert a markdown draft into `blog/<slug>/index.html` and update listing files.

## Workflow

1. Validate that the draft has required frontmatter fields.
2. Render markdown body blocks into HTML for the post page.
3. Write `blog/<slug>/index.html`.
4. Prepend a new post card to `blog/index.html` if missing.
5. Append post URL to `sitemap.xml` if missing.

## Command

```bash
python3 skills/blog-publish/scripts/publish_post.py blog/drafts/2026-04-04-post-slug.md
```

Optional flags:

- `--overwrite`: replace existing `blog/<slug>/index.html`
- `--skip-sitemap`: skip `sitemap.xml` edits

## Frontmatter Contract

The draft must include:

- `title`
- `date` (`YYYY-MM-DD`)
- `slug` (lowercase letters, digits, hyphens)
- `category`
- `excerpt`
- `description`

## Markdown Support

The publisher supports common blocks:

- `##` and `###` headings
- paragraphs
- ordered lists (`1. item`)
- unordered lists (`- item`)
- blockquotes (`> line`)

If richer markdown is needed, publish first and then refine HTML manually.
