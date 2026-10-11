import render, asyncio, os, subprocess, shutil
from ui import *
FR="../img/frames"; shutil.rmtree(FR,ignore_errors=True); os.makedirs(FR)
tabs="".join(f'<div class="chip" data-i="{i}">{t}</div>' for i,t in enumerate(TABS))
feats=["Fully automated formulas","Debt payoff + savings goals","Overspending turns red","Instant digital download"]
fe="".join(f'<div class="ft" data-i="{i}"><span>✓</span>{f}</div>' for i,f in enumerate(feats))
html=page(f'''
<style>
#stage{{position:absolute;inset:0;overflow:hidden}}
.sc{{position:absolute;inset:0;opacity:0}}
.w{{display:inline-block;will-change:transform}}
.chip{{position:absolute;left:50%;padding:22px 40px;border-radius:999px;background:#fff;font-weight:800;font-size:40px;color:{G};box-shadow:0 12px 30px rgba(40,50,40,.12);white-space:nowrap}}
.ft{{display:flex;align-items:center;gap:26px;font-size:50px;font-weight:700;margin:26px 0;opacity:0}} .ft span{{width:70px;height:70px;border-radius:50%;background:{G};color:#fff;display:grid;place-items:center;font-size:40px;flex:none}}
.tbar>div{{transform-origin:left}} .mb{{transform-origin:bottom}}
.ic{{width:100%;height:100%}}
</style>
<div id=stage>
<!-- S1 titre -->
<div class=sc id=s1><div style="position:absolute;top:110px;left:0;right:0;text-align:center">
<div id=kick style="font-size:34px;font-weight:700;color:{CO};letter-spacing:.16em">GOOGLE SHEETS + EXCEL · 2027</div>
<div style="font-family:'Inter Display',Inter;font-size:112px;font-weight:900;line-height:.98;color:{G};margin-top:18px;letter-spacing:-.02em"><span class=w id=w1>ANNUAL</span> <span class=w id=w2>BUDGET</span><br><span class=w id=w3>SPREADSHEET</span></div></div>
<div id=pill style="position:absolute;left:90px;top:470px;background:{CO};color:#fff;font-weight:900;font-size:44px;padding:16px 34px;border-radius:999px">7 AUTO TABS</div></div>
<!-- laptop partagé S1-S3 -->
<div id=cam style="position:absolute;inset:0;transform-origin:22% 72%">
<div id=lap style="position:absolute;left:115px;top:560px;opacity:0">{laptop(dashboard("10.6px"),850)}</div></div>
<div class=sc id=s3txt><div id=cap style="position:absolute;left:0;right:0;top:0;padding:56px 60px 40px;background:linear-gradient(#F3F0EA 82%,rgba(243,240,234,0));text-align:center;font-size:62px;font-weight:900;color:{G}">See exactly where your money goes</div></div>
<!-- S4 onglets -->
<div class=sc id=s4><div style="position:absolute;top:110px;left:0;right:0;text-align:center;font-family:'Inter Display',Inter;font-size:92px;font-weight:900;color:{G}">7 tabs. One file.</div>{tabs}
<div id=bdg style="position:absolute;bottom:90px;left:0;right:0">{badges(size=86)}</div></div>
<!-- S5 arguments + fin -->
<div class=sc id=s5><div style="position:absolute;left:120px;top:150px">{fe}</div>
<div id=end style="position:absolute;left:0;right:0;bottom:120px;text-align:center;opacity:0"><div style="font-size:40px;color:{MUT};font-weight:600">Start budgeting today</div><div style="font-family:'Inter Display',Inter;font-size:96px;font-weight:900;color:{G}">Oakfold</div></div></div>
</div>
<script>
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const cl=(x)=>Math.max(0,Math.min(1,x)), r=(t,a,b)=>cl((t-a)/(b-a));
const eo=x=>1-Math.pow(1-x,3), eio=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2, back=x=>{{const c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)}};
const kpis=$$('.k b'), kv=kpis.map(e=>parseFloat(e.textContent.replace(/[$,]/g,'')));
const bars=$$('.tbar>div'), mbs=$$('.mb'), dn=$('.dn');
const rows=$$('.ct tr');
function seek(t){{
  // S1
  const s1in=1, s1out=1-r(t,4.6,5.0); $('#s1').style.opacity=s1out;
  $('#kick').style.opacity=eo(r(t,0,.5)); $('#kick').style.transform=`translateY(${{(1-eo(r(t,0,.5)))*20}}px)`;
  ['#w1','#w2','#w3'].forEach((s,i)=>{{const p=eo(r(t,.15+i*.14,.75+i*.14));$(s).style.transform=`translateY(${{(1-p)*80}}px)`;$(s).style.opacity=p}});
  const pp=back(r(t,1.0,1.5)); $('#pill').style.transform=`scale(${{pp}}) rotate(-6deg)`; $('#pill').style.opacity=r(t,1.0,1.1);
  // laptop
  const lp=eo(r(t,.9,1.9)); const lout=1-r(t,8.0,8.4);
  $('#lap').style.opacity=Math.min(lp,lout); $('#lap').style.transform=`translateY(${{(1-lp)*260}}px)`;
  // compteurs, barres, anneau
  const c=eo(r(t,1.6,3.0)); kpis.forEach((e,i)=>e.textContent='$'+Math.round(kv[i]*c).toLocaleString('en-US'));
  bars.forEach((b,i)=>b.style.transform=`scaleX(${{eo(r(t,1.8+i*.05,2.8+i*.05))}})`);
  mbs.forEach((b,i)=>b.style.transform=`scaleY(${{eo(r(t,2.2+i*.06,3.0+i*.06))}})`);
  const d=eo(r(t,1.8,3.2))*360; dn.style.webkitMask=dn.style.mask=`conic-gradient(#000 ${{d}}deg, transparent ${{d}}deg)`;
  // S2→S3 : montée de caméra puis zoom sur le tableau
  const up=eio(r(t,4.4,5.4)), z=eio(r(t,5.4,6.8));
  $('#cam').style.transform=`translateY(${{-up*330}}px) scale(${{1+z*.8}})`;
  $('#s3txt').style.opacity=Math.min(eo(r(t,5.0,5.5)),1-r(t,7.9,8.3)); $('#cap').style.transform=`translateY(${{(1-eo(r(t,5.0,5.6)))*30}}px)`;
  // ligne mise en avant
  rows.forEach(x=>x.style.background='');
  if(t>6.6&&t<8.3){{const row=rows[2]; const a=eo(r(t,6.6,7.0)); row.style.background=`rgba(255,242,198,${{a}})`}}
  // S4
  $('#s4').style.opacity=Math.min(r(t,8.2,8.6),1-r(t,10.6,11.0));
  $$('.chip').forEach((e,i)=>{{const p=back(r(t,8.4+i*.12,8.9+i*.12)); const side=i%2?1:-1; const y=250+i*78;
     const x=side*(180)+(1-p)*side*700; e.style.transform=`translate(calc(-50% + ${{x}}px),0)`; e.style.top=y+'px'; e.style.opacity=r(t,8.4+i*.12,8.6+i*.12)}});
  const bp=eo(r(t,9.4,10.0)); $('#bdg').style.transform=`translateY(${{(1-bp)*160}}px)`; $('#bdg').style.opacity=bp;
  // S5
  $('#s5').style.opacity=r(t,10.8,11.1);
  $$('.ft').forEach((e,i)=>{{const p=eo(r(t,11.0+i*.18,11.5+i*.18)); e.style.opacity=p; e.style.transform=`translateX(${{(1-p)*-60}}px)`}});
  const ep=eo(r(t,11.9,12.5)); $('#end').style.opacity=ep; $('#end').style.transform=`scale(${{.9+.1*ep}})`;
}}
window.seek=seek; seek(0);
</script>''',w=1080,h=1080)
open("../img/html/video.html","w").write(html)
from playwright.async_api import async_playwright
async def go():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg=await b.new_page(viewport={"width":1080,"height":1080}); await pg.set_content(html); await pg.wait_for_timeout(400)
        N=13*30
        for i in range(N):
            await pg.evaluate(f"seek({i/30})"); await pg.screenshot(path=f"{FR}/f{i:04d}.png")
        await b.close()
asyncio.run(go())
subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","30","-i",f"{FR}/f%04d.png","-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-shortest","-c:v","libx264","-profile:v","main","-pix_fmt","yuv420p","-crf","20","-movflags","+faststart","-c:a","aac","-b:a","64k","../img/video.mp4"],check=True)
print("ok")
