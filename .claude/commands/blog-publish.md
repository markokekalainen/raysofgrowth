Publish a markdown blog draft into the static HTML blog structure.

## Steps

1. Validate the draft has all required frontmatter: `title`, `date`, `slug`, `category`, `excerpt`, `description`.
2. Run the publish script:

```bash
python3 skills/blog-publish/scripts/publish_post.py blog/drafts/YYYY-MM-DD-slug.md
```

Optional flags:
- `--overwrite`: replace existing `blog/<slug>/index.html`
- `--skip-sitemap`: skip `sitemap.xml` edits

3. Verify the output:
   - `blog/<slug>/index.html` was created
   - A post card was prepended to `blog/index.html`
   - The post URL was appended to `sitemap.xml`

## Notes

- If `$ARGUMENTS` is provided, treat it as the draft file path. Otherwise look for drafts in `blog/drafts/` and ask the user which to publish.
- Supported markdown blocks: `##`/`###` headings, paragraphs, ordered lists, unordered lists, blockquotes.
- For richer markdown, publish first and refine the HTML manually.
