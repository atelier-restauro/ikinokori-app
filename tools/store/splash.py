import asyncio,base64
from playwright.async_api import async_playwright
JS=r'''
(async()=>{await document.fonts.load('40px DotGothic16');
const c=document.createElement('canvas');c.width=c.height=2732;const g=c.getContext('2d');g.imageSmoothingEnabled=false;
g.fillStyle='#16110b';g.fillRect(0,0,2732,2732);
const s=spr({f:'fish',r:9,c:'#ffd23f',pl:1,fr:1});const k=16;g.drawImage(s,1366-s.width*k/2,1180-s.height*k/2,s.width*k,s.height*k);
g.textAlign='center';g.fillStyle='#fff3dc';g.font='200px DotGothic16';g.fillText('イキノコリ！',1366,1620);
g.fillStyle='#c9b08c';g.font='96px DotGothic16';g.fillText('大絶滅5回の旅',1366,1760);
g.fillStyle='#ffc21a';for(let x=0;x<2732;x+=56){g.beginPath();g.moveTo(x,1840);g.lineTo(x+28,1840);g.lineTo(x+8,1864);g.lineTo(x-20,1864);g.fill()}
return c.toDataURL()})()
'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(); await pg.goto('file:///home/claude/qa/expose.html'); await pg.wait_for_timeout(800)
        v=await pg.evaluate(JS); open('splash.png','wb').write(base64.b64decode(v.split(',')[1])); await b.close()
asyncio.run(main())
