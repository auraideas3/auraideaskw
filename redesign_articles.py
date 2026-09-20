from pathlib import Path
from bs4 import BeautifulSoup
from html import escape

ROOT = Path(__file__).resolve().parent
slugs = {
    'five-essential-conditions-successful-research-plan': 'خطة البحث',
    'prepare-masters-defense-powerpoint-without-anxiety': 'العروض الأكاديمية',
    'best-ways-search-peer-reviewed-journals': 'التوثيق والنشر',
    'common-graduation-research-rejection-mistakes': 'بحوث جامعية',
    'theoretical-framework-methodology-masters-phd': 'الدراسات العليا',
    'spss-data-entry-results-interpretation': 'التحليل الإحصائي',
    'review-previous-studies-research-gap': 'الدراسات العليا',
    'academic-translation-articles-theses': 'التدقيق والترجمة',
    'university-research-ready-for-print': 'بحوث جامعية',
    'academic-services-gulf-accuracy-speed-confidentiality': 'خدمات أكاديمية',
    'academic-research-support-start-success': 'بحوث جامعية',
    'academic-powerpoint-design-for-better-defense': 'العروض الأكاديمية',
}

STYLE = r'''
<style id="aura-article-redesign">
:root{--article-navy:#103b56;--article-blue:#167c9b;--article-mint:#eaf7f1;--article-gold:#d6a642;--article-ink:#253947;--article-muted:#637783;--article-border:#dce9e8}
body{background:#f4f8f7!important}
.article-page{width:100%;padding:34px 20px 88px;background:linear-gradient(180deg,#eff8f6 0,#f7fbfa 420px,#f4f8f7 100%);color:var(--article-ink);font-family:inherit}
.article-page>.article-wrap{max-width:1180px;margin:0 auto}
.article-breadcrumb{max-width:1040px;margin:0 auto 18px;color:#607783;font-size:13px;line-height:1.8}
.article-breadcrumb a{color:var(--article-blue);text-decoration:none;font-weight:700}
.article-hero{max-width:1040px;margin:0 auto 28px;padding:42px 56px 38px;border:1px solid #d7ebe5;border-radius:22px;background:linear-gradient(135deg,#fff 0,#f5fcf8 60%,#e8f5f6 100%);box-shadow:0 16px 40px rgba(16,59,86,.09);text-align:center}
.article-kicker{display:inline-flex;align-items:center;gap:8px;margin-bottom:16px;padding:7px 15px;border-radius:99px;background:var(--article-mint);color:#28775e;font-size:13px;font-weight:800}
.article-kicker:before{content:"✦";color:var(--article-gold);font-size:16px}
.article-hero h1{max-width:880px;margin:0 auto 16px;color:var(--article-navy);font-size:clamp(30px,4.1vw,52px);font-weight:900;line-height:1.28;letter-spacing:-.02em}
.article-lead{max-width:790px;margin:0 auto;color:#526975;font-size:18px;line-height:2.05}
.article-meta{display:flex;justify-content:center;flex-wrap:wrap;gap:9px;margin-top:22px}
.article-meta span{padding:7px 13px;border:1px solid #d8e9e3;border-radius:99px;background:#fff;color:#54706e;font-size:12px;font-weight:700}
.article-layout{display:grid;grid-template-columns:minmax(0,1fr) 245px;gap:24px;align-items:start;direction:rtl}
.article-content{min-width:0!important;max-width:none!important;margin:0!important;padding:42px 58px 50px!important;border:1px solid var(--article-border);border-radius:20px;background:#fff;box-shadow:0 12px 32px rgba(16,59,86,.07);font-size:17px;line-height:2.05}
.article-content>p:first-child{margin:0 0 30px;padding:19px 22px;border-right:4px solid var(--article-gold);border-radius:10px;background:#f3faf7;color:#315466;font-size:18px;line-height:2}
.article-content section{margin:0 0 34px;padding:0 0 8px;border-bottom:1px solid #edf2f1}
.article-content section:last-child{border-bottom:0;margin-bottom:0}
.article-content h2{margin:0 0 14px;color:var(--article-blue);font-size:clamp(24px,3vw,32px);line-height:1.45;font-weight:900}
.article-content h2:before{content:"";display:inline-block;width:5px;height:1.05em;margin-left:11px;vertical-align:-.13em;border-radius:5px;background:var(--article-gold)}
.article-content h3{margin:22px 0 6px;color:var(--article-navy);font-size:20px;line-height:1.55;font-weight:900}
.article-content p{margin:0 0 15px;color:#334b58}
.article-content a{color:var(--article-blue);font-weight:800}
.article-sidebar{position:sticky;top:18px;direction:rtl}
.article-toc{padding:23px 20px;border:1px solid #d9ebe5;border-radius:16px;background:#fff;box-shadow:0 10px 24px rgba(16,59,86,.06)}
.article-toc strong{display:block;margin-bottom:13px;color:var(--article-navy);font-size:17px}
.article-toc a{display:block;padding:8px 0;border-bottom:1px solid #edf3f1;color:#58717b;text-decoration:none;font-size:13px;line-height:1.6}
.article-toc a:last-child{border-bottom:0}
.article-toc a:hover{color:var(--article-blue)}
.article-sidebar .article-cta{display:block;margin-top:15px;padding:14px 15px;border-radius:12px;background:var(--article-blue);color:#fff;text-align:center;text-decoration:none;font-size:14px;font-weight:800;line-height:1.6;box-shadow:0 9px 18px rgba(22,124,155,.2)}
.article-sidebar .article-cta:hover{background:var(--article-navy)}
@media(max-width:900px){.article-page{padding:24px 14px 60px}.article-hero{padding:32px 25px 28px;border-radius:17px}.article-layout{grid-template-columns:1fr}.article-sidebar{position:static;grid-row:1}.article-content{grid-row:2;padding:30px 25px 36px!important}.article-toc{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 17px}.article-toc strong{grid-column:1/-1}.article-sidebar .article-cta{display:none}}
@media(max-width:560px){.article-page{padding:16px 10px 45px}.article-breadcrumb{font-size:12px;margin-bottom:12px}.article-hero{padding:26px 17px 23px;margin-bottom:17px}.article-hero h1{font-size:29px;line-height:1.4}.article-lead{font-size:15px;line-height:1.9}.article-meta{margin-top:16px}.article-meta span{font-size:11px;padding:6px 10px}.article-content{padding:24px 18px 28px!important;border-radius:15px;font-size:16px;line-height:2}.article-content>p:first-child{padding:15px 15px;font-size:16px}.article-content h2{font-size:23px}.article-content h3{font-size:18px}.article-toc{grid-template-columns:1fr;padding:17px}.article-toc strong{grid-column:auto}}
@media(prefers-reduced-motion:no-preference){.article-content section{scroll-margin-top:24px}.article-toc a{transition:color .18s ease}}
</style>
'''

