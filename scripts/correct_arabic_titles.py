from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

# Preserve href/src values so correcting visible language never changes existing URLs.
ATTR_RE = re.compile(r'\b(?:href|src|action)\s*=\s*(["\'])(.*?)\1', re.I | re.S)

def protect_urls(text: str):
    saved = []
    def repl(m):
        saved.append(m.group(0))
        return f'__PRESERVE_URL_{len(saved)-1}__'
    return ATTR_RE.sub(repl, text), saved

def restore_urls(text: str, saved):
    for i, value in enumerate(saved):
        text = text.replace(f'__PRESERVE_URL_{i}__', value)
    return text

# Exact corrections supported by the surrounding article context.
REPLACEMENTS = [
    ("الأمدينة الكويتات", "الدراسات السابقة"),
    ("أمدينة الكويتات", "الدراسات السابقة"),
    ("الأالكويتات الأكاديمية", "مراجعة الدراسات السابقة الأكاديمية"),
    ("الأالكويتية الأكاديمية", "مراجعة الدراسات السابقة الأكاديمية"),
    ("الأالكويتات", "الدراسات السابقة"),
    ("الأالكويتية", "الدراسات السابقة"),
    ("الكويتات", "الكويتية"),
    ("الابحاث", "الأبحاث"),
    ("الاحصائية", "الإحصائية"),
    ("اورا للافكار", "أورا للأفكار"),
    ("أورا للافكار", "أورا للأفكار"),
    ("Reseach writing in kuwait", "كتابة الأبحاث الجامعية في الكويت"),
    ("Ai tools", "أدوات الذكاء الاصطناعي"),
    ("AI tools", "أدوات الذكاء الاصطناعي"),
    ("Masterthesisi", "رسالة الماجستير"),
    ("masterthesisi", "رسالة الماجستير"),
    ("التعلم عن بعد في الالكويت", "التعلم عن بُعد في الإمارات"),
]

changed = []
for path in ROOT.rglob("*.html"):
    if ".git" in path.parts or "bing-webmaster-tools" in path.parts:
        continue
    original = path.read_text(encoding="utf-8", errors="replace")
    protected, saved = protect_urls(original)
    updated = protected
    for old, new in REPLACEMENTS:
        updated = updated.replace(old, new)
    updated = restore_urls(updated, saved)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        changed.append(path)

# The four known weak article pages receive exact, human-readable title/H1/OG wording.
page_titles = {
    Path("2025/12/21/ai-tools/index.html"): "أدوات الذكاء الاصطناعي للبحث العلمي | أورا للأفكار في الكويت",
    Path("2025/12/24/موقع-لعمل-الابحاث-الجامعية/index.html"): "موقع لعمل الأبحاث الجامعية | أورا للأفكار في الكويت",
    Path("2026/01/22/reseach-writing-in-kuwait/index.html"): "كتابة الأبحاث الجامعية في الكويت | أورا للأفكار في الكويت",
    Path("2026/03/01/التعلم-عن-بعد-في-الامارات/index.html"): "التعلم عن بُعد في الإمارات | أورا للأفكار في الكويت",
}
for rel, title in page_titles.items():
    path = ROOT / rel
    if not path.exists():
        continue
    s = path.read_text(encoding="utf-8", errors="replace")
    s = re.sub(r'<title[^>]*>.*?</title>', f'<title>{title}</title>', s, count=1, flags=re.I | re.S)
    s = re.sub(r'(<h1\b[^>]*>).*?(</h1>)', lambda m: m.group(1) + title.split(" | ")[0] + m.group(2), s, count=1, flags=re.I | re.S)
    s = re.sub(r'(<meta[^>]+property=["\']og:title["\'][^>]+content=["\']).*?(["\'])', lambda m: m.group(1) + title + m.group(2), s, count=1, flags=re.I | re.S)
    path.write_text(s, encoding="utf-8")
    if path not in changed:
        changed.append(path)

print("Corrected HTML files:", len(changed))
for p in changed[:20]:
    print(p.relative_to(ROOT))
if len(changed) > 20:
    print("...")
