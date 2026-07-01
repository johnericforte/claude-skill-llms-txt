---
name: llms-txt
description: Use when reading, writing, editing, reviewing, auditing, or generating an llms.txt, llms-full.txt, llms-ctx.txt, llms-ctx-full.txt, or per-page .md file, or a site's AI-ingestion text files, across the llmstxt.org and Mintlify specs, even when the spec is not named. Covers the H1 + blockquote + H2 link-list grammar, the Optional section, the .md page convention, discovery headers, and llms_txt2ctx XML generation for any tech stack. Not for general markdown, robots.txt, or sitemap work.
---

# llms.txt family

These are the files that let AI engines read a site: `llms.txt`, `llms-full.txt`, `llms-ctx.txt`, `llms-ctx-full.txt`, and per-page `.md`. Two standards overlap here, and files in the wild drift from both. Your job is to keep them correct against the real grammar, not against a plausible guess.

The files are the same on every stack. Validating and authoring them is stack-neutral. Only three things depend on the stack: serving the files, adding the discovery headers, and generating the per-page `.md`. Those live in `reference/stacks.md`. The grammar and sources live in `reference/spec.md`. Read `spec.md` before ruling on anything subtle; if a rule is not quoted there, do not assert it.

## The family, in one pass

- `llms.txt` is the curated index: an H1 name, a blockquote summary, optional body prose, then H2 sections that are lists of links. This is the file with a strict grammar.
- `llms-full.txt` is a Mintlify convention: one markdown file holding the whole site's content. A dump, not an index. Not in the core llmstxt.org spec.
- `llms-ctx.txt` and `llms-ctx-full.txt` are generated from `llms.txt` by the `llms_txt2ctx` tool. One excludes the Optional section, one includes it. You do not hand-edit these.
- Per-page `.md` is the clean markdown of a single page, served at the page URL with `.md` appended.

The one trap to avoid: `llms-full.txt` (Mintlify) and `llms-ctx-full.txt` (Answer.AI tooling) are different files from different lineages. Keep them straight.

## Validate a file

Run the bundled validator. It is Python standard library only, so it runs anywhere Python does.

```
python3 scripts/validate_llms_txt.py <path>
```

It picks the check from the file's basename. For a draft that is not named yet, force the type with `--as llms.txt`. Add `--json` for machine-readable output. Findings come in three levels: error (exit 1), warn, and note (advisory). Read them, explain each in plain terms, and offer the fix.

What the `llms.txt` check enforces, from the spec:

- Exactly one H1, and it is the first content line. The H1 is the only required section.
- No heading of any level in the body before the first H2. The body is prose and lists only.
- Every non-blank line inside an H2 section is a `[name](url)` markdown link. Prose, stray headings, and bare `- Label: url` rows are all flagged, because H2 sections are file lists.
- Each H2 link target is a fetchable `http(s)` URL. A `mailto:`, relative, or `#` target is flagged, because the context tool fetches these (see below).
- The `## Optional` section is the one whose links a shorter-context tool may skip.

## The rule that keeps context clean

H2 sections are lists of your own fetchable document pages. `llms_txt2ctx` downloads every H2 link to build the context file, so anything that is not a fetchable page breaks or pollutes it. Put contact details, email (`mailto:`), and external links (a booking page, social profiles) in the body, not in an H2 link section. The body accepts prose and lists, so that is where non-page information belongs.

## Repair and author

When a file is off-spec, the fixes are structural:

- Prose or a non-link list sitting inside an H2 section: move it into the body (before the first H2), or convert it to `[name](url)` links if it was meant to be a file list. A `## Pricing` section written as sentences belongs in the body.
- Contact and external links inside an H2 section: move them into the body as plain text. Keep the H2 sections to your own site pages.
- A heading in the body: promote the section to a real H2 file-list section, or demote it to bold text.
- More than one H1: keep the site name as the single H1; the rest become H2s or body text.

When authoring from scratch, follow the order in `reference/spec.md`: H1 name, blockquote summary, short body context, then H2 sections of links, with `## Optional` last. Both link styles are valid: a link to an HTML page (llmstxt.org style) and a link that carries a `.md` extension (Mintlify style).

## Per-page .md

Each page gets a clean markdown copy at its URL plus `.md` (a directory URL uses `index.html.md`). Source it from the page's own content, not from a summary: a CMS body, the page's markdown source, or an HTML-to-markdown pass on the rendered page. Give the page title a single top-level `# ` heading and shift the body headings down so nothing competes with it (a section that was `##` on a page fed by a larger file becomes `##` here under the one `#`). How to serve these varies by stack, see `reference/stacks.md`.

Linking `llms.txt` at the `.md` versions (the Mintlify style) is what lets the context tool build clean markdown instead of inlining raw HTML. If the validator notes that H2 links point to non-`.md` pages, that is the fix.

## Generate the context files

`llms-ctx.txt` and `llms-ctx-full.txt` come from the reference tool, not from your keyboard. It fetches every H2 link and inlines it, so a few realities matter:

- Install without a global pip: `pipx run --spec llms-txt llms_txt2ctx ...`, or `uvx --from llms-txt llms_txt2ctx ...`, or a throwaway venv (`python3 -m venv .venv && .venv/bin/pip install llms-txt`). A bare `pip install` fails on a managed Python (PEP 668).
- Run it against the DEPLOYED site, after the pages and their `.md` files are live. It fetches live URLs; local files and dynamic routes (a generated sitemap or robots) will not resolve on your machine.
- Point `llms.txt` links at the `.md` versions first. Otherwise the tool inlines each page's raw HTML and the output balloons.
- Strip the tool's diagnostic lines: it prints the parsed link list before the real output, so drop everything before the first `<project` line.

```
llms_txt2ctx llms.txt > llms-ctx.txt            # excludes the Optional section
llms_txt2ctx llms.txt --optional True > llms-ctx-full.txt   # includes it
```

The output is an XML structure meant to be pasted into an LLM. If someone asks you to edit a `llms-ctx` file by hand, redirect them: change the source `llms.txt` and regenerate.

## llms-full.txt

This is the Mintlify single-file dump of the full site content. Author or maintain it as one clean markdown file, not an index of links. The validator warns if it has no H1 or if it reads like a link index. If a site is on Mintlify, this file is auto-generated and a custom file at the same path overrides it.

## Serve and advertise the files

Serving the files, adding the `Link` and `X-Llms-Txt` discovery headers, and exposing `/.well-known/llms.txt` all depend on the stack. See `reference/stacks.md` for static generators, Next.js and Vercel, Netlify, Apache, Nginx, WordPress, and managed docs. Do not assume the Next.js approach fits another stack.

## Why this matters

An llms.txt that drifts from the grammar still renders in a browser, so the breakage is silent: a strict parser drops the malformed lines, and the site loses exactly the context it published the file to provide. Getting the shape right is the whole value. Validate, explain, fix, and only assert rules you can quote from `reference/spec.md`.
