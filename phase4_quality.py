from pathlib import Path
from bs4 import BeautifulSoup
from datetime import date
import json, re

BASE = 'https://www.auraideaskw.com'
ARCHIVE_PARTS = {'author', 'category', 'tag', 'page'}
UTILITY_PARTS = {'elementor-hf', 'payment', 'form', 'scan'}

def set_robots(raw, value):
    pat = re.compile(r'(<meta\b[^>]*\bname=["\']robots["\'][^>]*\bcontent=["\'])[^"\']*(["\'])', re.I)
    if pat.search(raw): return pat.sub(lambda m: m.group(1)+value+m.group(2), raw, count=1)
    return re.sub(r'</head\s*>', f'<meta name="robots" content="{value}"></head>', raw, count=1, flags=re.I)

def canonical(raw):
    m = re.search(r'<link\b[^>]*\brel=["\'][^"\']*canonical[^"\']*["\'][^>]*\bhref=["\']([^"\']+)', raw, re.I)
    if not m:
        m = re.search(r'<link\b[^>]*\bhref=["\']([^"\']+)["\'][^>]*\brel=["\'][^"\']*canonical', raw, re.I)
    return m.group(1) if m else None

def meta(raw, name):
    soup = BeautifulSoup(raw, 'html.parser')
    tag = soup.find('meta', attrs={'name': name})
    return tag.get('content', '') if tag else ''

def title_and_h1(raw):
    soup = BeautifulSoup(raw, 'html.parser')
    title = soup.title.get_text(' ', strip=True) if soup.title else ''
    h1 = soup.find('h1')
    return title, (h1.get_text(' ', strip=True) if h1 else '')

def add_article_schema(raw, rel):
    if re.search(r'"@type"\s*:\s*"Article"', raw): return raw, False
    title, h1 = title_and_h1(raw)
    desc = meta(raw, 'description')
    url = canonical(raw)
    if not title or not h1 or not desc or not url: return raw, False
    parts = rel.parts
    published = None
    if len(parts) >= 3 and re.fullmatch(r'20\d\d', parts[0]) and re.fullmatch(r'\d{2}', parts[1]):
        day = parts[2].split('/')[0]
        if re.fullmatch(r'\d{2}', day): published = f'{parts[0]}-{parts[1]}-{day}'
    obj = {
        '@context':'https://schema.org', '@type':'Article',
        'headline': h1[:180], 'description': desc[:300], 'url': url,
        'inLanguage':'ar', 'author':{'@type':'Organization','name':'أورا للأفكار','url':BASE+'/'},
        'publisher':{'@type':'Organization','name':'أورا للأفكار','url':BASE+'/','logo':{'@type':'ImageObject','url':BASE+'/logo-512.png'}},
        'mainEntityOfPage':{'@type':'WebPage','@id':url}
    }
    if published:
        obj['datePublished'] = published
        obj['dateModified'] = published
    script = '<script type="application/ld+json">'+json.dumps(obj, ensure_ascii=False, separators=(',',':'))+'</script>'
    return re.sub(r'</head\s*>', script+'</head>', raw, count=1, flags=re.I), True

def main():
    noindex = 0; articles = 0
    for p in Path('.').rglob('index.html'):
        rel = p.relative_to('.')
        raw = p.read_text('utf-8', errors='ignore')
        if any(x in ARCHIVE_PARTS for x in rel.parts) or any(x in UTILITY_PARTS for x in rel.parts):
            updated = set_robots(raw, 'noindex,follow')
            if updated != raw:
                p.write_text(updated, encoding='utf-8'); noindex += 1
            continue
        if len(rel.parts) >= 3 and re.fullmatch(r'20\d\d', rel.parts[0]):
            updated, changed = add_article_schema(raw, rel)
            if changed:
                p.write_text(updated, encoding='utf-8'); articles += 1
    print('noindex archives/utilities updated', noindex)
    print('Article schemas added', articles)

if __name__ == '__main__': main()
