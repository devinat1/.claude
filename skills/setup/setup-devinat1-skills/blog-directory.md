# Blog content directory

The `/blog` and `/update-blog-refs` skills read existing posts from this directory to match writing style and suggest cross-links.

## Path

Read `external_resources.blog_content` from `~/.agentic/index.json`.
Update that index entry when the blog moves.

## Notes

- Exclude `index.md` and any `images/` subdirectory when scanning posts.
- Post titles are typically the filename without `.md`.
