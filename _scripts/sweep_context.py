"""Sweep 2: papers of WIDER scope that mention the Indo-Burma region in their abstract.
Region term must appear in the ABSTRACT; papers whose title is already regional are skipped
(sweep.py has those). Output: data/sweep_ctx.json"""
import os as _os, requests, json, re, time, sys
_D=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'data')+'/'
M='saikiatapaswi2025@gmail.com'; S=requests.Session(); S.headers['User-Agent']=f'IBR/1.0 (mailto:{M})'
QUERIES=[
 'India Asia collision tectonic reconstruction','eastern Himalayan syntaxis tectonics',
 'Sundaland Southeast Asia tectonic evolution','Sunda subduction zone seismicity',
 'Bay of Bengal Andaman Sea tectonics','global subduction zone megathrust comparison',
 'Tibetan Plateau eastward extrusion India indentation','Himalaya seismic hazard India catalogue',
 'global seismicity b-value subduction zones comparison','Indian plate motion GPS deformation Asia',
 'Bengal fan sediment provenance Himalaya erosion','Tethyan suture ophiolite belt Asia',
 'slab tomography Southeast Asia upper mantle','great earthquake tsunami Indian Ocean hazard',
 'India intraplate deformation stress field','ionospheric precursor earthquake global GNSS statistics',
 'machine learning global earthquake catalog subduction','oblique convergence strain partitioning forearc sliver',
 'monsoon hydrology seismicity modulation Himalaya','crustal structure receiver function Indian shield Himalaya',
]
REG=re.compile(r'indo[- ]?burm|indo[- ]?myanmar|\bmyanmar\b|\bburma\b|burmese|northeast(ern)? india|'
    r'north[- ]east(ern)? india|shillong|assam|manipur|mizoram|nagaland|meghalaya|arakan|rakhine|'
    r'sagaing|kopili|dauki|bengal basin|sylhet|brahmaputra|kabaw|chindwin|imphal|tripura|arunachal',re.I)
GEO=re.compile(r'tecton|seismi|earthquake|fault|subduct|ophiolit|crust|mantle|lithosph|geolog|geochem|'
    r'zircon|magmat|metamorph|stratigraph|sediment|basin|gps|gnss|geodet|deformation|slab|moho|'
    r'tomograph|ionospher|hazard|velocity|provenance|convergen|plate|orogen|terrane|suture|gravity|'
    r'anisotrop|attenuat|palaeoseism|paleoseism|machine learning|deep learning|neural',re.I)
seen={}
for q in QUERIES:
    for off in (0,100):
        try:
            items=S.get('https://api.crossref.org/works',params={'query.bibliographic':q,'rows':100,
                'offset':off,'select':'DOI,title,container-title,author,issued,abstract,type',
                'mailto':M},timeout=45).json()['message']['items']
        except Exception as e:
            print('ERR',q,e,file=sys.stderr); break
        for it in items:
            t=(it.get('title') or [''])[0]
            ab=re.sub(r'<[^>]+>',' ',it.get('abstract') or '')
            if not t or not ab: continue
            if it.get('type') not in ('journal-article','book-chapter'): continue
            if REG.search(t): continue                 # title-regional -> sweep.py's job
            if not REG.search(ab): continue            # must MENTION the region
            if not (GEO.search(t) or GEO.search(ab)): continue
            seen[it['DOI'].lower()]=it
        time.sleep(.2)
    print(q,'->',len(seen),file=sys.stderr,flush=True)
json.dump(list(seen.values()),open(_D+'sweep_ctx.json','w'),indent=1)
print('TOTAL',len(seen),file=sys.stderr)
