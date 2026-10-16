"""Attach the GA4 tag to every locale and page without inline executable code."""
from pathlib import Path
root=Path(__file__).parent/'dist'
for p in root.rglob('*.html'):
 s=p.read_text()
 if 'gtag/js?id=G-VGBHY89WZX' in s:continue
 prefix='../'*len(p.relative_to(root).parts[:-1])
 tag=f'<script src="{prefix}analytics.js"></script><script async src="https://www.googletagmanager.com/gtag/js?id=G-VGBHY89WZX"></script>'
 s=s.replace('</head>',tag+'</head>',1)
 p.write_text(s)
