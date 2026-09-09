"""Regenerate IBR_bibliography.csv / .md and IBR_method_gaps.md from data/final3.json."""
import os,json,csv,re
_H=os.path.dirname(os.path.abspath(__file__)); _D=os.path.join(_H,'data')+'/'
OUT=os.path.dirname(_H)+'/'
d=json.load(open(_D+'final3.json'))
exec(open(os.path.join(_H,'gaps.py')).read())
tg=lambda r:' '.join(x for x in (('TEC' if 'TEC' in r['tags'] else ''),
    ('b-value' if 'bvalue' in r['tags'] else ''),('AI/ML' if 'ML' in r['tags'] else '')) if x)
with open(OUT+'IBR_bibliography.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['#','Year','Authors','Title','Journal / kind','Quartile','DOI','Tags','Scope','Held locally'])
    for i,r in enumerate(d,1):
        w.writerow([i,r['year'],'; '.join(a.strip(', ') for a in (r.get('authors') or [])) or (r.get('author') or ''),
            r['title'],r['journal'] or (r['kind'] or ''),r['quart'] or (r['kind'] or ''),r['doi'] or '',
            tg(r),r.get('scope','focused'),'yes' if r['source']=='library' else 'no'])
nlib=sum(1 for r in d if r['source']=='library')
strip=lambda t: re.sub(r'<[^>]+>','',t).replace('&amp;','&')
with open(OUT+'IBR_method_gaps.md','w') as f:
    f.write('# Methods proven elsewhere, not yet applied to the Indo-Burma Ranges\n\n')
    f.write(f"{len(GAPS)} approaches standard on other complex margins, checked against {len(d)} regional publications.\n"
            f"{sum(1 for g in GAPS if g[3]=='archive')} need nothing but data already in hand.\n\n")
    f.write('Ranked 1-%d, most startable first. The order scores each opening on what could begin with the\n'
            'archive and one GPU already in hand, how novel the regional result would be, and how much the\n'
            'answer would matter, with ties broken towards work that unlocks the items below it. It assumes\n'
            'no field budget and no ship time: ranks 14-17 are held back by money and permissions, not by\n'
            'science. It is a judgement, not a measurement.\n' % len(GAPS))
    for rank,g in sorted((RANK[g[1]][0],g) for g in GAPS):
        t,name,st,cost,proven,why,need,refs = g
        f.write(f"\n## {rank:02d}. {name}\n\n**Track:** {t} · **Status:** {st} · **Cost:** {cost}\n\n"
                f"- **Why this rank:** {strip(RANK[name][1])}\n"
                f"- **Proven elsewhere:** {strip(proven)}\n- **Why it fits here:** {strip(why)}\n"
                f"- **What you need:** {strip(need)}\n")
        if refs:
            f.write("- **Read these:**\n")
            for r in refs:
                j=f" — *{r['j']}*" if r['j'] else ''
                f.write(f"    - {r['t']}{j} — [{r['doi']}](https://doi.org/{r['doi']})\n")
with open(OUT+'IBR_bibliography.md','w') as f:
    f.write('# Indo-Burma Ranges & Northeast India — chronological bibliography (1934–2026)\n\n')
    f.write(f"{len(d)} entries, oldest first. {sum(1 for r in d if r.get('scope')=='focused')} focused on the region, {sum(1 for r in d if r.get('scope')=='context')} wider-scope studies that mention it. {nlib} held locally as PDFs.\n\n")
    f.write(f"Quartile = journal best SJR quartile (assigned from journal knowledge — verify before quoting). "
            f"Tags: TEC ({sum(1 for r in d if 'TEC' in r['tags'])}), b-value ({sum(1 for r in d if 'bvalue' in r['tags'])}), "
            f"AI/ML ({sum(1 for r in d if 'ML' in r['tags'])}). See `IBR_method_gaps.md`.\n\n")
    f.write('| # | Year | Author | Title | Journal / kind | Q | DOI | Tags | Scope | Held |\n|--:|--:|---|---|---|---|---|---|---|---|\n')
    for i,r in enumerate(d,1):
        a=(r.get('authors') or [None])[0]; a=a.split(',')[0].strip() if a else (r.get('author') or '—')
        if r.get('authors') and len(r['authors'])>1: a+=' et al.'
        doi=f"[{r['doi']}](https://doi.org/{r['doi']})" if r['doi'] else '—'
        f.write(f"| {i} | {r['year']} | {a} | {r['title'].replace('|','/')} | "
                f"{(r['journal'] or r['kind'] or '—').replace('|','/')} | {r['quart'] or '—'} | {doi} | {tg(r)} "
                f"| {'yes' if r['source']=='library' else ''} |\n")
print(f'exported {len(d)} entries + {len(GAPS)} gaps to {OUT}')
