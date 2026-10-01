"""Export the single Markdown source into complete Markdown/HTML reading copies."""
from pathlib import Path
from html import escape, unescape
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import argparse
import re
import markdown
import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'

def nav_entries(items):
    for item in items:
        for label, value in item.items():
            if isinstance(value, list):
                yield from nav_entries(value)
            else:
                yield label, (DOCS / value).resolve()

class Headings(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.ids = []
        self.feed(html)
    def handle_starttag(self, tag, attrs):
        if re.fullmatch(r'h[1-6]', tag):
            self.ids.append(dict(attrs).get('id', ''))

def export(destination):
    destination.mkdir(parents=True, exist_ok=True)
    core = (DOCS / 'CORE_SPEC.md').read_text()
    version = re.search(r'Core Spec (v[\d.]+)', core).group(1)
    date = re.search(r'日期：(\d{4}-\d{2}-\d{2})', core).group(1)
    entries = list(nav_entries(yaml.safe_load((ROOT / 'mkdocs.yml').read_text())['nav']))
    prefixes = {p: f'chapter-{i:02}' for i, (_, p) in enumerate(entries, 1)}
    def link(href, current):
        u = urlsplit(unescape(href))
        if u.scheme or u.netloc:
            return href
        target = (current.parent / unquote(u.path)).resolve() if u.path else current
        if target in prefixes:
            return '#' + prefixes[target] + ('-' + unquote(u.fragment) if u.fragment else '')
        return href

    html_sections, md_sections = [], []
    for number, (label, path) in enumerate(entries, 1):
        prefix = prefixes[path]
        text = path.read_text()
        if text.startswith('---\n'):
            text = text.split('---\n', 2)[-1]
        rendered = markdown.markdown(text, extensions=['tables', 'toc', 'fenced_code', 'attr_list', 'md_in_html'])
        heading_ids = iter(Headings(rendered).ids)
        rendered = re.sub(r'id="([^"]+)"', lambda m: f'id="{prefix}-{m[1]}"', rendered)
        rendered = re.sub(r'href="([^"]+)"', lambda m: 'href="' + escape(link(m[1], path), quote=True) + '"', rendered)
        rendered = rendered.replace('<table>', '<div class="table-wrap"><table>').replace('</table>', '</table></div>')
        html_sections.append(f'<section id="{prefix}"><div class="chapter-number">{number:02} / {len(entries)}</div>{rendered}</section>')

        md = re.sub(r'<a id="([^"]+)"></a>', lambda m: f'<a id="{prefix}-{m[1]}"></a>', text)
        md = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', lambda m: '[' + m[1] + '](' + link(m[2], path) + ')', md)
        lines = []
        in_fence = False
        for line in md.splitlines():
            if line.startswith('```'):
                in_fence = not in_fence
            if not in_fence and re.match(r'^#{1,6} ', line):
                hid = next(heading_ids)
                lines.append(f'<a id="{prefix}-{hid}"></a>\n')
                line = re.sub(r'\s*\{#[^}]+\}\s*$', '', line)
                line = '#' + line if not line.startswith('###### ') else line
            lines.append(line)
        md_sections.append(f'<a id="{prefix}"></a>\n\n' + '\n'.join(lines))

    md_toc = '\n'.join(f'{i}. [{label}](#{prefixes[p]})' for i, (label, p) in enumerate(entries, 1))
    manuscript = f'# 认知语言工程｜完整体系 {version}\n\n{date} · 正式工程基线\n\n本稿由项目正文生成，包含理论架构、工程组件、使用案例、评估、来源和维护说明。修改以项目 docs 为准。\n\n## 目录\n\n' + md_toc + '\n\n---\n\n' + '\n\n---\n\n'.join(md_sections) + '\n'
    md_path = destination / f'CLE_{version}_完整体系.md'
    md_path.write_text(manuscript)
    toc = ''.join(f'<li><a href="#{prefixes[p]}"><span>{i:02}</span>{escape(label)}</a></li>' for i, (label, p) in enumerate(entries, 1))
    template = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>认知语言工程 · 完整体系 VERSION</title>
<style>
:root {color-scheme:light dark;--bg:#faf9f6;--paper:#fff;--ink:#202c35;--muted:#5e6b76;--line:#dce3e6;--accent:#176b72;--soft:#eff5f4}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.85 system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}aside{position:fixed;inset:0 auto 0 0;width:270px;overflow:auto;border-right:1px solid var(--line);padding:28px 20px;background:var(--paper)}
aside strong{font-size:19px}aside p{font-size:13px;color:var(--muted);margin:6px 0 20px}aside ol{list-style:none;padding:0;margin:0}aside li{margin:0 0 6px}aside a{display:flex;gap:10px;color:var(--ink);font-size:13px;padding:3px 0}aside span{color:var(--muted);font-variant-numeric:tabular-nums}
main{margin-left:270px;padding:48px 44px;max-width:1350px}header{padding:24px 0 42px;border-bottom:2px solid var(--accent);margin-bottom:30px}header .eyebrow{font-size:12px;letter-spacing:.13em;color:var(--accent)}header h1{font-size:38px;line-height:1.3;margin:12px 0}header p{max-width:720px;color:var(--muted)}section{padding:42px 0;border-bottom:1px solid var(--line);scroll-margin-top:20px}.chapter-number{font-size:12px;color:var(--accent);letter-spacing:.1em;margin-bottom:12px}h1{font-size:28px;line-height:1.4}h2{font-size:21px;line-height:1.5;margin:34px 0 16px}h3{font-size:18px;margin-top:28px}p{margin:14px 0}li{margin:5px 0}strong{font-weight:650}.table-wrap{overflow-x:auto;margin:22px 0}table{border-collapse:collapse;width:100%;font-size:14px;line-height:1.65}th,td{border:1px solid var(--line);padding:10px 12px;vertical-align:top}th{background:var(--soft);text-align:left}code{background:var(--soft);padding:2px 5px;border-radius:3px;font-size:.88em}pre{background:var(--soft);padding:18px;overflow:auto}pre code{padding:0}blockquote{border-left:3px solid var(--accent);padding-left:18px;color:var(--muted)}footer{font-size:13px;color:var(--muted);padding:30px 0}a[id]{scroll-margin-top:20px}
@media(prefers-color-scheme:dark){:root{--bg:#142028;--paper:#192730;--ink:#e1e8eb;--muted:#adbdc5;--line:#344751;--accent:#76c8cb;--soft:#21363f}}
@media(max-width:900px){aside{position:static;width:auto;max-height:310px;border-right:0;border-bottom:1px solid var(--line)}aside ol{columns:2}aside a{break-inside:avoid}main{margin:0;padding:28px 20px}header h1{font-size:30px}h1{font-size:24px}table{min-width:560px}}
@media print{aside{display:none}main{margin:0;padding:0;max-width:none}body{background:white;color:black;font-size:11pt}section{break-before:page}h1,h2,h3{break-after:avoid}a{color:inherit}.table-wrap{overflow:visible}table{font-size:9pt}header{break-after:page}}
</style></head><body><aside><strong>认知语言工程</strong><p>VERSION · 完整体系 · CHAPTER_COUNT章<br>目录可点击；全文可搜索或打印。</p><ol>TOC</ol></aside><main><header><div class="eyebrow">COGNITIVE LANGUAGE ENGINEERING</div><h1>让语言主动服务于人的目的</h1><p>完整体系 VERSION · DATE<br>从架构与状态接口，到语言操作、任务协议、实际结果和反馈。正式工程基线，可继续修订。</p></header>CONTENT<footer>此阅读副本由 Markdown 正文生成。工程完成与实证效果、用户验收和公开部署分别记录。© 文献版权归原作者；本书仅保留来源信息与必要转述。</footer></main></body></html>'''
    html_path = destination / f'CLE_{version}_完整体系.html'
    html_path.write_text(template.replace('VERSION', version).replace('DATE', date).replace('CHAPTER_COUNT', str(len(entries))).replace('TOC', toc).replace('CONTENT', '\n'.join(html_sections)))
    return md_path, html_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    for path in export(args.output_dir):
        print(path)
