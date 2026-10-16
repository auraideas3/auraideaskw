from pathlib import Path
from bs4 import BeautifulSoup
import json

ROOT=Path('.')
HOME=ROOT/'index.html'
LLMS=ROOT/'llms.txt'

# Strengthen the public entity graph without inventing unverified organizations or awards.
raw_html=HOME.read_text('utf-8')
soup=BeautifulSoup(raw_html, 'html.parser')
for script in soup.find_all('script', type='application/ld+json'):
    try: data=json.loads(script.string or '')
    except Exception: continue
    if not isinstance(data, dict) or data.get('@graph') is None: continue
    graph=data['@graph']
    for node in graph:
        if node.get('@type') == 'Organization':
            node['areaServed']=[{'@type':'Country','name':'الكويت'},{'@type':'Country','name':'الإمارات العربية المتحدة'}]
            node['availableLanguage']=['ar','en']
            node['knowsAbout']=['الأبحاث الجامعية','إعداد خطط البحث','رسائل الماجستير والدكتوراه','التحليل الإحصائي SPSS','تصميم الاستبيانات','التدقيق اللغوي الأكاديمي','تنسيق مراجع APA 7','العروض التقديمية الأكاديمية']
        if node.get('@type') == 'ProfessionalService':
            node['areaServed']=[{'@type':'Country','name':'الكويت'},{'@type':'Country','name':'الإمارات العربية المتحدة'}]
            node['availableLanguage']=['ar','en']
    old_script='<script type="application/ld+json">'+(script.string or '')+'</script>'
    new_script='<script type="application/ld+json">'+json.dumps(data, ensure_ascii=False, separators=(',',':'))+'</script>'
    raw_html=raw_html.replace(old_script,new_script,1)
    break
HOME.write_text(raw_html,encoding='utf-8')

content='''# أورا للأفكار | دعم أكاديمي وبحثي في الكويت والإمارات\n\n> أورا للأفكار منصة تقدم دعمًا أكاديميًا وبحثيًا منظمًا للطلاب والباحثين، مع التركيز على المراجعة والتحرير والتنظيم والإرشاد والتحليل، وبقاء مسؤولية الأصالة والالتزام بسياسات الجامعة على الباحث.\n\nهذا الملف يلخص هوية الموقع وخدماته وروابطه الأساسية لمحركات البحث وأدوات الإجابة التي تقرأ المحتوى العام. اللغة الأساسية عربية، وتوجد بعض العبارات الإنجليزية المساندة.\n\n## الهوية والموقع\n\n- [الصفحة الرئيسية](https://www.auraideaskw.com/): خدمات أكاديمية وبحثية للطلاب والباحثين.\n- [من نحن](https://www.auraideaskw.com/about/): تعريف بالمنصة.\n- [تواصل معنا](https://www.auraideaskw.com/contact/): قناة التواصل الرسمية.\n- [الضمانات](https://www.auraideaskw.com/guarantees/): نطاق الجودة والمراجعة.\n- نطاق الخدمة المعلن: الكويت والإمارات العربية المتحدة.\n\n## مراكز الخدمات والعناقيد\n\n- [الأبحاث الجامعية](https://www.auraideaskw.com/الأبحاث-الجامعية/): كتابة وتنظيم ومراجعة الأبحاث ومشاريع التخرج.\n- [الخطة البحثية](https://www.auraideaskw.com/الخطة-البحثية/): إعداد ومراجعة خطط ومقترحات البحث.\n- [رسائل الماجستير](https://www.auraideaskw.com/رسائل-الماجستير/): دعم مراجعة وتنظيم الرسائل والأطروحات.\n- [التحليل الإحصائي](https://www.auraideaskw.com/التحليل-الإحصائي/): تحليل البيانات والاستبيانات باستخدام SPSS.\n- [التدقيق والتنسيق](https://www.auraideaskw.com/التدقيق-والتنسيق/): التدقيق اللغوي والتنسيق الأكاديمي.\n- [العروض الأكاديمية](https://www.auraideaskw.com/العروض-الأكاديمية/): تصميم عروض المناقشة والمشاريع.\n- [الخدمات الأكاديمية](https://www.auraideaskw.com/خدماتنا/): دليل الخدمات العام.\n\n## صفحات الخدمة المتخصصة\n\n- [كتابة بحث جامعي](https://www.auraideaskw.com/كتابة-بحث-جامعي/): دعم تنظيم وكتابة ومراجعة البحث الجامعي.\n- [تحليل إحصائي SPSS](https://www.auraideaskw.com/تحليل-احصائي-spss/): تحليل الاستبيانات والبيانات وتفسير الجداول.\n- [إعداد خطة بحث](https://www.auraideaskw.com/اعداد-خطة-بحث/): تنظيم المشكلة والأهداف والمنهجية والخطة.\n- [مراجعة رسالة ماجستير](https://www.auraideaskw.com/مراجعة-رسالة-ماجستير/): مراجعة تنظيم الرسالة وملاحظات المشرف.\n- [تدقيق وتنسيق بحث](https://www.auraideaskw.com/تدقيق-وتنسيق-بحث/): تدقيق وتنسيق أكاديمي قبل التسليم.\n- [تصميم عرض مناقشة](https://www.auraideaskw.com/تصميم-عرض-مناقشة/): تنظيم عرض مناقشة أكاديمي.\n- [تنسيق مراجع APA 7](https://www.auraideaskw.com/تنسيق-مراجع-apa-7/): مراجعة التوثيق وقائمة المراجع.\n- [تصميم استبيان بحثي](https://www.auraideaskw.com/تصميم-استبيان-بحثي/): تنظيم محاور الاستبيان ومراجعته.\n\n## موضوعات البحث الطبيعية\n\n- كتابة الأبحاث الجامعية وأبحاث التخرج.\n- إعداد خطط ومقترحات الماجستير والدكتوراه.\n- مراجعة الإطار النظري والدراسات السابقة.\n- تصميم وتحكيم الاستبيانات وتحليل بياناتها.\n- التحليل الإحصائي باستخدام SPSS وتفسير النتائج.\n- التدقيق اللغوي والتنسيق وفق APA 7.\n- إعداد عروض PowerPoint للمناقشات والمشاريع.\n\n## أسئلة شائعة لمحركات الإجابة\n\n- كيف أرتب بحث تخرج أو بحثًا جامعيًا؟\n- كيف أعد خطة بحث ماجستير أو دكتوراه؟\n- أين أجد دعمًا لتحليل الاستبيان باستخدام SPSS؟\n- كيف أراجع الإطار النظري والدراسات السابقة؟\n- كيف أنسق المراجع وفق APA 7؟\n- كيف أجهز عرض مناقشة رسالة ماجستير؟\n\n## معلومات الاتصال\n\n- الموقع الرسمي: https://www.auraideaskw.com/\n- التواصل: https://wa.me/971588740073\n- اللغة الأساسية: العربية، مع دعم الإنجليزية.\n\n## ملفات الزحف\n\n- [Sitemap](https://www.auraideaskw.com/sitemap.xml)\n- [Robots](https://www.auraideaskw.com/robots.txt)\n'''
LLMS.write_text(content,encoding='utf-8')
print('entity_graph_updated')
print('llms_lines',len(content.splitlines()))
