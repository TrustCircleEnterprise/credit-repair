with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

old = 'credit report analyst. Extract ALL negative accounts from this credit report. For each, output one line: Creditor Name, #AccountNumber, $Balance, Status\\n\\nOnly output these lines, nothing else. If no negatives found, output: NO_NEGATIVES_FOUND'

new = 'credit report data extractor. Extract ALL negative accounts and output ONLY in this exact CSV format, one per line:\\nCreditor Name, #AccountNumber, $Balance, Status\\n\\nCritical rules:\\n1. Negative accounts = collections, charge-offs, late payments, repossessions, judgments, bankruptcies\\n2. NEVER use commas inside any field value - remove commas from dollar amounts ($12456 not $12,456)\\n3. Output ONLY the data lines - no explanations, headers, notes or summaries\\n4. If no negatives found output exactly: NO_NEGATIVES_FOUND'

print('Found:', old in c)
c = c.replace(old, new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')
