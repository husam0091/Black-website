"""Apply the bilingual conversion and accessibility brief to the static output."""
from pathlib import Path
import re,json
root=Path(__file__).parent/'dist'
content=root/'content';content.mkdir(exist_ok=True)
wa='https://wa.me/966593300978?text=Hello%20Black%20C%2C%20I%20would%20like%20to%20discuss%20my%20project.'
project_data=[]
for p in sorted(root.glob('project-*.html')):
 s=p.read_text();ar=(root/'ar'/p.name).read_text()
 def text(x):return re.sub('<[^>]+>','',x)
 def field(label):
  m=re.search(r'<dt>'+label+r'</dt><dd>(.*?)</dd>',s);return text(m[1]) if m else ''
 project_data.append(dict(id=p.stem[8:],title={'en':text(re.search('<h1>(.*?)</h1>',s)[1]),'ar':text(re.search('<h1>(.*?)</h1>',ar)[1])},url=p.name,city=text(re.search(r'</h1><p>(.*?)</p>',s)[1]),category=re.search(r'<span class="eyebrow">[^<]* / ([^<]+)</span>',s)[1],area=field('Area'),duration=field('Project duration'),cover=f'assets/{p.stem[8:]}-photo.jpg',gallery=[f'assets/{p.stem[8:]}-photo.jpg'],description={'en':'; '.join(re.findall(r'<li>(.*?)</li>',re.search(r'<ul>(.*?)</ul>',s)[1])),'ar':'؛ '.join(re.findall(r'<li>(.*?)</li>',re.search(r'<ul>(.*?)</ul>',ar)[1]))}))
