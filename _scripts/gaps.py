GAPS=[
('Seismology','Deep-learning phase picking and association over the whole NE India archive','none here','archive',
 'Yang et al. (2024, <i>GRL</i>) ran a deep-learning picker on a temporary network in central Myanmar and recovered <b>twice</b> the events of standard processing, resolving activity on the Kabaw Fault.',
 'Your library already holds every manual — PhaseNet, EQTransformer, SeisBench, GaMMA, PyOcto — and not one has been turned on the Indian side. Regional catalogues still start near M<sub>c</sub> 3.5; a DL catalogue typically drops M<sub>c</sub> by a full unit and sharpens fault planes.',
 'The continuous waveform archive you already have, plus one GPU. No fieldwork, no permissions.',
 [
  {"t":'Zhu et al. 2018',"j":'Geophysical Journal International',"doi":'10.1093/gji/ggy423'},
  {"t":'Mousavi et al. 2020',"j":'Nature Communications',"doi":'10.1038/s41467-020-17591-w'},
  {"t":'Woollam et al. 2022',"j":'Seismological Research Letters',"doi":'10.1785/0220210324'},
  {"t":'Zhu et al. 2022',"j":'Journal of Geophysical Research: Solid Earth',"doi":'10.1029/2021jb023249'},
  {"t":'Münchmeyer 2024',"j":'Seismica',"doi":'10.26443/seismica.v3i1.1130'},
  {"t":'Yang et al. 2024',"j":'Geophysical Research Letters',"doi":'10.1029/2023gl105159'}
 ]),
('Seismology','Matched-filter / template-matching catalogue extension','none here','archive',
 'Standard practice in Japan and California for two decades — and in your own library it has been applied to <i>Mars</i> (2026 InSight marsquake catalogue) but never to the Indo-Burma Ranges.',
 'Kopili and Churachandpur–Mao need dense microseismicity before their fault planes can be drawn. Template matching finds events 1–2 magnitude units below the network threshold using the events you already catalogued as templates.',
 'Existing catalogue as templates + continuous data. Pairs naturally with the DL catalogue above.',
 [
  {"t":'Gibbons et al. 2006',"j":'Geophysical Journal International',"doi":'10.1111/j.1365-246x.2006.02865.x'},
  {"t":'Shelly et al. 2007',"j":'Nature',"doi":'10.1038/nature05666'},
  {"t":'Ross et al. 2019',"j":'Science',"doi":'10.1126/science.aaw6888'}
 ]),
('Seismology','A search for slow slip and tectonic tremor','none here','archive',
 'Cascadia (Rogers &amp; Dragert 2003), Nankai, Hikurangi and Guerrero all host episodic tremor and slip on locked, shallow-dipping megathrusts.',
 'Steckler et al. (2016, <i>Nature Geoscience</i>) showed the Indo-Burman megathrust is locked and loading with exactly that geometry. Every comparable margin that has been searched has found ETS. <b>Nobody has searched here</b> — a CrossRef query returns zero regional studies.',
 'Continuous GNSS (already recording) for transients, plus broadband envelope cross-correlation for tremor. A genuinely first-of-its-kind result if it exists.',
 [
  {"t":'Rogers et al. 2003',"j":'Science',"doi":'10.1126/science.1084783'},
  {"t":'Obara 2002',"j":'Science',"doi":'10.1126/science.1070378'},
  {"t":'Wallace et al. 2016',"j":'Science',"doi":'10.1126/science.aaf2349'}
 ]),
('Seismology','Ambient-noise monitoring of velocity change (dv/v)','none here','archive',
 'Brenguier and co-workers established dv/v monitoring at Parkfield and Merapi; Lecocq et al. (2017), in your library, used it to track groundwater storage over 30 years.',
 "Assam's monsoon hydrological loading and the Kopili fault are an ideal pairing — seasonal pore-pressure modulation of seismicity is measurable, and no one has tried it in the region.",
 'Two or more continuously recording broadbands and a noise-correlation pipeline. Retrospective — works on archived data.',
 [
  {"t":'Brenguier et al. 2008',"j":'Science',"doi":'10.1126/science.1160943'},
  {"t":'Brenguier et al. 2008',"j":'Nature Geoscience',"doi":'10.1038/ngeo104'},
  {"t":'Lecocq et al. 2017',"j":'Scientific Reports',"doi":'10.1038/s41598-017-14468-9'}
 ]),
('Seismology','Full-waveform / adjoint tomography','none here','compute',
 'Now routine for Japan, Europe and North America (Fichtner, Tape and successors).',
 "Every tomographic image of the Indo-Burma slab to date is ray-based travel-time inversion. Slab geometry below ~150 km is still argued over — Rao &amp; Kumar's cessation hypothesis versus continued subduction. Waveform inversion resolves what ray theory smears.",
 'Waveform archive plus HPC time. The bottleneck is compute, not data.',
 [
  {"t":'Tape et al. 2009',"j":'Science',"doi":'10.1126/science.1175298'},
  {"t":'Fichtner et al. 2009',"j":'Geophysical Journal International',"doi":'10.1111/j.1365-246x.2009.04368.x'}
 ]),
('Seismology','Distributed acoustic sensing on telecom dark fibre','none here','field',
 'Ajo-Franklin (2019), Sladen (2019) and Williams (2019) — <b>all three sit in your library</b> — turned unused telecom fibre into thousands of seismic channels.',
 'A CrossRef search returns zero DAS seismology papers for India. Fibre already runs along the highways and rail across the Shillong Plateau and up the Assam valley. It is dense-array sampling without vaults, permits or power.',
 'An interrogator unit (rentable) and a dark-fibre agreement with a telecom operator. The single cheapest route to dense data here.',
 [
  {"t":'Ajo-Franklin et al. 2019',"j":'Scientific Reports',"doi":'10.1038/s41598-018-36675-8'},
  {"t":'Sladen et al. 2019',"j":'Nature Communications',"doi":'10.1038/s41467-019-13793-z'},
  {"t":'Williams et al. 2019',"j":'Nature Communications',"doi":'10.1038/s41467-019-13262-7'}
 ]),
('Seismology','Ocean-bottom seismometers on the Rakhine–Bengal margin','none here','major',
 'Cascadia, Hikurangi and Sumatra all resolved their updip megathrust only after going offshore.',
 'Cummins (2007, <i>Nature</i>) argued the northern Bay of Bengal can host a giant tsunamigenic earthquake. The updip, offshore part of that megathrust — the part that would generate the tsunami — is sampled by <b>no</b> instrument. Onshore networks cannot resolve it.',
 'A ship, an OBS pool and international collaboration. The most expensive item here and the most consequential.',
 [
  {"t":'Cummins 2007',"j":'Nature',"doi":'10.1038/nature06088'},
  {"t":'Wallace et al. 2016',"j":'Science',"doi":'10.1126/science.aaf2349'}
 ]),
('Seismology','Dense nodal (large-N) array deployments','one study','field',
 'Thousands-of-node deployments are now routine in California and Oklahoma. Regionally there is exactly one — a 2025 site-amplification study in Yangon.',
 'Three-to-six-week nodal deployments across the Kopili fault, the Dauki front or the Shillong Plateau margin would give basin depth, fault location and site response at a spatial density no permanent network can reach.',
 '100–300 rentable nodes and a few weeks of fieldwork. No vaults, no telemetry, batteries only.',
 [
  {"t":'Ben-Zion et al. 2015',"j":'Geophysical Journal International',"doi":'10.1093/gji/ggv142'}
 ]),
('AI / ML','Modern b-value estimators with significance testing','none here','archive',
 'Mizrahi et al. (2024, <i>SRL</i>) — <b>in your library</b> — showed that most published spatial b-value variations fail a significance test, and introduced b-positive and the b-significant framework.',
 'Every one of the 28 b-value papers in this bibliography uses maximum-curvature or MLE with no significance testing. Re-analysing the NE India b-value literature with these estimators is a direct, publishable methodological correction of your own field.',
 'Published catalogues only. This is a laptop project with a high citation ceiling.',
 [
  {"t":'Mirwald et al. 2024',"j":'Seismological Research Letters',"doi":'10.1785/0220240190'},
  {"t":'van der Elst 2021',"j":'Journal of Geophysical Research: Solid Earth',"doi":'10.1029/2020jb021027'}
 ]),
('AI / ML','Self-supervised denoising of regional waveforms','none here','archive',
 'DeepDenoiser and successors routinely recover signal from stations with poor SNR.',
 'NE India station noise is a documented, well-characterised problem — much of your library is about exactly that. Nobody has applied learned denoising to it, and it multiplies the yield of every other method on this list.',
 'Archive waveforms plus a GPU. Natural companion to the DL picker.',
 [
  {"t":'Zhu et al. 2019',"j":'IEEE Transactions on Geoscience and Remote Sensing',"doi":'10.1109/tgrs.2019.2926772'}
 ]),
('AI / ML','Graph neural networks for association and declustering','none here','archive',
 'GNN associators and ML declustering now outperform nearest-neighbour and window methods on dense catalogues.',
 'Once a DL catalogue exists for NE India it will contain far more events than classical declustering handles well — and declustering choice propagates straight into every b-value and hazard number in this bibliography.',
 'The catalogue you build in step one.',
 [
  {"t":'McBrearty et al. 2023',"j":'Bulletin of the Seismological Society of America',"doi":'10.1785/0120220182'}
 ]),
('AI / ML','Machine learning for ionospheric TEC anomaly detection','none here','archive',
 'Global seismo-ionospheric work has moved to LSTM and autoencoder anomaly detection with proper false-alarm accounting.',
 'All eight TEC papers here still use fixed 2σ thresholds over a sliding window. That method cannot quantify its own false-alarm rate — which is precisely the criticism levelled at earthquake-precursor claims. An ML treatment with honest skill scores would be a real contribution.',
 'IGS/GNSS TEC archives, all public.',
 []),
('Hazard','A 3-D basin velocity model and physics-based ground-motion simulation','partial','compute',
 "SCEC's CyberShake for California and NIED's work for the Kanto basin simulate ground motion from 3-D structure rather than empirical attenuation.",
 'Two broadband simulation papers exist for NE India, but there is <b>no 3-D velocity model of the Assam valley or the Sylhet trough</b> — among the deepest sediment basins on Earth. Empirical GMPEs cannot capture basin resonance at those thicknesses; Guwahati, Silchar and Sylhet sit on it.',
 'Receiver functions, gravity and existing well logs to build the model; HPC for the simulation.',
 [
  {"t":'Graves et al. 2010',"j":'Pure and Applied Geophysics',"doi":'10.1007/s00024-010-0161-6'}
 ]),
('Hazard','Tsunami inundation modelling for the Bengal coast','none here','compute',
 'Standard practice for every other subduction margin after 2004.',
 'Cummins (2007) raised the giant-tsunami scenario for the northern Bay of Bengal nineteen years ago. There is still no inundation study for the Bangladesh–Myanmar coastline — one of the most densely populated, lowest-lying coasts on the planet.',
 'A rupture scenario, bathymetry and a shallow-water solver. All open-source.',
 [
  {"t":'Cummins 2007',"j":'Nature',"doi":'10.1038/nature06088'}
 ]),
('Hazard','Time-dependent and operational earthquake forecasting','none here','archive',
 'Italy runs an operational earthquake forecast; New Zealand runs time-dependent hazard with renewal models.',
 'Every PSHA in this bibliography is Poissonian — memoryless. For a margin with a documented 1897 M8.1 and a strain budget, renewal and ETAS models are the appropriate tool and nobody has fitted them.',
 'Existing catalogues plus a declustering choice. Directly extends the b-value work already being done.',
 [
  {"t":'Marzocchi et al. 2014',"j":'Seismological Research Letters',"doi":'10.1785/0220130219'}
 ]),
('Hazard','Palaeoseismic trenching on the fold-belt faults','partial','field',
 'The Himalayan front has a dense trenching record establishing recurrence for great earthquakes.',
 'Shillong and Dauki have some palaeoseismic control (Bilham &amp; England 1999; Sukhija 1999), but the Churachandpur–Mao and Kopili faults — the structures now shown to be creeping and seismically active — have <b>no</b> trench-derived recurrence at all.',
 'Field seasons, trenching permits and radiocarbon dating. Slow, but it is the only source of pre-instrumental recurrence.',
 [
  {"t":'Bilham et al. 2001',"j":'Nature',"doi":'10.1038/35071057'},
  {"t":'Sukhija et al. 1999',"j":'Earth and Planetary Science Letters',"doi":'10.1016/s0012-821x(99)00015-1'}
 ]),
('Hazard','Exposure, fragility and risk — not just hazard','none here','archive',
 'Nath and co-workers built a full vulnerability and risk model for Kolkata (2015, in your library).',
 'The NE India literature stops at hazard: PGA maps and source zones. No comparable exposure inventory or fragility-based loss model exists for Guwahati, Imphal, Shillong or Silchar, so the hazard numbers never convert into decisions.',
 'Building inventories (remote sensing plus survey) and published fragility curves.',
 [
  {"t":'Nath et al. 2015',"j":'Natural Hazards and Earth System Sciences',"doi":'10.5194/nhess-15-1103-2015'}
 ]),
]

