# ScoreBoss Final Builder
# Reads the clean base and adds ALL features in one shot

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

print("Base loaded. Size:", len(c))

# ═══════════════════════════════════════
# 1. UPDATE NAV - Add all new sections
# ═══════════════════════════════════════
old_nav_end = """    <button class="nav-link" onclick="showSection('resources')">
      <svg class="icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M8 2a6 6 0 100 12A6 6 0 008 2z"/><path d="M8 7v4M8 5.5v.5"/></svg>Resources &amp; Laws
    </button>"""

new_nav_end = """    <button class="nav-link" onclick="showSection('pfd')">
      <svg class="icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="8" cy="8" r="6"/><path d="M6 8h4M8 6v4"/></svg>Pay-for-Delete
    </button>
    <button class="nav-link" onclick="showSection('address')">
      <svg class="icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M8 2a3 3 0 100 6 3 3 0 000-6z"/><path d="M8 2C5.8 2 4 4 4 6c0 3 4 8 4 8s4-5 4-8c0-2-1.8-4-4-4z"/></svg>Address Removal
    </button>
    <button class="nav-link" onclick="showSection('closed')">
      <svg class="icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="2" width="12" height="12" rx="2"/><path d="M5 8h6"/></svg>Closed Accounts
    </button>
    <button class="nav-link" onclick="showSection('resources')">
      <svg class="icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M8 2a6 6 0 100 12A6 6 0 008 2z"/><path d="M8 7v4M8 5.5v.5"/></svg>Resources &amp; Laws
    </button>"""

if old_nav_end in c:
    c = c.replace(old_nav_end, new_nav_end)
    print("Nav updated OK")
else:
    print("Nav NOT found")

# ═══════════════════════════════════════
# 2. UPDATE showSection MAP
# ═══════════════════════════════════════
c = c.replace(
    "['analyze','disputes','letters','rebuild','tracker','clients','simulator','resources']",
    "['analyze','disputes','letters','rebuild','tracker','clients','simulator','pfd','address','closed','resources']"
)
print("Map updated")

