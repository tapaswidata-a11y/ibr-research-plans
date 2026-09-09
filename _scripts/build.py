import os as _os
_D=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'data')+'/'
import json,re,html
S=_D
d=json.load(open(S+'enriched.json'))

# --- clear non-literature: own notes, unidentifiable chapter scans, duplicate atlases
DROP_KEYS={'chatgptdeepresearch1972','MM_pipeline_reference_report','indoburma2020','subduction2020a','chapter2006','chapter2006b','andf','fullnde','fullndc','fullndd','indonda','earthquake2020','geosystems2022a'}
BAD_MATCH={'Encyclopedia of Astrobiology','Open-File Report'}

Q1={'Nature','Nature Geoscience','Scientific Reports','Earth and Planetary Science Letters',
 'Earth-Science Reviews','Tectonics','Journal of Geophysical Research: Solid Earth',
 'Journal of Geophysical Research','Geophysical Research Letters','Geology',
 'Geological Society of America Bulletin','Gondwana Research','Tectonophysics',
 'Journal of Asian Earth Sciences','Journal of Southeast Asian Earth Sciences','Geosphere',
 'Journal of Metamorphic Geology','Geophysical Journal International',
 'Physics of the Earth and Planetary Interiors','Bulletin of the Seismological Society of America',
 'Seismological Research Letters','Journal of the Geological Society','Earthquake Spectra',
 'Soil Dynamics and Earthquake Engineering','Remote Sensing','Sedimentary Geology',
 'Cretaceous Research','Lithosphere','Space Weather','AAPG Bulletin','Natural Hazards',
 'Geosystems and Geoenvironment'}
Q2={'Quaternary International','Journal of Seismology','Pure and Applied Geophysics',
 'pure and applied geophysics','Geological Journal','International Journal of Earth Sciences',
 'Journal of Geodynamics','Island Arc','Journal of Applied Geophysics','Earthquake Science',
 'Journal of the Geological Society of Australia'}
Q3={'Journal of Earth System Science','Acta Geophysica','Journal of the Geological Society of India',
 'Indian Journal of History of Science','All Earth'}
NR={'International Journal of Geosciences','IOSR Journal of Applied Physics',
 'Physics &amp; Astronomy International Journal'}
BOOK={'Geological Society, London, Memoirs','Geological Society, London, Special Publications',
 'Microearthquake Seismology and Seismotectonics of South Asia',
 'New Frontiers in Tectonic Research - General Problems, Sedimentary Basins and Island Arcs'}

def quart(j):
    if not j: return None
    if j in Q1: return 'Q1'
    if j in Q2: return 'Q2'
    if j in Q3: return 'Q3'
    if j in NR: return 'not indexed'
    if j in BOOK: return 'book series'
    return '?'

# manual repairs
FIX={
 'sedimentation2016a':dict(journal='Geological Society of America Bulletin',
    cr_title='Sedimentation and tectonics of the Sylhet trough, Bangladesh',
    doi='10.1130/0016-7606(1991)103<1513:SATOTS>2.3.CO;2',cr_year=1991,cr_author='Johnson'),
 'united1990':dict(journal=None,doi=None,cr_title='Sedimentation and Tectonics of the Sylhet Trough, Northeastern Bangladesh',cr_year=1990,kind='USGS report'),
 'comment2023':dict(cr_title='Comment on “Age, depositional history and tectonics of the Indo-Myanmar Ranges”',doi=None,journal='Journal of the Geological Society',cr_year=2023),
}
FIX2={
 'anonnd\x87':dict(cr_title='Microearthquake Seismology and Seismotectonics of South Asia',cr_year=2008,cr_author='Kayal',doi='10.1007/978-1-4020-8180-4',journal=None,kind='book (Springer)'),
 'fullndb':dict(cr_title='Geodynamics of Northeastern India and the Adjoining Region',cr_year=2001,cr_author='Nandy',kind='book (ACB Publications, Kolkata)'),
 'geochemicalnd':dict(cr_title='Tectonic Setting and Provenance of Eocene Sandstones of Disang Group, Tirap District, Arunachal Pradesh',cr_year=2021,cr_author='Gogoi',journal='Journal of the Indian Association of Sedimentologists',kind=None),
 'bachelors2023':dict(cr_title='Correlation between earthquake precursors and ionosphere scintillation measured with GNSS remote sensing techniques',cr_year=2023,cr_author='Carvajal Librado',kind='BSc thesis (UPC)'),
 'laboratoire1984a':dict(cr_title='Active faulting and tectonics of Burma and surrounding regions',cr_year=1984,cr_author='Le Dain',journal='Journal of Geophysical Research',doi='10.1029/JB089iB01p00453'),
 'indond':dict(cr_title='Indo-Burmese Convergent Margin (scanned book chapter)',cr_year=None,kind='book chapter (scan, source unidentified)',journal=None,doi=None),
 'maneerat2022':dict(cr_title='Short- and Long-Term Tectonics across the Indo-Burma Range',cr_year=2022,cr_author='Maneerat',journal=None,kind='PhD thesis (UC Berkeley)'),
 'methods2023':dict(cr_title='Methods and software for estimation of total electron content in ionosphere using GNSS observations',cr_year=2023,cr_author='Naumov',journal='Engineering Applications',kind=None),
 'fullnd':dict(cr_title='Geology of Burma',cr_year=1983,cr_author='Bender',kind='book (Gebruder Borntraeger)'),
 'seismotectonics2010':dict(cr_title='Seismicity of northeast India and surroundings: development over the past 100 years',cr_year=2010,cr_author='Kayal',journal='Journal of Geography and Geology',kind=None),
}
NR.add('Journal of the Indian Association of Sedimentologists')
NR.add('Engineering Applications')
Q3.add('Journal of Geography and Geology')
KIND={'lithospheric2025':'PhD thesis','analysis2025':'PhD thesis','bachelors2023':'BSc thesis',
 'shear2025':'project report','characterizing2026':'in preparation','fullnd':'book (Bender, Geology of Burma)',
 'rescue_fullndb':'book (Nandy, Geodynamics of North East India)','methods2023':'technical note',
 'earthquake2011':'conference/report','geochemicalnd':'journal article (Indian Assoc. Sedimentologists)',
 'tectonic2010':'report','tif2015':'report','maneerat2022':'preprint/report',
 'seismotectonics2010':'review article','MM_pipeline_reference_report':'report'}

