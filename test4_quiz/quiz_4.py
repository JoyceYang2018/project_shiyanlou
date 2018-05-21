import re

text = open('character.txt').read()
ans = "".join(re.findall('[^A-Z][A-Z]{3}([a-z])[A-Z]{3}[^A-Z]',text))
print(ans)