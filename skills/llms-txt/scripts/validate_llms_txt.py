#!/usr/bin/env python3
"""Validate an llms.txt-family file against the llmstxt.org and Mintlify specs.

Usage: validate_llms_txt.py <path> [--json] [--as <name>]
  llms.txt               -> full llmstxt.org grammar check
  llms-full.txt          -> Mintlify full-dump checks
  llms-ctx*.txt          -> generated XML context: recognize + house-rules
  *.md                   -> per-page markdown: house-rules only
The check type is chosen from the file's basename. Use --as to override it
when the file is not yet named (e.g. --as llms.txt to grammar-check a draft).

Findings have three levels: error (exit 1), warn, and note (advisory).
Exit 0 = clean, warnings, or notes only. Exit 1 = at least one error.
"""
import sys, os, re, json

LINK_ITEM_RE = re.compile(r'^- \[[^\]]+\]\([^)]+\)(: .+)?$')
LINK_URL_RE = re.compile(r'^- \[[^\]]+\]\(([^)]+)\)')
BARE_LABEL_RE = re.compile(r'^- [^\[].*:\s*https?://')
HEADING_RE = re.compile(r'^#{1,6} ')
HTTP_RE = re.compile(r'^https?://', re.I)
MD_URL_RE = re.compile(r'\.md($|[?#])', re.I)
KEEP_EXT_RE = re.compile(r'\.(xml|txt|json|md)($|[?#])', re.I)
EM_DASH = '—'
BANNED = ('piecemeal', 'runs out of road')


def house_rules(lines):
    out = []
    for i, l in enumerate(lines, 1):
        if EM_DASH in l:
            out.append(('warn', i, 'Em dash present (house rule: use none).'))
        low = l.lower()
        for b in BANNED:
            if b in low:
                out.append(('warn', i, f'Banned term "{b}".'))
    return out


def strip_bom(body):
    if body and body[0].startswith('﻿'):
        body[0] = body[0][1:]
    return body


def check_llms_txt(lines):
    f = []
    body = strip_bom([l.rstrip('\n') for l in lines])
    first = next((i for i, l in enumerate(body) if l.strip() != ''), 0)

    # H1: exactly one, first content line
    h1s = [i for i, l in enumerate(body) if l.startswith('# ') and not l.startswith('## ')]
    if not h1s:
        f.append(('error', 1, 'Missing required H1 (the only required section).'))
    else:
        if h1s[0] != first:
            f.append(('error', h1s[0] + 1, 'H1 must be the first content line.'))
        for extra in h1s[1:]:
            f.append(('error', extra + 1, 'Only one H1 is allowed.'))

    # Body (before first H2) must not contain headings
    h2s = [i for i, l in enumerate(body) if l.startswith('## ')]
    first_h2 = h2s[0] if h2s else len(body)
    for i in range(first + 1, first_h2):
        if HEADING_RE.match(body[i]):
            f.append(('error', i + 1, 'Heading not allowed in the body before the first H2.'))

    # H2 sections are file lists: every non-blank line is a [name](url) item
    has_non_md_http = False
    for s in h2s:
        header = body[s][3:].strip()
        nxt = next((j for j in h2s if j > s), len(body))
        for i in range(s + 1, nxt):
            l = body[i]
            if l.strip() == '':
                continue
            if l.startswith('- ') and LINK_ITEM_RE.match(l):
                m = LINK_URL_RE.match(l)
                url = m.group(1) if m else ''
                if not HTTP_RE.match(url):
                    f.append(('warn', i + 1, f'Link target "{url}" is not http(s); llms_txt2ctx cannot fetch it. Use a fetchable doc URL or move this to the body. (section "{header}")'))
                elif not KEEP_EXT_RE.search(url):
                    has_non_md_http = True
            elif l.startswith('- '):
                if BARE_LABEL_RE.match(l):
                    f.append(('warn', i + 1, f'Bare "- Label: url" is not a markdown link; spec wants [name](url). (section "{header}")'))
                else:
                    f.append(('warn', i + 1, f'List item is not a [name](url) file-list link. (section "{header}")'))
            else:
                f.append(('warn', i + 1, f'Non-link content inside an H2 section (H2 sections are link lists; move prose to the body before the first H2). (section "{header}")'))

    if has_non_md_http:
        f.append(('note', 0, 'Some H2 links point to HTML pages, not .md. llms_txt2ctx will inline page HTML; point links at the .md versions for clean context.'))

    f.extend(house_rules(body))
    return f


def check_llms_full(lines):
    body = strip_bom([l.rstrip('\n') for l in lines])
    f = house_rules(body)
    if not any(l.startswith('# ') and not l.startswith('## ') for l in body):
        f.append(('warn', 1, 'No H1 found; a full-content dump should open with the site name as an H1.'))
    nonblank = [l for l in body if l.strip()]
    links = [l for l in nonblank if l.startswith('- [') and '](' in l]
    if nonblank and len(links) >= max(5, len(nonblank) * 0.5):
        f.append(('warn', 1, 'This reads like a link index, not a full-content dump; llms-full.txt should hold the pages full text.'))
    return f


def main():
    argv = sys.argv[1:]
    as_json = '--json' in argv
    forced = None
    args = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == '--json':
            i += 1
        elif a == '--as':
            forced = argv[i + 1] if i + 1 < len(argv) else None
            i += 2
        elif a.startswith('--as='):
            forced = a.split('=', 1)[1]
            i += 1
        else:
            args.append(a)
            i += 1
    if not args:
        print('usage: validate_llms_txt.py <path> [--json] [--as <name>]')
        return 2
    path = args[0]
    base = (forced or os.path.basename(path)).lower()
    with open(path, encoding='utf-8') as fh:
        lines = fh.readlines()
    if base == 'llms.txt':
        kind, findings = 'llms.txt', check_llms_txt(lines)
    elif base == 'llms-full.txt':
        kind, findings = 'llms-full.txt (Mintlify full-dump)', check_llms_full(lines)
    elif base.startswith('llms-ctx'):
        kind, findings = 'llms-ctx (generated XML context)', house_rules([l.rstrip('\n') for l in lines])
    elif base.endswith('.md'):
        kind, findings = 'per-page markdown', house_rules([l.rstrip('\n') for l in lines])
    else:
        kind, findings = 'unknown', house_rules([l.rstrip('\n') for l in lines])

    errors = [x for x in findings if x[0] == 'error']
    warns = [x for x in findings if x[0] == 'warn']
    notes = [x for x in findings if x[0] == 'note']
    if as_json:
        print(json.dumps({'file': path, 'kind': kind,
                          'findings': [{'severity': s, 'line': ln, 'message': m} for s, ln, m in findings]}, indent=2))
    else:
        print(f'{path}  [{kind}]')
        for s, ln, m in findings:
            loc = f'line {ln}: ' if ln else ''
            print(f'  {s.upper():5} {loc}{m}')
        print(f'  {len(errors)} error(s), {len(warns)} warning(s), {len(notes)} note(s).')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
