from pathlib import Path
from urllib.parse import quote
from xml.sax.saxutils import escape
from datetime import datetime, timezone
from bs4 import BeautifulSoup

root = Path(__file__).resolve().parent
base = 'https://www.auraideaskw.com'
paths = []
for f in root.rglob('index.html'):
    rel = f.relative_to(root)
    if any(part in {'.git', 'node_modules'} for part in rel.parts):
        continue
    # Exclude filesystem paths produced by broken Arabic encoding conversion.
    if any(any(mark in part for mark in ('┘', '╪', '�')) for part in rel.parts):
        continue
    path = '/' if rel.parts == ('index.html',) else '/' + '/'.join(rel.parts[:-1]) + '/'
    segments = [part for part in path.strip('/').split('/') if part]
    if any(a == b for a, b in zip(segments, segments[1:])):
        continue
    try:
        soup = BeautifulSoup(f.read_text(encoding='utf-8', errors='ignore'), 'html.parser')
        robots = soup.find('meta', attrs={'name': lambda x: x and x.lower() == 'robots'})
        title = soup.find('title')
        canonical = soup.find('link', rel=lambda v: v and 'canonical' in v)
        if (robots and 'noindex' in robots.get('content', '').lower()) or not title or not title.get_text(strip=True) or not canonical or not canonical.get('href'):
            continue
    except Exception:
        continue
    if path == '/blog/':
        continue
    paths.append(path)

paths = sorted(set(paths), key=lambda p: (0 if p in {'/', '/المدونة/', '/about/', '/خدماتنا/', '/contact/'} else 1, p))
now = datetime.now(timezone.utc).date().isoformat()
xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for path in paths:
    loc = base + quote(path, safe='/:')
    xml.append(f'  <url><loc>{escape(loc)}</loc><lastmod>{now}</lastmod></url>')
xml.append('</urlset>')
(root / 'sitemap.xml').write_text('\n'.join(xml) + '\n', encoding='utf-8')

# Keep the index valid for crawlers that discover it directly.
index_xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    f'  <sitemap><loc>{base}/sitemap.xml</loc><lastmod>{now}</lastmod></sitemap>',
    '</sitemapindex>',
]
(root / 'sitemap_index.xml').write_text('\n'.join(index_xml) + '\n', encoding='utf-8')
print('wrote', len(paths), 'indexable URLs')
print('first', paths[:10])
