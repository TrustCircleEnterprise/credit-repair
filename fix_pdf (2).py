with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('NO_NEGATIVES_FOUND')
print("Found at:", idx)
chunk = c[idx-20:idx+50]
print("Context:", repr(chunk))

# Add the comma fix instruction right after NO_NEGATIVES_FOUND
old = c[idx:idx+len('NO_NEGATIVES_FOUND')]
new = 'NO_NEGATIVES_FOUND. IMPORTANT: Never use commas inside field values. Remove commas from dollar amounts (write $12456 not $12,456)'

c = c.replace(c[idx-20:idx+18], c[idx-20:idx] + new, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("Done!")
