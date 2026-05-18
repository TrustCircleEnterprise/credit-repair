with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Add nav link
c = c.replace(
    "showSection('resources')\">\n      <svg class=\"icon\" viewBox=\"0 0 16 16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"><path d=\"M8 2a6 6 0 100 12A6 6 0 008 2z\"/><path d=\"M8 7v4M8 5.5v.5\"/></svg>Resources &amp; Laws\n    </button>",
    "showSection('closed')\">\n      <svg class=\"icon\" viewBox=\"0 0 16 16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"><rect x=\"2\" y=\"2\" width=\"12\" height=\"12\" rx=\"2\"/><path d=\"M5 8h6\"/></svg>Closed Accounts\n    </button>\n    <button class=\"nav-link\" onclick=\"showSection('resources')\">\n      <svg class=\"icon\" viewBox=\"0 0 16 16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"><path d=\"M8 2a6 6 0 100 12A6 6 0 008 2z\"/><path d=\"M8 7v4M8 5.5v.5\"/></svg>Resources &amp; Laws\n    </button>"
)

# Update map
c = c.replace(
    "['analyze','disputes','letters','rebuild','tracker','clients','simulator','resources']",
    "['analyze','disputes','letters','rebuild','tracker','clients','simulator','closed','resources']"
)

# Add HTML section
section = """
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
  <div class="card" id="closed-letter-card" style="display:none">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem;flex-wrap:wrap;gap:8px">
      <div class="card-title" style="margin-bottom:0">Closed Account Dispute Letter</div>
      <div style="display:flex;gap:8px">
        <button class="btn btn-sm" onclick="copyClosedLetter()">Copy</button>
        <button class="btn btn-sm btn-green" onclick="printClosedLetter()">Print / PDF</button>
      </div>
    </div>
    <div id="closed-letter-body" class="letter-output"></div>
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
"""

c = c.replace('<div id="sec-resources"', section + '\n<div id="sec-resources"')

# Add JS - written as a proper string, no escaping nightmares
js = """
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
  var r={};
  r['balance']='This account has been paid in full and closed'+(date?' as of '+date:'')+' yet records continue reporting an outstanding balance. I demand this account reflect $0 and Paid/Closed status, or be deleted entirely.';
  r['settled']='This account was settled via written agreement'+(date?' in '+date:'')+'. Records inaccurately report this as Charged Off. This is a willful inaccuracy under 15 U.S.C. 1681s-2. I demand status be corrected to Settled or account deleted.';
  r['wrong-date']='The date of first delinquency is inaccurate. Under FCRA 605(c), the 7-year period begins from the date of first delinquency. The incorrect date extends reporting beyond what is legally permitted. I demand the date be corrected or account deleted.';
  r['too-old']='This account has exceeded the 7-year reporting period mandated by FCRA 605(a). Continued reporting is a violation of federal law. I demand immediate deletion.';
  r['reaging']='This account appears to have been re-aged, which violates FCRA 605(c) and the FDCPA. I demand the original date of first delinquency be restored and the account reviewed for immediate deletion.';
  r['duplicate']='This account is reported as a duplicate entry. The same debt appears under both the original creditor and a collection agency, violating FCRA 1681e(b). One entry must be removed immediately.';
  r['inaccurate']='The information reported for this closed account contains material inaccuracies including incorrect balance, payment history, account status, and/or dates.';
  var reason=r[type]||r['inaccurate'];
  var letter=name+'\\n'+addr+'\\nSSN: ***-**-'+ssn+'     Date of Birth: '+dob+'\\nDate: '+today+'\\n\\nEquifax Information Services LLC, P.O. Box 740256, Atlanta, GA 30374\\n(Also send to: Experian P.O. Box 4500 Allen TX 75013 and TransUnion P.O. Box 2000 Chester PA 19016)\\n\\nRE: DISPUTE OF CLOSED ACCOUNT - REQUEST FOR CORRECTION OR DELETION\\nCreditor: '+creditor+' | Account: '+acct+'\\n\\nTo Whom It May Concern:\\n\\nI am writing pursuant to the Fair Credit Reporting Act, 15 U.S.C. 1681 et seq., to dispute the above-referenced closed account.\\n\\nNATURE OF DISPUTE:\\n'+reason+(details?'\\n\\nAdditional Details: '+details:'')+'\\n\\nLEGAL DEMANDS:\\nYou must conduct a reasonable investigation within 30 days per 15 U.S.C. 1681i(a)(1).\\nDelete this account if information cannot be verified.\\n\\nFailure to comply may result in CFPB complaints and statutory damages per 15 U.S.C. 1681n.\\n\\nSincerely,\\n\\n\\n'+name+'\\n\\nEnclosures: Government-issued photo ID, Proof of address, Supporting documentation';
  document.getElementById('closed-letter-body').textContent=letter;
  document.getElementById('closed-letter-card').style.display='block';
}

function copyClosedLetter(){
  navigator.clipboard.writeText(document.getElementById('closed-letter-body').textContent);
  event.target.textContent='Copied!';
  setTimeout(function(){event.target.textContent='Copy';},2000);
}

function printClosedLetter(){
  var content=document.getElementById('closed-letter-body').textContent;
  var w=window.open('','_blank');
  w.document.write('<html><head><title>ScoreBoss Closed Account Dispute</title><style>body{font-family:Georgia,serif;max-width:700px;margin:60px auto;line-height:1.8;font-size:14px;white-space:pre-wrap}</style></head><body>'+content+'</body></html>');
  w.document.close();
  w.print();
}

function calcRemoval(){
  var input=document.getElementById('calc-date').value;
  var parts=input.split('/');
  if(parts.length!==2){alert('Please enter date as MM/YYYY');return;}
  var removal=new Date(parseInt(parts[1])+7,parseInt(parts[0])-1,1);
  var today=new Date();
  var daysLeft=Math.ceil((removal-today)/(1000*60*60*24));
  var output;
  if(daysLeft<=0){
    output='<strong style="color:var(--green)">This account MUST be removed NOW!</strong><br>It passed the 7-year removal date on '+removal.toLocaleDateString('en-US',{month:'long',year:'numeric'})+'. File a dispute immediately.';
  }else{
    output='Mandatory removal date: <strong style="color:var(--amber)">'+removal.toLocaleDateString('en-US',{month:'long',year:'numeric'})+'</strong><br>Days until removal: <strong>'+daysLeft+' days</strong>';
    if(daysLeft<365)output+='<br><strong style="color:var(--amber)">Less than 1 year away - dispute now!</strong>';
  }
  document.getElementById('calc-output').innerHTML=output;
  document.getElementById('calc-result').style.display='block';
}
"""

c = c.replace('</script>', js + '\n</script>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Done! Size:', len(c))
print('sec-closed added:', 'sec-closed' in c)
print('generateClosedLetter added:', 'generateClosedLetter' in c)
print('Nav link added:', 'Closed Accounts' in c)
