import asyncio, os
from playwright.async_api import async_playwright
async def go():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        pg = await b.new_page(viewport={'width': 1080, 'height': 1080})
        await pg.goto('file://' + os.path.abspath('video/v.html')); await pg.wait_for_timeout(800)
        os.makedirs('video/f', exist_ok=True)
        for i in range(13 * 30):
            await pg.evaluate(f'seek({i/30})')
            await pg.screenshot(path=f'video/f/{i:04d}.png')
        await b.close()
asyncio.run(go())
