import os as _os
_D=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'data')+'/'
import json,html,collections
exec(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'gaps.py')).read())
S=_D
d=json.load(open(S+'final3.json'))
e=lambda s: html.escape(str(s or ''),quote=True)

QORD={'Q1':1,'Q2':2,'Q3':3,'not indexed':4,'book series':5}
counts=collections.Counter(r['year'] for r in d)
years=list(range(1934,2027))
mx=max(counts.values())

# --- year bar strip
bars=[]
for y in years:
    c=counts.get(y,0)
    h=0 if not c else max(3, round(c/mx*100))
    cls=' zero' if not c else ''
    lbl=f'{y}: {c} paper{"s" if c!=1 else ""}'
    if c:
        bars.append(f'<button type="button" class="bar" style="--h:{h}%" data-y="{y}" data-c="{c}" '
                    f'title="{lbl} - click to filter" aria-pressed="false"><span class="sr">{lbl}</span></button>')
    else:
        bars.append(f'<div class="bar zero" data-y="{y}" data-c="0" title="{lbl}"><span class="sr">{lbl}</span></div>')

def authline(r):
    a=r.get('authors') or []
    if not a: return e(r.get('author') or 'Author not resolved')
    names=[x.split(',')[0].strip() for x in a if x.strip()]
    names=[n for n in names if n]
    if not names: return e(r.get('author') or '')
    if len(names)==1: return e(names[0])
    if len(names)==2: return e(f'{names[0]} & {names[1]}')
    return e(f'{names[0]} et al.')

rows=[]; last=None
for i,r in enumerate(d,1):
    y=r['year']
    if y!=last:
        rows.append(f'<li class="ymark" data-year="{y}"><span>{y}</span></li>')
        last=y
    q=r['quart']
    badge = f'<span class="q q{QORD.get(q,6)}">{e(q)}</span>' if q else (f'<span class="q q0">{e(r["kind"] or "not a journal article")}</span>')
    tec='<span class="tag-tec">TEC</span>' if 'TEC' in r['tags'] else ''
    if 'bvalue' in r['tags']: tec+='<span class="tag-bv">b-value</span>'
    if 'ML' in r['tags']: tec+='<span class="tag-ml">AI / ML</span>'
    if r.get('scope')=='context': tec+='<span class="tag-ctx">mentions IBR</span>'
    doi=r['doi']
    doilink=(f'<a class="doi" href="https://doi.org/{e(doi)}" target="_blank" rel="noopener">{e(doi)}</a>'
             if doi else '<span class="doi none">no DOI</span>')
    venue = e(r['journal']) if r['journal'] else e(r['kind'] or '—')
    ft=' '.join([r['title'],r['journal'] or '',r['author'] or '',' '.join(r.get('authors') or []),str(y),doi or '']).lower()
    rows.append(
      f'<li class="rec" data-q="{e(q or "none")}" data-tec="{1 if "TEC" in r["tags"] else 0}" '
      f'data-year="{y}" data-bv="{1 if "bvalue" in r["tags"] else 0}" '
      f'data-ml="{1 if "ML" in r["tags"] else 0}" data-src="{r["source"]}" '
      f'data-scope="{r.get("scope","focused")}" data-f="{e(ft)}">'
      f'<span class="n">{i}<em class="{"held" if r["source"]=="library" else "ref"}" title="{"PDF in your library" if r["source"]=="library" else "found via CrossRef - not in your library"}"></em></span>'
      f'<div class="body"><p class="t">{e(r["title"])}{tec}</p>'
      f'<p class="m"><span class="au">{authline(r)}</span><span class="sep">·</span>'
      f'<span class="v">{venue}</span></p></div>'
      f'<div class="right">{badge}{doilink}</div></li>')

COST={'archive':('Archive only','c-arch'),'compute':('Needs HPC','c-comp'),
      'field':('Field campaign','c-field'),'major':('Major infrastructure','c-major')}
STAT={'none here':('No regional study','s-none'),'one study':('One regional study','s-one'),
      'partial':('Partially done','s-part')}
