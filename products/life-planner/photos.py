# Listing photos 2000x2500 built from real renders in r/*.png
import os, sys
D = os.path.abspath('r'); OUT = os.path.abspath('photos')
TEAL, CREAM, SAND, CORAL, INK, SAGE = '#1F4E5A', '#FBF7F1', '#E9DCC9', '#E07A5F', '#1E2B2F', '#A8C3A0'
BASE = f'''<html><head><meta charset="utf-8"><style>
@font-face{{font-family:I;src:local("Inter")}}
*{{box-sizing:border-box;margin:0;padding:0}} body{{width:2000px;height:2500px;overflow:hidden;font-family:Inter,Arial,sans-serif;color:{INK}}}
.img{{display:block;border-radius:14px;box-shadow:0 30px 70px rgba(20,40,45,.28),0 6px 18px rgba(20,40,45,.18);background:#fff}}
.laptop{{position:absolute;background:#22272b;border-radius:34px 34px 0 0;padding:34px 34px 46px}}
.laptop img{{display:block;width:100%;border-radius:4px}}
.base{{position:absolute;height:44px;background:linear-gradient(#d9dde0,#a9afb4);border-radius:0 0 40px 40px}}
.pill{{display:inline-block;border-radius:999px;font-weight:800}}
.h{{font-weight:900;letter-spacing:-2px;line-height:.95}}
.chip{{display:inline-block;background:#fff;border:3px solid {TEAL};color:{TEAL};border-radius:18px;padding:18px 30px;font-size:46px;font-weight:800;margin:0 10px}}
</style></head><body>'''
def page(name, body):
    p = f'{OUT}/{name}.html'; open(p, 'w').write(BASE + body + '</body></html>'); return p