# ═══════════════════════════════════════
# 3. ADD ALL NEW SECTIONS before resources
# ═══════════════════════════════════════
new_sections = '''
<!-- PAY FOR DELETE -->
<div id="sec-pfd" class="section fade-up">
  <div class="page-header"><div class="page-title">Pay-for-Delete Scripts</div><div class="page-sub">Negotiate collection removal in exchange for payment</div></div>
  <div class="tip-box"><strong>How it works:</strong> You offer to pay a collection ONLY if the collector agrees in writing to DELETE it from all 3 bureaus. Never pay without a written agreement first!</div>
  <div class="warn-box"><strong>Warning:</strong> Never pay a collection without a signed pay-for-delete agreement. Paying without this can restart reporting without removing the negative mark.</div>
  <div class="g2" style="margin-bottom:1rem">
    <div class="card">
      <div class="card-title">Strategy guide</div>
      <div class="factor-row"><div class="factor-info"><div class="factor-name">Step 1 - Check the debt</div><div class="factor-sub">Verify it is within the statute of limitations and amount is accurate before offering anything.</div></div><span class="badge badge-blue">First</span></div>
      <div class="factor-row"><div class="factor-info"><div class="factor-name">Step 2 - Start low</div><div class="factor-sub">Offer 25-40% of balance first. Collectors often accept 50-60% for older debts.</div></div><span class="badge badge-amber">Negotiate</span></div>
      <div class="factor-row"><div class="factor-info"><div class="factor-name">Step 3 - Get it in writing</div><div class="factor-sub">Do NOT pay until you have a signed agreement that says DELETE from all 3 bureaus.</div></div><span class="badge badge-red">Critical</span></div>
      <div class="factor-row"><div class="factor-info"><div class="factor-name">Step 4 - Pay as agreed</div><div class="factor-sub">Pay via certified check or money order. Keep copies of everything.</div></div><span class="badge badge-green">Final step</span></div>
      <div class="factor-row"><div class="factor-info"><div class="factor-name">Step 5 - Verify deletion</div><div class="factor-sub">Pull your credit reports 30-45 days after payment to confirm deletion from all 3 bureaus.</div></div><span class="badge badge-green">Confirm</span></div>
    </div>
    <div class="card">
      <div class="card-title">Generate your script</div>
      <label>Collection agency name</label><input type="text" id="pfd-creditor" placeholder="LVNV Funding, Midland Credit, etc."/>
      <label>Account number</label><input type="text" id="pfd-acct" placeholder="****8834"/>
      <label>Current balance owed</label><input type="text" id="pfd-balance" placeholder="$750"/>
      <label>Your offer amount</label><input type="text" id="pfd-offer" placeholder="$300"/>
      <label>Script type</label>
      <select id="pfd-type">
        <option value="letter">Written pay-for-delete letter</option>
        <option value="phone">Phone call script</option>
        <option value="agreement">Pay-for-delete agreement template</option>
        <option value="followup">Follow-up if they refuse</option>
      </select>
      <button class="btn btn-primary" onclick="generatePFD()">Generate Script</button>
    </div>
  </div>
  <div class="card" id="pfd-card" style="display:none">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem;flex-wrap:wrap;gap:8px">
      <div class="card-title" style="margin-bottom:0" id="pfd-title">Pay-for-Delete Script</div>
      <div style="display:flex;gap:8px">
        <button class="btn btn-sm" onclick="copyEl('pfd-body',this)">Copy</button>
        <button class="btn btn-sm btn-green" onclick="printEl('pfd-body','ScoreBoss Pay-for-Delete')">Print / PDF</button>
      </div>
    </div>
    <div id="pfd-body" class="letter-output"></div>
  </div>
  <div class="card" style="margin-top:1rem">
    <div class="card-title">Tips by debt size</div>
    <div class="g2">
      <div><div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:6px">Under $500</div><div style="font-size:13px;color:var(--text2);line-height:1.7">Offer 25-30%. Many small collectors accept because pursuing payment costs more than settling.</div></div>
      <div><div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:6px">$500 - $2,000</div><div style="font-size:13px;color:var(--text2);line-height:1.7">Offer 40-50%. If they refuse PFD, dispute the debt first. If unverifiable, gets deleted free.</div></div>
      <div><div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:6px">Over $2,000</div><div style="font-size:13px;color:var(--text2);line-height:1.7">Offer 30-40%. Debts bought for pennies on the dollar so collectors have huge room to negotiate.</div></div>
      <div><div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:6px">Original creditors</div><div style="font-size:13px;color:var(--text2);line-height:1.7">Harder to get PFD. Try goodwill letters instead. Some will do PFD if you ask nicely.</div></div>
    </div>
  </div>
</div>

<!-- ADDRESS REMOVAL -->
<div id="sec-address" class="section fade-up">
  <div class="page-header"><div class="page-title">Address Removal</div><div class="page-sub">Remove old and inaccurate addresses from your credit report</div></div>
  <div class="tip-box"><strong>Why this matters:</strong> Old addresses can be used by debt collectors to locate you and may indicate identity theft or a mixed credit file. You have the right to remove inaccurate addresses.</div>
  <div class="g2" style="margin-bottom:1rem">
    <div class="card">
      <div class="card-title">Why remove old addresses</div>
      <div class="factor-row"><div class="factor-info"><div class="factor-name">Identity theft protection</div><div class="factor-sub">Old addresses can be used by fraudsters to open accounts in your name.</div></div><span class="badge badge-red">Security risk</span></div>
      <div class="factor-row"><div class="factor-info"><div class="factor-name">Mixed credit file fix</div><div class="factor-sub">Wrong addresses may mean your file is mixed with someone else with a similar name.</div></div><span class="badge badge-amber">Common issue</span></div>
      <div class="factor-row"><div class="factor-info"><div class="factor-name">Debt collector access</div><div class="factor-sub">Collectors use addresses to locate you. Remove old ones to limit access.</div></div><span class="badge badge-amber">Privacy</span></div>
      <div class="factor-row"><div class="factor-info"><div class="factor-name">Clean credit file</div><div class="factor-sub">A clean accurate file with only current info looks better to lenders.</div></div><span class="badge badge-green">Best practice</span></div>
    </div>
    <div class="card">
      <div class="card-title">Generate address removal letter</div>
      <label>Address to remove</label><input type="text" id="addr-remove" placeholder="123 Old St, Atlanta, GA 30301"/>
      <label>Reason for removal</label>
      <select id="addr-reason">
        <option value="never">Never lived at this address</option>
        <option value="old">No longer current address</option>
        <option value="fraud">Fraudulent - possible identity theft</option>
        <option value="mixed">Belongs to someone else - mixed file</option>
        <option value="inaccurate">Address information is inaccurate</option>
      </select>
      <label>Send to bureau(s)</label>
      <select id="addr-bureau">
        <option>All three bureaus (separate letters)</option>
        <option>Equifax</option>
        <option>Experian</option>
        <option>TransUnion</option>
      </select>
      <label>Current correct address</label><input type="text" id="addr-current" placeholder="5000 Macland Rd, Powder Springs, GA 30127"/>
      <button class="btn btn-primary" onclick="generateAddrLetter()">Generate Address Removal Letter</button>
    </div>
  </div>
  <div class="card" id="addr-card" style="display:none">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem;flex-wrap:wrap;gap:8px">
      <div class="card-title" style="margin-bottom:0">Address Removal Letter</div>
      <div style="display:flex;gap:8px">
        <button class="btn btn-sm" onclick="copyEl('addr-body',this)">Copy</button>
        <button class="btn btn-sm btn-green" onclick="printEl('addr-body','ScoreBoss Address Removal')">Print / PDF</button>
      </div>
    </div>
    <div id="addr-body" class="letter-output"></div>
  </div>
  <div class="card" style="margin-top:1rem">
    <div class="card-title">Step by step</div>
    <div class="check-item"><input type="checkbox"><div><div class="check-text">Pull all 3 credit reports from AnnualCreditReport.com</div><div class="check-sub">Note every address listed that is incorrect or old</div></div></div>
    <div class="check-item"><input type="checkbox"><div><div class="check-text">Generate a removal letter for each incorrect address</div><div class="check-sub">Use the tool above - send to all 3 bureaus</div></div></div>
    <div class="check-item"><input type="checkbox"><div><div class="check-text">Include proof of your current address</div><div class="check-sub">Utility bill, bank statement, or government ID with current address</div></div></div>
    <div class="check-item"><input type="checkbox"><div><div class="check-text">Send via certified mail with return receipt</div><div class="check-sub">Bureaus have 30 days to investigate and respond</div></div></div>
    <div class="check-item"><input type="checkbox"><div><div class="check-text">Follow up after 30 days</div><div class="check-sub">Pull your reports again to confirm addresses were removed</div></div></div>
  </div>
</div>

<!-- CLOSED ACCOUNTS -->
<div id="sec-closed" class="section fade-up">
  <div class="page-header"><div class="page-title">Closed Account Removal</div><div class="page-sub">Negative closed accounts can still be disputed</div></div>
  <div class="tip-box"><strong>Key fact:</strong> Closed accounts stay on your report for 7 years from the date of first delinquency. You can dispute them at any time if information is inaccurate.</div>
  <div class="g2" style="margin-bottom:1rem">
    <div class="card">
      <div class="card-title">Types you can dispute</div>
      <div class="factor-row"><div class="factor-info"><div class="factor-name">Paid/Closed still showing balance</div><div class="factor-sub">Demand correction to $0 or deletion.</div></div><span class="badge badge-green">Easy win</span></div>
      <div class="factor-row"><div class="factor-info"><div class="factor-name">Settled still showing charged off</div><div class="factor-sub">Demand status update to Settled.</div></div><span class="badge badge-green">Easy win</span></div>
      <div class="factor-row"><div class="factor-info"><div class="factor-name">Wrong date of first delinquency</div><div class="factor-sub">Dispute the date to force earlier removal.</div></div><span class="badge badge-amber">Medium</span></div>
      <div class="factor-row"><div class="factor-info"><div class="factor-name">Past 7 years - Must be removed</div><div class="factor-sub">Any negative item older than 7 years must be removed by law.</div></div><span class="badge badge-green">Must remove</span></div>
      <div class="factor-row"><div class="factor-info"><div class="factor-name">Re-aging - Collector reset the date</div><div class="factor-sub">Illegal practice to keep old debt on your report longer.</div></div><span class="badge badge-red">FCRA violation</span></div>
      <div class="factor-row"><div class="factor-info"><div class="factor-name">Duplicate closed accounts</div><div class="factor-sub">Same closed account reported by original creditor AND a collector.</div></div><span class="badge badge-amber">Medium</span></div>
    </div>
    <div class="card">
      <div class="card-title">Generate closed account dispute letter</div>
      <label>Creditor name</label><input type="text" id="ca-creditor" placeholder="Citibank, LVNV Funding, etc."/>
      <label>Account number</label><input type="text" id="ca-acct" placeholder="****1234"/>
      <label>Issue type</label>
      <select id="ca-type">
        <option value="balance">Paid/closed but still showing balance</option>
        <option value="settled">Settled but still showing charged off</option>
        <option value="wrong-date">Wrong date of first delinquency</option>
        <option value="too-old">Past 7 years - must be removed</option>
        <option value="reaging">Re-aging - date was illegally reset</option>
        <option value="duplicate">Duplicate listing</option>
        <option value="inaccurate">General inaccurate information</option>
      </select>
      <label>Date account closed (if known)</label><input type="text" id="ca-date" placeholder="MM/YYYY"/>
      <label>Additional details</label><input type="text" id="ca-details" placeholder="e.g. Paid in full 2022..."/>
      <button class="btn btn-primary" onclick="generateClosedLetter()">Generate Closed Account Letter</button>
    </div>
  </div>
  <div class="card" id="closed-card" style="display:none">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem;flex-wrap:wrap;gap:8px">
      <div class="card-title" style="margin-bottom:0">Closed Account Dispute Letter</div>
      <div style="display:flex;gap:8px">
        <button class="btn btn-sm" onclick="copyEl('closed-body',this)">Copy</button>
        <button class="btn btn-sm btn-green" onclick="printEl('closed-body','ScoreBoss Closed Account Dispute')">Print / PDF</button>
      </div>
    </div>
    <div id="closed-body" class="letter-output"></div>
  </div>
  <div class="card" style="margin-top:1rem">
    <div class="card-title">7-year removal date calculator</div>
    <div style="font-size:13px;color:var(--text2);margin-bottom:12px">Enter the date of first delinquency to find out when this account must be removed.</div>
    <div class="g2">
      <div><label>Date of first delinquency</label><input type="text" id="calc-date" placeholder="MM/YYYY"/><button class="btn btn-primary btn-sm" onclick="calcRemoval()">Calculate</button></div>
      <div id="calc-result" style="display:none;padding:1rem;background:var(--bg3);border-radius:var(--r);border:1px solid var(--border2)"><div id="calc-output" style="font-size:13px;line-height:1.8"></div></div>
    </div>
  </div>
</div>
'''

