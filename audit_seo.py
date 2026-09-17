from pathlib import Path
from urllib.parse import quote
from bs4 import BeautifulSoup
from collections import Counter

root = Path(__file__).resolve().parent
base = 'https://www.auraideaskw.com'
html_files = list(root.rglob('index.html'))
noindex = []
missing_title = []
missing_canonical = []
canonical_counts = Counter()
for f in html_files:
    if '.git' in f.parts:
        continue
    rel = f.relative_to(root)
    text = f.read_text(encoding='utf-8', errors='ignore')
    soup = BeautifulSoup(text, 'html.parser')
    robots = soup.find('meta', attrs={'name': lambda x: x and x.lower() == 'robots'})
    if robots and 'noindex' in robots.get('content', '').lower():
        noindex.append(str(rel))
    if not soup.title or not soup.title.get_text(strip=True):
        missing_title.append(str(rel))
    canon = soup.find('link', rel=lambda v: v and 'canonical' in v)
    if not canon or not canon.get('href'):
        missing_canonical.append(str(rel))
    else:
        canonical_counts[canon['href']] += 1
print(f'html={len(html_files)} noindex={len(noindex)} missing_title={len(missing_title)} missing_canonical={len(missing_canonical)}')
print('noindex sample:', noindex[:10])
print('missing canonical sample:', missing_canonical[:10])
print('duplicate canonical targets:', [(u, n) for u, n in canonical_counts.items() if n > 1][:20])

for name in ['sitemap.xml', 'sitemap_index.xml']:
    p = root / name
    print(name, 'exists=', p.exists(), 'bytes=', p.stat().st_size if p.exists() else 0)
    if p.exists():
        text = p.read_text(encoding='utf-8', errors='ignore')
        print(' relative locs=', text.count('<loc>/'), 'absolute locs=', text.count('<loc>http'))
        print(' invalid/malformed markers=', sum(text.count(x) for x in ['�', '╪', '┘']))

for name in ('sitemap.xml', 'sitemap_index.xml'):
    text = (root / name).read_text(encoding='utf-8', errors='ignore')
    if '<loc>/' in text or any(mark in text for mark in ('�', '╪', '┘')):
        raise SystemExit(f'invalid sitemap artifact: {name}')
print('sitemap artifacts passed absolute-URL and encoding checks')
