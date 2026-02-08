# Repository Guidelines

## Project Structure & Module Organization
- `index.html` is the single-page entry point and contains the page markup.
- `styles.css` holds all styling for typography, layout, and backgrounds.
- `assets/` stores static assets such as `assets/logos/` and `assets/fonts/`.
- `favicon.svg` and `CNAME` support deployment and branding.

Keep changes minimal and focused: update HTML for content structure and CSS for visuals, and add new assets under `assets/` with clear, descriptive names.

## Build, Test, and Development Commands
This is a static site, so there is no build step.
- `python3 -m http.server` serves the site locally at `http://localhost:8000`.
- `open index.html` (or your OS equivalent) opens the page directly without a server.

Use the local server when testing fonts or asset paths to match production behavior.

## Coding Style & Naming Conventions
- Indentation: 2 spaces in both HTML and CSS.
- Use lowercase, hyphenated class names (e.g., `.header-inner`, `.idea-card`).
- Keep CSS grouped by component and avoid unused selectors.
- Prefer semantic HTML elements (`header`, `main`, `h1`, `p`) for structure.

No formatter is configured; keep style consistent with existing files.

## Testing Guidelines
There are no automated tests. Validate changes by loading the page and checking:
- Layout at multiple viewport widths.
- Asset loading (fonts, logos, background images).
- Visual contrast and readability.

## Commit & Pull Request Guidelines
- Commit messages are short and imperative (e.g., “simplify front page”).
- Keep commits focused on a single visual or content change.
- PRs should include a brief summary and before/after screenshots for UI changes.
- Link any relevant issue or brief design reference when available.

## Security & Configuration Tips
- Avoid introducing external scripts or dependencies without discussion.
- Keep all assets committed locally; do not hotlink fonts or images.
