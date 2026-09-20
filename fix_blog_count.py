from pathlib import Path
from bs4 import BeautifulSoup
p = Path(__file__).resolve().parent / 'المدونة/index.html'
s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
count = len(s.select('#posts article'))
for node in s.select('.count'):
    node.string = f'{count} مقالًا ودليلًا'
for node in s.find_all(string=lambda text: text and ('229+' in text or '230+' in text or '239+' in text)):
    node.replace_with(node.replace('229+', f'{count}+').replace('230+', f'{count}+').replace('239+', f'{count}+'))
p.write_text(str(s), encoding='utf-8')
print('blog cards:', count)
