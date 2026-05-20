with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find the exact draft letter button code
idx = c.find('Draft letter</button>')
print("Found at:", idx)
print("Context:", repr(c[idx-200:idx+30]))