I = lambda n: f'file://{D}/{n}.png'
pages = {}
# ---- MAIN A: cream, laptop dashboard + side cards
pages['main_a'] = page('main_a', f'''
<div style="position:absolute;inset:0;background:linear-gradient(180deg,{CREAM},#F2EADF)"></div>
<div style="position:absolute;top:110px;width:100%;text-align:center">
 <div class="h" style="font-size:190px;color:{TEAL}">LIFE PLANNER</div>
 <div class="h" style="font-size:118px;color:{INK};margin-top:14px;letter-spacing:-1px">SPREADSHEET</div>
 <div style="font-size:58px;margin-top:34px;color:#4a5a5e;font-weight:600">Budget · Tasks · Habits · Meals · Goals</div>
</div>
<div class="laptop" style="left:170px;top:760px;width:1660px"><img src="{I('dash')}"></div>
<div class="base" style="left:90px;top:1955px;width:1820px"></div>
<img class="img" src="{I('habits')}" style="position:absolute;left:60px;top:1700px;width:880px;transform:rotate(-3deg)">
<img class="img" src="{I('budget')}" style="position:absolute;left:1400px;top:1480px;width:520px;transform:rotate(3deg)">
<div class="pill" style="position:absolute;right:90px;top:560px;background:{CORAL};color:#fff;width:330px;height:330px;border-radius:50%;text-align:center;padding-top:72px;transform:rotate(8deg);box-shadow:0 18px 40px rgba(224,122,95,.4)">
 <div style="font-size:150px;line-height:1">14</div><div style="font-size:54px;margin-top:6px">TABS</div></div>
<div style="position:absolute;bottom:90px;width:100%;text-align:center">
 <span class="chip">Google Sheets</span><span class="chip">Excel</span><span class="chip" style="background:{TEAL};color:#fff">Undated</span></div>
''')
# ---- MAIN B: dark teal, fanned screenshots
pages['main_b'] = page('main_b', f'''
<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 30%,#2b6676,{TEAL} 60%,#173c45)"></div>
<div style="position:absolute;top:120px;width:100%;text-align:center;color:#fff">
 <div style="font-size:64px;font-weight:700;color:{SAND};letter-spacing:10px">ALL-IN-ONE</div>
 <div class="h" style="font-size:200px;margin-top:20px">LIFE PLANNER</div>
 <div style="font-size:66px;margin-top:30px;font-weight:600;color:{SAND}">Google Sheets &amp; Excel Spreadsheet</div>
</div>
<img class="img" src="{I('budget')}" style="position:absolute;left:80px;top:900px;width:760px;transform:rotate(-8deg)">
<img class="img" src="{I('habits')}" style="position:absolute;left:1020px;top:960px;width:900px;transform:rotate(7deg)">
<img class="img" src="{I('dash')}" style="position:absolute;left:300px;top:850px;width:1400px;z-index:2">
<div style="position:absolute;left:0;right:0;top:1900px;text-align:center;z-index:3">
 <span class="pill" style="background:{CORAL};color:#fff;font-size:84px;padding:30px 70px">14 LINKED TABS</span></div>
<div style="position:absolute;bottom:110px;width:100%;text-align:center;color:#fff;font-size:58px;font-weight:600">Budget · Tasks · Habits · Meals · Cleaning · Goals</div>
''')
# ---- MAIN C: sand, tablet w/ dashboard, stacked tabs left
pages['main_c'] = page('main_c', f'''
<div style="position:absolute;inset:0;background:{SAND}"></div>
<div style="position:absolute;left:110px;top:120px;width:1800px">
 <div class="h" style="font-size:176px;color:{TEAL}">Life Planner</div>
 <div class="h" style="font-size:176px;color:{CORAL}">Spreadsheet</div>
 <div style="font-size:60px;margin-top:30px;font-weight:600">Budget, tasks, habits &amp; meals in one file</div>
</div>
<div style="position:absolute;left:120px;top:760px;width:1760px;background:#22272b;border-radius:60px;padding:50px;box-shadow:0 40px 90px rgba(0,0,0,.3)"><img src="{I('dash')}" style="width:100%;display:block;border-radius:10px"></div>
<div class="pill" style="position:absolute;right:110px;top:150px;background:{CORAL};color:#fff;width:300px;height:300px;border-radius:50%;text-align:center;padding-top:62px;transform:rotate(8deg);box-shadow:0 18px 40px rgba(224,122,95,.4)"><div style="font-size:140px;line-height:1">14</div><div style="font-size:50px;margin-top:4px">TABS</div></div>
<div style="position:absolute;left:120px;top:2150px;width:1760px;display:flex;justify-content:space-between">
 {''.join(f'<span class="pill" style="background:#fff;color:{TEAL};font-size:50px;padding:24px 40px">{t}</span>' for t in ['Google Sheets','Excel','Undated','Any currency'])}
</div>
<div style="position:absolute;bottom:90px;width:100%;text-align:center;font-size:44px;color:#5b5047">Instant download · Example + blank copy included</div>
''')
# ---- 2 What you get
tabs = ['Dashboard', 'Setup', 'Money Log', 'Monthly Budget', 'Annual Overview', 'Savings & Debt', 'Task List', 'Habit Tracker', 'Cleaning Schedule', 'Goal Tracker', 'Weekly Planner', 'Meal Planner & Grocery List', 'Monthly Calendar', 'Start Here guide']
pages['p2'] = page('p2', f'''
<div style="position:absolute;inset:0;background:{CREAM}"></div>
<div style="position:absolute;top:120px;width:100%;text-align:center"><div class="h" style="font-size:130px;color:{TEAL}">What you get</div>
<div style="font-size:54px;margin-top:20px;color:#4a5a5e">One spreadsheet · 14 tabs that talk to each other</div></div>
<div style="position:absolute;left:150px;top:470px;width:1700px;columns:2;column-gap:80px">
{''.join(f'<div style="break-inside:avoid;display:flex;align-items:center;margin-bottom:46px;font-size:56px;font-weight:600"><span class="pill" style="flex:none;width:96px;height:96px;line-height:96px;text-align:center;background:{TEAL if i%2==0 else CORAL};color:#fff;font-size:44px;margin-right:34px">{i+1}</span>{t}</div>' for i,t in enumerate(tabs))}
</div>
<div style="position:absolute;bottom:120px;left:150px;right:150px;background:#fff;border-radius:30px;padding:46px;font-size:50px;text-align:center;box-shadow:0 10px 30px rgba(0,0,0,.08)">
 Files: <b>.xlsx</b> with example data + <b>.xlsx</b> blank · PDF quick-start guide</div>
''')
def shot(name, title, sub, img, w=1800, extra='', maxh=1820):
    pages[name] = page(name, f'''
<div style="position:absolute;inset:0;background:{CREAM}"></div>
<div style="position:absolute;top:130px;width:100%;text-align:center"><div class="h" style="font-size:120px;color:{TEAL}">{title}</div>
<div style="font-size:54px;margin-top:26px;color:#4a5a5e;padding:0 120px">{sub}</div></div>
<div style="position:absolute;top:560px;left:{(2000-w)//2}px;width:{w}px;height:{maxh}px;display:flex;justify-content:center;align-items:flex-start"><img class="img" src="{I(img)}" style="max-width:100%;max-height:100%"></div>{extra}''')
shot('p3', 'Budget that fills itself', 'Type each expense once in the Money Log. Actual, left to spend and safe-to-spend per day update instantly.', 'budget', 1400)
shot('p4', 'Habit tracker', '20 habits × 31 days. Type x — streak, total and month score are automatic.', 'habits', 1860)
shot('p5', 'Savings goals & debt payoff', 'Live progress bars for 12 savings goals and 12 debts.', 'savings', 1500)
shot('p6', 'Tasks & cleaning on autopilot', 'Due dates, days left and next cleaning dates are calculated for you.', 'tasks', 1800,
     f'<div style="position:absolute;top:1380px;left:100px;width:1800px;height:1020px;display:flex;justify-content:center"><img class="img" src="{I("cleaning")}" style="max-width:100%;max-height:100%"></div>', maxh=760)
