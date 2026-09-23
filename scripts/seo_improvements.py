from pathlib import Path
from datetime import date
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
SITEMAP = ROOT / "sitemap.xml"

html = INDEX.read_text(encoding="utf-8", errors="replace")

# Strengthen crawl/indexing directives and social previews without changing visible copy.
anchor = '<meta name="description"'
robots = '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">'
if 'name="robots"' not in html:
    html = html.replace(anchor, robots + anchor, 1)

extras = '''<meta name="author" content="أورا للأفكار">
<link rel="alternate" hreflang="ar-KW" href="https://www.auraideaskw.com/">
<link rel="alternate" hreflang="x-default" href="https://www.auraideaskw.com/">
<meta property="og:image:alt" content="شعار أورا للأفكار للخدمات الأكاديمية والبحثية في الكويت">
<meta name="twitter:title" content="أورا للأفكار | دعم أكاديمي وبحثي في الكويت">
<meta name="twitter:description" content="دعم أكاديمي وبحثي منظم للطلاب والباحثين في الكويت، من الخطة البحثية إلى التحليل الإحصائي.">
'''
if 'hreflang="ar-KW"' not in html:
    html = html.replace('<link rel="canonical"', extras + '<link rel="canonical"', 1)

# Replace the single Organization object with a connected graph describing the homepage,
# business, and website. This gives Google clearer entity and site relationships.
old = re.search(r'<script type="application/ld\+json">.*?</script>', html, flags=re.S)
new_json = '''<script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"Organization","@id":"https://www.auraideaskw.com/#organization","name":"أورا للأفكار","url":"https://www.auraideaskw.com/","logo":{"@type":"ImageObject","url":"https://www.auraideaskw.com/logo-512.png"},"areaServed":{"@type":"Country","name":"الكويت"},"telephone":"+971588740073","sameAs":["https://www.facebook.com/auraideaskw1"]},{"@type":"ProfessionalService","@id":"https://www.auraideaskw.com/#business","name":"أورا للأفكار للخدمات الأكاديمية","url":"https://www.auraideaskw.com/","description":"خدمات ودعم أكاديمي وبحثي للطلاب والباحثين في الكويت.","areaServed":{"@type":"Country","name":"الكويت"},"provider":{"@id":"https://www.auraideaskw.com/#organization"},"serviceType":["إعداد الخطط البحثية","الأبحاث الجامعية","رسائل الماجستير والدكتوراه","التحليل الإحصائي","التدقيق والتنسيق"]},{"@type":"WebSite","@id":"https://www.auraideaskw.com/#website","url":"https://www.auraideaskw.com/","name":"أورا للأفكار","inLanguage":"ar-KW","publisher":{"@id":"https://www.auraideaskw.com/#organization"}}]}</script>'''
if old:
    html = html[:old.start()] + new_json + html[old.end():]
else:
    raise SystemExit("Expected homepage JSON-LD block was not found")

INDEX.write_text(html, encoding="utf-8")

# Mark only the homepage as updated; do not fabricate dates for unchanged articles.
sitemap = SITEMAP.read_text(encoding="utf-8")
sitemap = re.sub(r'(<loc>https://www\.auraideaskw\.com/</loc><lastmod>)[^<]+(</lastmod>)', r'\g<1>2026-09-23\g<2>', sitemap, count=1)
SITEMAP.write_text(sitemap, encoding="utf-8")
print("Updated", INDEX)
print("Updated homepage lastmod in", SITEMAP)
print("Homepage size:", INDEX.stat().st_size)
print("Sitemap URLs:", sitemap.count("<loc>"))
