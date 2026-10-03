"""Add Black C's cinematic homepage composition to both language variants."""
from pathlib import Path

root=Path(__file__).parent/'dist'
config={
 'index.html':{
  'asset':'assets/',
  'brand':'BLACK CONSTRUCTION / RIYADH',
  'profile_action':'Explore our company profile',
  'projects_action':'View our projects',
  'stages':[
   ('Riyadh is always building.','A new beginning','A city moving forward. Every remarkable space starts with a vision.'),
   ('From vision to structure.','The city takes shape','Progress rises through planning, coordination and care at every stage.'),
   ('Built for what comes next.','A new skyline','The ambition behind each build shapes the city around us.'),
   ('Beyond the skyline.','The next horizon','Black C builds with the precision and commitment that tomorrow demands.')],
  'visual_note':'CONCEPTUAL RIYADH CONSTRUCTION VISUAL',
  'hero_cue':'SCROLL TO EXPLORE',
  'mode':'A STORY OF PRECISION',
  'intro_label':'WHO WE ARE',
  'intro_image_alt':'Architectural study from Black Construction company profile',
  'services_label':'WHAT WE DO',
  'services_title':'One team.<br><em>Every stage of the build.</em>',
  'services_link':'Explore our expertise',
  'services':[
   ('Construction','Civil and structural works, from foundation to handover.','nbc-photo.jpg'),
   ('Fit-out & finishing','Carefully coordinated interiors and architectural details.','dforma-photo.jpg'),
   ('MEP & systems','Electrical, mechanical and building systems working together.','neutral-photo.jpg'),
   ('Project delivery','Planning, site control and quality across every phase.','hashem-photo.jpg')],
  'promise_label':'THE BLACK-C STANDARD',
  'promise_title':'Quality is visible.<br><em>Commitment is felt.</em>',
  'promise_desc':'Disciplined planning, clear accountability and attention to detail guide the work from first discussion to final handover.',
  'promises':[('01','Built on trust','Open communication and respect for every project partner.'),('02','Managed with clarity','Scope, quality, cost and time stay in view at every stage.'),('03','Delivered with care','Materials, workmanship and safety are checked throughout.')],
  'promise_link':'Get to know Black C'
 },
 'ar/index.html':{
  'asset':'../assets/',
  'brand':'بلاك للإنشاءات / الرياض',
  'profile_action':'استكشف ملف الشركة',
  'projects_action':'شاهد مشاريعنا',
  'stages':[
   ('الرياض لا تتوقف عن البناء.','بداية جديدة','مدينة تتقدم باستمرار. وكل مساحة استثنائية تبدأ برؤية.'),
   ('من الرؤية إلى الهيكل.','تتشكّل المدينة','يرتفع الإنجاز بالتخطيط والتنسيق والعناية في كل مرحلة.'),
   ('نبني لما هو قادم.','أفق عمراني جديد','الطموح الذي يقود كل مشروع يرسم ملامح المدينة من حولنا.'),
   ('إلى أفقٍ أبعد.','الأفق القادم','نبني بالدقة والالتزام اللذين يستحقهما المستقبل.')],
  'visual_note':'تصور بصري لمشهد البناء في الرياض',
  'hero_cue':'مرّر لاكتشاف قصتنا',
  'mode':'رحلة من الدقة والإتقان',
  'intro_label':'من نحن',
  'intro_image_alt':'تفاصيل معمارية من ملف بلاك للإنشاءات',
  'services_label':'ماذا نقدم',
  'services_title':'فريق واحد.<br><em>في كل مرحلة من المشروع.</em>',
  'services_link':'استكشف خبراتنا',
  'services':[
   ('الإنشاءات','أعمال مدنية وإنشائية، من الأساسات حتى التسليم.','nbc-photo.jpg'),
   ('التشطيبات','مساحات داخلية وتفاصيل معمارية بتنسيق دقيق.','dforma-photo.jpg'),
   ('الأنظمة الكهروميكانيكية','حلول الكهرباء والميكانيكا وخدمات المباني المتكاملة.','neutral-photo.jpg'),
   ('تسليم المشاريع','تخطيط ورقابة ميدانية وجودة في جميع المراحل.','hashem-photo.jpg')],
  'promise_label':'معيار بلاك',
  'promise_title':'جودة تراها.<br><em>والتزام تلمسه.</em>',
  'promise_desc':'التخطيط المنضبط والمسؤولية الواضحة والعناية بالتفاصيل تقود العمل من أول نقاش إلى التسليم النهائي.',
  'promises':[('01','ثقة متبادلة','تواصل واضح واحترام لجميع شركاء المشروع.'),('02','إدارة بوضوح','نراقب النطاق والجودة والتكلفة والوقت في كل مرحلة.'),('03','تنفيذ بعناية','نتابع المواد والأعمال والسلامة طوال المشروع.')],
  'promise_link':'تعرّف على بلاك'
 }
}
for file,c in config.items():
 p=root/file;s=p.read_text();asset=c['asset']
 s=s.replace('<body>','<body class="home">',1)
 start=s.index('<section class="hero hero-film"');end=s.index('</section>',start)+len('</section>')
 hero=s[start:end].replace('hero hero-film', 'hero hero-film has-video', 1)
 slides=f'<div class="hero-slides" aria-hidden="true" style="background-image:url(\'{asset}riyadh-build-start.jpg\')"><canvas class="riyadh-frames" width="960" height="540" data-frame-base="{asset}riyadh-frames/frame-"></canvas></div>'
 a=hero.index('<div class="hero-slides"');b=hero.index('<div class="hero-film-shade">',a)
 hero=hero[:a]+slides+hero[b:]
 def format_title(title):
  first,last=title.rsplit(' ',1)
  return f'<span class="hero-title-first">{first}</span><span class="hero-title-accent">{last}</span>'
 def format_description(desc):
  return ''.join(f'<span>{sentence.strip()}</span>' for sentence in desc.replace('. ','.|').split('|'))
 panels=''.join(f'<div class="hero-copy-panel'+(' is-active' if i==0 else '')+f'" data-stage="{i}" aria-hidden="'+('false' if i==0 else 'true')+f'"><h1>{format_title(title)}</h1><p>{format_description(desc)}</p></div>' for i,(title,_,desc) in enumerate(c['stages']))

 content=f'<div class="hero-film-content"><div class="hero-copy-stack">{panels}</div></div>'
 a=hero.index('<div class="hero-film-content">')
 hero=hero[:a]+content+f'<div class="hero-scroll-cue"><span></span>{c["hero_cue"]}</div></section>'
 s=s[:start]+'<div class="hero-sequence">'+hero+'</div>'+s[end:]
 # Adapt the reference's chapter sequence using Black C's own content.
 import re
 ar=file.startswith('ar/')
 def tr(en,arabic):return arabic if ar else en
 start=s.index('<section class="section" id="introduction">');end=s.index('</section>',start)+len('</section>')
 intro=s[start:end].replace('class="section"','class="section narrative-intro"',1)
 intro=intro.replace('<div class="split-heading">','<div class="split-heading">',1)
 intro=re.sub(r'<span class="eyebrow">.*?</span>',f'<span class="eyebrow">{c["intro_label"]}</span>',intro,count=1)
 services=''.join(f'<a class="service-tile" href="expertise.html"><span class="service-no">{i:02}</span><h3>{name}</h3><p>{desc}</p><span class="service-link">{tr("Explore service","استكشف الخدمة")}</span></a>' for i,(name,desc,_) in enumerate(c['services'],1))
 block=f'<section class="section narrative-services" id="services"><div class="chapter-heading"><span class="eyebrow">{c["services_label"]}</span><h2>{c["services_title"]}</h2></div><div class="service-tiles">{services}</div></section>'
 signature=f'<section class="section narrative-signature" style="--signature-photo:url(\'{asset}dforma-photo.jpg\')"><div class="chapter-heading"><span class="eyebrow">{tr("SIGNATURE LINES","خطوط أعمالنا")}</span><h2>{tr("Your ambition.<br><em>A tailored approach.</em>","طموحك.<br><em>ومنهج يناسبه.</em>")}</h2></div><div class="signature-links"><a href="collections.html#nova"><strong>NOVA</strong><span>{tr("Fast-track delivery","التنفيذ السريع")}</span></a><a href="collections.html#aura"><strong>AURA</strong><span>{tr("Premium fit-out","التشطيبات الراقية")}</span></a><a href="collections.html#velare"><strong>VELARE</strong><span>{tr("Bespoke luxury","الفخامة الخاصة")}</span></a></div></section>'
 reasons=''.join(f'<article><span class="reason-number">{num}</span><h3>{title}</h3><p>{desc}</p></article>' for num,title,desc in c['promises'])
 promise=f'<section class="section narrative-why"><div class="chapter-heading"><span class="eyebrow">{tr("WHY BLACK C","لماذا بلاك")}</span><h2>{c["promise_title"]}</h2><p>{c["promise_desc"]}</p></div><div class="reason-grid">{reasons}</div></section>'
 projects=re.findall(r'<article class="project-card".*?</article>',s,re.S)
 assert len(projects)==8
 work=f'<section class="section narrative-work" id="featured-work"><div class="section-title"><div><span class="eyebrow">{tr("OUR WORK","أعمالنا")}</span><h2>{tr("Selected projects.<br><em>Visible quality.</em>","مشاريع مختارة.<br><em>جودة تراها.</em>")}</h2></div><a class="underlined" href="projects.html">{tr("Explore all projects","استكشف جميع المشاريع")}</a></div><div class="featured-grid">'+''.join(projects[:4])+'</div></section>'
 sectors=f'<section class="section narrative-sectors"><div class="chapter-heading"><span class="eyebrow">{tr("WHERE WE BUILD","حيث نبني")}</span><h2>{tr("Spaces for life.<br><em>Places for business.</em>","مساحات للحياة.<br><em>وأماكن للأعمال.</em>")}</h2></div><div class="sector-names"><span>{tr("Residential","سكني")}</span><span>{tr("Commercial","تجاري")}</span><span>{tr("Interiors & fit-out","التصميم الداخلي والتشطيبات")}</span><span>{tr("Specialized works","الأعمال المتخصصة")}</span></div></section>'
 s=s[:start]+intro+block+signature+promise+work+sectors+s[s.index('</main>',end):]
 s=s.replace('class="home"','class="home reference-layout"',1)
 p.write_text(s)
print('Restructured both homepages around Black C chapters.')
import runpy
runpy.run_path(str(Path(__file__).parent/'refine-site.py'))
runpy.run_path(str(Path(__file__).parent/'conversion-site.py'))
