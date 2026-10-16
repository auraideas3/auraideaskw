from pathlib import Path
from bs4 import BeautifulSoup
from html import escape
import json, re

BASE='https://www.auraideaskw.com'
HUBS={
 'stats':('التحليل الإحصائي','/التحليل-الإحصائي/'),
 'method':('الخطة البحثية','/الخطة-البحثية/'),
 'thesis':('رسائل الماجستير والدكتوراه','/رسائل-الماجستير/'),
 'editing':('التدقيق والتنسيق','/التدقيق-والتنسيق/'),
 'presentation':('العروض الأكاديمية','/العروض-الأكاديمية/'),
 'research':('الأبحاث الجامعية','/الأبحاث-الجامعية/'),
}

def subject(text):
 t=text.lower()
 if any(k in t for k in ['spss','استبان','تحليل إحصائي','التحليل الإحصائي']): return 'stats'
 if any(k in t for k in ['خطة بحث','الخطة البحثية','منهجية','الإطار النظري','الدراسات السابقة']): return 'method'
 if any(k in t for k in ['ماجستير','دكتوراه','رسالة','أطروحة']): return 'thesis'
 if any(k in t for k in ['تدقيق','تنسيق','apa','توثيق','مراجع','اقتباس']): return 'editing'
 if any(k in t for k in ['بوربوينت','عرض تقديمي','مناقشة']): return 'presentation'
 return 'research'

def canonical(soup):
 x=soup.find('link', rel=lambda v:v and 'canonical' in v)
 return x.get('href') if x else None

def main():
 changed=0
 for p in Path('.').rglob('index.html'):
  rel=p.relative_to('.')
  raw=p.read_text('utf-8',errors='ignore')
  soup=BeautifulSoup(raw,'html.parser')
  if not soup.find('h1') or not soup.title or soup.select_one('.seo-breadcrumbs'): continue
  robots=soup.find('meta',attrs={'name':'robots'})
  if robots and 'noindex' in robots.get('content','').lower(): continue
  url=canonical(soup)
  h1=soup.find('h1').get_text(' ',strip=True)
  if not url or not h1: continue
  hub_label,hub_href=HUBS[subject(soup.title.get_text(' ',strip=True)+' '+h1)]
  visible=(f'<nav class="seo-breadcrumbs" aria-label="مسار التنقل" style="max-width:1000px;margin:18px auto;padding:0 20px;color:#607684;font-size:14px">'
           f'<a href="/" style="color:#0f82a6">الرئيسية</a><span aria-hidden="true"> › </span>'
           f'<a href="{hub_href}" style="color:#0f82a6">{escape(hub_label)}</a><span aria-hidden="true"> › </span>'
           f'<span aria-current="page">{escape(h1[:140])}</span></nav>')
  item=[{'@type':'ListItem','position':1,'name':'الرئيسية','item':BASE+'/'}]
  if hub_href != '/': item.append({'@type':'ListItem','position':2,'name':hub_label,'item':BASE+hub_href})
  item.append({'@type':'ListItem','position':len(item)+1,'name':h1[:140],'item':url})
  schema={'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':item}
  schema_tag='<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False,separators=(',',':'))+'</script>'
  raw2=re.sub(r'</head\s*>',schema_tag+'</head>',raw,count=1,flags=re.I) if 'BreadcrumbList' not in raw else raw
  marker=re.search(r'<section\b[^>]*class=["\'][^"\']*seo-cluster-links',raw2,re.I)
  if marker: raw2=raw2[:marker.start()]+visible+raw2[marker.start():]
  else:
   marker=re.search(r'</footer\s*>',raw2,re.I) or re.search(r'</body\s*>',raw2,re.I)
   if not marker: continue
   raw2=raw2[:marker.start()]+visible+raw2[marker.start():]
  p.write_text(raw2,encoding='utf-8'); changed+=1
 print('breadcrumbs_added',changed)

if __name__=='__main__': main()
