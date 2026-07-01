# claude-skill-llms-txt

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Built for Claude](https://img.shields.io/badge/Built%20for-Claude-d97757.svg)](https://claude.com/claude-code)
[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](.claude-plugin/plugin.json)

> Validate, author, and generate the whole llms.txt file family against the llmstxt.org and Mintlify specs.

By [Eric Forte](https://www.ericforte.com), AI Automation Engineer.

A Claude skill for the files that let AI engines read a site: `llms.txt`, `llms-full.txt`, `llms-ctx.txt`, `llms-ctx-full.txt`, and per-page `.md`. It knows the grammar from both standards, validates a file with a deterministic script, repairs the common mistakes, and generates the pieces you are missing. In Claude Code it also activates on its own the moment one of these files is edited or mentioned.

---

## Why this skill exists

The llms.txt spec has a strict shape, and most files in the wild drift from it: prose gets dropped inside a links-only section, contact rows get written as plain text instead of markdown links, a stray heading lands in the summary. On top of that, two standards overlap here. The core llmstxt.org grammar defines `llms.txt` plus the generated `llms-ctx` context files, while Mintlify popularized `llms-full.txt`, the single-file dump of a whole site. It is easy to conflate them.

This skill holds both specs with their sources, so edits stay correct instead of plausible. It checks a file against the real grammar, tells you exactly which line broke which rule, and never invents a rule that is not in the spec.

---

## What it does

- Validates `llms.txt` against the llmstxt.org grammar (H1, blockquote, headings-free body, H2 link-list sections, the Optional section).
- Recognizes and applies house rules to `llms-full.txt` (the Mintlify full-content dump) and per-page `.md`.
- Explains and generates the `llms-ctx.txt` and `llms-ctx-full.txt` context files via the reference tool.
- Repairs the common violations: non-link content in a links section, bare `Label: url` rows, headings in the body.
- Ships a standard-library validator script, so checks are deterministic and run anywhere Python does.
- Cites a primary source for every normative claim and refuses to state a rule the spec does not contain.

---

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

Works in Claude Code. For Claude Desktop, claude.ai, or cowork, add the `skills/llms-txt/` folder per the current skills install path for that surface. That folder is self-contained and needs no plugin manifest.

---

## Quick start

Invoke directly, or just point at a file and let it trigger:

```
/llms-txt:llms-txt
Audit my public/llms.txt and tell me what is off-spec.
```

In Claude Code the skill also wakes up on its own whenever you edit or mention an `llms.txt`, `llms-full.txt`, or `llms-ctx` file.

Run the validator on its own any time:

```bash
python3 skills/llms-txt/scripts/validate_llms_txt.py path/to/llms.txt
```

---

## Use cases

- Auditing a site's `/llms.txt` before shipping it.
- Fixing a file a generator produced that drifts from the spec.
- Authoring `llms.txt` and `llms-full.txt` from scratch for a new site.
- Generating `llms-ctx-full.txt` for pasting a whole doc set into an LLM.
- Keeping a hand-maintained `llms-full.txt` in sync and on house style.

---

## FAQ

**Is `llms-full.txt` part of the official spec?** No. The core llmstxt.org spec defines `llms.txt` and the generated `llms-ctx` files. `llms-full.txt` is a Mintlify convention, now widely used, for a single file holding a site's full content. This skill supports both and keeps the distinction clear.

**Does it change my files automatically?** No. It validates and proposes fixes. You decide what to apply.

**What are `llms-ctx.txt` and `llms-ctx-full.txt`?** Context files the `llms_txt2ctx` tool generates from your `llms.txt` (one excludes the Optional section, one includes it). The skill explains and generates them; you do not hand-edit them.

**Does the auto-activation work outside Claude Code?** The hook is Claude Code only. On Desktop, claude.ai, and cowork the skill triggers from its description when you mention or work on these files.

---

## Author

Built by **Eric Forte**, AI Automation Engineer.

- Website: [ericforte.com](https://www.ericforte.com)
- Blog: [ericforte.com/blog](https://www.ericforte.com/blog)
- LinkedIn: [@johnericforte](https://www.linkedin.com/in/johnericforte/)

---

## License

MIT. See [LICENSE](LICENSE).
