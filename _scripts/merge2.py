import os as _os
_D=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'data')+'/'
import json,re,html,collections
SC=_D
lib=json.load(open(SC+'final.json'))          # 172 library records
cand=json.load(open(SC+'cand3.json'))         # CrossRef sweep, geo-filtered
ml=json.load(open(SC+'ml.json'))              # AI/ML papers

Q1={'Nature','Nature Geoscience','Nature Communications','Scientific Reports','Earth and Planetary Science Letters',
 'Earth-Science Reviews','Tectonics','Journal of Geophysical Research: Solid Earth','Journal of Geophysical Research',
 'Geophysical Research Letters','Geology','Reviews of Geophysics','Geological Society of America Bulletin','GSA Bulletin',
 'Gondwana Research','Tectonophysics','American Journal of Science','Journal of Asian Earth Sciences',
 'Journal of Southeast Asian Earth Sciences','Geosphere','The Journal of Geology','Journal of Metamorphic Geology',
 'Geophysical Journal International','Geological Magazine','Physics of the Earth and Planetary Interiors',
 'Bulletin of the Seismological Society of America','Seismological Research Letters','Journal of the Geological Society',
 'Earthquake Spectra','Soil Dynamics and Earthquake Engineering','Remote Sensing','Sedimentary Geology','Cretaceous Research',
 'Lithosphere','Space Weather','AAPG Bulletin','Natural Hazards','Geoscience Frontiers','Lithos','Chemical Geology',
 'Precambrian Research','Journal of Structural Geology','Marine and Petroleum Geology','Ore Geology Reviews','Geomorphology',
 'Basin Research','Palaeogeography, Palaeoclimatology, Palaeoecology','Marine Geology','Earth, Planets and Space',
 'Journal of Sedimentary Research','SEPM Journal of Sedimentary Research','Science China Earth Sciences','Minerals',
 'Environmental Earth Sciences','Geomatics, Natural Hazards and Risk','International Geology Review','Sensors',
 'Journal of Radioanalytical and Nuclear Chemistry','Organic Geochemistry','Applied Energy','Geosystems and Geoenvironment',
 'Mineralogical Magazine','The Canadian Mineralogist','Journal of Earth Science','Geodesy and Geodynamics'}
Q2={'Quaternary International','Journal of Seismology','Pure and Applied Geophysics','pure and applied geophysics',
 'Geological Journal','International Journal of Earth Sciences','Journal of Geodynamics','Island Arc',
 'Journal of Applied Geophysics','Earthquake Science','Journal of the Geological Society of Australia','Episodes',
 'Journal of Earthquake Engineering','Mineralogy and Petrology','Geosciences Journal','Acta Geochimica','Geochemistry',
 'Acta Geologica Sinica - English Edition','Arabian Journal of Geosciences','Comptes Rendus. Géoscience',
 'International Journal of Remote Sensing','Journal of the Indian Society of Remote Sensing','Physics and Chemistry of the Earth',
 'Natural Hazards Review','Earthquake Research Advances','Geoenvironmental Disasters','The Seismic Record',
 'Natural Hazards Research','Advances in Structural Engineering','Annals of Geophysics','Journal of Earthquake and Tsunami'}
Q3={'Journal of Earth System Science','Acta Geophysica','Journal of the Geological Society of India',
 'Journal Geological Society of India','Journal Of The Geological Society Of India','Indian Journal of History of Science',
 'All Earth','Journal of Geography and Geology','Current Science','Geotectonics','Journal of Physics of the Earth',
 'Terrestrial, Atmospheric and Oceanic Sciences','Bulletin of the Geological Society of Malaysia','Geologische Rundschau',
 'Journal of Nepal Geological Society','Journal of the Palaeontological Society of India','The Palaeobotanist',
 'Proceedings of the Indian National Science Academy','Resource Geology','Micropaleontology'}
NR={'International Journal of Geosciences','IOSR Journal of Applied Physics','Physics &amp; Astronomy International Journal',
 'Journal of the Indian Association of Sedimentologists','Journal of The Indian Association of Sedimentologists',
 'Engineering Applications','MAUSAM','ISET Journal of Earthquake Technology','Open Journal of Geology','BIBECHANA',
 'Journal of Geosciences Research','Himalayan Physics','Himalayan Journal of Sciences','Journal of Life and Earth Science',
 'ASEAN Engineering Journal','International Journal of Scientific Engineering and Research','Geoexploration'}
BOOKW=re.compile(r'geological society, london|memoirs|special publication|encyclopedia|series$|abstracts|expanded abstracts|conference|proceedings|developments in|topics in|special paper|atlas|volume iii|swarms|indian shield|earthquake time bombs|wit transactions|archives of the photogrammetry|show$|meeting of')
Q1|={'Science','Nature','Geochemistry, Geophysics, Geosystems','Journal of Petrology',
 'Paleoceanography','Journal of Asian Earth Sciences X','Quarterly Journal of the Geological Society',
 'Russian Geology and Geophysics','Annals of Glaciology','Journal of Hydrology'}
