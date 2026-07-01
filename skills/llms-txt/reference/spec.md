# llms.txt family: specs and sources

Every normative claim below carries a verbatim quote and a source URL. If a rule is not quoted here, do not assert it as spec.

## The five artifacts

| Artifact | Origin | What it is | Skill role |
| --- | --- | --- | --- |
| `llms.txt` | llmstxt.org (Answer.AI, Jeremy Howard) and Mintlify | Curated index: H1 + blockquote + body + H2 link-list sections | validate, author, repair |
| `llms-ctx.txt` | llmstxt.org tooling (`llms_txt2ctx`) | XML context generated from `llms.txt`, excludes the Optional section | generate, explain |
| `llms-ctx-full.txt` | llmstxt.org tooling (`llms_txt2ctx`) | XML context generated from `llms.txt`, includes the Optional section | generate, explain |
| `llms-full.txt` | Mintlify (with Anthropic) | One markdown file holding the site's full content | author, house-rule check |
| per-page `.md` | llmstxt.org and Mintlify | Clean markdown of each page at the page URL + `.md` | advise, check links |

Two lineages meet here. The `llms-ctx*.txt` files come from the Answer.AI reference tool. `llms-full.txt` is Mintlify's. Do not conflate them: the string "llms-full.txt" does not appear in the core llmstxt.org spec.

## llmstxt.org spec

Source: https://llmstxt.org/

- Location: the file lives at `/llms.txt` at the root of a site (a subpath is allowed).
- Ordered structure (quote): "An optional byte-order mark (BOM) - An H1 with the name of the project or site. This is the only required section - A blockquote with a short summary of the project, containing key information necessary for understanding the rest of the file - Zero or more markdown sections (e.g. paragraphs, lists, etc) of any type except headings, containing more detailed information about the project and how to interpret the provided files - Zero or more markdown sections delimited by H2 headers, containing 'file lists' of URLs where further detail is available".
- The H1 is the only required section (quote): "This is the only required section".
- File-list item format (quote): "Each 'file list' is a markdown list, containing a required markdown hyperlink `[name](url)`, then optionally a `:` and notes about the file".
- The Optional section (quote): "Note that the 'Optional' section has a special meaning, if it's included, the URLs provided there can be skipped if a shorter context is needed".
- Per-page markdown (quote): "provide a clean markdown version of those pages at the same URL as the original page, but with `.md` appended. (URLs without file names should append `index.html.md` instead.)".
- Context tooling (quote): the context files "are created using the `llms_txt2ctx` command line application"; the tool produces "llms-ctx.txt, which does not include the optional URLs, and llms-ctx-full.txt, which does include them", in "an XML-based structure suitable for use in LLMs such as Claude".

Read from this: the body carries free prose and lists but no headings; headings resume only at the H2 file-list sections; each file-list item must be a markdown link, with the note after the colon optional; the Optional section is the one whose links a shorter context may drop.

## Mintlify spec

Source: https://mintlify.com/docs/ai/llmstxt

- llms.txt (quote): Mintlify "automatically hosts an `llms.txt` file at the root of your project that lists all available pages in your documentation".
- llms-full.txt (quote): Mintlify "automatically hosts an `llms-full.txt` file at the root of your project" combining "your entire documentation site into a single file as context for AI tools and LLM indexing".
- Also served at `/.well-known/llms.txt` and `/.well-known/llms-full.txt`.
- Discovery headers (quote): `Link: </llms.txt>; rel="llms-txt", </llms-full.txt>; rel="llms-full-txt"` and `X-Llms-Txt: /llms.txt`.
- llms.txt structure (quote): "Site title as an H1 heading. Site description as a blockquote summary below the title. Structured content sections with links and a description of each page".
- Ordering and links (quote): pages are listed "alphabetically in the order they appear in your repository, starting from the root directory. Page links in the `llms.txt` file include a `.md` extension so AI tools can fetch the Markdown version".
- Descriptions (quote): sourced from frontmatter's `description` field, "truncate at 300 characters and the first line break".
- Overrides (quote): "Adding a custom file overrides the automatically generated file of the same name. If you delete a custom file, Mintlify restores the automatically generated file".

Read from this: Mintlify's llms.txt matches the llmstxt.org shape, with two house choices worth noting, links carry a `.md` extension (they point at the markdown version of each page), and page entries are alphabetical from the repo root. Both the plain-HTML link style and the `.md`-link style are valid.

## Checklist: common violations

For `llms.txt`:
- Missing H1, or the H1 is not the first content line, or more than one H1.
- A heading (any level) in the body before the first H2. The body is prose and lists only.
- A list item inside an H2 section that is not a `[name](url)` markdown link (for example a bare `- Label: https://...` row).
- Misusing the `## Optional` section, or expecting a shorter-context tool to keep its links.

For `llms-full.txt`: it is a single markdown file of the full content, not a link index. Check house rules (no em dashes, no banned terms) and that it is not accidentally structured as an index.

For `llms-ctx.txt` / `llms-ctx-full.txt`: these are generated by `llms_txt2ctx`, not hand-edited. Regenerate from `llms.txt` rather than editing.

For per-page `.md`: the markdown lives at the page URL + `.md` (or `index.html.md` for directory URLs).
