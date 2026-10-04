"""Check learning connections and preserved baseline definitions; not efficacy."""
from pathlib import Path
from collections import Counter
import re,json,hashlib,sys
from update_registry import parse_model_cards

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'docs'
errors=[]
ops_text=(D/'engineering/OPERATORS.md').read_text()
ops={op:body for op,body in re.findall(r'^## (OP\d+)\. (.*?)(?=^## OP|\Z)',ops_text,re.M|re.S)}
patterns={op:re.search(r'\*\*语言模式 (LP\d+)',body)[1] for op,body in ops.items()}
assert len(set(patterns.values()))==len(patterns), 'duplicate principal language pattern'
cards={}
registry=json.loads((ROOT/'scripts/registry_snapshot.json').read_text())
records={r['id']:r for r in registry}
targets={op:set(re.findall(r'\[([RCIABO]-[PC]\d+)\]',re.search(r'\*\*目标变化：\*\* (.+)',body)[1])) for op,body in ops.items()}
def component_closure(ident):
    out={ident}
    rec=records[ident]
    for child in rec['components']+([rec['specializes']] if rec['specializes'] else []):
        if child in records:
            out|=component_closure(child)
    return out
for model in ['M1','M2','M3','M4']:
 text=(D/f'models/{model}.md').read_text()
 baseline=(ROOT/f'archive/full-v0.5-frozen/docs/models/{model}.md').read_text()
 def parse(source):
  return {card['id']:card['body'] for card in parse_model_cards(source)}
 current,old=parse(text),parse(baseline)
 if set(current)!=set(old):errors.append(f'{model}: original interface set changed')
 for ident,body in current.items():
  cards[ident]=body
  for field in ['操作入口','怎样做','语言模式','状态变化','完成检查']:
   if '**'+field+'：**' not in body:errors.append(f'{ident}: missing {field}')
  for field in ['状态变化','完成检查','边界与失效','可复用组成','跨域过程引用','类型','机制候选']:
   def value(content):
    m=re.search(r'\*\*'+re.escape(field)+r'：\*\* ([^\n]+)',content)
    return m[1] if m else None
   if value(body)!=value(old[ident]):errors.append(f'{ident}: baseline definition changed: {field}')
  route=re.search(r'\*\*操作入口：\*\* ([^\n]+)',body)[1]
  used=re.findall(r'\[(OP\d+)\]',route)
  if not used:errors.append(f'{ident}: no operator entry')
  elif not any(targets.get(op,set())&component_closure(ident) for op in used):
   errors.append(f'{ident}: no route reaches this target or its reusable components')
  language=re.search(r'\*\*语言模式：\*\* ([^\n]+)',body)[1]
  for op in used:
   if op not in ops:errors.append(f'{ident}: undefined operator {op}')
   elif '['+patterns[op]+']' not in language:errors.append(f'{ident}: missing pattern for {op}')
  example=re.search(r'\*\*语言模式示例：\*\* “([^\n]+)”',body)
  if not example:errors.append(f'{ident}: missing language pattern example')
  elif not re.search(r'〔[^〕]+〕',example[1]):errors.append(f'{ident}: missing pattern slots')

index=(D/'learning/INTERFACE_PATHS.md').read_text()
rows=re.findall(r'^\| \[([RCIA]-[PC]\d+)\]',index,re.M)
if set(rows)!=set(cards) or len(rows)!=len(cards):errors.append('index does not cover each interface exactly once')
for ident,body in cards.items():
 row=re.search(r'^\| \['+ident+r'\].+$',index,re.M)
 route=re.search(r'\*\*操作入口：\*\* ([^\n]+)',body)[1]
 lang=re.search(r'\*\*语言模式：\*\* ([^\n]+)',body)[1]
 if row:
  for pattern,source in [(r'\[(OP\d+)\]',route),(r'\[(LP\d+)\]',lang)]:
   if re.findall(pattern,source)!=re.findall(pattern,row[0]):errors.append(f'{ident}: index/card mismatch')

manifest=json.loads((ROOT/'archive/full-v0.5-frozen/manifest.json').read_text())
for relative,digest in manifest.items():
 p=ROOT/'archive/full-v0.5-frozen'/relative
 if hashlib.sha256(p.read_bytes()).hexdigest()!=digest:errors.append(f'frozen baseline changed: {relative}')
frozen=ROOT/'archive/structural-core-v0.2-frozen'
for name in ['index.md','SELECTION.md']:
 if (D/'essentials'/name).read_bytes()!=(frozen/name).read_bytes():errors.append(f'frozen core changed: {name}')

print(json.dumps({'interfaces':len(cards),'operators':len(ops),'principal_patterns':len(patterns),'all_interfaces_have_methods_pattern_examples_checks':not errors,'baseline_definitions_and_archives_preserved':not errors,'errors':errors},ensure_ascii=False,indent=2))
sys.exit(bool(errors))
