import sys,asyncio
from playwright.async_api import async_playwright
async def main(pairs):
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        for html,out,w,h in pairs:
            pg=await b.new_page(viewport={"width":w,"height":h}); await pg.set_content(open(html).read()); await pg.wait_for_timeout(300)
            await pg.screenshot(path=out,type="jpeg",quality=92); await pg.close()
        await b.close()
def run(pairs): asyncio.run(main(pairs))