TRK={'Seismology':'t-seis','AI / ML':'t-ml','Hazard':'t-haz'}
gap_html=[]
for rank,g in sorted((RANK[g[1]][0],g) for g in GAPS):
    tr,name,st,cost,proven,why,need,refs = g
    sl,sc=STAT[st]; cl,cc=COST[cost]
    gap_html.append(
      f'<article class="gap" id="gap{rank}"><div class="gh">'
      f'<span class="rank">{rank:02d}</span><h4>{e(name)}</h4>'
      f'<div class="gchips"><span class="gt {TRK[tr]}">{e(tr)}</span>'
      f'<span class="gs {sc}">{sl}</span><span class="gc {cc}">{cl}</span></div></div>'
      f'<dl><dt>Why this rank</dt><dd class="wr">{RANK[name][1]}</dd>'
      f'<dt>Proven elsewhere</dt><dd>{proven}</dd>'
      f'<dt>Why it fits here</dt><dd>{why}</dd>'
      f'<dt>What you would need</dt><dd>{need}</dd>'
      + (f'<dt>Read these</dt><dd class="refs">' + ' '.join(
          f'<a class="mref" href="https://doi.org/{e(r["doi"])}" target="_blank" rel="noopener">'
          f'<span class="rt">{e(r["t"])}</span>'
          + (f'<span class="rj">{e(r["j"])}</span>' if r["j"] else '')
          + f'<span class="rd">{e(r["doi"])}</span></a>' for r in refs) + '</dd>' if refs else '')
      + '</dl></article>')
ngap=len(GAPS); narch=sum(1 for g in GAPS if g[3]=='archive')

stats=collections.Counter(r['quart'] or 'other' for r in d)
ntec=sum(1 for r in d if 'TEC' in r['tags'])
nbv=sum(1 for r in d if 'bvalue' in r['tags'])
nml=sum(1 for r in d if 'ML' in r['tags'])
nlib=sum(1 for r in d if r['source']=='library')
nfoc=sum(1 for r in d if r.get('scope')=='focused')
nctx=len(d)-nfoc
ndoi=sum(1 for r in d if r['doi'])

HTML=f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Indo-Burma Ranges Bibliography</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
:root{{
  --paper:#F4F6F3; --surface:#FFFFFF; --surface2:#EDF0EC;
  --ink:#16211F; --ink2:#3C4A46; --muted:#6E7A75; --rule:#DCE1DB;
  --accent:#0F5F58; --accent2:#14766C; --accent-soft:#DCEBE7;
  --rust:#9A4520; --rust-soft:#F3E2D8;
  --gold:#7A5A17; --gold-soft:#F0E7D2;
  --viol:#4B3E86; --viol-soft:#E4E1F1;
  --q1:#0F5F58; --q2:#4A7F78; --q3:#7E948F; --q4:#94A09B; --q5:#8A9490; --q0:#98A29D;
  --shadow:0 1px 2px rgba(20,40,36,.06);
}}
@media (prefers-color-scheme:dark){{
  :root:not([data-theme="light"]){{
    --paper:#0E1513; --surface:#151E1B; --surface2:#1B2622;
    --ink:#E7ECE9; --ink2:#BFC9C5; --muted:#8D9A95; --rule:#26332F;
    --accent:#5CBBAD; --accent2:#7ACEC1; --accent-soft:#173029;
    --rust:#D98A5E; --rust-soft:#33231A;
    --gold:#C7A34E; --gold-soft:#2C2617;
    --viol:#A79BE0; --viol-soft:#221E33;
    --q1:#5CBBAD; --q2:#4E938A; --q3:#7E948F; --q4:#7A8681; --q5:#788480; --q0:#7A8681;
    --shadow:0 1px 2px rgba(0,0,0,.4);
  }}
}}
:root[data-theme="dark"]{{
  --paper:#0E1513; --surface:#151E1B; --surface2:#1B2622;
  --ink:#E7ECE9; --ink2:#BFC9C5; --muted:#8D9A95; --rule:#26332F;
  --accent:#5CBBAD; --accent2:#7ACEC1; --accent-soft:#173029;
  --rust:#D98A5E; --rust-soft:#33231A;
  --gold:#C7A34E; --gold-soft:#2C2617;
  --viol:#A79BE0; --viol-soft:#221E33;
  --q1:#5CBBAD; --q2:#4E938A; --q3:#7E948F; --q4:#7A8681; --q5:#788480; --q0:#7A8681;
  --shadow:0 1px 2px rgba(0,0,0,.4);
}}
*{{box-sizing:border-box}}
body{{background:var(--paper);color:var(--ink);
  font-family:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}}
.sr{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}
.wrap{{max-width:1020px;margin:0 auto;padding:0 24px 96px}}
a{{color:var(--accent)}}
:focus-visible{{outline:2px solid var(--accent);outline-offset:2px;border-radius:3px}}

