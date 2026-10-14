"""Vector scientific figures generated from the analysis, not decorative art."""
import csv
from pathlib import Path
from reportlab.graphics.shapes import Drawing, Line, Rect, String, PolyLine
from reportlab.graphics import renderPDF
from reportlab.lib.colors import HexColor

ROOT=Path(__file__).resolve().parents[1]
BLUE=HexColor('#244d75'); TEAL=HexColor('#187c78'); RED=HexColor('#ad4a40')
GRAY=HexColor('#64717e'); LIGHT=HexColor('#dfe5e9'); ORANGE=HexColor('#bc761f')

def s(d,x,y,txt,size=9,color=GRAY,anchor='start'):
    d.add(String(x,y,txt,fontName='Helvetica',fontSize=size,fillColor=color,textAnchor=anchor))

def timing():
    d=Drawing(470,220); left=140; scale=290/455
    s(d,0,203,'Required permissions combine before recovery cover is assessed',10,BLUE)
    def bar(y,a,b,label,color):
        s(d,0,y+4,label,9)
        d.add(Rect(left+a*scale,y,(b-a)*scale,15,fillColor=color,strokeColor=None))
        s(d,left+b*scale+4,y+4,str(b),8,color)
    bar(165,0,365,'Service permission',BLUE)
    bar(130,0,180,'Required site permission',RED)
    bar(95,0,180,'Effective path: intersection',GRAY)
    bar(60,0,91,'Covered start days (R=90)',TEAL)
    for tick in [0,90,180,276,365,455]:
        x=left+tick*scale
        d.add(Line(x,40,x,44,strokeColor=GRAY))
        s(d,x,27,str(tick),8,GRAY,'middle')
    d.add(Line(left,42,left+455*scale,42,strokeColor=GRAY))
    s(d,285,9,'Hypothetical day index; intervals are half-open',8,GRAY,'middle')
    return d

def sensitivity():
    d=Drawing(470,280); x0,y0,w,h=48,73,398,145
    s(d,0,265,'Coverage over a 365-day candidate-start horizon',10,BLUE)
    for frac in [0,.25,.5,.75,1]:
        y=y0+h*frac
        d.add(Line(x0,y,x0+w,y,strokeColor=LIGHT,strokeWidth=.5))
        s(d,x0-7,y-3,f'{100*frac:.0f}%',8,GRAY,'end')
    for day in [1,30,60,90,120,150,180]:
        x=x0+(day-1)*w/179
        d.add(Line(x,y0,x,y0-3,strokeColor=GRAY))
        s(d,x,y0-15,str(day),8,GRAY,'middle')
    rows=list(csv.DictReader((ROOT/'results/stress_grid.csv').open()))
    series=[('365_day_service_180_day_site',RED,'Service + shorter site'),
            ('one_365_day_path',BLUE,'One path / two co-expiring paths'),
            ('two_staggered_paths',ORANGE,'Two staggered paths'),
            ('365_day_path_90_day_continuation',TEAL,'90-day continuation')]
    for name,col,label in series:
        pts=[]
        for row in rows:
            if row['portfolio']==name and row['switching']=='0':
                x=x0+(int(row['duration_days'])-1)*w/179
                y=y0+float(row['coverage_fraction'])*h
                pts += [x,y]
        d.add(PolyLine(pts,strokeColor=col,strokeWidth=1.6,fillColor=None))
    s(d,x0+w/2,y0-33,'Required recovery duration (days)',9,GRAY,'middle')
    for i,(_,col,label) in enumerate(series):
        x=8 if i%2==0 else 245; y=11+(1-i//2)*14
        d.add(Line(x,y+3,x+15,y+3,strokeColor=col,strokeWidth=2))
        s(d,x+20,y,label,8,col)
    return d

def run():
    for name,figure in [('permission_intersection',timing()),('duration_sensitivity',sensitivity())]:
        renderPDF.drawToFile(figure,str(ROOT/'figures'/f'{name}.pdf'))
    print('Two vector figure PDFs generated')
if __name__=='__main__':run()
