"""Arabic landing page and grouped header actions."""
from pathlib import Path
import re
root=Path(__file__).parent/'dist'
# Preserve the English homepage at its own address before promoting Arabic.
english=root/'en'/'index.html';english.parent.mkdir(exist_ok=True)
if '<html lang="en"' in (root/'index.html').read_text():
 s=(root/'index.html').read_text()
 s=re.sub(r'((?:src|href|data-frame-base|data-mobile-base|data-content-base)=")([^"#]+)(")',lambda m:m[0] if m[2].startswith(('http:','https:','tel:','mailto:','data:','/')) else m[1]+'../'+m[2]+m[3],s)
 s=s.replace("url('assets/", "url('../assets/")
 english.write_text(s)
for p in root.rglob('*.html'):
 s=p.read_text()
 if 'header-actions' not in s:
  s=re.sub(r'(<a class="header-call".*?</a>)(<a class="header-quote".*?</a>)',r'<div class="header-actions">\1\2</div>',s)
 ar='<html lang="ar"' in s
 if not ar:
  s=re.sub(r'(class="brand" href=")[^"]*',r'\1/en/',s)
  s=re.sub(r'<a href="(?:\./|\.\./|\.\./\./)"([^>]*>Home</a>)',r'<a href="/en/"\1',s)
 else:
  s=re.sub(r'(<a class="lang-link" href=")(?:\.\./|\.\./index(?:\.html)?)"',r'\1/en/"',s)
 p.write_text(s)
# Arabic is rendered immediately at /, with no redirect or language flash.
s=(root/'ar/index.html').read_text()
s=s.replace('../assets/','assets/').replace('../style.css','style.css').replace('../app.js','app.js').replace('../content/','content/').replace('../favicon.svg','favicon.svg')
def root_link(m):
 url=m[2]
 if url.startswith(('http:','https:','tel:','mailto:','data:','#','/','assets/','style.css','favicon.svg')):return m[0]
 if url.startswith('../'):return m[1]+url[3:]+m[3]
 return m[1]+'/ar/'+('' if url=='./' else url)+m[3]
s=re.sub(r'(href=")([^"]*)(")',root_link,s)
s=s.replace('https://black-c-construction.husam009.chatgpt.site/ar/index.html','https://black-c-construction.husam009.chatgpt.site/')
(root/'index.html').write_text(s)
