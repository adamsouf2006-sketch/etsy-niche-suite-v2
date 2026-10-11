# Composants visuels communs à tous les produits (cadres, icônes Sheets/Excel).
INK="#1F2A24"
money=lambda v,d=0: ("-" if v<0 else "")+"$"+f"{abs(v):,.{d}f}"
SHEETS_ICON='''<svg viewBox="0 0 48 64" class="ic"><path d="M4 0h28l16 16v44a4 4 0 0 1-4 4H4a4 4 0 0 1-4-4V4a4 4 0 0 1 4-4z" fill="#1E9E5A"/><path d="M32 0l16 16H36a4 4 0 0 1-4-4z" fill="#8ED1AC"/><rect x="10" y="28" width="28" height="22" rx="1.5" fill="#fff"/><path d="M10 35.3h28M10 42.6h28M20 28v22" stroke="#1E9E5A" stroke-width="2.4"/></svg>'''
EXCEL_ICON='''<svg viewBox="0 0 64 64" class="ic"><rect x="18" y="6" width="42" height="52" rx="4" fill="#33A06A"/><path d="M39 6h17a4 4 0 0 1 4 4v14H39z" fill="#5CC08B"/><path d="M39 24h21v16H39z" fill="#2A8A59"/><path d="M39 40h21v14a4 4 0 0 1-4 4H39z" fill="#1F6E46"/><rect x="2" y="16" width="34" height="32" rx="4" fill="#185C3A"/><path d="M11 24l14 16M25 24L11 40" stroke="#fff" stroke-width="4.2" stroke-linecap="round"/></svg>'''
FONT="<style>*{box-sizing:border-box;margin:0}body{font-family:Inter,'DejaVu Sans',sans-serif;color:"+INK+"}</style>"
def laptop(inner,w):
    return f'''<div style="width:{w}px"><div style="background:#1E2421;border-radius:{w*.03}px {w*.03}px 0 0;padding:{w*.022}px {w*.022}px {w*.03}px;box-shadow:0 {w*.04}px {w*.08}px rgba(40,50,40,.28)"><div style="aspect-ratio:16/10;overflow:hidden;border-radius:4px">{inner}</div></div>
<div style="height:{w*.035}px;background:linear-gradient(#D6D9D7,#A9AEAB);margin:0 -{w*.07}px;border-radius:0 0 {w*.06}px {w*.06}px;position:relative"><div style="position:absolute;left:42%;width:16%;top:0;height:35%;background:#9CA19E;border-radius:0 0 8px 8px"></div></div></div>'''
def tablet(inner,w,ratio="4/3"):
    return f'''<div style="width:{w}px;background:#1E2421;border-radius:{w*.05}px;padding:{w*.035}px;box-shadow:0 {w*.05}px {w*.1}px rgba(40,50,40,.32)"><div style="aspect-ratio:{ratio};overflow:hidden;border-radius:{w*.015}px">{inner}</div></div>'''
def badges(color=INK,size=92):
    return f'''<div style="display:flex;gap:56px;justify-content:center;align-items:center;font-weight:700;font-size:{size*.5}px;color:{color}"><div style="display:flex;align-items:center;gap:20px"><div style="height:{size}px;width:{size*.75}px">{SHEETS_ICON}</div>Google Sheets</div><div style="display:flex;align-items:center;gap:20px"><div style="height:{size}px;width:{size}px">{EXCEL_ICON}</div>Excel</div></div><style>.ic{{width:100%;height:100%}}</style>'''