header.top{{padding:52px 0 26px;border-bottom:1px solid var(--rule)}}
.eyebrow{{font-family:"IBM Plex Mono",monospace;font-size:11.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--muted);margin:0 0 14px}}
h1{{font-family:Spectral,Georgia,serif;font-weight:600;font-size:clamp(30px,4.4vw,46px);
  line-height:1.1;letter-spacing:-.015em;margin:0 0 14px;text-wrap:balance;max-width:22ch}}
.lede{{font-family:Spectral,Georgia,serif;font-size:17.5px;line-height:1.62;color:var(--ink2);
  max-width:64ch;margin:0 0 4px}}
.lede em{{color:var(--ink)}}

.stats{{display:flex;flex-wrap:wrap;gap:0;margin:30px 0 0;border-top:1px solid var(--rule)}}
.stat{{flex:1 1 128px;padding:16px 18px 14px;border-right:1px solid var(--rule)}}
.stat:last-child{{border-right:0}}
.stat b{{display:block;font-family:"IBM Plex Mono",monospace;font-size:25px;font-weight:500;
  color:var(--ink);font-variant-numeric:tabular-nums;line-height:1.15}}
.stat span{{display:block;font-size:11.5px;letter-spacing:.07em;text-transform:uppercase;
  color:var(--muted);margin-top:5px}}

section.strip{{margin:38px 0 0}}
.strip h2,.listhead h2{{font-family:"IBM Plex Mono",monospace;font-size:11.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--muted);font-weight:400;margin:0 0 14px}}
.chart{{display:flex;align-items:flex-end;gap:2px;height:104px;
  border-bottom:1px solid var(--rule);padding-bottom:0}}
.bar{{flex:1 1 0;min-width:0;height:var(--h);background:var(--accent);
  border:0;padding:0;font:inherit;color:inherit;-webkit-appearance:none;appearance:none;
  border-radius:2px 2px 0 0;position:relative;cursor:pointer;
  transition:background .12s,opacity .12s}}
.bar.zero{{height:2px;background:var(--rule);border-radius:0;cursor:default}}
button.bar:hover{{background:var(--accent2)}}
button.bar::after{{content:"";position:absolute;left:-1px;right:-1px;top:-10px;bottom:0}}
.bar.muted{{opacity:.26}}
.bar.sel,button.bar.sel:hover{{background:var(--rust)}}
.chart.picking button.bar:not(.sel){{opacity:.34}}
.chart.picking button.bar:not(.sel):hover{{opacity:.7}}
.ysel{{display:flex;align-items:center;gap:11px;flex-wrap:wrap;margin:12px 0 0;
  font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--ink2)}}
.ysel b{{color:var(--rust);font-weight:500}}
#yclear{{font:inherit;font-size:11.5px;color:var(--muted);background:var(--surface);
  border:1px solid var(--rule);border-radius:999px;padding:3px 11px;cursor:pointer}}
#yclear:hover{{border-color:var(--rust);color:var(--rust)}}
.caption b{{color:var(--ink)}}
.axis{{display:flex;justify-content:space-between;font-family:"IBM Plex Mono",monospace;
  font-size:11px;color:var(--muted);margin-top:7px;font-variant-numeric:tabular-nums}}
.caption{{font-size:12.5px;color:var(--muted);margin:12px 0 0;max-width:62ch}}

section.gaps{{margin:52px 0 0;padding-top:34px;border-top:2px solid var(--ink)}}
.gaptitle{{font-family:Spectral,Georgia,serif;font-weight:600;font-size:clamp(23px,3vw,31px);
  line-height:1.16;margin:0 0 12px;letter-spacing:-.01em;text-wrap:balance;max-width:20ch}}
.gaplede{{font-size:14.5px;line-height:1.65;color:var(--ink2);max-width:66ch;margin:0 0 26px}}
.gaplist{{display:flex;flex-direction:column;gap:0}}
.rankaxis{{border-left:2px solid var(--rule);padding-left:14px}}
.startbox{{background:var(--surface);border:1px solid var(--rule);
  border-left:3px solid var(--rust);border-radius:6px;padding:16px 19px;margin:0 0 28px}}
.startbox h3{{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--rust);margin:0 0 8px;font-weight:400}}
.startbox p{{margin:0 0 9px;font-size:14.5px;line-height:1.62;color:var(--ink2);max-width:70ch}}
.startbox p:last-child{{margin:0}}
.startbox b{{color:var(--ink);font-weight:600}}
.rank{{font-family:"IBM Plex Mono",monospace;font-size:12.5px;font-weight:500;
  color:var(--surface);background:var(--ink);border-radius:4px;padding:2px 7px;
  font-variant-numeric:tabular-nums;position:relative;top:-1px}}
