"""Sweep 3: OpenAlex - papers whose ABSTRACT names the Indo-Burma region but whose TITLE does
not: wider-scope studies where IBR is one component. -> data/sweep_oa.json"""
import os as _os, requests, json, re, time, sys
_D=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'data')+'/'
M='saikiatapaswi2025@gmail.com'; S=requests.Session(); S.headers['User-Agent']=f'IBR/1.0 (mailto:{M})'
PHRASES=['Indo-Burma','Indo-Burman','Indo-Myanmar','Burmese arc','Burma plate','Shillong Plateau',
 'Sagaing Fault','Kopili fault','Naga Hills','Indo-Burmese','northeast India','Arakan',
 'Bengal basin','Sylhet trough','Chindwin','Rakhine']
REG=re.compile(r'indo[- ]?burm|indo[- ]?myanmar|\bmyanmar\b|\bburma\b|burmese|northeast(ern)? india|'
  r'north[- ]east(ern)? india|shillong|assam|manipur|mizoram|nagaland|meghalaya|arakan|rakhine|sagaing|'
  r'kopili|dauki|bengal basin|sylhet|brahmaputra|kabaw|chindwin|imphal|tripura|arunachal',re.I)
GEO=re.compile(r'tecton|seismi|earthquake|fault|subduct|ophiolit|crust|mantle|lithosph|geolog|geochem|'
  r'zircon|magmat|metamorph|stratigraph|sediment|basin|gps|gnss|geodet|deformation|slab|moho|tomograph|'
  r'ionospher|hazard|velocity|provenance|convergen|plate\b|orogen|terrane|suture|gravity|anisotrop|'
  r'attenuat|paleoseism|palaeoseism|geophys|geodynam|rupture|strain|magnitude|microseism|receiver function|'
  r'b-value|catalog|exhumation|thermochron|uplift|erosion|denudation|palaeomagnet|paleomagnet',re.I)
BIO=re.compile(r'biodiversity|hotspot|species|genus|\bnov\.|taxonom|phylogen|conservation|forest|primate|'
  r'orchid|amphibian|reptile|\bbird|fish\b|insect|flora|fauna|vegetation|habitat|endemi|malaria|health|'
  r'agricultur|ethnobot|livelihood|refugee|linguist|poverty|gender|tourism|epidemi|nutrition|crop',re.I)
def unroll(ii):
    if not ii: return ''
    w=[(p,t) for t,ps in ii.items() for p in ps]
    return ' '.join(t for _,t in sorted(w))
seen={}
for ph in PHRASES:
    cur='*'
    for _ in range(6):
        try:
            r=S.get('https://api.openalex.org/works',params={
                'filter':f'title_and_abstract.search:"{ph}"','per-page':200,'cursor':cur,'mailto':M,
                'select':'doi,title,publication_year,primary_location,authorships,type,abstract_inverted_index'},
                timeout=60).json()
        except Exception as e:
            print('ERR',ph,e,file=sys.stderr); break
        for w in r.get('results',[]):
            t=w.get('title') or ''; doi=(w.get('doi') or '').replace('https://doi.org/','')
            if not t or not doi: continue
            if w.get('type') not in ('article','book-chapter','review'): continue
            if REG.search(t): continue                       # titled about the region -> sweep.py
            ab=unroll(w.get('abstract_inverted_index'))
            if not ab or not REG.search(ab): continue        # must genuinely MENTION it
            src=((w.get('primary_location') or {}).get('source') or {}).get('display_name') or ''
            if BIO.search(t+' '+src+' '+ab[:600]): continue
            if not GEO.search(t+' '+src+' '+ab[:600]): continue
            seen[doi.lower()]=dict(doi=doi,title=t,year=w.get('publication_year'),journal=src,
                authors=[(a.get('author') or {}).get('display_name') for a in (w.get('authorships') or [])[:12]])
        cur=(r.get('meta') or {}).get('next_cursor')
        if not cur: break
        time.sleep(.15)
    print(ph,'->',len(seen),file=sys.stderr,flush=True)
json.dump(list(seen.values()),open(_D+'sweep_oa.json','w'),indent=1)
print('TOTAL',len(seen),file=sys.stderr)
