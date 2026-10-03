#!/usr/bin/env python3
"""Repack local dist/assets and company profile for the container build."""
from pathlib import Path
import tarfile
root = Path(__file__).resolve().parents[1]
parts = root / 'site-assets'
parts.mkdir(exist_ok=True)
archive = parts / 'site-assets.tar.gz'
with tarfile.open(archive, 'w:gz') as output:
    output.add(root / 'dist/assets', arcname='assets')
    output.add(root / 'dist/black-c-company-profile.pdf', arcname='black-c-company-profile.pdf')
for old in parts.glob('part-*'):
    old.unlink()
with archive.open('rb') as source:
    number = 0
    while chunk := source.read(524288):
        (parts / f'part-{number:03}').write_bytes(chunk)
        number += 1
archive.unlink()
print(f'Packed assets into {number} parts.')