.gt{{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.06em;
  text-transform:uppercase;padding:3px 8px;border-radius:3px;white-space:nowrap;border:1px solid}}
.t-seis{{background:var(--accent-soft);color:var(--accent);border-color:var(--accent)}}
.t-ml{{background:var(--viol-soft);color:var(--viol);border-color:var(--viol)}}
.t-haz{{background:var(--rust-soft);color:var(--rust);border-color:var(--rust)}}
dd.wr{{font-family:Spectral,Georgia,serif;font-size:15px;font-style:italic;color:var(--ink)}}
article.gap{{padding:17px 0;border-bottom:1px solid var(--rule)}}
.gh{{display:flex;gap:14px;align-items:baseline;flex-wrap:wrap;margin-bottom:9px}}
.gh h4{{font-family:Spectral,Georgia,serif;font-size:18px;font-weight:600;margin:0;
  line-height:1.28;flex:1 1 300px;color:var(--ink)}}
.gchips{{display:flex;gap:6px;flex-wrap:wrap}}
.gs,.gc{{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.06em;
  text-transform:uppercase;padding:3px 8px;border-radius:3px;white-space:nowrap}}
.s-none{{background:var(--rust);color:#fff}}
.s-one,.s-part{{background:var(--gold-soft);color:var(--gold);border:1px solid var(--gold)}}
.c-arch{{background:var(--accent);color:var(--surface)}}
.c-comp{{background:var(--accent-soft);color:var(--accent);border:1px solid var(--accent)}}
.c-field,.c-major{{background:transparent;color:var(--muted);border:1px solid var(--rule)}}
article.gap dl{{margin:0;display:grid;grid-template-columns:132px 1fr;gap:5px 18px;align-items:baseline}}
article.gap dt{{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.07em;
  text-transform:uppercase;color:var(--muted);padding-top:2px}}
article.gap dd{{margin:0;font-size:14.5px;line-height:1.6;color:var(--ink2);max-width:70ch}}
article.gap dd b{{color:var(--ink);font-weight:600}}
dd.refs{{display:flex;flex-wrap:wrap;gap:7px;margin-top:3px}}
a.mref{{display:flex;flex-direction:column;gap:1px;text-decoration:none;
  background:var(--surface);border:1px solid var(--rule);border-radius:5px;
  padding:6px 10px;transition:border-color .12s,background .12s;max-width:250px}}
a.mref:hover{{border-color:var(--accent);background:var(--accent-soft)}}
a.mref .rt{{font-size:13px;color:var(--ink);font-weight:500;line-height:1.3}}
a.mref .rj{{font-size:11.5px;color:var(--muted);font-style:italic;line-height:1.3;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
a.mref .rd{{font-family:"IBM Plex Mono",monospace;font-size:10px;color:var(--accent);
  margin-top:2px;word-break:break-all;line-height:1.25}}
h2.listhead2{{font-family:Spectral,Georgia,serif;font-weight:600;font-size:clamp(23px,3vw,31px);
  margin:54px 0 0;padding-top:32px;border-top:2px solid var(--ink);letter-spacing:-.01em}}
@media (max-width:640px){{article.gap dl{{grid-template-columns:1fr;gap:2px}}
  article.gap dt{{margin-top:8px}}}}
.controls{{position:sticky;top:0;z-index:20;background:var(--paper);
  padding:16px 0 13px;margin:34px 0 0;border-bottom:1px solid var(--rule);
  display:flex;flex-wrap:wrap;gap:10px;align-items:center}}
#q{{flex:1 1 240px;min-width:190px;font:inherit;font-size:14px;color:var(--ink);
  background:var(--surface);border:1px solid var(--rule);border-radius:6px;padding:8px 11px}}
#q::placeholder{{color:var(--muted)}}
.chips{{display:flex;gap:6px;flex-wrap:wrap}}
.chip{{font:inherit;font-size:12.5px;color:var(--ink2);background:var(--surface);
  border:1px solid var(--rule);border-radius:999px;padding:6px 13px;cursor:pointer;
  white-space:nowrap;transition:.12s}}
.chip:hover{{border-color:var(--accent)}}
.chip[aria-pressed="true"]{{background:var(--accent);border-color:var(--accent);color:var(--surface)}}
.chip.tec[aria-pressed="true"]{{background:var(--rust);border-color:var(--rust);color:#fff}}
.chip.bv[aria-pressed="true"]{{background:var(--gold);border-color:var(--gold);color:#fff}}
.chip.ml[aria-pressed="true"]{{background:var(--viol);border-color:var(--viol);color:#fff}}
.count{{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--muted);
  margin-left:auto;font-variant-numeric:tabular-nums}}

ol.list{{list-style:none;margin:0;padding:0}}
li.ymark{{font-family:"IBM Plex Mono",monospace;font-size:12px;letter-spacing:.1em;
  color:var(--muted);padding:26px 0 8px;border-bottom:1px solid var(--rule);
  position:sticky;top:59px;background:var(--paper);z-index:10}}
li.ymark span{{color:var(--ink);font-size:14px;letter-spacing:.02em}}
li.rec{{display:grid;grid-template-columns:38px 1fr 190px;gap:14px;align-items:start;
  padding:13px 0;border-bottom:1px solid var(--rule)}}
li.rec .n{{font-family:"IBM Plex Mono",monospace;font-size:11.5px;color:var(--muted);
  padding-top:3px;font-variant-numeric:tabular-nums}}
li.rec .t{{font-family:Spectral,Georgia,serif;font-size:16.5px;line-height:1.4;
  margin:0 0 3px;color:var(--ink)}}
li.rec .m{{margin:0;font-size:13px;color:var(--muted)}}
li.rec .au{{color:var(--ink2)}}
li.rec .sep{{margin:0 6px;opacity:.55}}
li.rec .v{{font-style:italic}}
.right{{display:flex;flex-direction:column;align-items:flex-end;gap:5px;padding-top:2px}}
.q{{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.06em;
  text-transform:uppercase;padding:2px 8px;border-radius:3px;white-space:nowrap;
  color:var(--surface);background:var(--q0)}}
.q1{{background:var(--q1)}} .q2{{background:var(--q2)}} .q3{{background:var(--q3)}}
.q4{{background:var(--q4)}} .q5{{background:var(--q5)}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]) .q{{color:#0E1513}}}}
:root[data-theme="dark"] .q{{color:#0E1513}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]) .c-arch{{color:#0E1513}}
  :root:not([data-theme="light"]) .s-none{{color:#0E1513}}}}
:root[data-theme="dark"] .c-arch,:root[data-theme="dark"] .s-none{{color:#0E1513}}
a.doi{{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--muted);
  text-decoration:none;word-break:break-all;text-align:right;line-height:1.35}}
a.doi:hover{{color:var(--accent);text-decoration:underline}}
.doi.none{{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--muted);opacity:.6}}
.tag-tec{{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.08em;
  color:var(--rust);background:var(--rust-soft);border-radius:3px;padding:1px 6px;
  margin-left:8px;vertical-align:2px;white-space:nowrap}}
.tag-bv{{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.08em;
  color:var(--gold);background:var(--gold-soft);border-radius:3px;padding:1px 6px;
  margin-left:6px;vertical-align:2px;white-space:nowrap}}
.tag-ctx{{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.06em;
  color:var(--muted);border:1px solid var(--rule);border-radius:3px;padding:0 6px;
  margin-left:6px;vertical-align:2px;white-space:nowrap}}
.tag-ml{{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.08em;
  color:var(--viol);background:var(--viol-soft);border-radius:3px;padding:1px 6px;
  margin-left:6px;vertical-align:2px;white-space:nowrap}}
li.rec .n em{{display:block;width:5px;height:5px;border-radius:50%;margin-top:5px}}
li.rec .n em.held{{background:var(--accent)}}
li.rec .n em.ref{{border:1px solid var(--muted)}}
.empty{{padding:44px 0;color:var(--muted);font-family:Spectral,Georgia,serif;font-size:17px}}
footer{{margin-top:44px;padding-top:22px;border-top:1px solid var(--rule);
  font-size:13px;color:var(--muted);max-width:70ch}}
footer p{{margin:0 0 9px}}
footer b{{color:var(--ink2);font-weight:600}}
@media (max-width:720px){{
  li.rec{{grid-template-columns:30px 1fr;gap:10px}}
  .right{{grid-column:2;flex-direction:row;align-items:center;gap:10px;flex-wrap:wrap}}
  a.doi{{text-align:left}}
  .chart{{height:74px}}
}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important}}}}
</style>
</head>
<body>

<div class="wrap">
<header class="top">
  <p class="eyebrow">Indo-Burma Ranges · Northeast India · 1934 – 2026</p>
  <h1>Sixty-four years of the Indo-Burma Ranges</h1>
  <p class="lede">Every paper, book and thesis on the <em>Indo-Burma Ranges, Northeast India
  and the adjoining Myanmar–Bengal margin</em> — the local library swept together with a
  CrossRef search of the published record — in strict chronological order, from a 1934 survey of
  India's oil and gas to Pn-anisotropy imaging of the subducting slab in 2026.
  Ionospheric TEC, b-value and AI/ML papers stay in the same sequence, flagged rather than
  split off. A closing section sets out {ngap} methods proven on other complex margins that
  this record shows have never been tried here.</p>
  <div class="stats">
    <div class="stat"><b>{len(d)}</b><span>Entries</span></div>
    <div class="stat"><b>{stats.get('Q1',0)}</b><span>Q1 journal</span></div>
    <div class="stat"><b>{stats.get('Q2',0)}</b><span>Q2 journal</span></div>
    <div class="stat"><b>{ndoi}</b><span>With DOI</span></div>
    <div class="stat"><b>{nfoc}</b><span>Focused on IBR</span></div>
    <div class="stat"><b>{nctx}</b><span>Mention IBR</span></div>
    <div class="stat"><b>{nlib}</b><span>In your library</span></div>
    <div class="stat"><b>{nbv}</b><span>b-value</span></div>
    <div class="stat"><b>{ntec}</b><span>TEC</span></div>
    <div class="stat"><b>{nml}</b><span>AI / ML</span></div>
  </div>
</header>

<section class="strip">
  <h2>Publications per year</h2>
  <div class="chart" id="chart">{''.join(bars)}</div>
  <div class="axis"><span>1934</span><span>1957</span><span>1980</span><span>2003</span><span>2026</span></div>
  <p class="ysel" id="ysel" hidden><span id="ynames"></span><button type="button" id="yclear">clear year filter</button></p>
  <p class="caption"><b>Click any bar to filter the bibliography to that year.</b> Click further bars to
  add years, click a selected bar again to drop it, or clear the filter to see the whole run. Bars fade
  as you search or filter, so the strip always shows how much of each year survives the current filter.
  One bar per year, 1934–2026; ticks on the baseline mark years with no publication found. Output is thin
  for three decades, lifts through the 1990s, then climbs steeply after the 2004 Sumatra–Andaman
  earthquake and the spread of continuous GPS — more than half of everything here was published
  since 2015.</p>
</section>

<section class="gaps">
  <h2 class="gaptitle">Methods proven elsewhere, not yet tried here</h2>
  <p class="gaplede">{ngap} approaches that are standard practice on other structurally complex
  margins — Cascadia, Nankai, Hikurangi, Sumatra, California, the Himalayan front — and that the
  {len(d)} entries above show have not been applied to the Indo-Burma Ranges. Each is anchored to
  where it was proven, most often to a method paper already sitting in your own library.
  <b>{narch} of them need nothing but the archive you already hold.</b> The three tracks — seismology,
  AI/ML and hazard — are now interleaved by rank rather than grouped, and each card carries its track
  as a chip.</p>
  <p class="gaplede rankaxis"><b>They are ranked 1–{ngap}, most startable first.</b> The order is a
  judgement, not a measurement. Each opening is scored on what could begin with the archive and the one
  GPU you already have, how novel the regional result would be, and how much the answer would matter —
  with ties broken towards work that unlocks the items below it. It assumes <b>no field budget and no
  ship time</b>. Ranks 14–17 are held back by money, permits and partnerships rather than by science, so
  tell me your actual compute, network access and funding and the order will change.</p>
  <div class="startbox">
    <h3>Start here — a concrete first experiment</h3>
    <p><b>Rank 01, and it needs nothing you do not already hold.</b> Take the merged ISC / NEIC / IMD
    catalogue for 22–28° N, 90–96° E, 1964–2025. Re-estimate M<sub>c</sub> and <i>b</i> with the
    b-positive estimator of van der Elst (2021), then run the b-significant test of Mirwald et al.
    (2024) — both papers are already in your library — against the spatial and temporal b-variations
    claimed in the {nbv} b-value papers listed below. Report which of those claimed anomalies survive
    a significance test and which do not.</p>
    <p>No new data, no GPU, no permissions, and no dependency on anything else on this list. It is a
    Short Note in length, it corrects the method of your own subfield rather than adding another
    application of it, and it leaves you with the completeness and declustering machinery that ranks
    07 and 08 need anyway.</p>
  </div>
  <div class="gaplist">{''.join(gap_html)}</div>
  <p class="caption">Absence was checked by CrossRef query, not assumed: "no regional study" means a
  targeted search returned no Indo-Burma or Northeast India result. Absence of a DOI-indexed paper is
  not proof no one has tried — check for grey literature and theses before writing a proposal on it.</p>
</section>

<h2 class="listhead2">The bibliography</h2>
<div class="controls">
  <input id="q" type="search" placeholder="Search title, author, journal, DOI…" aria-label="Search the bibliography">
  <div class="chips">
    <button class="chip" data-q="Q1" aria-pressed="false">Q1</button>
    <button class="chip" data-q="Q2" aria-pressed="false">Q2</button>
    <button class="chip" data-q="Q3" aria-pressed="false">Q3</button>
    <button class="chip" data-q="other" aria-pressed="false">Books &amp; theses</button>
    <button class="chip tec" data-tec="1" aria-pressed="false">TEC only</button>
    <button class="chip bv" data-bv="1" aria-pressed="false">b-value only</button>
    <button class="chip ml" data-ml="1" aria-pressed="false">AI / ML only</button>
    <button class="chip" data-src="library" aria-pressed="false">In my library</button>
    <button class="chip" data-scope="focused" aria-pressed="false">Focused on IBR</button>
    <button class="chip" data-scope="context" aria-pressed="false">Mentions IBR</button>
  </div>
  <span class="count" id="count">{len(d)} of {len(d)}</span>
</div>

<div class="listhead"></div>
<ol class="list" id="list">
{chr(10).join(rows)}
</ol>
<p class="empty" id="empty" hidden>No entry matches that filter.</p>

<footer>
  <p><b>Ordering.</b> Strictly by year of publication, oldest first; within a year, by journal
  then title. The numbering runs straight through the sequence.</p>
  <p><b>Two scopes, one sequence.</b> {nfoc} entries are <i>about</i> the Indo-Burma region —
  its name is in the title. {nctx} more, marked <span class="tag-ctx">mentions IBR</span>, are
  wider-scope studies that cover the region as one component: India–Asia collision
  reconstructions, Sunda and global subduction comparisons, Himalayan and Bengal-fan work,
  all-India seismicity and hazard compilations. They were found by searching OpenAlex over
  abstracts and full text and keeping only records whose <b>abstract</b> names the region while
  the title does not. Filter with <i>Focused on IBR</i> / <i>Mentions IBR</i>.</p>
  <p><b>What was thrown out.</b> Matching on the abstract alone also caught papers that merely
  name the region in passing — Bengal arsenic hydrochemistry, monsoon and cyclone meteorology,
  a mollusc description, several humanities and policy articles. <b>58 such entries were removed</b>
  by a topical filter: a wider-scope record must read as earth science and must not belong to one of
  those off-topic subjects. The filter never touches an entry whose PDF is in your library, and never
  touches the {nfoc} focused entries, which were gated on their titles in the first place. The
  discarded list is kept at <code>_scripts/data/dropped_offtopic.txt</code> — check it before
  claiming this bibliography is exhaustive.</p>
  <p><b>Where each entry came from.</b> A filled dot beside the number means the PDF is in your
  local library ({nlib} entries); a hollow dot means it was found by searching CrossRef across
  the published record and you do not hold it ({len(d)-nlib} entries). Use the
  <i>In my library</i> filter to separate them.</p>
  <p><b>Quartiles.</b> Q1/Q2/Q3 are the journal's best Scimago (SJR) subject-area quartile as
  of the most recent ranking. Scimago's bulk table is behind a bot challenge, so these were
  assigned from journal-level knowledge rather than pulled from the live file —
  <b>re-check any quartile you intend to quote in a submission</b>. Legacy titles carry their
  successor's standing (e.g. <i>Journal of Southeast Asian Earth Sciences</i> → <i>Journal of
  Asian Earth Sciences</i>). Books, memoir chapters and theses are labelled by kind instead.</p>
  <p><b>DOIs.</b> Resolved through CrossRef — first from the DOI printed in the PDF, then by
  bibliographic title match. {len(d)-ndoi} entries carry no DOI: theses, scanned books, an
  unpublished comment and two in-house reports.</p>
  <p><b>Coverage.</b> The CrossRef sweep ran twenty regional queries (Indo-Burma, Indo-Myanmar,
  Sagaing, Shillong, Kopili, Naga Hills, Bengal basin, and others), kept only records whose
  <i>title</i> carries both a regional and an earth-science term, and dropped conference
  abstracts. It is thorough, not exhaustive — CrossRef misses work that was never assigned a
  DOI, which is most Indian journal literature before about 1990.</p>
  <p><b>Tags.</b> <span class="tag-tec">TEC</span> marks ionospheric total-electron-content work;
  <span class="tag-bv">b-value</span> marks papers deriving a Gutenberg–Richter <i>b</i>, a
  magnitude of completeness, or spatial/temporal seismicity parameters;
  <span class="tag-ml">AI / ML</span> marks machine-learning and neural-network seismology.
  All three are filters, not sections — the sequence stays strictly chronological.</p>
</footer>
</div>

<script>
(function(){{
  var list=document.getElementById('list'), q=document.getElementById('q'),
      count=document.getElementById('count'), empty=document.getElementById('empty'),
      recs=Array.prototype.slice.call(list.querySelectorAll('li.rec')),
      marks=Array.prototype.slice.call(list.querySelectorAll('li.ymark')),
      chips=Array.prototype.slice.call(document.querySelectorAll('.chip')),
      chart=document.getElementById('chart'),
      bars=Array.prototype.slice.call(chart.querySelectorAll('.bar')),
      ybox=document.getElementById('ysel'), ynames=document.getElementById('ynames'),
      yclear=document.getElementById('yclear'), controls=document.querySelector('.controls'),
      total=recs.length, qsel=new Set(), tec=false, bv=false, mlf=false, srcf=false,
      scp=new Set(), ysel=new Set();

  function apply(){{
    var term=q.value.trim().toLowerCase(), shown=0, live={{}}, base={{}};
    recs.forEach(function(r){{
      var qv=r.dataset.q, cat=(qv==='Q1'||qv==='Q2'||qv==='Q3')?qv:'other';
      // every filter EXCEPT the year: this is what the bar heights report
      var ok=(qsel.size===0||qsel.has(cat)) &&
             (!tec||r.dataset.tec==='1') && (!bv||r.dataset.bv==='1') &&
             (!mlf||r.dataset.ml==='1') && (!srcf||r.dataset.src==='library') &&
             (scp.size===0||scp.has(r.dataset.scope)) &&
             (!term||r.dataset.f.indexOf(term)>-1);
      if(ok){{base[r.dataset.year]=1;}}
      var vis=ok&&(ysel.size===0||ysel.has(r.dataset.year));
      r.hidden=!vis;
      if(vis){{shown++;live[r.dataset.year]=1;}}
    }});
    marks.forEach(function(m){{m.hidden=!live[m.dataset.year];}});
    bars.forEach(function(b){{
      var y=b.dataset.y, on=ysel.has(y);
      b.classList.toggle('sel',on);
      b.classList.toggle('muted', b.dataset.c!=='0' && !base[y]);
      if(b.tagName==='BUTTON'){{b.setAttribute('aria-pressed',on?'true':'false');}}
    }});
    chart.classList.toggle('picking',ysel.size>0);
    if(ysel.size){{
      var ys=Array.prototype.slice.call(ysel).sort();
      ynames.innerHTML='Year filter: <b>'+ys.join(', ')+'</b>';
      ybox.hidden=false;
    }} else {{ybox.hidden=true;}}
    count.textContent=shown+' of '+total;
    empty.hidden=shown>0;
  }}
  q.addEventListener('input',apply);
  bars.forEach(function(b){{
    if(b.tagName!=='BUTTON'){{return;}}
    b.addEventListener('click',function(){{
      var y=b.dataset.y, first=ysel.size===0;
      if(ysel.has(y)){{ysel['delete'](y);}} else {{ysel.add(y);}}
      apply();
      // jump to the list only when opening the filter, not while adding years
      if(first&&ysel.size){{controls.scrollIntoView({{behavior:'smooth',block:'start'}});}}
    }});
  }});
  yclear.addEventListener('click',function(){{ysel.clear();apply();}});
  chips.forEach(function(c){{
    c.addEventListener('click',function(){{
      var on=c.getAttribute('aria-pressed')!=='true';
      c.setAttribute('aria-pressed',on?'true':'false');
      if(c.dataset.tec){{tec=on;}}
      else if(c.dataset.bv){{bv=on;}}
      else if(c.dataset.ml){{mlf=on;}}
      else if(c.dataset.src){{srcf=on;}}
      else if(c.dataset.scope){{on?scp.add(c.dataset.scope):scp.delete(c.dataset.scope);}}
      else{{on?qsel.add(c.dataset.q):qsel.delete(c.dataset.q);}}
      apply();
    }});
  }});
}})();
</script>
</body>
</html>
'''
open(_os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),'ibr.html'),'w').write(HTML)
print('wrote',len(HTML),'bytes;',len(d),'entries')
