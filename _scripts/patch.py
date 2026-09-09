import os as _os
_D=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'data')+'/'
import json,glob,re,os,subprocess,time,sys,requests
BASE='/home/tapaswi/all_papers'; MAIL='saikiatapaswi2025@gmail.com'
S=requests.Session(); S.headers['User-Agent']=f'IBR-biblio/1.0 (mailto:{MAIL})'
sys.path.insert(0,_os.path.dirname(_os.path.abspath(__file__)))
cards=[json.load(open(f)) for f in glob.glob(BASE+'/cards/*.json')]
def blob(c): return ' '.join(str(c.get(k,'')) for k in ('_title','problem','regions','topic_tags','novelty','key_findings')).lower()
OLD=re.compile(r'indo[- ]?burma|indoburman|indoburma|burmese|burma arc|myanmar|northeast(ern)? india|north[- ]east(ern)? india|\bne india\b|shillong|assam|manipur|mizoram|tripura|nagaland|naga hills|naga ophiolite|arunachal|meghalaya|bengal basin|sagaing|kopili|dauki|brahmaputra|imphal|silchar|guwahati|indo[- ]?myanmar|arakan')
NEW=re.compile(r'\bburma|\bmyanmar|\bandaman|\bsylhet|\bmikir|\bbarail|\bdisang|\bcachar|\bhaflong|\bchittagong|\bmogok|\bwuntho|\bsibumasu|\bbengal fan|eastern himalaya|\bkabaw|\bchindwin|\bkaladan|lohit|mishmi|churachandpur')
fin=json.load(open(_D+'final.json'))
have={(r['title'] or '').lower()[:40] for r in fin}
DROP={'rescue_created2008a'}  # user's own summary of Li et al. 2008 (real paper kept)
new=[c for c in cards if not c.get('_is_fragment') and NEW.search(blob(c)) and not OLD.search(blob(c))
     and (c.get('_title') or '').lower()[:40] not in have and c.get('_citekey') not in DROP]
print('to enrich:',len(new),file=sys.stderr)

def clean(d):
    if not d: return None
    m=re.search(r'10\.\d{4,9}/[^\s"<>]+',str(d).lower())
    if not m: return None
    return re.sub(r'\.pdf$','',m.group(0).rstrip('.,;)'))
def pdfdoi(p):
    if not p or not os.path.exists(p): return None
    try: t=subprocess.run(['pdftotext','-f','1','-l','3',p,'-'],capture_output=True,timeout=60).stdout.decode('utf8','ignore')
    except Exception: return None
    for m in re.finditer(r'(?:doi[:\s/]*|doi\.org/)(10\.\d{4,9}/[^\s,;"\']+)',t,re.I):
        if clean(m.group(1)): return clean(m.group(1))
def cr(doi):
    try:
        r=S.get(f'https://api.crossref.org/works/{doi}',params={'mailto':MAIL},timeout=30)
        return r.json()['message'] if r.status_code==200 else None
    except Exception: return None
def crt(t):
    if not t or len(t)<12: return None
    try: items=S.get('https://api.crossref.org/works',params={'query.bibliographic':t,'rows':3,'mailto':MAIL},timeout=30).json()['message']['items']
    except Exception: return None
    tn=re.sub(r'[^a-z0-9]','',t.lower())
    for it in items:
        cn=re.sub(r'[^a-z0-9]','',((it.get('title') or [''])[0]).lower())
        if cn and (cn[:45]==tn[:45] or (len(tn)>25 and (tn[:35] in cn or cn[:35] in tn))): return it
    return None
out=[]
for c in new:
    doi=clean(c.get('_doi')) or pdfdoi(c.get('_src_path') or '')
    m=cr(doi) if doi else None
    if not m:
        m=crt(c.get('_title'))
    ct=(m or {}).get('container-title') or []
    au=(m or {}).get('author') or []
    yr=None
    for k in ('published-print','published-online','issued','created'):
        dp=((m or {}).get(k) or {}).get('date-parts') or []
        if dp and dp[0] and dp[0][0]: yr=dp[0][0];break
    out.append(dict(citekey=c['_citekey'],tags=['IBR'],card_title=c.get('_title'),card_year=c.get('_year'),
        card_author=c.get('_author'),file=c.get('_file'),src=c.get('_src_path'),paper_type=c.get('paper_type'),
        cr_title=(m or {}).get('title',[None])[0],journal=ct[0] if ct else None,cr_year=yr,
        cr_author=((au[0].get('family') or au[0].get('name')) if au else None),
        doi=(m or {}).get('DOI') or doi,
        authors=[((a.get('family') or '')+', '+(a.get('given') or '')).strip(', ') for a in au[:12]]))
    print(' ',out[-1]['cr_year'],out[-1]['journal'],file=sys.stderr,flush=True); time.sleep(0.12)
json.dump(out,open(_D+'extra.json','w'),indent=1)
print('DONE',len(out),file=sys.stderr)
