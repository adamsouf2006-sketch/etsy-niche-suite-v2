import sys,os,asyncio,subprocess,shutil,base64; sys.path.insert(0,os.path.abspath("../../commun"))
from mockups import FONT
from content import DOCS, ACC
ACC2="#FFB020"; INK="#1F2933"; MUT="#616E7C"; BG="#F2F0EC"
img=lambda n: "data:image/png;base64,"+base64.b64encode(open(f"../img/pages/{n}.png","rb").read()).decode()
FR="../img/frames"; shutil.rmtree(FR,ignore_errors=True); os.makedirs(FR)
cards="".join(f'<img class=pc src="{img(f"p{i+1:02d}")}" style="position:absolute;width:300px;left:390px;top:420px;box-shadow:0 14px 34px rgba(40,30,20,.25);border-radius:4px;opacity:0">' for i in range(8))
chips="".join(f'<div class=chip>{t}</div>' for t in ["Fillable PDF","Word","Google Docs","US Letter","A4"])
feats="".join(f'<div class=ft><span>✓</span>{t}</div>' for t in ["8 essential documents","Contract + change orders","Estimate, work order, invoice","Instant download"])
html=f'''<!doctype html><html><head><meta charset=utf-8>{FONT}<style>*{{margin:0;box-sizing:border-box}}body{{font-family:Inter,sans-serif;color:{INK};width:1080px;height:1080px;overflow:hidden;background:{BG}}}
.sc{{position:absolute;inset:0;opacity:0}} .w{{display:inline-block}}
.chip{{position:absolute;left:50%;padding:20px 40px;border-radius:999px;background:#fff;border:3px solid {ACC};font-weight:800;font-size:44px;color:{ACC};white-space:nowrap}}
.ft{{display:flex;align-items:center;gap:26px;font-size:52px;font-weight:700;margin:28px 0;opacity:0}} .ft span{{width:72px;height:72px;border-radius:50%;background:{ACC};color:#fff;display:grid;place-items:center;font-size:40px;flex:none}}</style></head><body>
<div class=sc id=s1 style="opacity:1"><div style="position:absolute;top:90px;left:0;right:0;text-align:center"><div id=kick style="font-size:34px;font-weight:800;color:{ACC2};letter-spacing:.14em">EDITABLE + FILLABLE</div>
<div style="font-family:'Inter Display',Inter;font-size:116px;font-weight:900;line-height:.96;color:{ACC};margin-top:16px"><span class=w id=w1>HANDYMAN</span><br><span class=w id=w2>BUSINESS</span> <span class=w id=w3>KIT</span></div></div>
<div id=badge style="position:absolute;right:70px;top:400px;width:190px;height:190px;border-radius:50%;background:{ACC2};display:grid;place-items:center;text-align:center;z-index:20"><div><div style="font-size:80px;font-weight:900;line-height:1">8</div><div style="font-size:26px;font-weight:800">DOCUMENTS</div></div></div></div>
{cards}
<div class=sc id=s2><div style="position:absolute;top:0;left:0;right:0;padding:50px 40px 30px;text-align:center;font-size:60px;font-weight:900;color:{ACC};background:linear-gradient({BG} 80%,rgba(242,240,236,0));z-index:5">Quote it. Sign it. Get paid.</div>
<div id=doc style="position:absolute;left:140px;top:170px;width:800px;transform-origin:50% 20%"><img src="{img("p02")}" style="width:800px;display:block;box-shadow:0 20px 50px rgba(40,30,20,.25)"><div id=fillwrap style="position:absolute;inset:0;overflow:hidden;clip-path:inset(0 0 100% 0)"><img src="{img("f02")}" style="width:800px;display:block"></div><div id=cur style="position:absolute;width:4px;height:26px;background:{ACC2};left:0;top:0"></div></div></div>
<div class=sc id=s3><div style="position:absolute;top:110px;left:0;right:0;text-align:center;font-family:'Inter Display',Inter;font-size:84px;font-weight:900;color:{ACC}">Every format you need</div>{chips}</div>
<div class=sc id=s4><div style="position:absolute;left:110px;top:150px">{feats}</div><div id=end style="position:absolute;left:0;right:0;bottom:120px;text-align:center;opacity:0"><div style="font-size:40px;color:{MUT};font-weight:600">Win jobs. Get paid. Stay protected.</div><div style="font-family:'Inter Display',Inter;font-size:96px;font-weight:900;color:{ACC}">Oakfold</div></div></div>
<script>
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const cl=x=>Math.max(0,Math.min(1,x)),r=(t,a,b)=>cl((t-a)/(b-a)),eo=x=>1-Math.pow(1-x,3),eio=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2,back=x=>{{const c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)}};
const pos=[[-350,70,-15],[-250,35,-10],[-150,10,-5],[-50,-5,-1],[50,-5,1],[150,10,5],[250,35,10],[350,70,15]];
window.seek=function(t){{
 $('#s1').style.opacity=1-r(t,4.2,4.6);
 $('#kick').style.opacity=eo(r(t,0,.5));
 ['#w1','#w2','#w3'].forEach((s,i)=>{{const p=eo(r(t,.1+i*.14,.7+i*.14));$(s).style.transform=`translateY(${{(1-p)*80}}px)`;$(s).style.opacity=p}});
 $('#badge').style.transform=`scale(${{back(r(t,1.8,2.3))}}) rotate(10deg)`;$('#badge').style.opacity=r(t,1.8,1.9);
 $$('.pc').forEach((e,i)=>{{const p=back(r(t,.6+i*.12,1.3+i*.12)),[x,y,a]=pos[i],out=eio(r(t,4,4.5));
   e.style.opacity=r(t,.6+i*.12,.8+i*.12)*(1-out);e.style.transform=`translate(${{x*p}}px,${{(1-p)*500+y*p+out*-80}}px) rotate(${{a*p}}deg)`;e.style.zIndex=10-Math.abs(i-3.5)}});
 const s2=Math.min(r(t,4.3,4.8),1-r(t,8.3,8.7));$('#s2').style.opacity=s2;
 const z=eio(r(t,5,6));$('#doc').style.transform=`scale(${{1+z*.35}}) translateY(${{-z*40}}px)`;
 const f=r(t,5.6,8.0);$('#fillwrap').style.clipPath=`inset(0 0 ${{(1-(.08+f*.72))*100}}% 0)`;
 $('#cur').style.top=(1035*(.08+f*.72)-30)+'px';$('#cur').style.left=(120+((t*6)%1)*300)+'px';$('#cur').style.opacity=(f>0&&f<1)?(Math.floor(t*4)%2?1:.2):0;
 $('#s3').style.opacity=Math.min(r(t,8.5,8.9),1-r(t,10.6,11));
 $$('.chip').forEach((e,i)=>{{const p=back(r(t,8.7+i*.15,9.2+i*.15)),s=i%2?1:-1;e.style.top=(290+i*120)+'px';e.style.transform=`translate(calc(-50% + ${{s*120+(1-p)*s*700}}px),0)`;e.style.opacity=r(t,8.7+i*.15,8.9+i*.15)}});
 $('#s4').style.opacity=r(t,10.8,11.1);
 $$('.ft').forEach((e,i)=>{{const p=eo(r(t,11+i*.18,11.5+i*.18));e.style.opacity=p;e.style.transform=`translateX(${{(1-p)*-60}}px)`}});
 const ep=eo(r(t,11.9,12.5));$('#end').style.opacity=ep;$('#end').style.transform=`scale(${{.9+.1*ep}})`;
}};seek(0);</script></body></html>'''
open("../img/html/video.html","w").write(html)
from playwright.async_api import async_playwright
async def go():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg=await b.new_page(viewport={"width":1080,"height":1080}); await pg.set_content(html); await pg.wait_for_timeout(500)
        for i in range(390): await pg.evaluate(f"seek({i/30})"); await pg.screenshot(path=f"{FR}/f{i:04d}.png")
        await b.close()
asyncio.run(go())
subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","30","-i",f"{FR}/f%04d.png","-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-shortest","-c:v","libx264","-profile:v","main","-pix_fmt","yuv420p","-crf","20","-movflags","+faststart","-c:a","aac","-b:a","64k","../img/video.mp4"],check=True)
from PIL import Image
fs=[20,50,80,120,165,200,235,280,330,385]; b=Image.new("RGB",(5*300,2*300))
for i,f in enumerate(fs): b.paste(Image.open(f"{FR}/f{f:04d}.png").resize((300,300)),((i%5)*300,(i//5)*300))
b.save("../img/video_contact.jpg"); shutil.rmtree(FR); print("ok")
