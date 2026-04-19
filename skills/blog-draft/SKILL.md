---
name: blog-draft
description: Create a new markdown blog draft in this repository using the shared post template. Use when the user wants to start a new blog post, define title/date/slug metadata, or create a consistent markdown source file before publishing.
---

# Blog Draft

Create a new markdown draft from `blog/_template.md` and save it to `blog/drafts/`.

## Workflow

1. Confirm the template exists at `blog/_template.md`.
2. Run `scripts/create_draft.py` with title and optional metadata.
3. Open the generated file and fill the post content.

## Command

```bash
python3 skills/blog-draft/scripts/create_draft.py "Post title" \
  --date 2026-04-04 \
  --slug post-slug \
  --excerpt "Lyhyt nosto blogin listaukseen." \
  --description "Hakukone- ja somekuvaus postaukselle."
```

## Output

- Draft path: `blog/drafts/YYYY-MM-DD-slug.md`
- Frontmatter fields required for publishing:
  - `title`
  - `date` (`YYYY-MM-DD`)
  - `slug` (lowercase, hyphenated)
  - `category`
  - `excerpt`
  - `description`

## Notes

- Keep slug stable after creation to avoid URL changes.
- Use Finnish or English content freely; script preserves UTF-8 text.
