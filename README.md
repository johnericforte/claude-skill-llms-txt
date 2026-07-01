# claude-skill-llms-txt: validate and generate llms.txt for AI search and Google Agentic Browsing

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Built for Claude](https://img.shields.io/badge/Built%20for-Claude-d97757.svg)](https://claude.com/claude-code)
[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](.claude-plugin/plugin.json)

> A Claude skill that validates, authors, and generates the whole llms.txt file family against the llmstxt.org and Mintlify specs, so your site passes Google's Lighthouse Agentic Browsing check and reads cleanly for AI search.

By [Eric Forte](https://www.ericforte.com), AI Automation Engineer.

**claude-skill-llms-txt** is a Claude skill (and Claude Code plugin) that checks and builds the files AI engines read: `llms.txt`, `llms-full.txt`, `llms-ctx.txt`, `llms-ctx-full.txt`, and per-page `.md`. It aligns them to the llmstxt.org spec and the Mintlify convention, which is what Google's Lighthouse **Agentic Browsing** score in PageSpeed Insights checks under "llms.txt follows recommendations." This is generative engine optimization (GEO) and answer engine optimization (AEO) for the era where ChatGPT, Perplexity, Claude, and Google AI Overviews read your site directly.

## Why I built it

I ran ericforte.com through PageSpeed Insights and it passed the Agentic Browsing score 3/3. One passed audit read:

> **llms.txt follows recommendations.** If your llms.txt file does not follow recommendations, large language models may not be able to understand how you want your website to be crawled or used for training. The llms.txt file should be a Markdown file containing at least one H1 header.

That check ([Chrome Lighthouse Agentic Browsing scoring](https://developer.chrome.com/docs/lighthouse/agentic-browsing/scoring)) is the reason this skill exists. Passing the header check is the floor. Following the full spec, keeping the file in sync, and adding the rest of the family is the work, and doing it by hand is easy to get subtly wrong. This skill makes it repeatable, for my site and yours.

## What is llms.txt?

`llms.txt` is a Markdown file at the root of a site (`/llms.txt`) that gives large language models a curated map of your content: an H1 site name, a blockquote summary, and H2 sections listing your key pages as links. It was proposed by Jeremy Howard of Answer.AI in September 2024 and is now served by thousands of sites, including through Mintlify's auto-generation. `llms-full.txt`, the Mintlify companion, holds the full text of every page in one file.

## What is Google Agentic Browsing scoring?

Agentic Browsing is a category in Google's Lighthouse (and PageSpeed Insights) that measures how ready a site is for AI agents to read and act on, using deterministic audits and a fractional pass score. Its "llms.txt follows recommendations" audit checks that your `llms.txt` is a Markdown file with at least one H1. This skill validates that and the rest of the llmstxt.org grammar, so the check passes and the file is genuinely useful to the models behind AI search.

## What this skill does

- Validates `llms.txt` against the real grammar: single H1, blockquote summary, headings-free body, H2 sections that are `[name](url)` link lists, correct `## Optional` section.
- Flags the subtle mistakes: prose or bare labels inside an H2, non-fetchable link targets (`mailto:`, relative), stray headings, and HTML links that should point at `.md`.
- Authors and repairs `llms.txt` from scratch or from a drifted file.
- Generates the `llms-ctx.txt` and `llms-ctx-full.txt` context files via the reference tool.
- Guides per-page `.md`, discovery headers (`Link`, `X-Llms-Txt`), and `/.well-known/` across any tech stack.
- Ships a deterministic, dependency-free Python validator and a Claude Code hook that auto-activates when you touch any of these files.

## Who it helps

Anyone who wants their site read correctly by AI search and to pass Google's Agentic Browsing check: founders, marketers, and engineers on Next.js, Astro, Hugo, WordPress, Mintlify, or plain HTML. The skill validates the files (stack-neutral) and gives per-stack guidance for serving and discovery.

## Install

### Option A: git clone (works today)

```bash
git clone https://github.com/johnericforte/claude-skill-llms-txt.git
claude --plugin-dir claude-skill-llms-txt
```

The skill loads as `llms-txt:llms-txt`.

### Option B: plugin marketplace

```
/plugin install llms-txt
```

Works in Claude Code. For Claude Desktop, claude.ai, or cowork, add the `skills/llms-txt/` folder per that surface's skills install path. That folder is self-contained.

## Quick start

```
/llms-txt:llms-txt
Audit my public/llms.txt and tell me what is off-spec.
```

Or run the validator directly on any file:

```bash
python3 skills/llms-txt/scripts/validate_llms_txt.py path/to/llms.txt
```

## The llms.txt family

| File | What it is |
| --- | --- |
| `llms.txt` | Curated index: H1, summary, H2 link lists. What Agentic Browsing checks. |
| `llms-full.txt` | Mintlify convention: the whole site's content in one Markdown file. |
| `llms-ctx.txt` / `llms-ctx-full.txt` | XML context generated from `llms.txt` by `llms_txt2ctx`. |
| per-page `.md` | Clean Markdown of each page at its URL plus `.md`. |

## Supported stacks

Serving the files, adding the discovery headers, and generating per-page `.md` vary by stack. The skill's `reference/stacks.md` covers static generators (Hugo, Jekyll, Astro, Eleventy), Next.js and Vercel, Netlify, Apache, Nginx, WordPress, and managed docs (Mintlify, GitBook).

## FAQ

### Is llms.txt part of SEO?

It is part of the newer branch of SEO aimed at AI: GEO (generative engine optimization) and AEO (answer engine optimization). Traditional SEO helps you rank in search results. llms.txt helps large language models read and cite your site, and it is now scored directly by Google's Lighthouse Agentic Browsing audit.

### Does llms.txt affect my Google Agentic Browsing score?

Yes. The Agentic Browsing category in PageSpeed Insights includes an "llms.txt follows recommendations" audit. A valid `llms.txt` (Markdown with at least one H1, following the spec) is what passes it.

### What is the difference between llms-full.txt and llms-ctx-full.txt?

`llms-full.txt` is a Mintlify convention: one Markdown file with the full site content. `llms-ctx-full.txt` is an XML context file generated from `llms.txt` by the `llms_txt2ctx` tool, including the Optional section. Different lineages, different jobs.

### Which AI crawlers use these files?

The files are read by the crawlers behind AI search and assistants, including OpenAI's GPTBot and OAI-SearchBot (ChatGPT), Anthropic's ClaudeBot (Claude), and PerplexityBot (Perplexity). A clean `llms.txt` gives them a curated map instead of leaving them to guess from raw HTML.

### Do I need a specific tech stack?

No. The validator parses the files, so validation and authoring are stack-neutral. Serving and discovery have per-stack recipes in `reference/stacks.md`.

## Author

Built by **Eric Forte**, AI Automation Engineer.

- Website: [ericforte.com](https://www.ericforte.com)
- Blog: [ericforte.com/blog](https://www.ericforte.com/blog)
- LinkedIn: [@johnericforte](https://www.linkedin.com/in/johnericforte/)

## Changelog

- **0.2.0**: Validator now flags non-link content and non-fetchable link targets inside H2 sections, and checks `llms-full.txt` for an H1 and index-vs-dump shape. Added `reference/stacks.md` for serving, discovery headers, and per-page `.md` across static generators, Next.js/Vercel, Netlify, Apache, Nginx, WordPress, and managed docs. Rewrote the context-file guidance for how the tool actually behaves.
- **0.1.0**: Initial release: validator, spec reference, and auto-activation hooks.

## License

MIT. See [LICENSE](LICENSE).