shot('p7', 'Meal planner + grocery list', 'Plan the week, then shop by aisle.', 'meals', 1860)
shot('p8', 'Your whole year at a glance', 'The annual overview is built from your Money Log — nothing extra to type.', 'annual', 1860)
pages['p9'] = page('p9', f'''
<div style="position:absolute;inset:0;background:{TEAL}"></div>
<div style="position:absolute;top:140px;width:100%;text-align:center;color:#fff"><div class="h" style="font-size:130px">How it works</div></div>
{''.join(f'<div style="position:absolute;left:180px;top:{520+i*430}px;width:1640px;background:#fff;border-radius:36px;padding:56px 60px 56px 230px;font-size:56px;line-height:1.3"><span class="pill" style="position:absolute;left:56px;top:50%;margin-top:-65px;width:130px;height:130px;line-height:130px;text-align:center;background:{CORAL};color:#fff;font-size:70px">{i+1}</span><b>{a}</b><br><span style="color:#4a5a5e;font-size:48px">{b}</span></div>' for i,(a,b) in enumerate([("Download & open","Open the .xlsx in Excel, or upload it to Google Drive and open with Google Sheets."),("Setup in 2 minutes","Your name, currency, month and your own budget categories."),("Type once","Log money, tasks and habits — every tab updates itself."),("Reuse every month","Undated: change the month in Setup and keep going.")]))}
''')
pages['p10'] = page('p10', f'''
<div style="position:absolute;inset:0;background:{CREAM}"></div>
<div style="position:absolute;top:140px;width:100%;text-align:center"><div class="h" style="font-size:130px;color:{TEAL}">Good to know</div></div>
<div style="position:absolute;left:170px;top:470px;width:1660px;font-size:56px;line-height:1.35">
{''.join(f'<div style="display:flex;margin-bottom:56px"><span style="color:{CORAL};font-weight:900;margin-right:34px">✓</span><span>{t}</span></div>' for t in ["Digital download — nothing is shipped.","Works in Google Sheets (free) and Microsoft Excel 2016 or newer.","Not made for Apple Numbers.","Undated and reusable: any month, any year.","Any currency: type your symbol in Setup.","Example copy to explore + blank copy to start fresh.","Personal use. Templates only — not financial advice."])}
</div>
<div style="position:absolute;bottom:110px;width:100%;text-align:center;font-size:60px;font-weight:800;color:{TEAL}">Oakfold</div>
''')
if __name__ == '__main__':
    import asyncio
    from playwright.async_api import async_playwright
    only = sys.argv[1:] or list(pages)
    async def go():
        async with async_playwright() as p:
            b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
            pg = await b.new_page(viewport={'width': 2000, 'height': 2500})
            for n in only:
                await pg.goto('file://' + pages[n]); await pg.wait_for_timeout(400)
                await pg.screenshot(path=f'{OUT}/{n}.jpg', type='jpeg', quality=90)
            await b.close()
    asyncio.run(go())
