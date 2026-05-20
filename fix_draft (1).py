with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

old = """a.disputeType+'\\\\')\\"";showSection(\\\\'letters\\\\');">Draft letter"""
new = """a.disputeType+'\\\\');showSection(\\\\'letters\\\\');">Draft letter"""

print("Try 1:", old in c)

# Try the actual raw string
old2 = '''a.disputeType+\'\\\\\')";showSection(\\\\'letters\\\\');">Draft letter'''
print("Try 2:", old2 in c)

# Direct character inspection
idx = c.find('Draft letter</button>')
chunk = c[idx-80:idx+20]
print("Raw chunk:", repr(chunk))

# Replace based on what we see
old3 = '\')";showSection(\\\\'
new3 = "');showSection(\\\\'"
if old3 in c:
    c = c.replace(old3, new3, 1)
    print("Fixed with try 3!")
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(c)
else:
    print("Try 3 also failed")
    # Show exact bytes
    for i, ch in enumerate(chunk):
        print(i, repr(ch))
