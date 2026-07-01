#!/usr/bin/env python3
"""Auto-activation gate for the llms-txt skill (Claude Code hook).

Reads the hook JSON on stdin.
- UserPromptSubmit: if the prompt mentions an llms.txt-family file, print a
  reminder to stdout. On this event, stdout is added to the model's context.
- PostToolUse (Edit|Write|MultiEdit): if the edited file's basename is an
  llms.txt-family file, print a {"systemMessage": ...} object so the reminder
  reaches the model.
Otherwise print nothing. Always exit 0 so the hook never blocks the tool.

Uses the Python standard library only, so it needs no jq or other dependency.
"""
import sys, os, re, json

REMINDER = (
    "llms.txt-family file in play. Use the llms-txt skill: validate against the "
    "llmstxt.org and Mintlify specs (H1 is the only required section, blockquote "
    "summary, body has no headings, H2 sections are [name](url) link lists, "
    "## Optional is skippable, per-page .md convention). llms-full.txt is the "
    "Mintlify full-content dump; llms-ctx.txt and llms-ctx-full.txt are generated "
    "by llms_txt2ctx, not hand-edited. Run scripts/validate_llms_txt.py on the file."
)

NAME_RE = re.compile(r'^llms(-full|-ctx|-ctx-full)?\.txt$', re.I)
MENTION_RE = re.compile(r'llms(-full|-ctx|-ctx-full)?\.txt|llmstxt', re.I)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    event = data.get('hook_event_name', '')
    if event == 'UserPromptSubmit':
        prompt = data.get('user_prompt', '') or ''
        if MENTION_RE.search(prompt):
            print(REMINDER)
        return 0
    if event == 'PostToolUse':
        fp = (data.get('tool_input') or {}).get('file_path', '') or ''
        if NAME_RE.match(os.path.basename(fp)):
            print(json.dumps({'systemMessage': REMINDER}))
        return 0
    return 0


if __name__ == '__main__':
    sys.exit(main())
