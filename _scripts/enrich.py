import os as _os
_D=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'data')+'/'
import json,glob,re,os,subprocess,time,sys
import requests

BASE='/home/tapaswi/all_papers'
MAIL='saikiatapaswi2025@gmail.com'
S=requests.Session()
S.headers['User-Agent']=f'IBR-biblio/1.0 (mailto:{MAIL})'

cards=[json.load(open(f)) for f in glob.glob(BASE+'/cards/*.json')]
def blob(c):
    return ' '.join(str(c.get(k,'')) for k in ('_title','problem','regions','topic_tags','novelty','key_findings')).lower()
IB=re.compile(r'indo[- ]?burma|indoburman|indoburma|burmese|burma arc|myanmar|northeast(ern)? india|north[- ]east(ern)? india|\bne india\b|shillong|assam|manipur|mizoram|tripura|nagaland|naga hills|naga ophiolite|arunachal|meghalaya|bengal basin|sagaing|kopili|dauki|brahmaputra|imphal|silchar|guwahati|indo[- ]?myanmar|arakan')
TEC=re.compile(r'\btec\b|total electron content|ionospher|vtec|stec|electron content')

sel={}
for c in cards:
    if c.get('_is_fragment'): continue
    b=blob(c)
    tags=[]
    if IB.search(b): tags.append('IBR')
    if TEC.search(b): tags.append('TEC')
    if tags:
        c['_tags']=tags
        sel[c['_citekey']]=c
print('selected',len(sel),file=sys.stderr)

def clean_doi(d):
    if not d: return None
    d=d.strip().lower()
    m=re.search(r'10\.\d{4,9}/[^\s"<>]+',d)
    if not m: return None
    d=m.group(0).rstrip('.,;)')
    d=re.sub(r'\.pdf$','',d)
    if d.startswith('10.13039'): return None   # funder id, not a work
    return d

def pdf_doi(path):
    if not path or not os.path.exists(path): return None
    try:
        t=subprocess.run(['pdftotext','-f','1','-l','3',path,'-'],capture_output=True,timeout=60).stdout.decode('utf8','ignore')
    except Exception: return None
    for m in re.finditer(r'(?:doi[:\s/]*|dx\.doi\.org/|doi\.org/)(10\.\d{4,9}/[^\s,;"\']+)',t,re.I):
        d=clean_doi(m.group(1))
        if d: return d
    return None

def cr_by_doi(doi):
    try:
        r=S.get(f'https://api.crossref.org/works/{doi}',params={'mailto':MAIL},timeout=30)
        if r.status_code!=200: return None
        return r.json()['message']
    except Exception: return None

def cr_by_title(title,author=None,year=None):
    if not title or len(title)<12: return None
    q={'query.bibliographic':title,'rows':3,'mailto':MAIL}
    try:
        r=S.get('https://api.crossref.org/works',params=q,timeout=30)
        if r.status_code!=200: return None
        items=r.json()['message']['items']
    except Exception: return None
    tn=re.sub(r'[^a-z0-9]','',title.lower())
    for it in items:
        t=(it.get('title') or [''])[0]
        cn=re.sub(r'[^a-z0-9]','',t.lower())
        if not cn: continue
        # require strong overlap
        if cn[:45]==tn[:45] or (len(tn)>25 and (tn[:35] in cn or cn[:35] in tn)):
            return it
    return None

def meta(m):
    if not m: return {}
    ct=m.get('container-title') or []
    au=m.get('author') or []
    first=None
    if au:
        a=au[0]
        first=(a.get('family') or a.get('name') or '').strip() or None
    yr=None
    for k in ('published-print','published-online','issued','created'):
        dp=(m.get(k) or {}).get('date-parts') or []
        if dp and dp[0] and dp[0][0]: yr=dp[0][0]; break
    return {'cr_title':(m.get('title') or [None])[0],'journal':ct[0] if ct else None,
            'publisher':m.get('publisher'),'type':m.get('type'),'cr_year':yr,
            'cr_author':first,'doi':m.get('DOI'),
            'authors':[( (a.get('family') or '')+', '+(a.get('given') or '') ).strip(', ') for a in au[:12]]}

out=[]
for i,(k,c) in enumerate(sorted(sel.items())):
    rec={'citekey':k,'tags':c['_tags'],'card_title':c.get('_title'),'card_year':c.get('_year'),
         'card_author':c.get('_author'),'file':c.get('_file'),'src':c.get('_src_path'),
         'paper_type':c.get('paper_type'),'collection':c.get('_collection')}
    doi=clean_doi(c.get('_doi'))
    src=c.get('_src_path') or (BASE+'/papers/'+ (c.get('_file') or ''))
    rec['doi_source']='card' if doi else None
    if not doi:
        doi=pdf_doi(src)
        if doi: rec['doi_source']='pdf'
    m=cr_by_doi(doi) if doi else None
    if m is None:
        m2=cr_by_title(c.get('_title'),c.get('_author'),c.get('_year'))
        if m2:
            m=m2; rec['doi_source']='crossref-title'
    rec.update(meta(m))
    if not rec.get('doi') and doi: rec['doi']=doi
    out.append(rec)
    if i%15==0: print(i,k,rec.get('journal'),file=sys.stderr,flush=True)
    time.sleep(0.12)

json.dump(out,open(_D+'enriched.json','w'),indent=1)
print('DONE',len(out),'with journal:',sum(1 for r in out if r.get('journal')),file=sys.stderr)
