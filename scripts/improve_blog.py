from pathlib import Path
from urllib.parse import urlparse, unquote
import json
import re
import html

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "المدونة" / "index.html"
SITEMAP = ROOT / "sitemap.xml"

# These are exported archive/legacy pages with generic duplicate content or duplicate destinations.
# Keep them reachable for existing links, but prevent them competing in organic search.
DUPLICATE_PATTERNS = [
    re.compile(r"^/20\d\d/\d\d/\d\d/(?:\d+|masterthesisi|assignment-solution)/$"),
]
DUPLICATE_PATHS = {
    "/مقالات-خدمات-طلابية/blog-auraideas/",
    "/البحوث-الجامعية-في-الإمارات/",
    "/تواصل-معنا/",
}
GENERIC_TITLE = "دليل أكاديمي عملي للطلاب في الكويت | أورا للأفكار في الكويت"


def is_duplicate_path(path: str) -> bool:
    return path in DUPLICATE_PATHS or any(p.match(path) for p in DUPLICATE_PATTERNS)


def add_or_replace_meta(html_text: str, name: str, content: str) -> str:
    pat = re.compile(r'<meta\s+[^>]*name=["\']' + re.escape(name) + r'["\'][^>]*>', re.I)
    tag = f'<meta name="{name}" content="{html.escape(content, quote=True)}">'
    if pat.search(html_text):
        return pat.sub(tag, html_text, count=1)
    return html_text.replace("</head>", tag + "</head>", 1)


# Curate the archive: remove generic duplicate cards from the rendered collection.
blog_html = BLOG.read_text(encoding="utf-8", errors="replace")
card_re = re.compile(r'<article\s+class="post-card".*?</article>', re.I | re.S)
removed_cards = 0
kept_cards = []
for card in card_re.findall(blog_html):
    hrefs = re.findall(r'href="([^"]+)"', card, re.I)
    path = hrefs[0] if hrefs else ""
    title_match = re.search(r'<h2[^>]*>.*?<a[^>]*>(.*?)</a>', card, re.I | re.S)
    title = re.sub(r"<[^>]+>", " ", html.unescape(title_match.group(1) if title_match else ""))
    title = " ".join(title.split())
    if is_duplicate_path(path) or title == "دليل أكاديمي عملي للطلاب في الكويت":
        removed_cards += 1
    else:
        kept_cards.append(card)

# Replace the contiguous card region, preserving the surrounding archive controls and scripts.
matches = list(card_re.finditer(blog_html))
if matches:
    blog_html = blog_html[:matches[0].start()] + "".join(kept_cards) + blog_html[matches[-1].end():]

# Improve archive-level metadata and visible hierarchy.
blog_html = add_or_replace_meta(blog_html, "robots", "index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1")
blog_html = re.sub(r'<link\s+href="[^"]+"\s+rel="canonical"\s*/?>', '<link rel="canonical" href="https://www.auraideaskw.com/المدونة/">', blog_html, count=1, flags=re.I)
if 'property="og:url"' not in blog_html:
    blog_html = blog_html.replace('<meta content="website" property="og:type"/>', '<meta content="website" property="og:type"/><meta content="https://www.auraideaskw.com/المدونة/" property="og:url"/>', 1)
if 'hreflang="ar-KW"' not in blog_html:
    blog_html = blog_html.replace('<link', '<link rel="alternate" hreflang="ar-KW" href="https://www.auraideaskw.com/المدونة/">\n<link', 1)
    blog_html = blog_html.replace('<link rel="alternate" hreflang="ar-KW" href="https://www.auraideaskw.com/المدونة/">\n<link rel="alternate"', '<link rel="alternate"') if False else blog_html
blog_html = blog_html.replace('<h1>مكتبة أورا<br/><span>المعرفية</span></h1>', '<h1>مدونة أورا للأفكار<br/><span>أدلة أكاديمية وبحوث جامعية</span></h1>', 1)
blog_html = blog_html.replace('مكتبة معرفية عملية للطلاب والباحثين في الكويت.', 'أدلة عملية للطلاب والباحثين في الكويت حول كتابة البحوث، خطط البحث، الدراسات العليا، التوثيق والتحليل الإحصائي.', 1)

# Build a CollectionPage + ItemList from the curated cards so article relationships are explicit.
items = []
for pos, card in enumerate(kept_cards, start=1):
    a = re.search(r'<h2[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', card, re.I | re.S)
    if not a:
        continue
    path = a.group(1)
    title = " ".join(re.sub(r"<[^>]+>", " ", html.unescape(a.group(2))).split())
    items.append({"@type": "ListItem", "position": pos, "url": "https://www.auraideaskw.com" + path, "name": title})
collection = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "@id": "https://www.auraideaskw.com/المدونة/#webpage",
    "url": "https://www.auraideaskw.com/المدونة/",
    "name": "مدونة أورا للأفكار | أدلة أكاديمية وبحوث جامعية",
    "inLanguage": "ar-KW",
    "description": "أدلة عملية للطلاب والباحثين في الكويت حول كتابة البحوث، خطط البحث، الدراسات العليا، التوثيق والتحليل الإحصائي.",
    "isPartOf": {"@id": "https://www.auraideaskw.com/#website"},
    "mainEntity": {"@type": "ItemList", "itemListElement": items},
}
json_tag = '<script type="application/ld+json">' + json.dumps(collection, ensure_ascii=False, separators=(",", ":")) + '</script>'
if '"@type":"CollectionPage"' in blog_html:
    blog_html = re.sub(r'<script type="application/ld\+json">.*?</script>', json_tag, blog_html, count=1, flags=re.S)
else:
    blog_html = blog_html.replace('</head>', json_tag + '</head>', 1)
BLOG.write_text(blog_html, encoding="utf-8")

# Mark duplicate legacy pages noindex and remove them from the XML sitemap.
sitemap = SITEMAP.read_text(encoding="utf-8", errors="replace")
locs = re.findall(r'<loc>(.*?)</loc>', sitemap)
kept_locs = []
removed_locs = []
for loc in locs:
    path = unquote(urlparse(loc).path)
    if is_duplicate_path(path) and path != "/المدونة/":
        removed_locs.append(path)
    else:
        kept_locs.append(loc)
for path in sorted(set(removed_locs)):
    f = ROOT / path.strip("/") / "index.html"
    if not f.exists():
        continue
    page = f.read_text(encoding="utf-8", errors="replace")
    page = add_or_replace_meta(page, "robots", "noindex,follow")
    f.write_text(page, encoding="utf-8")

entries = [f'  <url><loc>{loc}</loc><lastmod>2026-09-23</lastmod></url>' if loc.endswith('/المدونة/') else f'  <url><loc>{loc}</loc><lastmod>2026-09-20</lastmod></url>' for loc in kept_locs]
sitemap_out = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(entries) + '\n</urlset>\n'
SITEMAP.write_text(sitemap_out, encoding="utf-8")
print(f"Curated blog cards: removed={removed_cards}, kept={len(kept_cards)}")
print(f"Curated sitemap URLs: removed={len(set(removed_locs))}, kept={len(kept_locs)}")
print("Added CollectionPage ItemList entries:", len(items))