if '<div id="sec-resources"' in c:
    c = c.replace('<div id="sec-resources"', new_sections + '\n<div id="sec-resources"')
    print("Sections added OK")
else:
    print("Resources section NOT found")

# ═══════════════════════════════════════
# 4. ADD ALL NEW JS before </script>
# ═══════════════════════════════════════
new_js = """
// ── SHARED HELPERS ──
function copyEl(id,btn){
  navigator.clipboard.writeText(document.getElementById(id).textContent);
  btn.textContent='Copied!';
  setTimeout(function(){btn.textContent='Copy';},2000);
}
function printEl(id,title){
  var content=document.getElementById(id).textContent;
  var w=window.open('','_blank');
  w.document.write('<html><head><title>'+title+'</title><style>body{font-family:Georgia,serif;max-width:700px;margin:60px auto;line-height:1.8;font-size:14px;white-space:pre-wrap}</style></head><body>'+content+'</body></html>');
  w.document.close();
  w.print();
}

// ── PAY FOR DELETE ──
function generatePFD(){
  var name=document.getElementById('your-name').value||'[Your Name]';
  var addr=document.getElementById('your-addr').value||'[Your Address]';
  var creditor=document.getElementById('pfd-creditor').value||'[Collection Agency]';
  var acct=document.getElementById('pfd-acct').value||'[Account Number]';
  var balance=document.getElementById('pfd-balance').value||'[Balance]';
  var offer=document.getElementById('pfd-offer').value||'[Offer Amount]';
  var type=document.getElementById('pfd-type').value;
  var today=new Date().toLocaleDateString('en-US',{year:'numeric',month:'long',day:'numeric'});
  var output='';
  var title='';
  if(type==='letter'){
    title='Pay-for-Delete Letter';
    var lines=[
      name,addr,'Date: '+today,'',creditor,'',
      'RE: Settlement Offer with Request for Deletion',
      'Account Number: '+acct+' | Current Balance: '+balance,'',
      'To Whom It May Concern:','',
      'I am writing regarding the above-referenced account currently appearing on my credit report. While I dispute the validity of this debt, I am willing to resolve this matter in the interest of moving forward.',
      '','SETTLEMENT OFFER:',
      'I am prepared to pay '+offer+' as full and final settlement of this account, PROVIDED that you agree to the following conditions:','',
      '1. You will completely DELETE this account from all three credit bureaus (Equifax, Experian, and TransUnion) within 30 days of receiving payment',
      '2. You will NOT report this as paid collection or settled - the account must be DELETED entirely',
      '3. You will provide written confirmation of this agreement before I submit payment',
      '4. You will cease all collection activity immediately upon receipt of this letter','',
      'This offer is contingent upon receiving your written agreement to delete this account. I will not submit payment without a signed agreement.',
      '','This offer expires in 30 days from the date of this letter.',
      '','Sincerely,','','',name,'',
      '--- ACCEPTED AND AGREED ---','',
      'Collection Agency Representative: _______________________',
      'Title: _______________________',
      'Date: _______________________','',
      'We agree to delete Account '+acct+' from all three credit bureaus within 30 days of receiving payment of '+offer+' as full and final settlement.'
    ];
    output=lines.join('\\n');
  } else if(type==='phone'){
    title='Phone Call Script';
    var lines=[
      'PHONE SCRIPT - Pay-for-Delete Negotiation',
      'Account: '+creditor+' | '+acct+' | Balance: '+balance,'',
      '--- OPENING ---',
      '"Hello, I am calling about account number '+acct+'. I would like to speak with someone who has authority to settle accounts and modify credit reporting."','',
      '--- THE OFFER ---',
      '"I can offer '+offer+' as a full and final settlement, but only if you agree to completely delete this account from all three credit bureaus. Not update it, not mark it paid - completely delete it."','',
      '--- IF THEY REFUSE ---',
      '"Can I speak with a supervisor who has authority to approve a pay-for-delete agreement? Many agencies do this regularly."','',
      '--- IF THEY ACCEPT ---',
      '"Please send me the agreement in writing before I submit payment. I need it to show: settlement amount of '+offer+', agreement to delete from all 3 bureaus within 30 days, and an authorized signature."','',
      '--- IMPORTANT NOTES ---',
      '- NEVER give your bank account or card number over the phone',
      '- NEVER pay until you have the written agreement',
      '- Record the name of who you spoke with and the date',
      '- Follow up with a written letter confirming what was agreed'
    ];
    output=lines.join('\\n');
  } else if(type==='agreement'){
    title='Pay-for-Delete Agreement Template';
    var lines=[
      'PAY-FOR-DELETE SETTLEMENT AGREEMENT',
      'Date: '+today,'',
      'Debtor: '+name+', '+addr,
      'Collection Agency: '+creditor,'',
      'Account Number: '+acct,
      'Original Balance: '+balance,
      'Settlement Amount: '+offer,'',
      'TERMS OF AGREEMENT:','',
      '1. PAYMENT: Debtor agrees to pay '+offer+' as full and final settlement within 5 business days of receiving this signed agreement.',
      '','2. DELETION: Collection Agency agrees to:',
      '   a. Request deletion of this account from Equifax, Experian, and TransUnion within 30 days of receiving payment',
      '   b. NOT report this account as paid, settled, or any other status - must be completely DELETED',
      '   c. Provide written confirmation of deletion requests to all three bureaus',
      '','3. FULL SATISFACTION: This payment represents full and final settlement. No further collection activity.',
      '','4. NO RE-INSERTION: Collection Agency agrees not to re-insert this account after deletion.',
      '','COLLECTION AGENCY:',
      'Signature: _______________________',
      'Printed Name: _______________________',
      'Title: _______________________',
      'Date: _______________________','',
      'DEBTOR:',
      'Signature: _______________________',
      'Printed Name: '+name,
      'Date: _______________________'
    ];
    output=lines.join('\\n');
  } else {
    title='Follow-Up Letter if They Refuse';
    var lines=[
      name,addr,'Date: '+today,'',creditor,'',
      'RE: Response to Declined Settlement Offer - Account '+acct,'',
      'To Whom It May Concern:','',
      'I previously contacted you regarding Account '+acct+' with an offer to settle for '+offer+' in exchange for deletion from my credit reports. I understand you declined this offer.',
      '','I want to inform you that I will now be pursuing the following actions:','',
      '1. FORMAL DISPUTE: I am filing a dispute with all three credit bureaus requesting verification of this debt.',
      '2. DEBT VALIDATION: Pursuant to the FDCPA 15 U.S.C. 1692g, I formally demand complete validation of this alleged debt within 30 days.',
      '3. CFPB COMPLAINT: I will be filing a complaint with the Consumer Financial Protection Bureau.',
      '','If you reconsider my settlement offer, please contact me immediately. My offer of '+offer+' for complete deletion remains open for 14 days.',
      '','Sincerely,','','',name
    ];
    output=lines.join('\\n');
  }
  document.getElementById('pfd-title').textContent=title;
  document.getElementById('pfd-body').textContent=output;
  document.getElementById('pfd-card').style.display='block';
}

// ── ADDRESS REMOVAL ──
function generateAddrLetter(){
  var name=document.getElementById('your-name').value||'[Your Name]';
  var currentAddr=document.getElementById('your-addr').value||'[Your Address]';
  var ssn=document.getElementById('your-ssn').value||'XXXX';
  var dob=document.getElementById('your-dob').value||'[DOB]';
  var removeAddr=document.getElementById('addr-remove').value||'[Address to Remove]';
  var reason=document.getElementById('addr-reason').value;
  var bureau=document.getElementById('addr-bureau').value;
  var newAddr=document.getElementById('addr-current').value||currentAddr;
  var today=new Date().toLocaleDateString('en-US',{year:'numeric',month:'long',day:'numeric'});
  var bureauAddr={
    'All three bureaus (separate letters)':'Equifax Information Services LLC, P.O. Box 740256, Atlanta, GA 30374\\n(Also send to: Experian P.O. Box 4500 Allen TX 75013 and TransUnion P.O. Box 2000 Chester PA 19016)',
    'Equifax':'Equifax Information Services LLC\\nP.O. Box 740256\\nAtlanta, GA 30374',
    'Experian':'Experian\\nP.O. Box 4500\\nAllen, TX 75013',
    'TransUnion':'TransUnion LLC\\nP.O. Box 2000\\nChester, PA 19016'
  };
  var reasons={
    'never':'I have never lived at the address listed above. This address does not belong to me and should never have been associated with my credit file.',
    'old':'This address is outdated and no longer current. I have not resided at this address for an extended period. Under the FCRA, all reported information must be accurate and current.',
    'fraud':'This address was fraudulently added to my credit file without my knowledge or consent. I am a victim of identity theft and this address is associated with fraudulent activity.',
    'mixed':'This address belongs to another individual and has been incorrectly associated with my credit file. This is a mixed credit file which violates FCRA accuracy requirements under 15 U.S.C. 1681e(b).',
    'inaccurate':'The address information listed contains errors in the street number, name, city, state, or zip code that make it incorrect.'
  };
  var lines=[
    name,currentAddr,
    'SSN: ***-**-'+ssn+'     Date of Birth: '+dob,
    'Date: '+today,'',
    (bureauAddr[bureau]||bureauAddr['All three bureaus (separate letters)']),'',
    'RE: REQUEST TO REMOVE INACCURATE ADDRESS FROM CREDIT FILE','',
    'To Whom It May Concern:','',
    'I am writing pursuant to the Fair Credit Reporting Act, 15 U.S.C. 1681 et seq., to request the immediate removal of an inaccurate address from my credit file.',
    '','ADDRESS TO BE REMOVED:',
    removeAddr,'',
    'REASON FOR REMOVAL:',
    (reasons[reason]||reasons['inaccurate']),'',
    'MY CORRECT CURRENT ADDRESS:',
    newAddr,'',
    'LEGAL BASIS:',
    'Under FCRA 15 U.S.C. 1681e(b), consumer reporting agencies must ensure maximum possible accuracy of reported information. Reporting an inaccurate address violates this requirement.',
    '','I request that you:',
    '1. Immediately remove the above address from my credit file',
    '2. Update my file to reflect only my current correct address listed above',
    '3. Provide written confirmation that this correction has been made','',
    'Failure to comply may result in CFPB complaints and statutory damages per 15 U.S.C. 1681n.',
    '','Sincerely,','','',name,'',
    'Enclosures:',
    '- Government-issued photo ID showing current address',
    '- Proof of current address (utility bill or bank statement)',
    '- Copy of credit report showing the incorrect address'
  ];
  document.getElementById('addr-body').textContent=lines.join('\\n');
  document.getElementById('addr-card').style.display='block';
}

// ── CLOSED ACCOUNTS ──
function generateClosedLetter(){
  var name=document.getElementById('your-name').value||'[Your Name]';
  var addr=document.getElementById('your-addr').value||'[Your Address]';
  var ssn=document.getElementById('your-ssn').value||'XXXX';
  var dob=document.getElementById('your-dob').value||'[DOB]';
  var creditor=document.getElementById('ca-creditor').value||'[Creditor]';
  var acct=document.getElementById('ca-acct').value||'[Account]';
  var type=document.getElementById('ca-type').value;
  var date=document.getElementById('ca-date').value||'';
  var details=document.getElementById('ca-details').value||'';
  var today=new Date().toLocaleDateString('en-US',{year:'numeric',month:'long',day:'numeric'});
  var reasons={
    'balance':'This account has been paid in full and closed'+(date?' as of '+date:'')+' yet records continue reporting an outstanding balance. I demand this account reflect $0 and Paid/Closed status, or be deleted entirely.',
    'settled':'This account was settled via written agreement'+(date?' in '+date:'')+'. Records inaccurately report this as Charged Off. This is a willful inaccuracy under 15 U.S.C. 1681s-2. I demand status be corrected to Settled or account deleted.',
    'wrong-date':'The date of first delinquency is inaccurate. Under FCRA 605(c), the 7-year period begins from the date of first delinquency. The incorrect date extends reporting beyond what is legally permitted. I demand the date be corrected or account deleted.',
    'too-old':'This account has exceeded the 7-year reporting period mandated by FCRA 605(a). Continued reporting is a violation of federal law. I demand immediate deletion.',
    'reaging':'This account appears to have been re-aged which violates FCRA 605(c) and the FDCPA. I demand the original date of first delinquency be restored and the account reviewed for immediate deletion.',
    'duplicate':'This account is reported as a duplicate entry. The same debt appears under both the original creditor and a collection agency, violating FCRA 1681e(b). One entry must be removed immediately.',
    'inaccurate':'The information reported for this closed account contains material inaccuracies including incorrect balance, payment history, account status, and/or dates.'
  };
  var lines=[
    name,addr,
    'SSN: ***-**-'+ssn+'     Date of Birth: '+dob,
    'Date: '+today,'',
    'Equifax Information Services LLC, P.O. Box 740256, Atlanta, GA 30374',
    '(Also send to: Experian P.O. Box 4500 Allen TX 75013 and TransUnion P.O. Box 2000 Chester PA 19016)','',
    'RE: DISPUTE OF CLOSED ACCOUNT - REQUEST FOR CORRECTION OR DELETION',
    'Creditor: '+creditor+' | Account: '+acct,'',
    'To Whom It May Concern:','',
    'I am writing pursuant to the Fair Credit Reporting Act, 15 U.S.C. 1681 et seq., to dispute the above-referenced closed account.',
    '','NATURE OF DISPUTE:',
    (reasons[type]||reasons['inaccurate']),
    (details?'\\nAdditional Details: '+details:''),'',
    'LEGAL DEMANDS:',
    'You must conduct a reasonable investigation within 30 days per 15 U.S.C. 1681i(a)(1).',
    'Delete this account if information cannot be verified.',
    '','Failure to comply may result in CFPB complaints and statutory damages per 15 U.S.C. 1681n.',
    '','Sincerely,','','',name,'',
    'Enclosures: Government-issued photo ID, Proof of address, Supporting documentation'
  ];
  document.getElementById('closed-body').textContent=lines.join('\\n');
  document.getElementById('closed-card').style.display='block';
}

// ── 7 YEAR CALCULATOR ──
function calcRemoval(){
  var input=document.getElementById('calc-date').value;
  var parts=input.split('/');
  if(parts.length!==2){alert('Please enter date as MM/YYYY');return;}
  var removal=new Date(parseInt(parts[1])+7,parseInt(parts[0])-1,1);
  var today=new Date();
  var daysLeft=Math.ceil((removal-today)/(1000*60*60*24));
  var output='';
  if(daysLeft<=0){
    output='<strong style="color:var(--green)">This account MUST be removed NOW!</strong><br>It passed the 7-year removal date on '+removal.toLocaleDateString('en-US',{month:'long',year:'numeric'})+'. File a dispute immediately.';
  } else {
    output='Mandatory removal date: <strong style="color:var(--amber)">'+removal.toLocaleDateString('en-US',{month:'long',year:'numeric'})+'</strong><br>Days until removal: <strong>'+daysLeft+' days</strong>';
    if(daysLeft<365)output+='<br><strong style="color:var(--amber)">Less than 1 year away - dispute now!</strong>';
  }
  document.getElementById('calc-output').innerHTML=output;
  document.getElementById('calc-result').style.display='block';
}
"""

c = c.replace('</script>', new_js + '\n</script>')
print("JS added")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('DONE! Final size:', len(c))
print('PFD:', 'sec-pfd' in c)
print('Address:', 'sec-address' in c)
print('Closed:', 'sec-closed' in c)
print('generatePFD:', 'generatePFD' in c)
print('generateAddrLetter:', 'generateAddrLetter' in c)
print('generateClosedLetter:', 'generateClosedLetter' in c)
print('calcRemoval:', 'calcRemoval' in c)
