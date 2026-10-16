from pathlib import Path
from bs4 import BeautifulSoup
from collections import Counter
import re
from urllib.parse import quote

EXCLUDE = {
    'payment','form','scan','privacy-policy','terms-and-conditions','wp-admin',
    'wp-login.php','blog','services','research','about','contact','guarantees',
    'الأبحاث-الجامعية','التحليل-الإحصائي','التدقيق-والتنسيق','الخطة-البحثية',
    'رسائل-الماجستير','العروض-الأكاديمية','خدمات-الدعم-الأكاديمي'
}
BASE = 'https://www.auraideaskw.com'
CLUSTERS = {
    'تحليل إحصائي': [
        ('التحليل الإحصائي SPSS في الكويت', '/التحليل-الإحصائي/'),
        ('تحليل الاستبانة باستخدام SPSS', '/questionnaire-analysis-using-spss/'),
        ('اختيار الاختبار الإحصائي المناسب', '/how-to-choose-statistical-test/'),
        ('خدمات الدعم الأكاديمي والبحثي', '/خدمات-الدعم-الأكاديمي/#spss-statistics'),
    ],
    'خطط ومنهجية': [
        ('إعداد خطة البحث', '/الخطة-البحثية/'),
        ('كتابة الإطار النظري', '/how-to-write-theoretical-framework/'),
        ('الأبحاث الجامعية في الكويت', '/الأبحاث-الجامعية/'),
        ('خدمات الدعم الأكاديمي والبحثي', '/خدمات-الدعم-الأكاديمي/#research-plan-preparation'),
    ],
    'رسائل ودراسات عليا': [
        ('دعم رسائل الماجستير والدكتوراه', '/رسائل-الماجستير/'),
        ('الإطار النظري والمنهجية للرسائل', '/theoretical-framework-methodology-masters-phd/'),
        ('تجهيز عرض مناقشة الماجستير', '/prepare-masters-defense-powerpoint-without-anxiety/'),
        ('خدمات الدعم الأكاديمي والبحثي', '/خدمات-الدعم-الأكاديمي/#masters-thesis-review'),
    ],
    'تدقيق وتوثيق': [
        ('تدقيق وتنسيق الأبحاث والرسائل', '/التدقيق-والتنسيق/'),
        ('دليل APA 7 لتوثيق المراجع', '/comprehensive-guide-apa-7/'),
        ('التدقيق اللغوي للأبحاث والرسائل', '/language-proofreading-academic-theses/'),
        ('خدمات الدعم الأكاديمي والبحثي', '/خدمات-الدعم-الأكاديمي/#academic-proofreading'),
    ],
    'عروض أكاديمية': [
        ('تصميم عروض المناقشة الأكاديمية', '/العروض-الأكاديمية/'),
        ('تصميم عرض أكاديمي احترافي', '/how-to-design-professional-academic-presentation/'),
        ('عرض مناقشة الماجستير بدون قلق', '/prepare-masters-defense-powerpoint-without-anxiety/'),
        ('خدمات الدعم الأكاديمي والبحثي', '/خدمات-الدعم-الأكاديمي/#academic-powerpoint'),
    ],
    'أبحاث جامعية': [
        ('كتابة الأبحاث الجامعية في الكويت', '/الأبحاث-الجامعية/'),
        ('كيف تكتب بحثًا جامعيًا خطوة بخطوة', '/how-to-write-excellent-university-research-step-by-step/'),
        ('الأبحاث الجامعية الجاهزة للطباعة', '/university-research-ready-for-print/'),
        ('خدمات أورا الأكاديمية', '/services/'),
    ],
}

def cluster_for(text):
    t = text.lower()
    if any(k in t for k in ['spss','استبان','تحليل إحصائي','التحليل الإحصائي']): return 'تحليل إحصائي'
    if any(k in t for k in ['خطة بحث','الخطة البحثية','منهجية','الإطار النظري','الدراسات السابقة']): return 'خطط ومنهجية'
    if any(k in t for k in ['ماجستير','دكتوراه','رسالة','أطروحة']): return 'رسائل ودراسات عليا'
    if any(k in t for k in ['تدقيق','تنسيق','apa','توثيق','مراجع','اقتباس']): return 'تدقيق وتوثيق'
    if any(k in t for k in ['بوربوينت','عرض تقديمي','مناقشة']): return 'عروض أكاديمية'
    return 'أبحاث جامعية'

def main():
    counts = Counter()
    for p in Path('.').rglob('index.html'):
        rel = p.relative_to('.')
        if any(x in EXCLUDE for x in rel.parts): continue
        soup = BeautifulSoup(p.read_text('utf-8', errors='ignore'), 'html.parser')
        if not soup.find('h1') or not soup.title or soup.find(class_='seo-cluster-links'): continue
        # Classify from the page's subject, not shared navigation/footer text.
        subject_nodes = [soup.title, soup.find('h1')]
        main = soup.find('main') or soup.find('article')
        if main: subject_nodes.append(main)
        else:
            clone = BeautifulSoup(str(soup.body or soup), 'html.parser')
            for node in clone.select('nav,header,footer,script,style,noscript'): node.decompose()
            subject_nodes.append(clone)
        text = ' '.join(node.get_text(' ', strip=True) for node in subject_nodes if node)
        if len(text) < 160: continue
        cluster = cluster_for(text)
        labels = CLUSTERS[cluster]
        items = "".join(f'<li><a href="{href}" style="color:#0f82a6;font-weight:700">{label}</a></li>' for label, href in labels)
        block = (
            '<section class="seo-cluster-links" aria-label="مواضيع وخدمات ذات صلة" style="max-width:1000px;margin:36px auto;padding:22px;border:1px solid #dcecf2;border-radius:16px;background:#f7fcfe;line-height:1.9">'
            '<h2 style="font-size:22px;margin:0 0 10px;color:#082d4d">مواضيع وخدمات ذات صلة</h2>'
            '<p style="margin:0 0 10px;color:#5f7482">يمكنك الانتقال إلى الدليل أو الخدمة الأقرب لموضوع هذه الصفحة:</p>'
            f'<ul style="display:flex;flex-wrap:wrap;gap:8px 22px;margin:0;padding-right:22px">{items}</ul></section>'
        )
        raw = p.read_text('utf-8', errors='ignore')
        marker = re.search(r'</footer\s*>', raw, re.I)
        if marker:
            raw = raw[:marker.start()] + block + raw[marker.start():]
        else:
            marker = re.search(r'</body\s*>', raw, re.I)
            if not marker: continue
            raw = raw[:marker.start()] + block + raw[marker.start():]
        p.write_text(raw, encoding='utf-8')
        counts[cluster] += 1
    print('updated', sum(counts.values()), 'pages')
    print(dict(counts))

if __name__ == '__main__': main()
