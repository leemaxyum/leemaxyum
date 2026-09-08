"""Deterministic, hand-composed glyph artwork. Requires Pillow; no image conversion."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random, html

ROOT = Path(__file__).resolve().parents[1]
W, H = 1200, 600
font_path = next(p for p in [Path('C:/Windows/Fonts/consola.ttf'), Path('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')] if p.exists())
fonts = {s: ImageFont.truetype(str(font_path), s) for s in (12, 14, 16, 20, 44)}
# Each line is composed by hand: profiles, shoulders, articulated arms and fingers.
lower = r'''
          .-:::::-.
        .:+=-..:-=+:.
       :+/.       .\+:
       +:   .    .  :+
       |:     .--.  :|_
       |:    (  .)  .: >
       :+.    `-'  .: /                          ./'
        \+:   .  .: _/                       ./:/'  ./'
         `+:    .: |                      ./:/' ./:/'
          |:    .: |                     /::/.:/:/' ./'
       .-:+:    .: :-.                  /::/::/:/.::/'
    .-:++/:.    .: .:++:-.             /:::::::/::/'
 .-:++/:.       .:   .:/++:--.       .:+:::.   .:/
:+/:.     .--::::::--.  .:/++:--..--:+/:.   .:/
+:.    .:+/---....---\+:.  .:/++++++/:.   .:/
|:.   .:+/.          .\+:   .:------:.  .:/
|:.   :+/.   .   .    .\+:   .      .:/
|:.   |:.              .\+:......::/'
|:.   |:.    .          .:++++++::'
|:.   |:.               .:|
|:.   |:.    .          .:|
'''.strip('\n').splitlines()
upper = r'''
                       .-:::::-.        .:++++/:.           .:++/
                     .:+=-..-=+:.   .:++/....:++:.       .:++/
                    :+/.      .\+:.:++/.       .\++:...:++/
                    +:   .     :++/:.    .      .:++++++/
                   _|: .--.    :|:.           .:++/----'
                  < :. (  .)   :|:.   .     .:++/
                   \ :. `-'   :+/::.     .:++/
                    \_ :.   :+/:. \+:..:++/
                      | :. :+/:. .:++++/'
                   .-:+:..:+/:. .:+/'
                .-:++/---:/:. .:+/'
             .-:++/:.   .:  .:+/'
          .-:++/:.    .:  .:+/'
        .:++/:.    .:  .:+/'
       /::/:.   .:  .:+/'
      /::/::...:..:+/'
     /::/::/::/::/'
    /::/::/::/::/
   /:'/::/::/:/'
     /:'/::/:/'
       /:'/:'
'''.strip('\n').splitlines()

random.seed(19)
stars = [(random.randrange(26,1174),random.randrange(22,550),random.choice('. . . +'.split()),random.choice([45,65,90,135])) for _ in range(170)]
art = []
for lines, ox, oy in [(lower,150,281),(upper,615,20)]:
    for row,line in enumerate(lines):
        for col,ch in enumerate(line):
            if ch != ' ':
                shade = 185 if ch in '+/\\|' else 88
                art.append((ox+col*7.2,oy+row*12,ch,shade))

def draw(stage, scan=False):
    im = Image.new('RGB',(W,H),'black'); d=ImageDraw.Draw(im)
    if stage >= 1:
        for x,y,ch,c in stars:
            if not (x<575 and y<230): d.text((x,y),ch,font=fonts[12],fill=(c,c,c))
    if stage >= 2:
        for i,(x,y,ch,c) in enumerate(art):
            if stage==2 and i%3: continue
            if stage==3 and i%4==0: continue
            d.text((x,y),ch,font=fonts[12],fill=(c,c,c))
    if stage>=4:
        d.text((42,47),'SIGNAL 001 / OPEN CHANNEL',font=fonts[14],fill='#777777')
        d.text((40,82),'PRADHNESH //',font=fonts[44],fill='#f0f0f0')
    if stage>=5:
        d.text((43,143),'BUILDING IN PUBLIC',font=fonts[20],fill='#bcbcbc')
        d.line((43,184,407,184),fill='#555555'); d.ellipse((41,182,45,186),fill='white')
        d.text((43,203),'systems / interfaces / experiments',font=fonts[16],fill='#8a8a8a')
        d.text((810,444),'DISTANCE IS AN INVITATION.',font=fonts[14],fill='#777777')
        d.text((810,470),'// keep reaching',font=fonts[14],fill='#b0b0b0')
        d.line((40,558,1160,558),fill='#333333')
        d.text((42,574),'BUILD > BREAK > UNDERSTAND > SHIP',font=fonts[14],fill='#a0a0a0')
        d.text((958,574),'ARCHIVE / OPEN',font=fonts[14],fill='#777777')
    if scan:
        d.line((40,343,1160,343),fill='#292929')
        for x in (240,754,1081): d.line((x,344,x+16,344),fill='#666666')
    return im

assets=ROOT/'assets'; assets.mkdir(exist_ok=True)
frames=[draw(s,scan) for s,scan in [(0,False),(1,False),(2,False),(3,False),(4,False),(5,False),(5,True),(5,False)]]
palette=Image.new('P',(1,1)); palette.putpalette([v for i in range(256) for v in (i,i,i)])
frames=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
frames[0].save(assets/'ascii-signal.gif',save_all=True,append_images=frames[1:],duration=[180,500,200,200,650,1200,120,5950],loop=0,optimize=True,disposal=1)
# SVG uses the exact same authored glyph positions, and remains fully standalone.
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="600" viewBox="0 0 1200 600" role="img" aria-labelledby="title desc">','<title id="title">Pradhnesh // Building in public</title>','<desc id="desc">Two ASCII figures reach across a star field. Systems, interfaces, experiments. Build, break, understand, ship.</desc>','<rect width="1200" height="600" fill="#000"/>']
def text(x,y,value,size,color):
    svg.append(f'<text x="{x}" y="{y+size*.8}" font-family="Consolas,DejaVu Sans Mono,monospace" font-size="{size}" fill="{color}" xml:space="preserve">{html.escape(value)}</text>')
for x,y,ch,c in stars:
    if not(x<575 and y<230): text(x,y,ch,12,f'#{c:02x}{c:02x}{c:02x}')
for x,y,ch,c in art: text(x,y,ch,12,f'#{c:02x}{c:02x}{c:02x}')
for x,y,t,s,c in [(42,47,'SIGNAL 001 / OPEN CHANNEL',14,'#777'),(40,82,'PRADHNESH //',44,'#f0f0f0'),(43,143,'BUILDING IN PUBLIC',20,'#bcbcbc'),(43,203,'systems / interfaces / experiments',16,'#8a8a8a'),(810,444,'DISTANCE IS AN INVITATION.',14,'#777'),(810,470,'// keep reaching',14,'#b0b0b0'),(42,574,'BUILD > BREAK > UNDERSTAND > SHIP',14,'#a0a0a0'),(958,574,'ARCHIVE / OPEN',14,'#777')]: text(x,y,t,s,c)
svg.extend(['<path d="M43 184H407M40 558H1160" stroke="#444"/>','<circle cx="43" cy="184" r="2" fill="white"/>','</svg>'])
(assets/'ascii-signal.svg').write_text('\n'.join(svg),encoding='utf-8')
print(f'Hero: {len(frames)} frames, {(assets/"ascii-signal.gif").stat().st_size:,} bytes')

