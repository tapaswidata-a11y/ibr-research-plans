import os as _os
_D=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'data')+'/'
import json,glob,re,html
S=_D
base=json.load(open(S+'final.json')); extra=json.load(open(S+'extra.json'))

Q1={'Nature','Nature Geoscience','Scientific Reports','Earth and Planetary Science Letters',
 'Earth-Science Reviews','Tectonics','Journal of Geophysical Research: Solid Earth',
 'Journal of Geophysical Research','Geophysical Research Letters','Geology','Reviews of Geophysics',
 'Geological Society of America Bulletin','Gondwana Research','Tectonophysics','American Journal of Science',
 'Journal of Asian Earth Sciences','Journal of Southeast Asian Earth Sciences','Geosphere','The Journal of Geology',
 'Journal of Metamorphic Geology','Geophysical Journal International','Geological Magazine',
 'Physics of the Earth and Planetary Interiors','Bulletin of the Seismological Society of America',
 'Seismological Research Letters','Journal of the Geological Society','Earthquake Spectra',
 'Soil Dynamics and Earthquake Engineering','Remote Sensing','Sedimentary Geology',
 'Cretaceous Research','Lithosphere','Space Weather','AAPG Bulletin','Natural Hazards'}
Q2={'Quaternary International','Journal of Seismology','Pure and Applied Geophysics','pure and applied geophysics',
 'Geological Journal','International Journal of Earth Sciences','Journal of Geodynamics','Island Arc',
 'Journal of Applied Geophysics','Earthquake Science','Journal of the Geological Society of Australia'}
Q3={'Journal of Earth System Science','Acta Geophysica','Journal of the Geological Society of India',
 'Indian Journal of History of Science','All Earth','Journal of Geography and Geology'}
NR={'International Journal of Geosciences','IOSR Journal of Applied Physics','Physics &amp; Astronomy International Journal',
 'Journal of the Indian Association of Sedimentologists','Engineering Applications'}
BOOK={'Geological Society, London, Memoirs','Geological Society, London, Special Publications',
 'Microearthquake Seismology and Seismotectonics of South Asia',
 'New Frontiers in Tectonic Research - General Problems, Sedimentary Basins and Island Arcs'}
def quart(j):
    if not j: return None
    for s,v in ((Q1,'Q1'),(Q2,'Q2'),(Q3,'Q3'),(NR,'not indexed'),(BOOK,'book series')):
        if j in s: return v
    return '?'

FIX={'seismological2012':dict(cr_title='Seismological Research in India, 2007–2011',cr_year=2012,
        cr_author='Gupta',journal=None,kind='national report (IUGG/INSA quadrennial review)')}
DROP={'created2008a'}   # user's own summary of Li et al. 2008 (the paper itself is kept)

seen={(r['title'] or '').lower()[:45] for r in base}
seendoi={(r['doi'] or '').lower() for r in base if r['doi']}
add=0
for r in extra:
    if r['citekey'] in DROP: continue
    r.update(FIX.get(r['citekey'],{}))
    t=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',(r.get('cr_title') or r.get('card_title') or '')))).strip()
    doi=(r.get('doi') or '').strip() or None
    if t.lower()[:45] in seen or (doi and doi.lower() in seendoi): continue
    seen.add(t.lower()[:45]);  doi and seendoi.add(doi.lower())
    au=r.get('cr_author') or (r.get('card_author') if r.get('card_author') not in ('[unattributed]','[scan]','(anonymous)') else None)
    base.append(dict(key=r['citekey'],title=t,year=r.get('cr_year') or r.get('card_year'),doi=doi,
        journal=r.get('journal'),authors=r.get('authors') or [],author=au,tags=['IBR'],
        quart=quart(r.get('journal')),kind=r.get('kind'),file=r.get('file')))
    add+=1

# --- b-value / seismicity-statistics tagging, from the source cards
cards={c['_citekey']:c for c in (json.load(open(f)) for f in glob.glob('/home/tapaswi/all_papers/cards/*.json'))}
BV=re.compile(r'\bb-?\s?values?\b|gutenberg[- ]richter|frequency[- ]magnitude distribution|magnitude of completeness|completeness magnitude|seismicity parameters|\ba-? and b-? ?values?')
for r in base:
    c=cards.get(r['key']) or {}
    txt=' '.join(str(c.get(k,'')) for k in ('_title','problem','topic_tags','novelty','key_findings','methods'))
    if BV.search((txt+' '+r['title']).lower()): r['tags']=sorted(set(r['tags'])|{'bvalue'})

base.sort(key=lambda r:(r['year'] or 9999,(r['journal'] or 'zzz'),r['title']))
json.dump(base,open(S+'final.json','w'),indent=1)
import collections
print('added',add,'-> total',len(base))
print(collections.Counter(r['quart'] for r in base))
print('bvalue:',sum(1 for r in base if 'bvalue' in r['tags']),'TEC:',sum(1 for r in base if 'TEC' in r['tags']))
print('unknown quartile:',{r['journal'] for r in base if r['quart']=='?'})
print('with doi:',sum(1 for r in base if r['doi']),'range:',base[0]['year'],base[-1]['year'])
