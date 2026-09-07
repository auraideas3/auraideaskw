from pathlib import Path
from urllib.parse import unquote, urlparse
from bs4 import BeautifulSoup
import html, re
ROOT=Path('/home/ubuntu/auraideaskw-fix')

def long_content(title):
    topic=title.strip() or 'البحث الأكاديمي'
    sections=['مقدمة حول الموضوع','تحديد المفاهيم الأساسية','اختيار السؤال المناسب','إعداد خطة العمل','جمع المصادر','تنظيم الأفكار','الكتابة الأكاديمية','التوثيق العلمي','التحليل والمناقشة','المراجعة والتدقيق','أخطاء شائعة','تطبيق عملي','أسئلة شائعة','توصيات نهائية','الخلاصة']
    def para(section):
        return '<p>'+('</p><p>'.join([f'يتناول هذا المحور موضوع «{topic}» من زاوية عملية تساعد الطلاب والباحثين في الكويت على تحويل الفكرة إلى عمل أكاديمي واضح. يبدأ ذلك بفهم السؤال وتحديد حدود الموضوع، ثم ترتيب المعلومات في مسار منطقي يسهّل المراجعة والتطوير.',f'في مرحلة {section}، لا يكفي جمع معلومات كثيرة؛ المطلوب هو اختيار ما يخدم الهدف وربطه بمصدر موثوق وشرحه بلغة عربية سليمة. ويساعد هذا الأسلوب على تجنب التكرار والانتقال المفاجئ بين الأفكار، كما يجعل النص أكثر وضوحًا للقارئ والمشرف.',f'ينبغي كذلك مراعاة تعليمات الجامعة أو القسم، مثل نمط التوثيق، حجم العمل، طريقة عرض الجداول، وعدد المراجع. ومن المفيد إعداد قائمة تحقق قصيرة بعد كل مرحلة، وتسجيل الملاحظات أولًا بأول بدل تأجيلها إلى يوم التسليم.',f'عند تطبيق هذه الخطوات على {topic}، يمكن تقسيم العمل إلى مهام صغيرة: قراءة، وتلخيص، وتصنيف، وكتابة، ثم مراجعة مستقلة. لا تعني السرعة حذف المراحل، بل تعني إدارة الوقت بحيث تبقى لكل مرحلة مساحة كافية وتقل التعديلات المتأخرة.',f'النتيجة الجيدة تجمع بين الدقة والوضوح. لذلك يجب أن يكون لكل فقرة سبب لوجودها، وأن ترتبط النتيجة بالسؤال، وأن يظهر الفرق بين الرأي الشخصي والدليل الذي تدعمه المصادر. بهذه الطريقة يصبح المقال أو البحث قابلًا للفهم والاستفادة والتقييم.']))+'</p>'
    out=[f'<div class="aura-expanded-article" dir="rtl"><p class="aura-article-lead">دليل أكاديمي مطوّل حول <strong>{html.escape(topic)}</strong>، موجّه للطلاب والباحثين في الكويت، ويجمع بين الشرح النظري والخطوات العملية والصياغة الواضحة.</p><figure class="aura-article-image"><img src="/0.webp" alt="العمل الأكاديمي والبحث العلمي" loading="lazy"><figcaption>تنظيم الفكرة والمصادر يساعد على بناء عمل أكاديمي متماسك.</figcaption></figure>']
    for i,section in enumerate(sections):
        out.append(f'<section class="aura-article-section"><h2>{section}</h2>{para(section)}</section>')
        if i in (4,9): out.append(f'<figure class="aura-article-image"><img src="/{"1.webp" if i==4 else "2.webp"}" alt="تنظيم ومراجعة البحث" loading="lazy"><figcaption>خطوة {section} ضمن خطة العمل.</figcaption></figure>')
    out.append('<section class="aura-article-faq"><h2>أسئلة شائعة</h2>'+''.join(f'<h3>{q}</h3><p>{a} ويستحسن تسجيل هذه الخطوة ضمن الخطة ومراجعتها قبل اعتماد النسخة النهائية.</p>' for q,a in [('كيف أبدأ؟','اقرأ المتطلبات، صغ سؤالًا واضحًا، ثم اكتب مخططًا مختصرًا.'),('كيف أختار المصادر؟','اختر مصادر متخصصة وموثوقة واحتفظ ببياناتها كاملة.'),('كيف أراجع العنوان؟','اجعله مكتملًا ومحددًا ويعكس محتوى العمل بدقة.'),('كيف أتجنب الأخطاء؟','استخدم قائمة تحقق تشمل اللغة والتوثيق والروابط والجداول.')])+'</section><section class="aura-article-conclusion"><h2>الخلاصة</h2>'+para('الخلاصة والتوصيات')+'</section></div>')
    return ''.join(out)
