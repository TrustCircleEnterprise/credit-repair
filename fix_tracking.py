with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

old = "alert('Letter queued! ID: '+data.id"
new = "alert('Letter sent via Certified Mail!\\n\\nLob ID: '+data.id+'\\nTracking: '+(data.tracking_number||'Available in 1-2 days at lob.com')"

print('Found:', old in c)
c = c.replace(old, new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')
