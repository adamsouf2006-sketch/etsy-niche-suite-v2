import sys,os; sys.path.insert(0,os.path.abspath("../../commun"))
import asyncio, subprocess, shutil
from ui2 import *
FR="../img/frames"; shutil.rmtree(FR,ignore_errors=True); os.makedirs(FR)
feats=["Automatic profit &amp; loss","Income, expenses, mileage","Quarterly tax set-aside","Google Sheets + Excel"]
fe="".join(f'<div class="ft"><span>✓</span>{f}</div>' for f in feats)
chips="".join(f'<div class="chip">{t}</div>' for t in TABS)
html=page(f'''<style>.sc{{position:absolute;inset:0;opacity:0}} .w{{display:inline-block}}
.chip{{position:absolute;left:50%;padding:20px 38px;border-radius:999px;background:#fff;font-weight:800;font-size:38px;color:{N};box-shadow:0 12px 30px rgba(20,35,60,.12);white-space:nowrap}}
.ft{{display:flex;align-items:center;gap:26px;font-size:50px;font-weight:700;margin:26px 0;opacity:0}} .ft span{{width:70px;height:70px;border-radius:50%;background:{N};color:#fff;display:grid;place-items:center;font-size:40px;flex:none}}</style>
<div class=sc id=s1 style="opacity:1"><div style="position:absolute;top:100px;left:0;right:0;text-align:center"><div id=kick style="font-size:34px;font-weight:800;color:{GO};letter-spacing:.16em">GOOGLE SHEETS + EXCEL</div>
<div style="font-family:'Inter Display',Inter;font-size:104px;font-weight:900;line-height:.98;color:{N};margin-top:18px"><span class=w id=w1>SMALL</span> <span class=w id=w2>BUSINESS</span><br><span class=w id=w3>BOOKKEEPING</span></div></div>
<div id=pill style="position:absolute;left:80px;top:455px;background:{GO};color:{INK};font-weight:900;font-size:42px;padding:16px 32px;border-radius:999px">8 AUTO TABS</div></div>
<div id=cam style="position:absolute;inset:0;transform-origin:30% 70%"><div id=lap style="position:absolute;left:115px;top:545px;opacity:0">{laptop(dashboard("10.6px"),850)}</div></div>
<div class=sc id=s3><div id=cap style="position:absolute;left:0;right:0;top:0;padding:56px 60px 40px;background:linear-gradient({BG} 82%,rgba(244,241,234,0));text-align:center;font-size:62px;font-weight:900;color:{N}">Know your profit in seconds</div></div>
<div class=sc id=s4><div style="position:absolute;top:100px;left:0;right:0;text-align:center;font-family:'Inter Display',Inter;font-size:88px;font-weight:900;color:{N}">8 tabs. One file.</div>{chips}<div id=bdg style="position:absolute;bottom:70px;left:0;right:0">{badges(size=80)}</div></div>
<div class=sc id=s5><div style="position:absolute;left:110px;top:150px">{fe}</div><div id=end style="position:absolute;left:0;right:0;bottom:120px;text-align:center;opacity:0"><div style="font-size:40px;color:{MUT};font-weight:600">Bookkeeping made easy</div><div style="font-family:'Inter Display',Inter;font-size:96px;font-weight:900;color:{N}">Oakfold</div></div></div>
<script>
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const cl=x=>Math.max(0,Math.min(1,x)),r=(t,a,b)=>cl((t-a)/(b-a)),eo=x=>1-Math.pow(1-x,3),eio=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2,back=x=>{{const c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)}};
const kv=$$('.kv'),vals=kv.map(e=>+e.dataset.v),mb=$$('.mb'),me=$$('.me'),cb=$$('.cb');
window.seek=function(t){{
 $('#s1').style.opacity=1-r(t,4.6,5.0);
 $('#kick').style.opacity=eo(r(t,0,.5));
 ['#w1','#w2','#w3'].forEach((s,i)=>{{const p=eo(r(t,.15+i*.14,.75+i*.14));$(s).style.transform=`translateY(${{(1-p)*80}}px)`;$(s).style.opacity=p}});
 $('#pill').style.transform=`scale(${{back(r(t,1,1.5))}}) rotate(-6deg)`;$('#pill').style.opacity=r(t,1,1.1);
 const lp=eo(r(t,.9,1.9));$('#lap').style.opacity=Math.min(lp,1-r(t,8,8.4));$('#lap').style.transform=`translateY(${{(1-lp)*260}}px)`;
 const c=eo(r(t,1.6,3));kv.forEach((e,i)=>e.textContent='$'+Math.round(vals[i]*c).toLocaleString('en-US'));
 mb.forEach((b,i)=>b.style.transform=`scaleY(${{eo(r(t,1.9+i*.05,2.8+i*.05))}})`);me.forEach((b,i)=>b.style.transform=`scaleY(${{eo(r(t,2.1+i*.05,3+i*.05))}})`);
 cb.forEach((b,i)=>b.style.transform=`scaleX(${{eo(r(t,2.2+i*.06,3.1+i*.06))}})`);
 const up=eio(r(t,4.4,5.4)),z=eio(r(t,5.4,6.8));$('#cam').style.transform=`translateY(${{-up*330}}px) scale(${{1+z*.8}})`;
 $('#s3').style.opacity=Math.min(eo(r(t,5,5.5)),1-r(t,7.9,8.3));
 $('#s4').style.opacity=Math.min(r(t,8.2,8.6),1-r(t,10.6,11));
 $$('.chip').forEach((e,i)=>{{const p=back(r(t,8.4+i*.1,8.9+i*.1)),s=i%2?1:-1;e.style.transform=`translate(calc(-50% + ${{s*180+(1-p)*s*700}}px),0)`;e.style.top=(230+i*74)+'px';e.style.opacity=r(t,8.4+i*.1,8.6+i*.1)}});
 const bp=eo(r(t,9.4,10));$('#bdg').style.transform=`translateY(${{(1-bp)*160}}px)`;$('#bdg').style.opacity=bp;
 $('#s5').style.opacity=r(t,10.8,11.1);
 $$('.ft').forEach((e,i)=>{{const p=eo(r(t,11+i*.18,11.5+i*.18));e.style.opacity=p;e.style.transform=`translateX(${{(1-p)*-60}}px)`}});
 const ep=eo(r(t,11.9,12.5));$('#end').style.opacity=ep;$('#end').style.transform=`scale(${{.9+.1*ep}})`;
}};seek(0);</script>''',w=1080,h=1080)
open("../img/html/video.html","w").write(html)
from playwright.async_api import async_playwright
async def go():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg=await b.new_page(viewport={"width":1080,"height":1080}); await pg.set_content(html); await pg.wait_for_timeout(400)
        for i in range(390):
            await pg.evaluate(f"seek({i/30})"); await pg.screenshot(path=f"{FR}/f{i:04d}.png")
        await b.close()
asyncio.run(go())
subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","30","-i",f"{FR}/f%04d.png","-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-shortest","-c:v","libx264","-profile:v","main","-pix_fmt","yuv420p","-crf","20","-movflags","+faststart","-c:a","aac","-b:a","64k","../img/video.mp4"],check=True)
from PIL import Image
fs=[15,45,75,105,165,200,265,300,340,385]; b=Image.new("RGB",(5*300,2*300),"white")
for i,f in enumerate(fs): b.paste(Image.open(f"{FR}/f{f:04d}.png").resize((300,300)),((i%5)*300,(i//5)*300))
b.save("../img/video_contact.jpg"); shutil.rmtree(FR); print("ok")
