"""Verify generated local links, resources and anchors before Pages deployment."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import sys
import yaml

SITE = Path(__file__).resolve().parents[1] / 'site'
config = yaml.safe_load((SITE.parent / 'mkdocs.yml').read_text())
base_path = urlsplit(config.get('site_url', '')).path.rstrip('/')

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids, self.urls = [], []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for attr in ('href', 'src'):
            if attr in attrs:
                self.urls.append(attrs[attr])

pages = {path: Page(path) for path in SITE.rglob('*.html')}
errors, checked = [], 0
if not pages:
    errors.append('No built HTML; run mkdocs build first.')
for path, page in pages.items():
    for anchor, count in Counter(page.ids).items():
        if count > 1:
            errors.append(f'{path.relative_to(SITE)}: duplicate ID {anchor}')
    for href in page.urls:
        url = urlsplit(href)
        if url.scheme or url.netloc:
            continue
        checked += 1
        if url.path.startswith('/'):
            local_path = unquote(url.path)
            if base_path and (local_path == base_path or local_path.startswith(base_path + '/')):
                local_path = local_path[len(base_path):]
            elif base_path:
                errors.append(f'{path.relative_to(SITE)}: URL outside configured site path {href}')
                continue
            target = (SITE / local_path.lstrip('/')).resolve()
        else:
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
        if target.is_dir():
            target = target / 'index.html'
        if not target.exists():
            errors.append(f'{path.relative_to(SITE)}: missing {href}')
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f'{path.relative_to(SITE)}: missing anchor {href}')
print(json.dumps({'html_pages': len(pages), 'local_urls_checked': checked, 'errors': errors}, ensure_ascii=False, indent=2))
sys.exit(bool(errors))