(content/'projects.json').write_text(json.dumps(project_data,ensure_ascii=False,indent=2))
stats=[{'value':'2018','label':{'en':'Our journey began','ar':'بداية رحلتنا'}},{'value':'07','label':{'en':'Core capabilities','ar':'قدرات أساسية'}},{'value':'03','label':{'en':'Signature lines','ar':'خطوط أعمال'}},{'value':'KSA','label':{'en':'Built around you','ar':'نبني وفق طموحك'}}]
(content/'stats.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2))
services=[]
for en,ar in zip(re.findall(r'<a class="service-tile".*?</a>',(root/'index.html').read_text()),re.findall(r'<a class="service-tile".*?</a>',(root/'ar/index.html').read_text())):
 services.append({'title':{'en':re.search('<h3>(.*?)</h3>',en)[1],'ar':re.search('<h3>(.*?)</h3>',ar)[1]},'description':{'en':re.search('<p>(.*?)</p>',en)[1],'ar':re.search('<p>(.*?)</p>',ar)[1]},'url':'expertise.html'})
(content/'services.json').write_text(json.dumps(services,ensure_ascii=False,indent=2))
for p in root.rglob('*.html'):
 s=p.read_text();ar=p.parent.name=='ar';prefix='../' if ar else ''
 def tr(en,a):return a if ar else en
 cta=tr('Discuss your project','ناقش مشروعك');promise=tr('We aim to reply within two business hours.','نسعى للرد خلال ساعتين عمل.')
 button=f'<a class="button quote-link" href="contact.html#quote">{cta}</a>'
 s=s.replace('</nav>',f'<div class="mobile-contact">{button}<a href="tel:+966593300978" dir="ltr">+966 59 330 0978</a><a href="{wa}">WhatsApp</a></div></nav>',1)
 s=s.replace('</header>',f'<a class="header-quote" href="contact.html#quote">{cta}</a></header>',1)
 s=s.replace('>Menu</button>','>Menu +</button>').replace('>القائمة</button>','>القائمة +</button>')
 s=s.replace('<body','<body data-content-base="'+prefix+'content/"',1)
 s=s.replace('</body>',f'<a class="floating-whatsapp" href="{wa}" aria-label="{tr("Message Black C on WhatsApp","راسل بلاك على واتساب")}">WhatsApp</a></body>')
 s=s.replace('<span>EXPLORE</span>','<span>EXPLORE</span>').replace('<span>CONTACT</span>','<span>CONTACT</span>')
 footer=s.index('<footer>');s=s[:footer]+s[footer:].replace('</div><div><span>'+tr('BASED IN','مقرنا')+'</span>',f'<a href="{wa}">WhatsApp</a></div><div><span>'+tr('BASED IN','مقرنا')+'</span>',1)
 s=s.replace('<section class="cta">','<section class="cta conversion-cta">',1)
 ca=s.index('<section class="cta');ce=s.index('</section>',ca)
 band=s[ca:ce].replace('href="contact.html"','href="contact.html#quote"')+f'<p class="response-note">{promise}</p><a class="underlined" href="{wa}">{tr("Chat on WhatsApp","تواصل عبر واتساب")}</a>'
 s=s[:ca]+band+s[ce:]
 if p.name=='index.html':
  s=s.replace('data-frame-base="'+prefix+'assets/riyadh-frames/frame-"','data-frame-base="'+prefix+'assets/riyadh-frames/frame-" data-mobile-base="'+prefix+'assets/riyadh-frames/m/frame-"')
  # One H1 for the page; later story chapters are H2s.
  first=True
  def title(m):
   nonlocal_placeholder=None
   return m.group(0)
  matches=list(re.finditer(r'<h1>.*?</h1>',s))
  for m in reversed(matches[1:]):s=s[:m.start()]+m[0].replace('<h1>','<h2 class="hero-stage-title">').replace('</h1>','</h2>')+s[m.end():]
  s=re.sub(r'(<div class="hero-copy-panel" data-stage="3"[^>]*>)(.*?)(</div>)',lambda m:m[1]+f'<img class="skyline-logo" src="{prefix}assets/logo-transparent.png" alt="Black Construction" width="700" height="214"><div class="skyline-copy">'+m[2]+'</div>'+m[3],s,count=1)
  s=s.replace('<div class="hero-scroll-cue">',f'<div class="hero-conversion">{button}</div><div class="hero-stats" data-stats>'+''.join(f'<div><strong>{x["value"]}</strong><span>{x["label"]["ar" if ar else "en"]}</span></div>' for x in stats)+'</div><div class="hero-scroll-cue">',1)
  for cls in ('service-tile','reason-grid'):
   pass
  n=[0]
  def numbered(m):
   n[0]+=1;return m[0]+f'<span class="tile-number">{n[0]:02}</span>'
  s=re.sub(r'<a class="service-tile"[^>]*>',numbered,s)
  s=s.replace('<div class="reason-grid">','<div class="reason-grid">',1)
  trust=f'<section class="section trusted-clients"><span class="eyebrow">{tr("SELECTED CLIENTS","من عملائنا")}</span><h2>{tr("Relationships built on <em>trust.</em>","علاقات أساسها <em>الثقة.</em>")}</h2><div class="client-names"><a href="project-nbc.html">NBC</a><a href="project-dforma.html">D-FORMAx</a><a href="project-hashem.html">{tr("Hashem Al Safi","هاشم الصافي")}</a></div></section>'
  s=s.replace('<section class="section narrative-sectors">',trust+'<section class="section narrative-sectors">',1)
  s=s.replace('<div class="facts">','<div class="facts" data-stats>',1)
 if p.name=='projects.html':
  fitlabel=tr('Fit-out','تشطيبات')
  s=s.replace('</div><p id="project-count"',f'<button data-filter="Fit-out" aria-pressed="false">{fitlabel} <span>2</span></button></div><p id="project-count"',1)
  s=re.sub(r'(<article class="project-card"[^>]*)(><a href="project-(?:dforma|resthouse)\.html")',r'\1 data-fitout="true"\2',s)
 if p.name=='contact.html':
  labels=[('name',tr('Name','الاسم'),'text',True),('phone',tr('Phone','رقم الهاتف'),'tel',True),('location',tr('Project location','موقع المشروع'),'text',True),('budget',tr('Budget range (optional)','نطاق الميزانية (اختياري)'),'text',False),('timeline',tr('Timeline (optional)','المدة المتوقعة (اختياري)'),'text',False)]
  fields=''.join(f'<label>{label}<input name="{name}" type="{kind}" '+('required ' if required else '')+('autocomplete="name" ' if name=='name' else 'autocomplete="tel" ' if name=='phone' else '')+'/></label>' for name,label,kind,required in labels)
  options=[tr('Residential','سكني'),tr('Commercial','تجاري'),tr('Industrial','صناعي'),tr('Fit-out','تشطيبات'),tr('Other','أخرى')]
  form=f'<section class="section quote-section" id="quote"><span class="eyebrow">{tr("LET’S TALK","لنتحدث")}</span><h2>{tr("Tell us about your <em>project.</em>","حدثنا عن <em>مشروعك.</em>")}</h2><form id="quote-form"><div class="quote-fields">{fields}<label>{tr("Project type","نوع المشروع")}<select name="project_type" required><option value="">{tr("Choose a type","اختر نوع المشروع")}</option>'+''.join(f'<option>{x}</option>' for x in options)+f'</select></label><label class="wide">{tr("Message","الرسالة")}<textarea name="message" rows="4" required></textarea></label></div><p>{tr("Your details will be prepared as a WhatsApp message. Review it there and send it to our team.","سنجهز بياناتك في رسالة واتساب لتراجعها وترسلها إلى فريقنا.")}</p><button class="button" type="submit">{tr("Continue to WhatsApp","المتابعة إلى واتساب")}</button><p class="response-note">{promise}</p><p id="quote-status" role="status"></p></form></section>'
  s=s.replace('</main>',form+'</main>')
 # Make the entire project card a single accessible link.
 def whole_card(m):
  card=m[0].replace('</a><p class="project-meta">','<p class="project-meta">')
  return card.replace('</article>','</a></article>')
 s=re.sub(r'<article class="project-card".*?</article>',whole_card,s,flags=re.S)
 s=s.replace('</head>',f'<link rel="alternate" hreflang="{ "ar" if ar else "en" }" href="{p.name}"></head>')
 # Unique route description and paired locale tags.
 title=re.search('<title>(.*?)</title>',s)[1]
 desc=tr(f'{title}. Explore Black Construction’s construction, fit-out and project delivery expertise in Saudi Arabia.',f'{title}. اكتشف خبرات بلاك في البناء والتشطيبات وتسليم المشاريع في المملكة العربية السعودية.')
 s=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{desc}">',s)
 schema={'@context':'https://schema.org','@type':'GeneralContractor','name':'Black Construction','telephone':'+966593300978','email':'info@black-c.com.sa','address':{'@type':'PostalAddress','addressLocality':'Riyadh','addressCountry':'SA'}}
 s=s.replace('</head>',f'<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:image" content="https://black-c-construction.husam009.chatgpt.site/assets/nbc-photo.jpg"><script type="application/ld+json">{json.dumps(schema)}</script></head>')
 p.write_text(s)
print('Applied bilingual conversion brief and exported CMS-ready content.')
