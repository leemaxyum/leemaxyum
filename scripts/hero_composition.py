"""Authored anatomical contours rendered as glyphs; never samples reference pixels."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math, random, html

ROOT=Path(__file__).resolve().parents[1]
W,H=1200,650
FONT=next(p for p in [Path('C:/Windows/Fonts/consola.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')] if p.exists())
fonts={n:ImageFont.truetype(str(FONT),n) for n in [9,12,14,16,20,42]}

# Contours are drawn by hand in composition space. The fingers are separate
# articulated silhouettes, not parallel slash marks. Bodies extend past the crop.
lower=[(-45,665),(-20,599),(37,555),(70,520),(123,492),(205,474),(221,453),(218,437),(200,421),(193,394),(198,368),(213,345),(239,334),(267,334),(297,343),(317,360),(330,374),(333,389),(344,399),(356,407),(360,413),(347,417),(348,424),(355,431),(351,438),(352,447),(344,461),(321,467),(306,477),(303,493),(326,509),(355,493),(383,487),(413,491),(438,483),(471,469),(486,450),(509,428),(533,414),(546,395),(553,377),(563,366),(571,349),(579,340),(580,346),(573,365),(584,357),(599,345),(612,338),(617,340),(612,346),(597,361),(584,374),(602,366),(621,357),(630,358),(632,363),(624,367),(603,378),(589,389),(607,385),(620,384),(630,388),(628,394),(612,396),(593,403),(580,414),(566,417),(552,439),(545,464),(534,486),(513,507),(480,521),(457,543),(434,564),(399,578),(363,588),(350,621),(338,665)]
upper=[(950,-30),(928,8),(904,38),(888,42),(871,37),(850,41),(830,53),(817,72),(811,94),(813,116),(820,134),(828,145),(830,158),(842,168),(857,171),(870,164),(881,155),(894,151),(915,163),(942,171),(969,170),(995,160),(1023,140),(1058,114),(1107,92),(1150,59),(1209,1),(1230,-30)]
arm=[(833,129),(817,140),(801,162),(784,177),(770,186),(753,197),(734,222),(715,240),(701,253),(687,263),(674,269),(657,279),(645,287),(634,299),(625,307),(626,311),(632,310),(650,300),(642,313),(634,326),(637,329),(643,324),(655,310),(651,327),(649,337),(653,339),(658,331),(664,314),(666,324),(666,335),(670,337),(673,332),(674,313),(682,304),(689,312),(690,322),(694,323),(698,315),(698,301),(702,291),(699,277),(714,264),(743,252),(772,240),(789,222),(802,202),(820,185),(840,166),(855,157)]

# Internal contour strokes describe skull, face, tendons, deltoids and torsos.
details=[
[(198,390),(204,368),(222,350),(248,342),(278,345),(305,359),(323,380)],
[(204,411),(216,428),(236,440),(259,445),(277,451),(291,468),(291,487)],
[(281,393),(273,389),(269,397),(274,414),(286,421),(292,414),(283,407),(279,398)],
[(319,383),(328,391),(321,397),(333,400),(341,407)],
[(305,407),(318,415),(325,433),(342,438)],
[(285,432),(306,453),(324,459),(342,454)],
[(227,448),(236,467),(223,483),(193,498),(162,517),(146,555),(130,601),(127,650)],
[(252,448),(267,472),(288,486),(320,511)],
[(43,556),(68,533),(106,518),(130,529),(137,553)],
[(7,621),(39,578),(80,553),(106,548)],
[(112,649),(123,592),(144,547),(174,521),(207,506),(243,506),(279,518),(309,531)],
[(160,648),(171,605),(185,566),(213,538),(246,526),(281,535),(312,542)],
[(229,650),(250,611),(287,592),(329,592),(357,580)],
[(320,515),(348,501),(376,495),(405,506),(417,520),(408,535),(381,547),(351,553)],
[(316,536),(345,548),(375,550),(408,539),(444,522),(469,496)],
[(348,573),(390,564),(424,548),(452,526),(474,519),(503,504),(518,484)],
[(437,488),(459,491),(480,476),(499,449),(526,427),(548,417)],
[(488,476),(508,465),(526,445),(545,426),(557,409)],
[(531,486),(535,460),(543,438),(558,417)],
[(548,396),(555,405),(568,409),(580,403),(583,393),(574,386),(559,389)],
[(555,385),(565,377),(571,365)],[(565,394),(580,381),(597,363)],
[(572,400),(590,392),(609,388)],
[(821,94),(825,73),(843,51),(864,44),(884,47),(898,59)],
[(820,113),(836,126),(850,126),(861,119),(880,115)],
[(833,131),(844,134),(849,144),(844,148),(853,152),(865,146)],
[(848,158),(858,163),(868,156)],
[(893,89),(902,92),(904,105),(896,119),(890,113),(895,103)],
[(908,38),(931,44),(945,69),(936,96),(915,117),(889,130)],
[(927,6),(955,19),(977,36),(984,62),(969,90),(946,110)],
[(955,124),(984,112),(1004,90),(1017,53),(1041,21),(1063,-5)],
[(903,140),(929,149),(956,155),(981,145),(1009,126)],
[(989,112),(1030,102),(1064,80),(1095,41),(1124,10)],
[(1008,73),(1034,67),(1056,51),(1077,24),(1094,-8)],
[(1060,99),(1095,85),(1130,60),(1162,32),(1190,0)],
[(819,151),(802,177),(778,196),(761,220),(738,241),(710,261)],
[(837,162),(814,184),(797,204),(784,223),(757,240),(733,246)],
[(797,179),(790,194),(772,206),(756,224)],
[(769,204),(751,208),(736,229),(718,248)],
[(701,263),(688,275),(686,289),(674,300),(659,301)],
[(683,278),(671,285),(658,290),(647,300)],
[(692,289),(686,296),(684,303)],
]

def smooth(points,closed=False):
    p=points[:]
    p=([p[-1]]+p+[p[0],p[1]]) if closed else ([p[0]]+p+[p[-1]])
    result=[]
    for a,b,c,d in zip(p,p[1:],p[2:],p[3:]):
        n=max(3,int(math.dist(b,c)/2))
        for j in range(n):
            t=j/n
            result.append(tuple(.5*((2*b[k])+(-a[k]+c[k])*t+(2*a[k]-5*b[k]+4*c[k]-d[k])*t*t+(-a[k]+3*b[k]-3*c[k]+d[k])*t**3) for k in [0,1]))
    return result

def compose():
    rng=random.Random(593)
    mask=Image.new('1',(W,H)); md=ImageDraw.Draw(mask)
    outlines=[smooth(lower,True),smooth(upper,True),smooth(arm,True)]
    for shape in outlines: md.polygon(shape,fill=1)
    glyphs={}
    # Sparse interior glyphs suggest a translucent material, leaving black volume.
    for y in range(0,H,7):
        for x in range(0,W,5):
            if mask.getpixel((x,y)) and rng.random()<.38:
                glyphs[(x,y)]=(rng.choice('..:·'),rng.choice([48,65,80,105]),9)
    def stroke(points,brightness):
        for i in range(0,len(points)-1,3):
            x,y=points[i]; nx,ny=points[i+1]
            if not(0<=x<W and 0<=y<H): continue
            dx,dy=nx-x,ny-y
            ch='_' if abs(dx)>abs(dy)*2 else ':' if abs(dy)>abs(dx)*2 else '/' if dx*dy<0 else '\\'
            if rng.random()<.16: ch=rng.choice('+*:=')
            key=(round(x/5)*5,round(y/7)*7)
            glyphs[key]=(ch,min(245,brightness+rng.randrange(-35,30)),9)
    for shape in outlines: stroke(shape,230)
    for line in details: stroke(smooth(line),190)
    # Local glints placed at anatomical turning points, not a uniform texture.
    for x,y in [(220,350),(281,346),(212,423),(230,486),(171,525),(269,541),(367,501),(448,518),(520,437),(553,405),(575,376),(847,51),(897,112),(943,73),(982,125),(1033,69),(1145,38),(788,196),(745,230),(696,274),(662,293)]:
        glyphs[(x,y)]=('+',245,12)
    stars=[]
    for _ in range(370):
        x,y=rng.randrange(10,W-10),rng.randrange(8,H-8)
        if mask.getpixel((x,y)) or (x<590 and y<190) or (x>700 and y>490): continue
        stars.append((x,y,rng.choices(['.','·','+','*'],[65,25,8,2])[0],rng.choice([48,72,90,120,175]),9))
    return [(x,y,ch,c,size) for (x,y),(ch,c,size) in glyphs.items()],stars

ART,STARS=compose()
COPY=[(40,35,'SIGNAL 002 / OPEN CHANNEL',12,100,4),(38,59,'PRADHNESH //',42,240,4),(40,113,'BUILDING IN PUBLIC',20,188,5),(40,154,'systems / interfaces / experiments',16,150,5),(736,547,'BUILD → BREAK → UNDERSTAND → SHIP',14,190,5),(736,578,'LEEMAXYUM / ARCHIVE OPEN',12,105,5)]

def draw(stage,scan=False):
    im=Image.new('RGB',(W,H),'black'); d=ImageDraw.Draw(im)
    if stage>=1:
        for x,y,ch,c,n in STARS: d.text((x,y),ch,font=fonts[n],fill=(c,c,c))
    if stage>=2:
        for i,(x,y,ch,c,n) in enumerate(ART):
            if stage==2 and i%3:continue
            if stage==3 and i%4==0:continue
            d.text((x,y),ch,font=fonts[n],fill=(c,c,c))
    for x,y,t,n,c,at in COPY:
        if stage>=at:d.text((x,y),t,font=fonts[n],fill=(c,c,c))
    if stage>=5:d.line((736,527,1150,527),fill='#383838')
    if scan:
        d.line((40,310,1150,310),fill='#1b1b1b')
        d.line((675,310,695,310),fill='#656565')
    return im

def main():
    out=ROOT/'assets'
    frames=[draw(s,b) for s,b in [(0,False),(1,False),(2,False),(3,False),(4,False),(5,False),(5,True),(5,False)]]
    palette=Image.new('P',(1,1));palette.putpalette([v for i in range(256) for v in (i,i,i)])
    frames=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
    frames[0].save(out/'ascii-signal.gif',save_all=True,append_images=frames[1:],duration=[180,500,200,200,650,1200,120,5950],loop=0,optimize=False,disposal=1)
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc" style="max-width:100%;height:auto;display:block;background:#000">','<title id="title">Pradhnesh // Building in public</title>','<desc id="desc">Two large ghostly human figures, composed of ASCII glyphs, enter from the lower left and upper right. Their outstretched hands nearly meet across a deliberate gap. Build, break, understand, ship.</desc>',f'<rect width="{W}" height="{H}" fill="#000"/>','<g font-family="Consolas,DejaVu Sans Mono,monospace" xml:space="preserve">']
    for x,y,t,c,n in STARS+ART:
        svg.append(f'<text x="{x}" y="{y+n*.8:.1f}" font-size="{n}" fill="#{c:02x}{c:02x}{c:02x}">{html.escape(t)}</text>')
    for x,y,t,n,c,_ in COPY:
        svg.append(f'<text x="{x}" y="{y+n*.8:.1f}" font-size="{n}" fill="#{c:02x}{c:02x}{c:02x}">{html.escape(t)}</text>')
    svg.extend(['</g>','<path d="M736 527H1150" stroke="#383838"/>','</svg>'])
    (out/'ascii-signal.svg').write_text('\n'.join(svg),encoding='utf-8')
    print(f'Hero: {len(ART)} authored glyphs, 8 frames, {(out/"ascii-signal.gif").stat().st_size:,} bytes')

if __name__=='__main__':main()