style='<style id="aura-expanded-article-style">.aura-expanded-article{max-width:920px;margin:0 auto;padding:10px 18px 60px;color:#233b50;line-height:2.05;font-size:18px}.aura-expanded-article h2{color:#0b5570;margin:42px 0 16px;font-size:clamp(1.45rem,2.5vw,2.1rem);border-right:5px solid #e9b92d;padding-right:12px}.aura-expanded-article h3{color:#0b5570;margin:24px 0 8px}.aura-article-lead{font-size:21px;background:#f1f7fa;border-radius:16px;padding:22px}.aura-article-image{text-align:center;margin:28px auto}.aura-article-image img{width:100%;max-width:820px;max-height:420px;object-fit:cover;border-radius:16px}.aura-article-image figcaption{font-size:13px;color:#607586}.aura-article-faq{background:#f8fbfc;padding:10px 22px 25px;border-radius:16px}@media(max-width:700px){.aura-expanded-article{font-size:16px}.aura-article-lead{font-size:18px}}</style>'
# Match links from both blog indexes to canonical or direct local path.
links=set()
for f in ['blog/index.html','مقالات-خدمات-طلابية/blog-auraideas/index.html']:
 s=BeautifulSoup((ROOT/f).read_text(errors='ignore'),'html.parser')
 links |= {a.get('href') for a in s.select('a[href]') if a.get('href','').startswith('/') and a.get('href') not in ['/','/blog/']}
canonical={}
for p in ROOT.rglob('index.html'):
 try:s=BeautifulSoup(p.read_text(errors='ignore'),'html.parser')
 except:continue
 for t in s.select('link[rel="canonical"],meta[property="og:url"]'):
  v=t.get('href') or t.get('content') or ''
  canonical[urlparse(v).path.rstrip('/') or '/']=p
count=0
for link in links:
 path=unquote(urlparse(link).path).rstrip('/') or '/'
 p=canonical.get(path)
 if not p and path != '/':
  q=ROOT/path.lstrip('/')/'index.html'
  if q.exists():p=q
 if not p:continue
 try:s=BeautifulSoup(p.read_text(errors='ignore'),'html.parser')
 except:continue
 if s.select_one('.aura-expanded-article'):continue
 h=s.find(['h1','h2'])
 target=s.select_one('.entry-content,.elementor-widget-theme-post-content,article') or s.body
 if not h or target is None:continue
 target.append(BeautifulSoup(long_content(h.get_text(' ',strip=True)),'html.parser'))
 if s.head:s.head.append(BeautifulSoup(style,'html.parser'))
 p.write_text(str(s),encoding='utf-8');count+=1
# Correct clearly truncated card titles in both blog indexes.
fixes={'دكتوراه الفلسفة في الذكاء الاصطناعي ج':'دكتوراه الفلسفة في الذكاء الاصطناعي: التخصصات والفرص','كيفية عمل بحث تخرج وكتابة بحث متميز بخط':'كيفية عمل بحث تخرج وكتابة بحث متميز بخطوات واضحة','رسالة الماجستير و الدكتوراه':'رسائل الماجستير والدكتوراه','ابحاث جامعية':'أبحاث جامعية'}
for f in ['blog/index.html','مقالات-خدمات-طلابية/blog-auraideas/index.html']:
 p=ROOT/f; s=BeautifulSoup(p.read_text(errors='ignore'),'html.parser')
 for node in s.find_all(['h2','p','span']):
  if node.string and node.string.strip() in fixes:node.string=fixes[node.string.strip()]
 p.write_text(str(s),encoding='utf-8')
print('extra article pages updated:',count)
