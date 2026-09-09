"""Merge wider-scope papers (region mentioned, not the title subject) into final3.json,
tagged scope='context'. Core papers from final2.json keep scope='focused'."""
import os as _os, json, re, html, collections
_D=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'data')+'/'
core=json.load(open(_D+'final2.json'))
oa=json.load(open(_D+'sweep_oa.json'))
try: ctx=json.load(open(_D+'sweep_ctx.json'))
except Exception: ctx=[]

_M=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'merge2.py')
_ns={'__file__':_M}; ns=_ns; exec(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'merge2.py')).read()
     .split('recs=[]')[0].replace("core=","_x="), ns)   # reuse Q1/Q2/Q3/NR/BOOKW + quart()
quart=ns['quart']

JUNK=re.compile(r'^dummy|ancient coinage|coinage of|\bhistory of the [a-z]+ people|colonial|'
  r'^review for |^comment on the|erratum|corrigendum|retraction',re.I)
def norm(t): return re.sub(r'[^a-z0-9]','',(t or '').lower())[:45]

recs=[]; seendoi=set(); seent=set()
for r in core:
    r['scope']='focused'; recs.append(r)
    if r['doi']: seendoi.add(r['doi'].lower())
    seent.add(norm(r['title']))

def add(title,year,journal,doi,authors):
    t=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',title or ''))).strip()
    if not t or not year or year<1900 or JUNK.search(t): return 0
    if doi and doi.lower() in seendoi: return 0
    if norm(t) in seent: return 0
    seendoi.add((doi or '').lower()); seent.add(norm(t))
    au=[a for a in (authors or []) if a]
    first=au[0].split(',')[0].strip() if au else None
    if first and ' ' in first: first=first.split()[-1]        # OpenAlex gives "Given Family"
    _q=quart(journal)
    if _q=='drop': return 0
    recs.append(dict(key='ctx_'+(doi or t)[:24],title=t,year=year,doi=doi,journal=journal or None,
        authors=au,author=first,tags=[],quart=_q,kind=None,file=None,
        source='reference',scope='context'))
    return 1

n1=sum(add(w['title'],w['year'],w['journal'],w['doi'],w.get('authors')) for w in oa)
n2=0
for it in ctx:
    yr=None
    for k in ('published-print','issued'):
        dp=(it.get(k) or {}).get('date-parts') or []
        if dp and dp[0] and dp[0][0]: yr=dp[0][0]; break
    n2+=add((it.get('title') or [''])[0],yr,(it.get('container-title') or [None])[0],it.get('DOI'),
            [((a.get('family') or '')+', '+(a.get('given') or '')).strip(', ') for a in (it.get('author') or [])[:12]])

# --- topical gate for wider-scope entries -----------------------------------
# The OpenAlex/CrossRef context sweep matched on the abstract alone, so it pulled in
# humanities, meteorology, water chemistry and biology papers that merely name the region.
# A context entry must read as earth science (GEO) and must not be one of the off-topic
# subjects (OFF), however geological its wording. Focused entries were already gated on the
# title, and anything whose PDF the user holds is never dropped.
# a wider-scope entry must look like earth science ...
GEO=re.compile('|'.join([r'seismic',r'seismo',r'earthquake',r'quake',r'tecton',r'fault',r'subduct',
 r'megathrust',r'rupture',r'tsunami',r'geolog',r'geophys',r'geodes',r'geodet',r'gnss',r'\bgps\b',
 r'insar',r'magnetotellur',r'gravity',r'crust',r'mantle',r'lithosph',r'moho',r'ophiolit',r'petrol',
 r'geochem',r'mineral',r'zircon',r'magmat',r'volcan',r'basalt',r'granit',r'metamorph',r'stratigraph',
 r'sediment',r'basin',r'provenance',r'palaeo',r'paleo',r'holocene',r'pleistocene',r'miocene',
 r'eocene',r'oligocene',r'cretaceous',r'jurassic',r'triassic',r'precambrian',r'geomorph',
 r'landslide',r'liquefaction',r'hazard',r'ground motion',r'attenuation',r'b-value',r'gutenberg',
 r'ionospher',r'total electron',r'slab',r'\bplate\b',r'orogen',r'thrust',r'anisotrop',r'tomograph',
 r'receiver function',r'rayleigh',r'shear[- ]wave',r'velocity structure',r'aftershock',r'foreshock',
 r'radon',r'thoron',r'deformation',r'strain',r'stress',r'geoscien',r'earth scien',r'geothermal',
 r'exhumation',r'thermochronol',r'coal',r'hydrocarbon',r'petroleum',r'reservoir',r'drainage',
 r'delta\b',r'\bfan\b',r'shelf',r'margin',r'ridge',r'seamount',r'chromit',r'peridotit',r'serpentin',
 r'amphibol',r'blueschist',r'eclogit',r'oil\b',r'\bgas\b',r'isotop',r'landform',r'quaternary',
 r'gondwana',r'terrane',r'syntaxis',r'accretion',r'wedge',r'uplift',r'\bdyke\b',r'dike',
 r'weathering',r'facies',r'foraminifer',r'radiolarian',r'palyno',r'ichno',r'erosion',r'denudation']),re.I)
