with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find the address button and fix its onclick
import re
# Replace any showSection that comes before Address Removal text
c = re.sub(
    r"showSection\('resources'\)(\"><svg[^>]+>(?:<[^>]+>)*</svg>Address Removal)",
    r"showSection('address')\1",
    c
)

print("showSection address:", "showSection('address')" in c)
print("showSection closed:", "showSection('closed')" in c)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("Done!")
