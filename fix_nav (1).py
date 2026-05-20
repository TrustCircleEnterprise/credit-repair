with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix 1: Add nav links
idx = c.find('Resources & Laws')
chunk = c[idx-300:idx+60]
print("Nav context:", repr(chunk[-100:]))

# Find the button tag before Resources & Laws and insert new buttons before it
# Look for the last <button before Resources & Laws
last_btn = c.rfind('<button class="nav-link"', 0, idx)
end_of_btn = c.find('</button>', last_btn) + len('</button>')
print("Inserting after:", repr(c[last_btn:end_of_btn]))

new_buttons = """
    <button class="nav-link" onclick="showSection('address')">
      <svg class="icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M8 2a3 3 0 100 6 3 3 0 000-6z"/><path d="M8 8C5.8 8 4 10 4 12h8c0-2-1.8-4-4-4z"/></svg>Address Removal
    </button>
    <button class="nav-link" onclick="showSection('closed')">
      <svg class="icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="2" width="12" height="12" rx="2"/><path d="M5 8h6"/></svg>Closed Accounts
    </button>"""

c = c[:end_of_btn] + new_buttons + c[end_of_btn:]

# Fix 2: Fix draft letter button - add showSection to prefill calls
import re
c = re.sub(
    r"(onclick=\"prefill\([^\"]+\))\"",
    r'\1;showSection(\'letters\')"',
    c
)

print("Address in nav:", "showSection('address')" in c)
print("Closed in nav:", "showSection('closed')" in c)
print("Draft letter fixed:", c.count("showSection('letters')"))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("Done!")
