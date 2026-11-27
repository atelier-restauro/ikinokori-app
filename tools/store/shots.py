import asyncio,json
from playwright.async_api import async_playwright
T={'form':'dino','size':8,'spd':1.05,'jaw':1,'shell':1,'pal':0,'dash':1,'tags':[]}
M={'tut':1,'runs':4,'best':4,'dex':{'fish':1,'amph':1,'rept':1,'reptJ':1,'dinoJ':1,'dinoJS':1,'mamm':1,'syn':1},'fp':12,'mseen':{'fin':1,'quick':1},
   'save':{'no':4,'gen':10,'era':4,'T':T,'stock':[dict(T,shell=0),dict(T,form='ptero',size=6,jaw=0,shell=0)],'asc':0,'hist':[],'rescued':0}}
SAVE="localStorage.setItem('ikinokori-v2',JSON.stringify(%s))"%json.dumps(M,ensure_ascii=False)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        c=await b.new_context(viewport={'width':360,'height':640},device_scale_factor=3,is_mobile=True,has_touch=True)
        pg=await c.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script(SAVE)
        await pg.goto('file:///home/claude/qa/expose.html'); await pg.wait_for_timeout(3500)
        await pg.screenshot(path='ss1_title.png')
        await pg.click('[data-act="play"]'); await pg.click('[data-act="cont"]')
        await pg.evaluate("G.P.inv=99"); await pg.wait_for_timeout(4000)
        await pg.evaluate("G.P.growth=.46"); await pg.wait_for_timeout(4200)
        await pg.evaluate("G.P.inv=0"); await pg.wait_for_timeout(60)
        await pg.screenshot(path='ss2_play.png'); await pg.evaluate("G.P.inv=99")
        await pg.evaluate("G.layEggs()"); await pg.wait_for_timeout(500); await pg.screenshot(path='ss3_kids.png')
        await pg.click('.kid'); await pg.wait_for_timeout(300)
        await pg.evaluate("G.P.inv=99;G.startEvent()"); await pg.wait_for_timeout(400); await pg.screenshot(path='ss4_mini.png')
        await pg.click('.mini'); await pg.wait_for_timeout(14000); await pg.evaluate('G.P.inv=0'); await pg.wait_for_timeout(60); await pg.screenshot(path='ss5_event.png')
        print(errs); await b.close()
asyncio.run(main())
