import os as _os
_D=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'data')+'/'
import requests,json,re,time,sys
M='saikiatapaswi2025@gmail.com'; S=requests.Session(); S.headers['User-Agent']=f'IBR/1.0 (mailto:{M})'
SC=_D
QUERIES=['Indo-Burma Ranges tectonics','Indo-Burman Ranges seismicity','Indo-Myanmar Ranges geology',
 'Indo-Burma subduction zone earthquake','Northeast India seismotectonics','Shillong Plateau earthquake',
 'Kopili fault Assam seismicity','Sagaing fault Myanmar','Burma plate GPS deformation',
 'Indo-Burmese wedge structure','Naga Hills ophiolite','Myanmar earthquake hazard machine learning',
 'Northeast India total electron content ionosphere earthquake','Indo-Burma b-value seismicity',
 'Bengal basin Sylhet trough tectonics','Manipur Nagaland geology ophiolite',
 'deep learning earthquake detection Myanmar','Indo-Burma receiver function crustal structure',
 'Myanmar seismic tomography slab','Indo-Burma ranges thermochronology provenance']
IB=re.compile(r'indo[- ]?burm|indo[- ]?myanmar|\bmyanmar\b|\bburma\b|northeast(ern)? india|north[- ]east(ern)? india|shillong|assam|manipur|mizoram|nagaland|naga hills|meghalaya|arakan|sagaing|kopili|dauki|bengal basin|sylhet|brahmaputra|kabaw|chindwin|imphal|tripura|arunachal|burmese')
seen={}
for q in QUERIES:
    for off in (0,100):
        try:
            r=S.get('https://api.crossref.org/works',params={'query.bibliographic':q,'rows':100,'offset':off,
                'select':'DOI,title,container-title,author,issued,published-print,type,abstract','mailto':M},timeout=45)
            items=r.json()['message']['items']
        except Exception as e:
            print('ERR',q,e,file=sys.stderr); break
        for it in items:
            t=(it.get('title') or [''])[0]
            if not t: continue
            hay=(t+' '+re.sub(r'<[^>]+>',' ',it.get('abstract') or '')).lower()
            if not IB.search(hay): continue
            if it.get('type') not in ('journal-article','book-chapter','proceedings-article'): continue
            seen[it['DOI'].lower()]=it
        time.sleep(.2)
    print(q,'->',len(seen),file=sys.stderr,flush=True)
json.dump(list(seen.values()),open(SC+'sweep.json','w'),indent=1)
print('TOTAL',len(seen),file=sys.stderr)
