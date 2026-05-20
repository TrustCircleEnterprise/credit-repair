with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

old = 'credit report analyst. Extract ALL negative accounts from this credit report. For each, output one line: Creditor Name, #AccountNumber, $Balance, Status\\n\\nOnly output these lines, nothing else. If no negatives found, output: NO_NEGATIVES_FOUND'

new = 'credit report data extractor. Output ONLY negative accounts in this exact format, one per line:\\nCreditor Name, #AccountNumber, $Balance, Status\\n\\nNegative accounts include: collections, charge-offs, late payments, repossessions, judgments, bankruptcies.\\nUse exact creditor name. Use account number shown or #Unknown. Use balance shown or $0.\\nStatus must be one of: Collections, Charged Off, Late Payment, Repossession, Bankruptcy, Judgment.\\nDo NOT include any explanations, headers, notes, summaries, or commentary.\\nOutput ONLY the data lines. If no negatives exist output: NO_NEGATIVES_FOUND'

print('Found:', old in c)
c = c.replace(old, new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')
