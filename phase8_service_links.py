from pathlib import Path
from bs4 import BeautifulSoup
from html import escape
import re

LANDINGS={
 'stats':[('صفحة خدمة تحليل إحصائي SPSS','/تحليل-احصائي-spss/'),('صفحة تصميم استبيان بحثي','/تصميم-استبيان-بحثي/')],
 'method':[('صفحة إعداد خطة بحث ماجستير ودكتوراه','/اعداد-خطة-بحث/'),('صفحة كتابة بحث جامعي','/كتابة-بحث-جامعي/')],
 'thesis':[('صفحة مراجعة رسالة ماجستير ودكتوراه','/مراجعة-رسالة-ماجستير/'),('صفحة تصميم عرض مناقشة','/تصميم-عرض-مناقشة/')],
 'editing':[('صفحة تدقيق وتنسيق بحث','/تدقيق-وتنسيق-بحث/'),('صفحة تنسيق مراجع APA 7','/تنسيق-مراجع-apa-7/')],
 'presentation':[('صفحة تصميم عرض مناقشة','/تصميم-عرض-مناقشة/')],
 'research':[('صفحة كتابة بحث جامعي','/كتابة-بحث-جامعي/')],
}

def classify(text):
 t=text.lower()
 if any(k in t for k in ['spss','استبان','تحليل إحصائي','التحليل الإحصائي']): return 'stats'
 if any(k in t for k in ['خطة بحث','الخطة البحثية','منهجية','الإطار النظري','الدراسات السابقة']): return 'method'
 if any(k in t for k in ['ماجستير','دكتوراه','رسالة','أطروحة']): return 'thesis'
 if any(k in t for k in ['تدقيق','تنسيق','apa','توثيق','مراجع','اقتباس']): return 'editing'
 if any(k in t for k in ['بوربوينت','عرض تقديمي','مناقشة']): return 'presentation'
 return 'research'

def main():
 changed=0; links=0
 for p in Path('.').rglob('index.html'):
  raw=p.read_text('utf-8',errors='ignore')
  if 'seo-cluster-links' not in raw or 'service-cluster-link' in raw: continue
  soup=BeautifulSoup(raw,'html.parser')
  title=soup.title.get_text(' ',strip=True) if soup.title else ''
  h1=soup.find('h1').get_text(' ',strip=True) if soup.find('h1') else ''
  main=soup.find('main') or soup.find('article')
  text=' '.join(x.get_text(' ',strip=True) for x in [soup.title,soup.find('h1'),main] if x)
  choices=LANDINGS[classify(text)]
  section=re.search(r'<section class="seo-cluster-links".*?</section>',raw,re.S)
  if not section: continue
  block=section.group(0)
  extra=''.join(f'<li class="service-cluster-link"><a href="{href}" style="color:#0f82a6;font-weight:800">{escape(label)}</a></li>' for label,href in choices)
  if '</ul>' not in block: continue
  newblock=block.replace('</ul>',extra+'</ul>',1)
  raw=raw[:section.start()]+newblock+raw[section.end():]
  p.write_text(raw,encoding='utf-8'); changed+=1; links+=len(choices)
 print('pages_updated',changed,'commercial_links_added',links)

if __name__=='__main__': main()
