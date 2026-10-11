import sys, asyncio
from playwright.async_api import async_playwright
async def main(pairs, w, h):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2)
        for src, dst in pairs:
            await pg.goto('file://' + src); await pg.wait_for_timeout(300)
            el = await pg.query_selector('table.sh')
            await (el.screenshot(path=dst) if el else pg.screenshot(path=dst, full_page=True))
        await b.close()
args = sys.argv[1:]; w, h = int(args[0]), int(args[1]); rest = args[2:]
asyncio.run(main(list(zip(rest[::2], rest[1::2])), w, h))