# --- Global ranking of the 17 openings, 1 = start here.
# Axis: (a) what can begin with the archive + one GPU already in hand, (b) how novel the
# regional result would be, (c) how much the answer matters — ties broken towards work that
# unlocks items below it. ASSUMES no field budget and no ship time. Keyed by gap name.
RANK={
 'Modern b-value estimators with significance testing':(1,
  'Laptop-scale, published catalogues only, and it lands squarely inside your own thesis topic. Mirwald et al. (2024) is already in your library and the 28 regional b-value papers in this bibliography are the ready-made test set. The most result per week of work on this list.'),
 'Deep-learning phase picking and association over the whole NE India archive':(2,
  'The catalogue that ranks 3, 6 and 8 are all built on. Archive plus one GPU, no permits, no fieldwork — and Yang et al. (2024) already proved the doubling on the Myanmar side of the same structure.'),
 'Matched-filter / template-matching catalogue extension':(3,
  'Runs on the same archive using your existing catalogue as templates, needs CPU rather than GPU, and gives an independent cross-check on the deep-learning catalogue instead of a second version of it.'),
 'A search for slow slip and tectonic tremor':(4,
  'The highest ceiling here and genuinely first-of-its-kind — but a null result is a real possibility, so it ranks below work that is certain to yield a paper. Best run alongside 1–3, not instead of them.'),
 'Ambient-noise monitoring of velocity change (dv/v)':(5,
  'Retrospective, archive-only and low-risk: it works on data already recorded. The monsoon-loading and Kopili pairing is half-written in the regional literature already.'),
 'Self-supervised denoising of regional waveforms':(6,
  'Cheap, archive-only, and it multiplies the yield of ranks 2 and 3 — but standing alone it reads as a methods note rather than a headline result.'),
 'Time-dependent and operational earthquake forecasting':(7,
  'Published catalogues plus a declustering choice. It extends the b-value work directly, and every PSHA in this bibliography is still Poissonian, so the correction is easy to motivate.'),
 'Graph neural networks for association and declustering':(8,
  'Sound and doable, but it needs the dense catalogue from rank 2 to exist first. Sequence it after, not in parallel.'),
 'Machine learning for ionospheric TEC anomaly detection':(9,
  'Public data and laptop-scale, and honest false-alarm accounting would be a genuine correction — but the precursor field itself is contested, which caps how far the result travels.'),
 'Tsunami inundation modelling for the Bengal coast':(10,
  'Open-source tools, modest compute and enormous societal weight — but it sits outside your seismological core and wants a bathymetry and rupture-scenario collaborator.'),
 'Exposure, fragility and risk — not just hazard':(11,
  'No new instruments needed in principle, yet the building inventory is months of survey and remote sensing, and the modelling is structural engineering rather than seismology.'),
 'A 3-D basin velocity model and physics-based ground-motion simulation':(12,
  'High value and directly hazard-relevant, but constructing the velocity model is itself a multi-year project before a single simulation runs.'),
 'Full-waveform / adjoint tomography':(13,
  'The science case is strong — slab geometry below 150 km is still argued over — but the HPC allocation is the gate, and the groups competing already have one.'),
 'Distributed acoustic sensing on telecom dark fibre':(14,
  'Technically the cheapest dense array available in this region, but blocked on a dark-fibre agreement and an interrogator. That is an institutional negotiation, not a technical problem.'),
 'Dense nodal (large-N) array deployments':(15,
  'A funded field season and 100–300 rented nodes. Excellent second-half-of-PhD work once money exists; impossible before it.'),
 'Palaeoseismic trenching on the fold-belt faults':(16,
  'The only route to pre-instrumental recurrence on Kopili and Churachandpur–Mao, but it is permits, field seasons, radiocarbon budgets and a different discipline.'),
 'Ocean-bottom seismometers on the Rakhine–Bengal margin':(17,
  'The most consequential item on the list and the least reachable alone: ship time, an OBS pool and an international consortium. A proposal to join, not to lead.'),
}
assert sorted(r for r,_ in RANK.values())==list(range(1,len(RANK)+1)), 'ranks must be 1..N unique'
assert set(RANK)=={g[1] for g in GAPS}, 'RANK keys must match GAPS names exactly'
