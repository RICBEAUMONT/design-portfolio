#!/usr/bin/env python3
"""Validate local pages, assets, fragment links, and Webflow gallery data."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGES = sorted([*ROOT.glob('*.html'), *ROOT.glob('portfolio/*.html')])

class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.tags = []
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

errors = []
references = 0
for path in PAGES:
    source = path.read_text()
    page = Page(source)
    def error(message):
        errors.append(f'{path.relative_to(ROOT)}: {message}')
    ids = [a['id'] for _, a in page.tags if 'id' in a]
    for identifier, count in Counter(ids).items():
        if count > 1:
            error(f'duplicate id {identifier}')
    if not any(t == 'html' and a.get('lang') == 'en' for t, a in page.tags):
        error('missing document language')
    for tag in ('main', 'h1', 'title'):
        if sum(t == tag for t, _ in page.tags) != 1:
            error(f'expected one {tag}')
    urls = []
    for tag, attrs in page.tags:
        if tag == 'img' and 'alt' not in attrs:
            error('image missing alt attribute')
        for attr in ('href', 'src'):
            if attr in attrs:
                urls.append(attrs[attr])
        urls.extend(item.strip().split()[0] for item in attrs.get('srcset', '').split(',') if item.strip())
    for block in re.findall(r'<script type="application/json" class="w-json">(.*?)</script>', source, re.S):
        try:
            urls.extend(item['url'] for item in json.loads(block).get('items', []))
        except (ValueError, KeyError) as exc:
            error(f'invalid lightbox JSON: {exc}')
    for url in urls:
        parts = urlsplit(url)
        if parts.scheme or parts.netloc:
            continue
        if not url:
            error('empty resource URL')
            continue
        target = (path.parent / unquote(parts.path)).resolve() if parts.path else path
        references += 1
        if not target.is_file():
            error(f'missing local resource {url}')
        elif parts.fragment and target.suffix == '.html':
            target_ids = {a.get('id') for _, a in Page(target.read_text()).tags}
            if unquote(parts.fragment) not in target_ids:
                error(f'missing fragment {url}')
for css in (ROOT / 'css').glob('*.css'):
    for url in re.findall(r'url\([\'"]?([^\)\'\"]+)', css.read_text()):
        if urlsplit(url).scheme or url.startswith('#'):
            continue
        references += 1
        if not (css.parent / unquote(urlsplit(url).path)).is_file():
            errors.append(f'{css.relative_to(ROOT)}: missing CSS resource {url}')
print(f'Checked {len(PAGES)} pages and {references} local references.')
for item in errors:
    print(item)
print(f'{len(errors)} errors.')
sys.exit(bool(errors))