# ... and must not be one of these off-topic subjects, however geological its wording
OFF=re.compile('|'.join([
 r'\barsenic\b',r'\bas\)? concentration',r'drinking water',r'groundwater (?:system|recharge|storage|quality|flow)',
 r'aquifer',r'tube ?well',r'wetland',r'\bponds?\b',r'water resources',r'organic-matter composition',
 r'monsoon (?:variabilit|simulat|rainfall)',r'summer monsoon',r'rainfall',r'precipitation',r'cloud',
 r'cyclone',r'storm surge',r'wave height',r'ozone',r'biomass burning',r'climatolog',r'climate change',
 r'\bclimate of\b',r'glacio',r'tropospher',r'bacteri',r'microbio',r'toxicolog',r'bivalv',r'mollus',
 r'\bsnail\b',r'diplommatina',r'wound healing',r'agronom',r'soil loss',r'nutrient',r'fertil',
 r'\bbricks?\b',r'glass production',r'compressive strength',r'recyclab',
 r'buddhis',r'rohingya',r'slave',r'toponym',r'ethnonym',r'foreign aid',r'civil society',
 r'archaeolog',r'tradisi',r'\bprofile of\b',r'birmanie',
 r'great slave lake',r'louisiana',r'\bsundarbans\b',r'\bhooghly\b']),re.I)

RESCUE={  # false positives of the rules above, kept deliberately
 '10.1002/2014gc005462',   # Andaman Sea sediment provenance - caught by "monsoon variability"
 '10.1007/s10346-021-01810-6', # Cox's Bazar landslide geology - caught by "Rohingya" (camp name)
 '10.20965/jdr.2020.p0377',    # Yangon ground information for disaster response
}
def ontopic(r):
    if r.get('scope')!='context' or r.get('source')=='library': return True
    if (r.get('doi') or '').lower() in RESCUE: return True
    t=(r.get('title') or '')+' '+(r.get('journal') or '')
    return bool(GEO.search(t)) and not OFF.search(t)

BV=re.compile(r'\bb-?\s?values?\b|gutenberg[- ]richter|frequency[- ]magnitude|magnitude of completeness|seismicity parameters')
TEC=re.compile(r'\btec\b|total electron content|ionospher|vtec|seismo-?ionospher')
MLR=re.compile(r'machine learning|deep learning|neural network|\bann\b|\bcnn\b|random forest|xgboost|'
  r'support vector|artificial intelligence|supervised learning|transformer|convolutional')
DASH=re.compile(r'[‐-―−­]')
for r in recs:
    t=DASH.sub('-',r['title']).lower(); tags=set(r.get('tags') or [])
    if BV.search(t): tags.add('bvalue')
    if TEC.search(t): tags.add('TEC')
    if MLR.search(t): tags.add('ML')
    r['tags']=sorted(tags)

_before=len(recs)
_dropped=[r for r in recs if not ontopic(r)]
recs=[r for r in recs if ontopic(r)]
with open(_D+'dropped_offtopic.txt','w') as f:
    f.write(f'{len(_dropped)} wider-scope entries removed as off-topic\n\n')
    for r in sorted(_dropped,key=lambda r:r['year'] or 0):
        f.write(f"{r['year']}  {(r['journal'] or '-')[:40]:40.40}  {r['title']}\n")
print(f'off-topic filter: {_before} -> {len(recs)} ({len(_dropped)} dropped, listed in data/dropped_offtopic.txt)')

recs.sort(key=lambda r:(r['year'] or 9999,(r['journal'] or 'zzz'),r['title']))
json.dump(recs,open(_D+'final3.json','w'),indent=1)
print(f'core {len(core)} + openalex {n1} + crossref-ctx {n2} = {len(recs)}')
print('scope:',collections.Counter(r['scope'] for r in recs))
print('quartile:',collections.Counter(r['quart'] for r in recs))
print('tags:',collections.Counter(t for r in recs for t in r['tags']))
print('range:',recs[0]['year'],'-',recs[-1]['year'],'| with doi:',sum(1 for r in recs if r['doi']))
