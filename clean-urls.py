"""Keep public navigation extensionless while retaining static HTML files."""
from pathlib import Path
import re
root=Path(__file__).parent/'dist'
for p in root.rglob('*.html'):
 s=p.read_text()
 def clean(m):
  before,url,after=m.groups()
  if url.startswith(('http:','https:','//','mailto:','tel:','#')):return m[0]
  url=re.sub(r'index\.html(?=[?#]|$)','',url)
  url=re.sub(r'\.html(?=[?#]|$)','',url)
  if not url or url.startswith(('#','?')):url='./'+url
  return before+url+after
 s=re.sub(r'((?:href|action)=")([^"]*)(")',clean,s)
 p.write_text(s)
p=root/'app.js';s=p.read_text().replace("item=items.find(x=>x.url===a?.getAttribute('href'))", "item=items.find(x=>x.url.replace(/\\.html$/, '')===a?.getAttribute('href')?.replace(/\\.html$/, ''))");p.write_text(s)
