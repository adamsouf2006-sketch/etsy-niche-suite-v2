import asyncio,os,zipfile,glob
from content import *
html=f'''<html><head><meta charset=utf-8><style>*{{margin:0;box-sizing:border-box}}body{{font-family:Carlito,sans-serif;color:#1F2937}}.pg{{width:8.5in;height:11in;padding:.7in;page-break-after:always;position:relative}}
h1{{font-size:34pt;color:{ACC}}} h2{{font-size:14pt;color:#fff;background:{ACC};padding:4px 10px;border-radius:4px;margin:18px 0 8px}} p,li{{font-size:11.5pt;line-height:1.45}} ol{{margin-left:20px}} li{{margin:5px 0}}
table{{width:100%;border-collapse:collapse;margin-top:6px}} td{{padding:7px 8px;border-bottom:1px solid #E5E7EB;font-size:11pt}} td:first-child{{color:{ACC};font-weight:700;width:40px}}</style></head><body>
<div class=pg><p style="color:#6B7280">{BRAND} · {KIT}</p><h1>START HERE</h1><p>Thank you for your purchase! This kit gives your home daycare or childcare program the 10 forms you need, from enrollment to daily reports.</p>
<h2>What's inside</h2><table>{"".join(f"<tr><td>{n}</td><td><b>{t}</b> - {s}</td></tr>" for n,t,s,_ in DOCS)}</table>
<h2>Two formats, two paper sizes</h2><p><b>Fillable PDF</b> - type directly in the fields with free Adobe Acrobat Reader (computer, tablet or phone), then save, print or email.<br><b>Word (.docx)</b> - edit everything: wording, prices, add your logo. Opens in Microsoft Word, Google Docs (File &gt; Open &gt; Upload) or Pages.<br>Each format comes in <b>US Letter</b> and <b>A4</b>.</p></div>
<div class=pg><h2>Quick start</h2><ol><li>Open the folder for your paper size (US-Letter or A4).</li><li>Open the Word files and "YOUR LOGO" with your logo; add your company details and prices (Price List, Agreement fees).</li><li>Save your own copies as PDF, or use the fillable PDFs as they are.</li><li>Give new families the Agreement, Enrollment, Medical, Pick-Up &amp; Photo Release forms. Use the Daily Report, Attendance Log, Medication and Incident forms every day.</li></ol>
<h2>Tips</h2><ol><li>Fillable PDFs: use Adobe Acrobat Reader for the best result; some browser viewers do not save typed fields.</li><li>Keep one folder per child with all signed forms; ask parents to update the Medical form every 6 months.</li><li>Store forms securely: they contain private family and health information.</li></ol>
<h2>Important</h2><p>These documents are general templates, not legal advice. Licensing rules and laws differ between states and countries: check your local requirements and have your agreements reviewed before using them.</p>
<h2>Need help?</h2><p>Send me a message on Etsy - I usually reply within 24 hours. If you enjoy the kit, a review helps my small shop a lot. Thank you!</p></div></body></html>'''
async def go():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"); pg=await b.new_page()
        await pg.set_content(html); await pg.pdf(path="../out/00 - START HERE.pdf",width="8.5in",height="11in",print_background=True); await b.close()
asyncio.run(go())
for size in ("US-Letter","A4"):
    with zipfile.ZipFile(f"../out/Childcare_Forms_Kit_{size}.zip","w",zipfile.ZIP_DEFLATED) as z:
        z.write("../out/00 - START HERE.pdf","00 - START HERE.pdf")
        for f in sorted(glob.glob(f"../out/{size}/*")):
            sub="Fillable PDF" if f.endswith(".pdf") else "Word"
            z.write(f,f"{sub}/{os.path.basename(f)}")
    print(size,os.path.getsize(f"../out/Childcare_Forms_Kit_{size}.zip")//1024,"Ko",len(zipfile.ZipFile(f"../out/Childcare_Forms_Kit_{size}.zip").namelist()),"fichiers")