for slug, category in slugs.items():
    path = ROOT / slug / 'index.html'
    soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    old_main = soup.find('main', class_='article-page')
    if not old_main:
        raise RuntimeError(f'missing main: {slug}')
    title_node = old_main.find('h1')
    lead_node = old_main.find('p', class_='article-lead')
    old_article = old_main.find('article', class_='article-content')
    if not title_node or not lead_node or not old_article:
        raise RuntimeError(f'missing article nodes: {slug}')
    title = title_node.get_text(' ', strip=True)
    lead = lead_node.get_text(' ', strip=True)
    intro = old_article.find('p')
    sections = old_article.find_all('section', recursive=False)
    toc_items = []
    for i, section in enumerate(sections, 1):
        h2 = section.find('h2', recursive=False)
        if not h2:
            continue
        section['id'] = 'article-section-' + str(i)
        toc_items.append((f'article-section-{i}', h2.get_text(' ', strip=True)))
    new_main = soup.new_tag('main', attrs={'class': 'article-page', 'dir': 'rtl'})
    wrap = soup.new_tag('div', attrs={'class': 'article-wrap'})
    breadcrumb = soup.new_tag('nav', attrs={'class': 'article-breadcrumb', 'aria-label': 'مسار التنقل'})
    a_home = soup.new_tag('a', href='/'); a_home.string = 'الرئيسية'
    a_blog = soup.new_tag('a', href='/المدونة/'); a_blog.string = 'المدونة'
    breadcrumb.append(a_home); breadcrumb.append(' ← '); breadcrumb.append(a_blog); breadcrumb.append(' ← '); breadcrumb.append(category)
    hero = soup.new_tag('header', attrs={'class': 'article-hero'})
    kicker = soup.new_tag('div', attrs={'class': 'article-kicker'}); kicker.string = category
    hero.append(kicker); hero.append(title_node)
    hero.append(lead_node)
    meta = soup.new_tag('div', attrs={'class': 'article-meta'})
    for text in ('دليل أكاديمي عملي', 'قراءة واضحة ومنظمة', 'مناسب للطلاب والباحثين'):
        span = soup.new_tag('span'); span.string = text; meta.append(span)
    hero.append(meta)
    layout = soup.new_tag('div', attrs={'class': 'article-layout'})
    content = soup.new_tag('article', attrs={'class': 'article-content container'})
    if intro:
        content.append(intro)
    for section in sections:
        content.append(section)
    sidebar = soup.new_tag('aside', attrs={'class': 'article-sidebar', 'aria-label': 'محتويات المقال'})
    toc = soup.new_tag('nav', attrs={'class': 'article-toc'})
    strong = soup.new_tag('strong'); strong.string = 'محتويات المقال'; toc.append(strong)
    for sid, text in toc_items:
        link = soup.new_tag('a', href='#' + sid); link.string = text; toc.append(link)
    sidebar.append(toc)
    cta = soup.new_tag('a', attrs={'class': 'article-cta', 'href': 'https://wa.me/971588740073'})
    cta.string = 'هل تحتاج مساعدة أكاديمية؟ تواصل معنا'
    sidebar.append(cta)
    layout.append(content); layout.append(sidebar)
    wrap.append(breadcrumb); wrap.append(hero); wrap.append(layout)
    for script in old_main.find_all('script', recursive=False):
        wrap.append(script)
    new_main.append(wrap)
    old_main.replace_with(new_main)
    old_style = soup.find('style', id='aura-article-redesign')
    if old_style: old_style.decompose()
    soup.head.append(BeautifulSoup(STYLE, 'html.parser'))
    path.write_text(str(soup), encoding='utf-8')
    print('redesigned', slug)
