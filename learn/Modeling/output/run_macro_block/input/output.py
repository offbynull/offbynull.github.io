from textwrap import dedent
import re
from sys import stdin

text = ''.join(stdin.readlines())
m = re.search('# MARKDOWN\s*\n([\s\S]+)\n\s*# MARKDOWN\s*[\n$]', text)
if m:
    text = m.group(1)
text = dedent(text)
text = text.strip()
ret = '\n'
ret += '```python\n'
ret += text + '\n'
ret += '```\n\n'
print(ret)