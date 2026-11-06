"""Блокирует публикацию, если в content/ есть название препарата или обещание результата.
Списки взяты из прототипа VP Aesthetics (docs/tools/design/prototype_content.py) и ждут проверки юристом."""
import pathlib, re, sys

DRUG_TERMS = ['Botox', 'botulin', 'Vistabel', 'Azzalure', 'Bocouture', 'Dysport', 'Xeomin',
              'ботокс', 'ботулин', 'ботулотоксин', 'вистабел', 'азалюр', 'аззалюр', 'бокутюр', 'бокотюр', 'бокутур', 'диспорт', 'ксеомин']
PROMISE_TERMS = ['100% гарантия', 'гарантированно', 'навсегда', 'garantiert', '100 % sicher', 'permanent', 'guaranteed']
WORDS = re.compile('|'.join(re.escape(t) for t in DRUG_TERMS + PROMISE_TERMS), re.I)

found = []
for p in sorted(pathlib.Path('content').rglob('*')):
    if p.is_file():
        for n, line in enumerate(p.read_text(encoding='utf-8').splitlines(), 1):
            for m in WORDS.finditer(line):
                found.append(f'{p}:{n}: «{m.group(0)}»')
if found:
    print('Публикация остановлена: найдены запрещённые слова')
    print('\n'.join(found))
    sys.exit(1)
print('Проверка слов: ок')
