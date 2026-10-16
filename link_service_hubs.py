from pathlib import Path
import re, html

ALL=[
 ('كتابة بحث جامعي منظم','/كتابة-بحث-جامعي/'),('تحليل إحصائي SPSS','/تحليل-احصائي-spss/'),('إعداد خطة بحث','/اعداد-خطة-بحث/'),('مراجعة رسالة ماجستير','/مراجعة-رسالة-ماجستير/'),('تدقيق وتنسيق بحث','/تدقيق-وتنسيق-بحث/'),('تصميم عرض مناقشة','/تصميم-عرض-مناقشة/'),('تنسيق مراجع APA 7','/تنسيق-مراجع-apa-7/'),('تصميم استبيان بحثي','/تصميم-استبيان-بحثي/')]
MAP={
 'الأبحاث-الجامعية':ALL[:1]+[ALL[7],ALL[2]],
 'التحليل-الإحصائي':[ALL[1],ALL[7]],
 'الخطة-البحثية':[ALL[2],ALL[0],ALL[3]],
 'رسائل-الماجستير':[ALL[3],ALL[5],ALL[6]],
 'التدقيق-والتنسيق':[ALL[4],ALL[6],ALL[0]],
 'العروض-الأكاديمية':[ALL[5],ALL[3]],
 'خدمات-الدعم-الأكاديمي':ALL,
 'services':ALL,
}

def main():
 n=0
 for hub,links in MAP.items():
  p=Path(hub)/'index.html';
  if not p.exists(): continue
  raw=p.read_text('utf-8',errors='ignore')
  if 'service-cluster-hubs' in raw: continue
  items=''.join(f'<a href="{href}" style="display:block;padding:14px 16px;border:1px solid #d9e9e8;border-radius:12px;color:#138ca1;font-weight:800;background:#fff">{html.escape(label)}</a>' for label,href in links)
  block=('<section class="service-cluster-hubs" aria-label="صفحات الخدمات المتخصصة" style="padding:48px 20px;background:#f6fbfb">'
         '<div style="max-width:1050px;margin:auto"><h2 style="text-align:center;color:#082d4d">صفحات خدمات متخصصة</h2>'
         '<p style="text-align:center;color:#607684;max-width:760px;margin:0 auto 24px">اختر الصفحة الأقرب إلى احتياجك للحصول على شرح تفصيلي وخطوات واضحة قبل التواصل.</p>'
         f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px">{items}</div></div></section>')
  marker=re.search(r'</main\s*>',raw,re.I)
  if not marker: continue
  raw=raw[:marker.start()]+block+raw[marker.start():]
  p.write_text(raw,encoding='utf-8'); n+=1
 print('hubs_linked',n)
if __name__=='__main__': main()
