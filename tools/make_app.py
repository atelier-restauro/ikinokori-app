#!/usr/bin/env python3
"""公開ページの HTML から、アプリ版の game.html を作る。

使い方：python3 tools/make_app.py 公開ページ.html game.html

公開ページを更新したら、そのHTMLを取り出してこれを通し直す。
置きかえる文がひとつでも見つからなければ止まる（公開ページ側が変わったしるし）。

アプリ版でやること
- フォントをネットから読まず、使う文字だけにしぼって中に入れる（電波がなくても同じ字）
- 縦向きの画面いっぱい。上のノッチ・下のバーをよける
- ランキングは出さず、自分の記録（ベスト5）だけ
- 「ブラウザ」の言い方を「端末」に
- テスト版の番号と「感想を送る」（FEEDBACK_URL が空なら出さない）
"""
import base64, io, re, sys
from pathlib import Path
from fontTools import subset
from fontTools.ttLib import TTFont

APP_VER = 'β0.1（2026-11-27）'
FEEDBACK_URL = ''  # Googleフォームができたら入れる

ROOT = Path(__file__).resolve().parent.parent
src, dst = Path(sys.argv[1]), Path(sys.argv[2])
h = src.read_text(encoding='utf-8')


def rep(old, new, count=1):
    global h
    n = h.count(old)
    if n != count:
        sys.exit(f'見つかった数が {n}（{count} のはず）：{old[:80]}')
    h = h.replace(old, new)


# ---- 画面（縦・ノッチよけ・拡大しない） ----
rep('<meta name="viewport" content="width=device-width,initial-scale=1">',
    '<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">')
rep('<link rel="preconnect" href="https://fonts.googleapis.com">\n', '')
rep('<link href="https://fonts.googleapis.com/css2?family=DotGothic16&family=M+PLUS+1p:wght@400;700;800&display=swap" rel="stylesheet">\n', '/*FONTS*/\n')
APP_CSS = '''
/* アプリ版：画面いっぱい。上下のノッチ・バーの分だけあける */
html,body{height:100%;background:#0b0704;overscroll-behavior:none;-webkit-text-size-adjust:100%}
main{display:block;padding:0}
.game{position:fixed;left:env(safe-area-inset-left);right:env(safe-area-inset-right);top:env(safe-area-inset-top);bottom:env(safe-area-inset-bottom);height:auto!important;min-height:0!important;border-radius:0;box-shadow:none}
.appver{display:block;margin-top:4px;font-size:12px;color:var(--mut)}
.fbk{display:inline-flex;align-items:center;min-height:44px;margin-top:10px;padding:0 14px;border-radius:10px;border:2px solid var(--cool);color:#8ff3ff;text-decoration:none;font:400 15px "DotGothic16",monospace}
</style>'''
rep('</style>', APP_CSS)

# ---- ランキング → 自分の記録 ----
rep("async function submitRank(score){", "async function submitRank(score){return;")
i0 = h.index('async function loadRank(el){')
i1 = h.index('function fakeAd(cb){')
h = h[:i0] + '''function loadRank(el){/* アプリ版：ランキングは出さず、自分のベスト5 */
  if(!el)return;const d=today(),L=Object.entries(M.daily).filter(([,v])=>v>0).sort((a,b)=>b[1]-a[1]).slice(0,5);
  el.innerHTML=L.length?`<table class="rk"><tbody>${L.map(([k,v],i)=>`<tr${k===d?' class="me"':''}><td>${i+1}位</td><td>${k.slice(5).replace('-','/')}${k===d?'（今日）':''}</td><td>${v}点</td></tr>`).join('')}</tbody></table>`:'<p class="empty">まだ記録はない</p>'}
''' + h[i1:]
rep('今日のランキング</h3><div id="prank"></div>', '自分のベスト5</h3><div id="prank"></div>')
rep('<div id="drank"></div>', '<p style="margin-top:6px;font-size:14px;color:#ffc21a">自分のベスト5</p><div id="drank"></div>')
rep('margin:14px 0 4px">自分の記録</h3>', 'margin:14px 0 4px">最近7日の記録</h3>')
rep("['c-daily','今日の地球','ランキング']", "['c-daily','今日の地球','自分の記録']")
rep('毎日1つ、全員が同じ時代・同じ条件で遊ぶ。最初の1回だけが正式記録。', '毎日1つ、みんなが同じ時代・同じ条件で遊ぶ。最初の1回だけが正式記録。')

# ---- 言い方・テスト版の表示 ----
rep('セーブ・図鑑・化石はこのブラウザに自動保存</span>',
    f'セーブ・図鑑・化石はこの端末に自動保存<small class="appver">テスト版 {APP_VER}</small>'
    + (f'<a class="fbk" href="{FEEDBACK_URL}" target="_blank" rel="noopener">感想を送る</a>' if FEEDBACK_URL else '') + '</span>')
rep("zip:'このブラウザでは読めないコード。新しめのブラウザで開いてみて。'", "zip:'この端末では読めないコード。アプリを最新にしてから、もう一度ためしてみて。'")

# ---- フォント（使う文字だけ） ----
chars = set(h)
for a, b in [(0x20, 0x7f), (0x3000, 0x3040), (0x3041, 0x3097), (0x30a0, 0x3100), (0xff01, 0xff5f)]:
    chars.update(chr(c) for c in range(a, b))
text = ''.join(sorted(c for c in chars if ord(c) >= 0x20))


def woff2(ttf):
    f = TTFont(ROOT / 'fonts' / ttf)
    o = subset.Options(); o.flavor = 'woff2'; o.layout_features = ['*']; o.name_IDs = ['*']; o.notdef_outline = True
    s = subset.Subsetter(o); s.populate(text=text); s.subset(f)
    b = io.BytesIO(); f.flavor = 'woff2'; f.save(b)
    return base64.b64encode(b.getvalue()).decode()


faces = []
for fam, ttf, w in [('DotGothic16', 'DotGothic16-Regular.ttf', 400), ('M PLUS 1p', 'MPLUS1p-Regular.ttf', 400),
                    ('M PLUS 1p', 'MPLUS1p-Bold.ttf', 700), ('M PLUS 1p', 'MPLUS1p-ExtraBold.ttf', 800)]:
    faces.append(f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:normal;font-display:block;src:url(data:font/woff2;base64,{woff2(ttf)}) format("woff2")}}')
rep('/*FONTS*/\n', '<style>/* フォント：SIL Open Font License 1.1（fonts/ の OFL を参照） */\n' + '\n'.join(faces) + '\n</style>\n')

assert 'fonts.googleapis' not in h
dst.write_text(h, encoding='utf-8')
print(f'{dst}：{len(h.encode()) // 1024} KB・フォントの文字数 {len(text)}')