Q2|={'Frontiers in Earth Science','Geophysical Prospecting','Hydrogeology Journal','Marine Geodesy',
 'Journal of Geophysics and Engineering','Remote Sensing Letters','Journal of Hydrology: Regional Studies',
 'Chinese Science Bulletin','Journal of Geophysical Research: Atmospheres','Evolving Earth'}
NR|={'International Journal of Science and Research','Zenodo','E-Periodica'}
_NONGEO={'revista de fomento social','international journal of social economics','water science & technology',
 'water science and technology','journal of southeast asian studies'}
def _n(j):
    import re as _re
    return _re.sub(r'[^a-z0-9 ]','',(j or '').lower()).replace('  ',' ').strip()
_Q1n={_n(x) for x in Q1}; _Q2n={_n(x) for x in Q2}; _Q3n={_n(x) for x in Q3}; _NRn={_n(x) for x in NR}
def quart(j):
    if not j: return None
    n=_n(j)
    if n in _NONGEO or _n(j) in {_n(x) for x in _NONGEO}: return 'drop'
    if n in _Q1n: return 'Q1'
    if n in _Q2n: return 'Q2'
    if n in _Q3n: return 'Q3'
    if n in _NRn: return 'not indexed'
    if n.startswith('journal of geophysical research'): return 'Q1'
    if BOOKW.search(j.lower()) or 'ebooks' in n: return 'book / proceedings'
    return 'unrated'
DROPJ=re.compile(r'contested civil society|zootaxa|phytotaxa|soil survey horizons|christianity|springerplus|indo-pacific archaeol|entomolog|goldschmidt\d+ abstracts')
DROPT=re.compile(r'relict vegetation|rugose coral|waagenophyllid')

def norm(t): return re.sub(r'[^a-z0-9]','',(t or '').lower())[:45]
recs=[]; seendoi=set(); seent=set()
for r in lib:
    r['source']='library'; recs.append(r)
    if r['doi']: seendoi.add(r['doi'].lower())
    seent.add(norm(r['title']))

def add(title,year,journal,doi,authors,src):
    t=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',title or ''))).strip()
    if not t or not year: return 0
    if journal and DROPJ.search(journal.lower()): return 0
    if DROPT.search(t.lower()): return 0
    if doi and doi.lower() in seendoi: return 0
    if norm(t) in seent: return 0
    seendoi.add((doi or '').lower()); seent.add(norm(t))
    au=authors or []
    first=au[0].split(',')[0] if au else None
    recs.append(dict(key='cr_'+(doi or t)[:24],title=t,year=year,doi=doi,journal=journal,
        authors=au,author=first,tags=[],quart=quart(journal),kind=None,file=None,source=src))
    return 1

n1=sum(add(c[3],c[0],c[1],c[2],[f'{a}, ' for a in (c[4] or []) if a],'reference') for c in cand)
n2=sum(add(m['cr_title'],m['cr_year'],m['journal'],m['doi'],m['authors'],'reference') for m in ml)
ex2=json.load(open(SC+'extra2.json'))
n4=sum(add(x['cr_title'],x['cr_year'],x['journal'],x['doi'],x['authors'],'reference')
       for x in ex2 if x['journal'])
n3=add('Tectono-structural framework of the Indo-Myanmar Ranges: Implications for the Rakhine Coastal Region, Myanmar',
       2022,'Geosystems and Geoenvironment','10.1016/j.geogeo.2022.100079',['Khin, Kyaw','Moe, Aung','Aung, Lin'],'library')

# ---- tags
BV=re.compile(r'\bb-?\s?values?\b|gutenberg[- ]richter|frequency[- ]magnitude|magnitude of completeness|completeness magnitude|seismicity parameters')
TEC=re.compile(r'\btec\b|total electron content|ionospher|vtec|seismo-?ionospher')
MLR=re.compile(r'machine learning|deep learning|neural network|\bann\b|\bcnn\b|\blstm\b|random forest|xgboost|support vector|artificial intelligence|supervised learning|deep-?learning|transformer|convolutional')
DASH=re.compile(r'[\u2010-\u2015\u2212\u00ad]')
for r in recs:
    t=DASH.sub('-',r['title']).lower()
    tags=set(r.get('tags') or [])
    if BV.search(t): tags.add('bvalue')
    if TEC.search(t): tags.add('TEC')
    if MLR.search(t): tags.add('ML')
    r['tags']=sorted(tags)

recs.sort(key=lambda r:(r['year'] or 9999,(r['journal'] or 'zzz'),r['title']))
json.dump(recs,open(SC+'final2.json','w'),indent=1)
print(f'library {len(lib)} + sweep {n1} + ml {n2} + late {n4} + fix {n3} = {len(recs)}')
print(collections.Counter(r['quart'] for r in recs))
print('tags:',collections.Counter(t for r in recs for t in r['tags']))
print('source:',collections.Counter(r['source'] for r in recs))
print('range:',recs[0]['year'],'-',recs[-1]['year'],' with doi:',sum(1 for r in recs if r['doi']))
print('unrated journals:',len({r['journal'] for r in recs if r['quart']=='unrated'}))
