# Serving the llms.txt family per stack

The files are the same everywhere. Only three tasks depend on the stack: serving the files, adding the discovery headers, and generating per-page `.md`. This reference maps those three to the common stacks.

Exact header and rewrite syntax changes between platform versions. Treat the snippets below as the shape to aim for, and confirm the current form in that platform's own docs. Do not assume a snippet is current without checking.

## The three stack-specific tasks

1. Serve `/llms.txt`, `/llms-full.txt`, and each page's `.md` (page URL + `.md`, directory URLs use `index.html.md`).
2. Advertise the files: a `Link` header (`rel="llms-txt"` and `rel="llms-full-txt"`) plus an `X-Llms-Txt` header, and serve the files under `/.well-known/` too.
3. Generate a clean `.md` for each page.

## Static site generators (Hugo, Jekyll, Astro, Eleventy, plain HTML, S3 or CDN)

- Serve: drop `llms.txt`, `llms-full.txt`, and the `.md` files into the output or static directory (Hugo `static/`, Jekyll site root, Astro/Eleventy `public/`). They ship as plain files.
- Per-page `.md`: most generators can emit a Markdown copy next to each HTML page through an output format or a small build step that writes the page's source Markdown to `<path>.md`. If the generator has no hook, a post-build script that walks the content tree and writes the `.md` files works.
- Discovery: static hosts do not run app code, so set the `Link` and `X-Llms-Txt` headers and the `/.well-known/` aliases in the host's config (see Netlify, Apache, or Nginx below, or the CDN's header rules).

## Next.js and Vercel

- Serve: static files in `public/` (served at the site root), or a Route Handler that returns the content with `Content-Type: text/markdown`.
- Discovery: `next.config` `headers()` for the `Link` and `X-Llms-Txt` headers, and `rewrites()` for `/.well-known/llms.txt` -> `/llms.txt`. This is the config already running on ericforte.com. On Vercel without Next config, `vercel.json` `headers` and `rewrites` do the same.
- Per-page `.md`: generate static `.md` into `public/` from your content source (this repo does that from Sanity for projects and from `llms-full.txt` for posts), or add a Route Handler per section that renders Markdown on demand.

`vercel.json` shape:

```json
{
  "headers": [
    { "source": "/(.*)", "headers": [
      { "key": "Link", "value": "</llms.txt>; rel=\"llms-txt\", </llms-full.txt>; rel=\"llms-full-txt\"" },
      { "key": "X-Llms-Txt", "value": "/llms.txt" }
    ]}
  ],
  "rewrites": [
    { "source": "/.well-known/llms.txt", "destination": "/llms.txt" },
    { "source": "/.well-known/llms-full.txt", "destination": "/llms-full.txt" }
  ]
}
```

## Netlify

- Serve: place the files in the publish directory.
- Discovery with a `_headers` file:

```
/*
  Link: </llms.txt>; rel="llms-txt", </llms-full.txt>; rel="llms-full-txt"
  X-Llms-Txt: /llms.txt
```

- `/.well-known/` with a `_redirects` file (200 keeps the URL):

```
/.well-known/llms.txt        /llms.txt        200
/.well-known/llms-full.txt   /llms-full.txt   200
```

## Apache

Serve the files normally. In `.htaccess` or the vhost, with `mod_headers` enabled:

```
Header set Link "</llms.txt>; rel=\"llms-txt\", </llms-full.txt>; rel=\"llms-full-txt\""
Header set X-Llms-Txt "/llms.txt"
Alias /.well-known/llms.txt /var/www/html/llms.txt
```

## Nginx

```
add_header Link '</llms.txt>; rel="llms-txt", </llms-full.txt>; rel="llms-full-txt"' always;
add_header X-Llms-Txt "/llms.txt" always;

location = /.well-known/llms.txt { alias /var/www/html/llms.txt; }
location = /.well-known/llms-full.txt { alias /var/www/html/llms-full.txt; }
```

## WordPress and other CMS

- Serve: an llms.txt plugin can generate and host `/llms.txt` (and often `/llms-full.txt`) from your posts and pages. Without a plugin, add a rewrite rule or a small template that outputs the file.
- Per-page `.md`: needs a template or plugin that renders each post as Markdown at its URL + `.md`. Confirm the chosen plugin actually emits per-page Markdown, since many only produce the index.
- Discovery: set the headers at the server or CDN layer (Apache, Nginx, or Cloudflare), since the CMS may not control response headers for static paths.

## Managed docs (Mintlify, GitBook)

- These auto-generate `/llms.txt` and `/llms-full.txt` and serve the `.md` versions and discovery headers for you. Do not hand-maintain the files unless you mean to override the generated ones. On Mintlify a custom file at the same path overrides the auto-generated one, and deleting it restores the default.

## Generating the context files anywhere

`llms-ctx.txt` and `llms-ctx-full.txt` do not depend on the stack. Run `llms_txt2ctx` against the deployed `llms.txt` once the pages and their `.md` versions are live. See the ctx section in `SKILL.md`.
