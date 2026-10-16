"""Apply the editorial homepage and shared navigation refinements."""
from pathlib import Path
import re
root=Path(__file__).parent/'dist'
for p in root.rglob('*.html'):
 s=p.read_text();ar='ar' in p.relative_to(root).parts;asset='../assets/' if ar else 'assets/'
 label='تواصل معنا' if ar else 'Contact us'
 s=re.sub(r'<a class="header-call"[^>]*>.*?</a>',f'<a class="header-call" href="contact.html">{label}</a>',s,count=1)
 s=re.sub(r'(<span class="photo-link">).*?(</span>)',lambda m:m[1]+('اكتشف المشروع' if ar else 'View project')+'<i class="project-frame" aria-hidden="true"></i>'+m[2],s)
 s=re.sub(r'(<div class="project-heading"><h3>.*?</h3>)<span>↗</span>',r'\1',s)
 if p.name=='index.html':
  s=re.sub(r'(<section[^>]*id="introduction".*?)(<div class="facts"[^>]*>.*?)(</section>)',lambda m:m[1]+m[3],s,count=1,flags=re.S)
  if 'service-editorial' not in s:
   s=s.replace('class="service-tiles"','class="service-tiles service-editorial"',1)
   photos=iter(['nbc-photo.jpg','dforma-photo.jpg','neutral-photo.jpg','hashem-photo.jpg'])
   def service(m):
    body=re.sub(r'<span class="tile-number">.*?</span>','',m[2])
    body=body.replace('<span class="service-link">','<span class="service-link">')
    return m[1]+f'<img class="service-image" src="{asset}{next(photos)}" alt="" loading="lazy"><div class="service-body">'+body+'</div></a>'
   s=re.sub(r'(<a class="service-tile"[^>]*>)(.*?)</a>',service,s,flags=re.S)
  if 'signature-gallery' not in s:
   s=s.replace('class="signature-links"','class="signature-links signature-gallery"',1)
   images=iter(['nbc-photo.jpg','dforma-photo.jpg','hashem-photo.jpg'])
   s=re.sub(r'(<a href="collections.html#(?:nova|aura|velare)">)(<strong>.*?</strong><span>.*?</span>)(</a>)',lambda m:m[1]+f'<img src="{asset}{next(images)}" alt="" loading="lazy"><div class="signature-caption">'+m[2]+'</div><span class="signature-discover">'+('اكتشف الخط' if ar else 'Discover the line')+'</span>'+m[3],s)
 p.write_text(s)
