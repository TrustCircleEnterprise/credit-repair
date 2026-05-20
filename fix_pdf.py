with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find the current PDF prompt
idx = c.find('credit report analyst')
if idx > 0:
    print("Found at:", idx)
    print("Current prompt:", repr(c[idx:idx+300]))
else:
    print("Not found - searching for alternatives")
    idx = c.find('negative accounts')
    print("Found 'negative accounts' at:", idx)
    print(repr(c[idx-50:idx+300]))
