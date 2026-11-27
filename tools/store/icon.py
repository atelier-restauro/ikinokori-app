import asyncio,base64
from playwright.async_api import async_playwright
JS=r'''
(()=>{
const N=64;
function mk(){const c=document.createElement('canvas');c.width=c.height=N;const g=c.getContext('2d');g.imageSmoothingEnabled=false;return [c,g]}
const hash=n=>{const x=Math.sin(n*127.1+311.7)*43758.5453;return x-Math.floor(x)};
const px=(g,x,y,w,h,c)=>{g.fillStyle=c;g.fillRect(x|0,y|0,w,h)};
const put=(g,s,x,y,k=1,left)=>{const w=s.width*k,h=s.height*k;g.save();if(left){g.translate(x,0);g.scale(-1,1);g.drawImage(s,-w/2,y-h/2,w,h)}else g.drawImage(s,x-w/2,y-h/2,w,h);g.restore()};
const out={};
// A：地層と海。黄色いちびの魚、右上から隕石
{const[c,g]=mk();const L=['#2b6c8a','#2b6c8a','#2b6c8a'];
 for(let y=0;y<N;y++)for(let x=0;x<N;x++){const h=hash(x*7.3+y*13.1);let col=h<.06?'#4f9bb5':h>.95?'#1d4d66':'#2b6c8a';
  const yy=y+Math.round(Math.sin(x*.18)*1.5);if(yy>46)col=['#a48b55','#8a6a3a','#c9b27a','#6b5a46','#a48b55'][Math.floor((yy-46)/4)%5];if(yy>46&&h<.05)col='#e0cc96';px(g,x,y,1,1,col)}
 put(g,spr({f:'fish',m:'trilo',r:3,c:'#efe3c4'}),14,55);
 for(let k=0;k<9;k++)px(g,44+k*2.2,15-k*1.6,k<4?3:2,2,k<3?'#fff2a0':k<6?'#ffc21a':'#ff7a3a');px(g,41,15,5,5,'#ffb020');px(g,42,16,3,3,'#fff2a0');
 put(g,spr({f:'fish',r:9,c:'#ffd23f',ex:0,pl:1,fr:1}),31,31);
 out.A=c.toDataURL()}
// B：観測窓。丸い窓の中にちびの魚、外は宇宙船の壁
{const[c,g]=mk();px(g,0,0,N,N,'#262b36');for(let y=0;y<N;y+=8)px(g,0,y,N,1,'#1b1f27');
 const R=27,cx=32,cy=32;for(let y=0;y<N;y++)for(let x=0;x<N;x++){const d=Math.hypot(x+.5-cx,y+.5-cy);if(d<R+3&&d>=R)px(g,x,y,1,1,d<R+1?'#0b0e14':'#7d889e');else if(d<R){const h=hash(x*3.1+y*9.7);px(g,x,y,1,1,y>46?(h<.1?'#5f9a4a':'#4f7434'):h<.06?'#74b8c4':h>.96?'#2c6470':'#3f8a9a')}}
 for(const[a,b]of[[8,8],[55,8],[8,55],[55,55]])px(g,a,b,2,2,'#7d889e');
 put(g,spr({f:'fish',r:8,c:'#ffd23f',ex:2,pl:1,fr:1}),32,31);
 px(g,14,22,1,6,'#ffffff33');px(g,16,18,1,4,'#ffffff33');
 px(g,48,12,3,3,(1)?'#ff5a2b':'');
 out.B=c.toDataURL()}
// C：大絶滅。下から溶岩、上へ逃げるちびの恐竜と翼竜
{const[c,g]=mk();for(let y=0;y<N;y++)for(let x=0;x<N;x++){const h=hash(x*5.1+y*3.3);px(g,x,y,1,1,y<20?(h<.04?'#ffffff':'#3a1e2a'):h<.08?'#9ec46a':'#6f9a4a')}
 for(let y=0;y<20;y++)for(let x=0;x<N;x++)if(hash(x+y*91)<.03)px(g,x,y,1,1,'#ffd0a0');
 for(let x=0;x<N;x++){const top=48+Math.round(Math.sin(x*.35)*2);px(g,x,top,1,N-top,'#ff4e1a');if(x%3==0)px(g,x,top-2,1,1,'#ff4e1a');if(hash(x*2)<.3)px(g,x,top+3,1,1,'#ffc21a')}
 for(let k=0;k<7;k++)px(g,58-k*2,4+k*2,3,2,k<2?'#fff2a0':k<4?'#ffc21a':'#ff7a3a');
 put(g,spr({f:'mamm',r:8,c:'#ffd23f',ex:2,pl:1,fr:1}),30,33);
 for(const[x,y]of[[44,22],[47,20],[46,24]])px(g,x,y,1,2,'#8fdcff');
 out.C=c.toDataURL()}
return out})()
'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(); await pg.goto('file:///home/claude/qa/expose.html'); await pg.wait_for_timeout(800)
        out=await pg.evaluate(JS)
        for k,v in out.items(): open(f'ic_{k}_64.png','wb').write(base64.b64decode(v.split(',')[1]))
        await b.close()
asyncio.run(main())
