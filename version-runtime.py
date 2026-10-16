"""Invalidate cached runtime when deploying the on-demand animation loader."""
from pathlib import Path
import re
for p in (Path(__file__).parent/'dist').rglob('*.html'):
 s=re.sub(r'(src="(?:\.\./)*app\.js)(?:\?[^" ]*)?"',r'\1?v=20261016-demand-frames"',p.read_text());p.write_text(s)
