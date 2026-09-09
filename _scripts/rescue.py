import os as _os
_D=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'data')+'/'
import json,glob,re,os,subprocess,time,sys,requests
BASE='/home/tapaswi/all_papers'; MAIL='saikiatapaswi2025@gmail.com'
SC=_D
S=requests.Session(); S.headers['User-Agent']=f'IBR-biblio/1.0 (mailto:{MAIL})'
cards=[json.load(open(f)) for f in glob.glob(BASE+'/cards/*.json')]
fin=json.load(open(SC+'final.json'))
have={(r['title'] or '').lower()[:40] for r in fin}
havedoi={(r['doi'] or '').lower() for r in fin if r['doi']}
todo=[c for c in cards if not c.get('_is_fragment')
      and (c.get('_title') or '').lower()[:40] not in have
      and str(c.get('_doi') or '').lower() not in havedoi]
print('to rescue:',len(todo),file=sys.stderr)
def clean(d):
    m=re.search(r'10\.\d{4,9}/[^\s"<>]+',str(d or '').lower())
    return re.sub(r'\.pdf$','',m.group(0).rstrip('.,;)')) if m else None
def pdfdoi(p):
    if not p or not os.path.exists(p): return None
    try: t=subprocess.run(['pdftotext','-f','1','-l','4',p,'-'],capture_output=True,timeout=60).stdout.decode('utf8','ignore')
    except Exception: return None
    for m in re.finditer(r'(?:doi[:\s/]*|doi\.org/)(10\.\d{4,9}/[^\s,;"\']+)',t,re.I):
        c=clean(m.group(1))
        if c and not c.startswith('10.13039'): return c
    return None
def cr(doi):
    try:
        r=S.get(f'https://api.crossref.org/works/{doi}',params={'mailto':MAIL},timeout=30)
        return r.json()['message'] if r.status_code==200 else None
    except Exception: return None
IB=re.compile(r'\bburma|\bmyanmar|indo[- ]?burm|indo[- ]?myanmar|northeast(ern)? india|north[- ]east(ern)? india|shillong|assam|manipur|mizoram|nagaland|naga hills|meghalaya|arakan|sagaing|kopili|dauki|bengal basin|sylhet|chittagong|brahmaputra|mikir|kabaw|chindwin|kaladan|imphal|tripura|arunachal|andaman')
res=[]
for i,c in enumerate(todo):
    src=c.get('_src_path') or (BASE+'/papers/'+(c.get('_file') or ''))
    doi=clean(c.get('_doi')) or pdfdoi(src)
    m=cr(doi) if doi else None
    if not m: continue
    title=(m.get('title') or [''])[0]
    ct=(m.get('container-title') or [''])
    abst=re.sub(r'<[^>]+>',' ',m.get('abstract') or '')
    hay=' '.join([title,abst,' '.join(str(x) for x in (c.get('regions') or [])),str(c.get('_title'))]).lower()
    if not IB.search(hay): continue
    au=m.get('author') or []
    yr=None
    for k in ('published-print','published-online','issued','created'):
        dp=(m.get(k) or {}).get('date-parts') or []
        if dp and dp[0] and dp[0][0]: yr=dp[0][0];break
    res.append(dict(citekey=c['_citekey'],cr_title=title,journal=ct[0] if ct else None,cr_year=yr,
        cr_author=((au[0].get('family') or au[0].get('name')) if au else None),doi=m.get('DOI'),
        authors=[((a.get('family') or '')+', '+(a.get('given') or '')).strip(', ') for a in au[:12]],
        card_title=c.get('_title'),card_year=c.get('_year'),card_author=c.get('_author'),file=c.get('_file')))
    print('  +',yr,'|',(title or '')[:58],'|',ct[0] if ct else None,file=sys.stderr,flush=True)
    time.sleep(0.1)
json.dump(res,open(SC+'rescued.json','w'),indent=1)
print('RESCUED',len(res),file=sys.stderr)
