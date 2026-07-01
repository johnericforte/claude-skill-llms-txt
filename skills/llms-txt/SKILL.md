---
name: llms-txt
description: Use when reading, writing, editing, reviewing, auditing, or generating an llms.txt, llms-full.txt, llms-ctx.txt, llms-ctx-full.txt, or per-page .md file, or a site's AI-ingestion text files, across the llmstxt.org and Mintlify specs, even when the spec is not named. Covers the H1 + blockquote + H2 link-list grammar, the Optional section, the .md page convention, discovery headers, and llms_txt2ctx XML generation. Not for general markdown, robots.txt, or sitemap work.
---

# llms.txt family

These are the files that let AI engines read a site: `llms.txt`, `llms-full.txt`, `llms-ctx.txt`, `llms-ctx-full.txt`, and per-page `.md`. Two standards overlap here, and files in the wild drift from both. Your job is to keep them correct against the real grammar, not against a plausible guess.

Ground every rule in `reference/spec.md`. It holds the verbatim quotes and source URLs for the llmstxt.org spec and the Mintlify spec. If a rule is not quoted there, do not assert it. Read that file before making a ruling on anything subtle.

## The family, in one pass

- `llms.txt` is the curated index: an H1 name, a blockquote summary, optional body prose, then H2 sections that are lists of links. This is the file with a strict grammar.
- `llms-full.txt` is a Mintlify convention: one markdown file holding the whole site's content. It is a dump, not an index. It is not in the core llmstxt.org spec.
- `llms-ctx.txt` and `llms-ctx-full.txt` are generated from `llms.txt` by the `llms_txt2ctx` tool. One excludes the Optional section, one includes it. You do not hand-edit these.
- Per-page `.md` is the clean markdown of a single page, served at the page URL with `.md` appended.

See the family table in `reference/spec.md` for origin and lineage. The one trap to avoid: `llms-full.txt` (Mintlify) and `llms-ctx-full.txt` (Answer.AI tooling) are different files from different lineages. Keep them straight.

## Validate a file

Run the bundled validator. It is Python standard library only, so it runs anywhere Python does, including a code sandbox.

```
python3 scripts/validate_llms_txt.py <path>
```

It picks the check from the file's basename. For a draft that is not named yet, force the type:

```
python3 scripts/validate_llms_txt.py draft.txt --as llms.txt
```

Add `--json` for machine-readable output. Exit code is 0 for clean or warnings only, 1 for hard errors. Read the findings, then explain each in plain terms and offer the fix. Do not stop at the script output; the script finds the lines, you decide the repair.

What the `llms.txt` check enforces, from the spec:

- Exactly one H1, and it is the first content line. The H1 is the only required section.
- No heading of any level in the body before the first H2. The body is prose and lists only; headings resume at the H2 file-list sections.
- Every list item inside an H2 section is a `[name](url)` markdown link, with an optional `: description` after it. A bare `- Label: https://...` row is the common miss.
- The `## Optional` section is the one whose links a shorter-context tool may skip. Treat it as secondary.

Both link styles are valid: a link to an HTML page (llmstxt.org style) and a link that carries a `.md` extension to the markdown version (Mintlify style). Do not flag one for being the other.

## Repair and author

When a file is off-spec, the fixes are usually structural, not creative:

- Prose or a non-link list sitting inside an H2 section: move it up into the body (the prose area before the first H2), or convert it into proper `[name](url)` links if it was meant to be a file list. A `## Pricing` section written as sentences belongs in the body; a `## Contact` list of `- Label: url` rows should become `- [Label](url)` links.
- A heading in the body: either promote the section to a real H2 file-list section (if it introduces links) or demote it to bold text or plain prose.
- More than one H1: keep the site name as the single H1; the rest become H2s or body text.

When authoring from scratch, follow the order in `reference/spec.md`: H1 name, blockquote summary, short body context, then H2 sections of links, with `## Optional` last for secondary links. For a Mintlify-style site, list page links alphabetically from the repo root and give each a short description from the page's own summary.

## Generate the context files

`llms-ctx.txt` and `llms-ctx-full.txt` come from the reference tool, not from your keyboard:

```
pip install llms-txt
llms_txt2ctx path/to/llms.txt > llms-ctx.txt
```

`llms-ctx-full.txt` is the same generation including the Optional section's links. The output is an XML structure meant to be pasted into an LLM. If someone asks you to edit a `llms-ctx` file by hand, redirect them: change the source `llms.txt` and regenerate.

## llms-full.txt

This is the Mintlify single-file dump of the full site content. Author or maintain it as one clean markdown file, not as an index of links. Run the validator on it to catch house-rule issues (no em dashes, no banned terms). If a site is on Mintlify, this file is auto-generated and a custom file at the same path overrides it; hand-maintain it only when you mean to override.

## Per-page .md and discovery

- Per-page markdown lives at the page URL with `.md` appended. A directory URL uses `index.html.md`.
- Mintlify also serves the files at `/.well-known/llms.txt` and `/.well-known/llms-full.txt`, and advertises them with a `Link` header (`rel="llms-txt"` and `rel="llms-full-txt"`) plus an `X-Llms-Txt` header. When advising on discovery, point to these.

## Why this matters

An llms.txt that drifts from the grammar still renders in a browser, so the breakage is silent: a strict parser drops the malformed lines, and the site loses exactly the context it published the file to provide. Getting the shape right is the whole value. Validate, explain, fix, and only assert rules you can quote from `reference/spec.md`.
