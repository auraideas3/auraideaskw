from pathlib import Path
from bs4 import BeautifulSoup

root = Path(__file__).resolve().parent
blog_path = root / 'المدونة/index.html'
slugs = ['five-essential-conditions-successful-research-plan','prepare-masters-defense-powerpoint-without-anxiety','best-ways-search-peer-reviewed-journals','common-graduation-research-rejection-mistakes','theoretical-framework-methodology-masters-phd','spss-data-entry-results-interpretation','review-previous-studies-research-gap','academic-translation-articles-theses','university-research-ready-for-print','academic-services-gulf-accuracy-speed-confidentiality','academic-research-support-start-success','academic-powerpoint-design-for-better-defense']
soup = BeautifulSoup(blog_path.read_text(encoding='utf-8'), 'html.parser')
posts = soup.find(id='posts')
if not posts:
    raise SystemExit('posts container not found')
by_slug = {}
for card in posts.find_all('article', recursive=False):
    links = [a.get('href', '') for a in card.find_all('a', href=True)]
    for slug in slugs:
        if f'/{slug}/' in links:
            by_slug[slug] = card
for slug in reversed(slugs):
    card = by_slug.get(slug)
    if card:
        posts.insert(0, card)
blog_path.write_text(str(soup), encoding='utf-8')
print('promoted:', sum(1 for slug in slugs if slug in by_slug))
print('first links:', [a.get('href') for a in posts.find_all('a', href=True)[:12]])
