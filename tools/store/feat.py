import asyncio,base64
from playwright.async_api import async_playwright
JS=r'''
(async()=>{await document.fonts.load('40px DotGothic16');
const W=128,H=63,c=document.createElement('canvas');c.width=W;c.height=H;const g=c.getContext('2d');g.imageSmoothingEnabled=false;
const hash=n=>{const x=Math.sin(n*127.1+311.7)*43758.5453;return x-Math.floor(x)};
const px=(x,y,w,h,col)=>{g.fillStyle=col;g.fillRect(x|0,y|0,w,h)};
const put=(s,x,y,k=1,left)=>{const w=s.width*k,h=s.height*k;g.save();if(left){g.translate(x,0);g.scale(-1,1);g.drawImage(s,-w/2,y-h/2,w,h)}else g.drawImage(s,x-w/2,y-h/2,w,h);g.restore()};
for(let y=0;y<H;y++)for(let x=0;x<W;x++){const h=hash(x*7.3+y*13.1);let col=h<.06?'#4f9bb5':h>.95?'#1d4d66':'#2b6c8a';const yy=y+Math.round(Math.sin(x*.18)*1.5);if(yy>48)col=['#a48b55','#8a6a3a','#c9b27a','#6b5a46','#a48b55'][Math.floor((yy-48)/4)%5];if(yy>48&&h<.05)col='#e0cc96';px(x,y,1,1,col)}
put(spr({f:'fish',m:'trilo',r:3,c:'#efe3c4'}),18,57);put(spr({f:'fish',m:'trilo',r:3,c:'#efe3c4'}),100,59,1,1);
for(let k=0;k<9;k++)px(112+k*2.2,10-k*1.6,k<4?3:2,2,k<3?'#fff2a0':k<6?'#ffc21a':'#ff7a3a');px(109,10,5,5,'#ffb020');px(110,11,3,3,'#fff2a0');
put(spr({f:'fish',r:7,c:'#ffd23f',pl:1,fr:1,ex:1}),28,28);
put(spr({f:'amph',r:5,c:'#8fe07a',pl:1}),54,40);put(spr({f:'mamm',r:4,c:'#d8b48a',pl:1,ex:1}),100,40,1,1);put(spr({f:'bird',r:4,c:'#4fd6e6',pl:1}),112,30,1,1);
const o=document.createElement('canvas');o.width=1024;o.height=500;const G=o.getContext('2d');G.imageSmoothingEnabled=false;G.drawImage(c,0,0,1024,504);
G.textAlign='center';G.lineJoin='round';G.font='92px DotGothic16';G.lineWidth=14;G.strokeStyle='#1a0f08';G.strokeText('イキノコリ！',612,168);G.fillStyle='#ffd23f';G.fillText('イキノコリ！',612,168);
G.font='44px DotGothic16';G.lineWidth=10;G.strokeText('大絶滅5回の旅',612,236);G.fillStyle='#fff3dc';G.fillText('大絶滅5回の旅',612,236);
return o.toDataURL()})()
'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(); await pg.goto('file:///home/claude/qa/expose.html'); await pg.wait_for_timeout(800)
        v=await pg.evaluate(JS); open('feature.png','wb').write(base64.b64decode(v.split(',')[1])); await b.close()
asyncio.run(main())