rows=[]
seen_doi={}
for r in d:
    k=r['citekey']
    if k in DROP_KEYS: continue
    if r.get('journal') in BAD_MATCH:
        r['journal']=None; r['doi']=None; r['cr_title']=None
    r.update(FIX.get(k,{})); r.update(FIX2.get(k,{}))
    title=(r.get('cr_title') or r.get('card_title') or '').strip()
    title=re.sub(r'<[^>]+>','',title); title=html.unescape(title)
    title=re.sub(r'\s+',' ',title).replace(' ',' ').strip()
    year=r.get('cr_year') or r.get('card_year')
    doi=r.get('doi')
    if doi: doi=doi.strip()
    au=r.get('cr_author') or (r.get('card_author') if r.get('card_author') not in ('[unattributed]','[scan]','(anonymous)') else None)
    if au and re.match(r'^10\.|^\d',str(au)): au=None
    rec=dict(key=k,title=title,year=year,doi=doi,journal=r.get('journal'),
             authors=r.get('authors') or [],author=au,tags=r['tags'],
             quart=quart(r.get('journal')),kind=r.get('kind') or KIND.get(k),
             file=r.get('file'))
    # dedup on DOI
    if doi:
        dl=doi.lower()
        if dl in seen_doi:
            prev=seen_doi[dl]
            if len(title)>len(prev['title']): prev.update(title=title)
            prev['tags']=sorted(set(prev['tags'])|set(rec['tags']))
            continue
        seen_doi[dl]=rec
    rows.append(rec)

# dedup on normalized title
byt={}
out=[]
for r in rows:
    n=re.sub(r'[^a-z0-9]','',r['title'].lower())[:50]
    if n and n in byt:
        byt[n]['tags']=sorted(set(byt[n]['tags'])|set(r['tags']))
        if not byt[n]['doi'] and r['doi']: byt[n]['doi']=r['doi']
        if not byt[n]['journal'] and r['journal']: byt[n]['journal']=r['journal']; byt[n]['quart']=r['quart']
        continue
    byt[n]=r; out.append(r)

out.sort(key=lambda r:( r['year'] or 9999, (r['journal'] or 'zzz'), r['title']))
json.dump(out,open(S+'final.json','w'),indent=1)
print('final rows:',len(out))
print('with doi:',sum(1 for r in out if r['doi']),' with journal:',sum(1 for r in out if r['journal']))
import collections
print(collections.Counter(r['quart'] for r in out))
print(collections.Counter(t for r in out for t in r['tags']))
print('unknown quartile journals:',{r['journal'] for r in out if r['quart']=='?'})
print('year range:',min(r['year'] for r in out if r['year']), max(r['year'] for r in out if r['year']))
print('no year:',sum(1 for r in out if not r['year']))
