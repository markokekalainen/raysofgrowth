Create a new markdown blog draft using the shared post template.

## Steps

1. Confirm the template exists at `blog/_template.md`.
2. Run the draft creation script:

```bash
python3 skills/blog-draft/scripts/create_draft.py "Post title" \
  --date YYYY-MM-DD \
  --slug post-slug \
  --excerpt "Lyhyt nosto blogin listaukseen." \
  --description "Hakukone- ja somekuvaus postaukselle."
```

3. Open the generated file at `blog/drafts/YYYY-MM-DD-slug.md` and fill in the post content.

## Notes

- If `$ARGUMENTS` is provided, use it as the post title and derive a slug from it (lowercase, hyphens). Ask for any missing required metadata before running the script.
- Required frontmatter: `title`, `date` (YYYY-MM-DD), `slug`, `category`, `excerpt`, `description`.
- Keep the slug stable after creation to avoid URL changes.
- Use today's date unless the user specifies otherwise.
