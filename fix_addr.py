with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find the exact position of Address Removal and work backwards to fix the onclick
idx = c.find('Address Removal')
# Get the chunk before it
chunk = c[idx-300:idx]
print("Before Address Removal:")
print(repr(chunk[-100:]))

# Replace the last showSection('resources') before Address Removal with showSection('address')
last_resources = chunk.rfind("showSection('resources')")
if last_resources >= 0:
    abs_pos = (idx-300) + last_resources
    c = c[:abs_pos] + "showSection('address')" + c[abs_pos+len("showSection('resources')"):]
    print("Fixed!")
else:
    print("Pattern not found")

print("showSection address count:", c.count("showSection('address')"))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)
