"""Shared navigation, portfolio taxonomy, and location refinements."""
from pathlib import Path
import re
root=Path(__file__).parent/'dist'
map_url='https://maps.app.goo.gl/ywA4Gn8dBtBoHspcA'
for p in root.rglob('*.html'):
 s=p.read_text();ar='ar' in p.relative_to(root).parts
 s=s.replace('Menu +','Menu').replace('القائمة +','القائمة')
 s=re.sub(r'<span class="(?:small-number|service-no|reason-number)">\s*\d+\s*</span>','',s)
 s=re.sub(r'<span[^>]*>\s*\d{2}\s*/\s*</span>','',s)
 s=re.sub(r'(<span[^>]*>)\s*\d{2}\s*/\s*',r'\1',s)
 location='الرياض<br>المملكة العربية السعودية' if ar else 'Riyadh<br>Kingdom of Saudi Arabia'
 map_label='عرض الموقع على خرائط Google' if ar else 'View on Google Maps'
 s=s.replace(f'<p>{location}</p>',f'<p><a class="map-location" href="{map_url}" target="_blank" rel="noopener">{location}</a></p><a class="map-link" href="{map_url}" target="_blank" rel="noopener">{map_label}</a>')
 if p.name=='contact.html':
  marker='خدمة المشاريع في المملكة العربية السعودية' if ar else 'Serving projects in Saudi Arabia'
  if marker in s:s=s.replace(f'<b>{marker}</b>',f'<a class="underlined" href="{map_url}" target="_blank" rel="noopener">{map_label}</a>')
 if p.name=='projects.html':
  cats=re.findall(r'<article class="project-card" data-category="([^"]+)"',s)
  labels=[('All','جميع المشاريع' if ar else 'All projects'),('Residential','سكني' if ar else 'Residential'),('Commercial','تجاري' if ar else 'Commercial'),('Industrial','صناعي' if ar else 'Industrial')]
  buttons=''.join(f'<button data-filter="{key}" aria-pressed="{str(i==0).lower()}">{label} <span>{len(cats) if key=="All" else cats.count(key)}</span></button>' for i,(key,label) in enumerate(labels))
  legend='تصفية حسب نوع المشروع' if ar else 'Filter by project type'
  filters=f'<div class="project-filter-heading">{legend}</div><div class="filters" role="group" aria-label="{legend}">{buttons}</div>'
  s=re.sub(r'<div class="filters".*?</div>',filters,s,count=1)
 p.write_text(s)
print('Simplified filters, removed decorative numbering, and added map links across 30 pages.')
