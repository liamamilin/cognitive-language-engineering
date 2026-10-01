"""Check source links, anchors, stable IDs and model component references.

Checks consistency of the delivered specification, not empirical CLE efficacy.
"""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
from urllib.parse import urlsplit, unquote
import json
import re
import sys
import markdown
import yaml
from update_registry import parse_registry

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
errors = []

class Parsed(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids, self.links = [], []
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])

pages = sorted(DOCS.rglob('*.md'))
parsed = {}
for p in pages + [ROOT / 'README.md']:
    source = p.read_text()
    if source.startswith('---\n'):
        source = source.split('---\n', 2)[-1]
    parsed[p] = Parsed(markdown.markdown(source, extensions=['tables', 'toc', 'fenced_code', 'attr_list', 'md_in_html']))
    for ident, count in Counter(parsed[p].ids).items():
        if count > 1:
            errors.append(f'{p.relative_to(ROOT)}: duplicate anchor {ident}')

link_count = 0
for p, doc in parsed.items():
    for href in doc.links:
        url = urlsplit(href)
        if url.scheme or url.netloc:
            continue
        link_count += 1
        target = (p.parent / unquote(url.path)).resolve() if url.path else p
        if not target.exists():
            errors.append(f'{p.relative_to(ROOT)}: missing {href}')
        elif url.fragment and target in parsed and unquote(url.fragment) not in parsed[target].ids:
            errors.append(f'{p.relative_to(ROOT)}: missing anchor {href}')

nav = yaml.safe_load((ROOT / 'mkdocs.yml').read_text())['nav']
def entries(items):
    for item in items:
        for value in item.values():
            if isinstance(value, list):
                yield from entries(value)
            else:
                yield value
nav_pages = list(entries(nav))
for page in nav_pages:
    if not (DOCS / page).exists():
        errors.append(f'Navigation: missing {page}')
for p in pages:
    if p.relative_to(DOCS).as_posix() not in nav_pages:
        errors.append(f'Navigation: unlisted {p.relative_to(DOCS)}')

snapshot = json.loads((ROOT / 'scripts/registry_snapshot.json').read_text())
if snapshot != parse_registry():
    errors.append('Registry: derived fields differ from model source; run update_registry.py')
ids = {r['id'] for r in snapshot}
if len(ids) != len(snapshot):
    errors.append('Registry snapshot: duplicate ID')
model_counts = Counter()
for model in ['M1', 'M2', 'M3', 'M4']:
    text = (DOCS / f'models/{model}.md').read_text()
    headings = dict(re.findall(r'^## ([RCIA]-[PC]\d+)\. (.+)$', text, re.M))
    registered = {r['id']: r for r in snapshot if r['model'] == model}
    if set(headings) != set(registered):
        errors.append(f'{model}: snapshot/source ID mismatch')
    for ident, name in headings.items():
        if ident in registered and registered[ident]['name'] != name:
            errors.append(f'{ident}: snapshot/source name mismatch')
    model_counts[model] = len(headings)

extra_ids = set()
for name, pattern in [('BRIDGES.md', r'B-C\d+'), ('OUTCOMES.md', r'O-C\d+'), ('MECHANISMS.md', r'ME\d+')]:
    extra_ids.update(re.findall(r'^## (' + pattern + r')\.', (DOCS / name).read_text(), re.M))
for r in snapshot:
    for target in r['components'] + r.get('cross_domain', []) + r['mechanisms'] + ([r['specializes']] if r['specializes'] else []):
        if target not in ids | extra_ids:
            errors.append(f"{r['id']}: undefined component {target}")

# Composite reuse must be expandable inside the model registry.
# Bridge cross-references are descriptive mappings, not mandatory execution dependencies.
graph = {r['id']: [x for x in r['components'] if x in ids] for r in snapshot}
def visit(node, active, complete):
    if node in active:
        errors.append('Model component cycle: ' + ' -> '.join(active + [node]))
        return
    if node in complete:
        return
    for child in graph[node]:
        visit(child, active + [node], complete)
    complete.add(node)
complete = set()
for ident in graph:
    visit(ident, [], complete)

op_text = (DOCS / 'engineering/OPERATORS.md').read_text()
op_cards = re.split(r'^## (OP\d+)\. ', op_text, flags=re.M)[1:]
operators = set(op_cards[::2])
op_fields = ['任务／应用情境', '前提', '目标变化', '机制候选', '语言模式', '变体与使用条件', '操作与输出', '完成检查', '主要失效', '取舍与扭曲', '易混对象', '证据／评价']
for ident, body in zip(op_cards[::2], op_cards[1::2]):
    for field in op_fields:
        if f'**{field}' not in body:
            errors.append(f'{ident}: missing {field}')
protocol_text = (DOCS / 'engineering/PROTOCOLS.md').read_text()
protocol_cards = re.split(r'^## (PR\d+)\. ', protocol_text, flags=re.M)[1:]
protocols = set(protocol_cards[::2])
protocol_fields = ['入口与目标', '使用组件', '步骤', '分支／回退', '目标达成检查', '未达成出口', '停止条件', '最小产出', '主要失效', '评价']
for ident, body in zip(protocol_cards[::2], protocol_cards[1::2]):
    for label in protocol_fields:
        if f'**{label}：**' not in body:
            errors.append(f'{ident}: missing {label}')
for ident in set(re.findall(r'\bOP\d+\b', protocol_text)):
    if ident not in operators:
        errors.append(f'Protocols: undefined {ident}')

# All identifiers used in normative prose must resolve to a registered card/pattern.
known = ids | extra_ids | operators
patterns = set(re.findall(r'\*\*语言模式 (LP\d+)', op_text))
patterns.update(re.findall(r'^## (LP\d+)\.', (DOCS / 'engineering/PATTERNS.md').read_text(), re.M))
sources = set(x.upper() for x in re.findall(r'<a id="(src\d+)"', (DOCS / 'sources/VERIFIED_SOURCES.md').read_text()))
known.update(protocols | patterns | sources)
for p in pages:
    for ident in set(re.findall(r'\b(?:[RCIABO]-[PC]\d+|ME\d+|OP\d+|PR\d+|LP\d+|SRC\d+)\b', p.read_text())):
        if ident not in known:
            errors.append(f'{p.relative_to(DOCS)}: undefined identifier {ident}')

summary = {'pages': len(pages), 'local_links': link_count, 'models': dict(model_counts), 'registry_interfaces': len(ids), 'snapshot_matches_source': snapshot == parse_registry(), 'operators': len(operators), 'protocols': len(protocols), 'patterns': len(patterns), 'mechanisms': len([x for x in extra_ids if x.startswith('ME')]), 'bridges': len([x for x in extra_ids if x.startswith('B-')]), 'outcomes': len([x for x in extra_ids if x.startswith('O-')]), 'sources': len(sources), 'errors': errors}
print(json.dumps(summary, ensure_ascii=False, indent=2))
sys.exit(bool(errors))
