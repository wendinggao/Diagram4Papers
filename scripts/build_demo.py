"""Independently authored AutoGPS overview from the public ICLR 2026 paper.
The Fig. 3 geometry is public. The derivation is a checked, compressed teaching
example, not a captured AutoGPS run or a measured experiment.
"""
from pathlib import Path
from fractions import Fraction
from math import isqrt
import argparse,json
from figure import Figure
ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/'assets/streamline/ledger.json'
INK='#19262F';MUTED='#59616A';WIRE='#8B9690'
BLUE='#E0F0FB';LILAC='#E8DFF5';AMBER='#FFF0CA';ROSE='#F5D0DF';GREEN='#D8EBC7';CYAN='#DDF0EC'
BS='#8DB5CF';LS='#AE93CD';AS='#CEAB63';RS='#C9799F';GS='#86A86D';CS='#8AB7AF'
def trace():
    base=10;side=13;half=Fraction(base,2);radicand=side*side-half*half
    height=isqrt(radicand.numerator)
    assert radicand.denominator==1 and height*height==radicand
    area=half*height
    return dict(public_paper='https://arxiv.org/abs/2505.23381',source_instance='Figure 3: isosceles triangle with sides 13, 13, 10',illustrative=True,autogps_execution=False,base=base,equal_sides=side,half_base=int(half),height=height,area=int(area),checks=dict(pythagoras=half*half+height*height==side*side,area=area==Fraction(base*height,2)),compression='Geometric and algebraic dependencies are grouped for explanation; not a literal execution trace.')
def build(output,style=None):
    f=Figure(2160,1180,'AutoGPS — multimodal formalization and deductive reasoning',style=style)
    def tx(i,s,x,y,w,h=36,size=26,bold=False,align='left',color=INK):return f.text(i,s,(x,y,w,h),size,align,bold,color)
    def box(i,x,y,w,h,fill='#FFFFFF',stroke='#AAB8C1',tier=None,family='blue',radius=7):return f.frame(i,(x,y,w,h),fill,stroke,radius=radius,tier=tier,family=family)
    def art(i,name,x,y,w=64,h=None):return f.asset(i,name,LEDGER,(x,y,w,h or w))
    def wire(i,pts,color=WIRE,weight=2.3,arrow=False):return f.line(i,pts,arrow,color,weight)
    def arr(i,pts,color=WIRE,weight=3):return wire(i,pts,color,weight,True)
    def chip(i,s,x,y,w,h=46,fill=BLUE,stroke=BS,size=26,bold=False):
        box(i,x,y,w,h,fill,stroke);tx(i+'-text',s,x+5,y+1,w-10,h-2,size,bold,'center')
    def panel(i,x,y,w,h,title,family,icon,titlew=None):
        p=f.tokens['families'][family];box(i,x,y,w,h,p['ground'],tier='outer',family=family)
        art(i+'-icon',icon,x+12,y+9,70)
        box(i+'-ribbon',x+91,y+13,titlew or w-111,59,p['band'],'none',radius=8)
        tx(i+'-title',title,x+103,y+12,w-113,60,35 if i=='input' else 36,True)
    def sec(i,x,y,w,h,title,family,fill='#FFFFFF',icon=None):
        box(i,x,y,w,h,fill,tier='section',family=family);off=12
        if icon:art(i+'-icon',icon,x+10,y+8,42);off=62
        if title:tx(i+'-title',title,x+off,y+6,w-off-10,44,28,True)
    def triangle(i,x,y,w,h,labels=False):
        f.vertex(i,(x,y,w,h),dict(shape='triangle',direction='north',fillColor='#FFE8B3',strokeColor='#A88444',strokeWidth=2.5),role='geometry')
        wire(i+'-height',[(x+w/2,y),(x+w/2,y+h)],'#CE748F',2.3)
        wire(i+'-right-angle',[(x+w/2,y+h-15),(x+w/2+15,y+h-15),(x+w/2+15,y+h)],'#92755C',1.7)
        tx(i+'-left-length','13',x-15,y+h*.46,50,36,27,False,'center')
        tx(i+'-right-length','13',x+w-32,y+h*.46,50,36,27,False,'center')
        if not labels:
            wire(i+'-base-dimension',[(x,y+h+24),(x+w,y+h+24)],'#87939A',1.5)
            for j,xx in enumerate([x,x+w]):wire(i+'-dimension-end'+str(j),[(xx,y+h+18),(xx,y+h+30)],'#87939A',1.5)
        tx(i+'-base-length','10',x+w/2-30,y+h+(38 if labels else 26),60,36,27,False,'center')
        if labels:
            for n,xx,yy in [('D',x+w/2,y),('A',x,y+h),('B',x+w/2,y+h),('C',x+w,y+h)]:
                f.shape(i+'-point-'+n,(xx-3,yy-3,6,6),'ellipse','#C76891','#9F5074')
                tx(i+'-label-'+n,n,xx+(-29 if n=='A' else 8),yy+(-32 if n=='D' else 0),30,34,27)
    panel('input',14,14,326,1152,'Geo problem','blue','compass',218)
    panel('formalize',354,14,748,700,'1. Multimodal formalization','rose','brain',640)
    panel('validate',354,730,748,436,'2. Symbolic validation','rose','check',512)
    panel('expand',1118,14,1028,724,'3. Expand a proof hypergraph','green','reasoner',767)
    panel('explain',1118,754,1028,412,'4. Minimize & explain','green','clipboard',579)
    sec('question',28,105,298,446,'Diagram + text','blue','#FAFDFF')
    tx('request','Find the area of\nthe triangle.',43,156,268,82,29)
    triangle('original-diagram',76,249,201,227)
    sec('tools',28,566,298,389,'MPF tool library','blue','#FAFDFF')
    for n,(label,asset,xx,yy) in enumerate([('Annotate','compass',45,628),('Diagram\nparser','image',188,628),('Text parser','memo',45,786),('Syntax\ncheck','syntax',188,786)]):
        art('tool-'+str(n),asset,xx+23,yy,79);tx('tool-label-'+str(n),label,xx-5,yy+87,136,57,23,False,'center')
    sec('goal',28,971,298,180,'Target quantity','blue','#FAFDFF',icon='search')
    tx('area-symbol','S = Area(△ADC)',43,1030,266,44,28,False,'center')
    chip('target-unknown','S = ?',46,1083,262,51,LILAC,LS,32)
    sec('annotation',370,105,231,319,'Annotation','rose','#FFFBFD')
    triangle('annotated-diagram',407,185,153,154,True)
    sec('diagram-parser',615,105,471,171,'Diagram parser','rose','#FFFBFD',icon='image')
    tx('segments','AB · AC · BC · AD · CD · BD',630,160,440,38,25)
    chip('parsed-incidence','B on AC',630,205,164,48,CYAN,CS,25)
    chip('parsed-orthogonal','BD ⟂ BC',805,205,264,48,LILAC,LS,25)
    sec('text-parser',615,290,471,134,'Text parser','rose','#FFFBFD',icon='memo')
    tx('partial-target','Find(AreaOf(Shape($)))',630,350,440,52,29)
    arr('annotation-to-align',[(485,428),(485,446)],RS)
    arr('parsers-to-align',[(850,428),(850,446)],RS)
    sec('alignment',370,450,716,247,'Multimodal alignment','rose','#FFFBFD',icon='align')
    art('alignment-agent','robot',382,516,88)
    chip('resolve-shape','$ → Triangle(A,D,C)',483,509,585,51,LILAC,LS,31)
    tx('alignment-model','MLLM',382,606,88,31,23,True,'center')
    tx('formalized-premises','B on AC · BD ⟂ BC\nAC = 10 · AD = CD = 13',484,570,584,76,27)
    box('final-target-band',383,652,689,34,'#F8E3ED','none')
    art('formalization-syntax','syntax',389,653,31)
    tx('final-target','Find(AreaOf(Triangle(A,D,C)))',433,650,631,37,26)
    sec('contradiction',370,821,350,140,'Reject contradictions','rose','#FFFBFD')
    art('contradiction-icon','warning',383,874,59)
    tx('collinear-counterexample','A, B, C collinear',453,870,253,35,24)
    tx('invalid-triangle','and △ABC   ✕',453,911,253,35,26,color='#A14F6F')
    sec('completion',736,821,350,140,'Complete relations','rose','#FFFBFD')
    art('completion-icon','book',750,876,58)
    tx('input-relation','BD ⟂ BC',820,870,250,36,27)
    tx('implied-relation','→ BD ⟂ AC',820,911,250,36,27)
    sec('validation-pass',370,975,716,70,'','rose','#FFFBFD')
    art('pass-icon','check',382,984,48)
    tx('validated-record','Consistent facts → proof hypergraph',445,991,623,38,27,True)
    box('feedback-band',370,1058,716,91,'#F8E6EE','#C99AB0')
    art('refine-icon','repeat',382,1070,58)
    tx('feedback-text','Error feedback → MPF refinement',452,1068,620,37,27)
    tx('feedback-limit','Refine and recheck · stop at the iteration limit',452,1107,620,31,23,color=MUTED)
    # Literal facts and explicit premise bundles for geometric hyperedges.
    sec('hypergraph',1134,105,996,290,'','green','#FCFEFA')
    chip('root','start',1150,116,86,36,'#EDF5E5','#9DB68A',22)
    art('known-facts-icon','memo',1249,115,34)
    tx('known-facts','Known facts',1295,114,217,39,26,True)
    chip('node-legend','Literal',1533,117,113,34,BLUE,BS,21)
    chip('edge-legend','Derivation',1661,117,145,34,LILAC,LS,21)
    tx('graph-caption','Premises → rule → fact',1820,113,292,40,24)
    wire('known-facts-bus',[(1193,152),(1193,161),(1999,161)],'#9BB38C',1.8)
    for n,x in enumerate([1270,1485,1724,1999]):arr('initial-fact-'+str(n),[(x,161),(x,172)],'#9BB38C',1.8)
    facts=[('equal','AD = CD\n= 13',1150,239,'ruler',25),('base','AC = 10',1405,159,'ruler',23),('configuration','B on AC\nBD ⟂ AC',1580,288,'compass',25),('triangles','△ADC\n△BCD',1884,230,'compass',25)]
    for ident,label,x,w,icon,size in facts:
        box('fact-'+ident,x,173,w,62,BLUE,BS)
        art('fact-'+ident+'-icon',icon,x+8,183,42)
        tx('fact-'+ident+'-text',label,x+58,175,w-66,58,size,False,'center')
    wire('equal-to-isosceles',[(1270,235),(1270,268)],'#9D87B8',2.2)
    wire('configuration-bus',[(1724,235),(1724,253),(1340,253),(1340,268)],'#9D87B8',2.2)
    wire('configuration-to-pythagoras',[(1724,253),(1641,253),(1641,268)],'#9D87B8',2.2)
    wire('configuration-to-area',[(1724,253),(1958,253),(1958,268)],'#9D87B8',2.2)
    wire('triangle-to-pythagoras',[(1999,235),(1999,243),(1691,243),(1691,268)],'#9D87B8',2.2)
    wire('triangle-to-area',[(1999,235),(1999,268)],'#9D87B8',2.2)
    for n,(ident,label,x,w,icon,size) in enumerate([('midpoint','Isosceles altitude',1150,305,'theorems',24),('pythagoras','Pythagoras',1481,306,'theorems',25),('area','Triangle area',1813,301,'ruler',25)]):
        box('deduce-'+ident,x,269,w,49,LILAC,LS)
        art('deduce-'+ident+'-icon',icon,x+8,271,46)
        tx('deduce-'+ident+'-text',label,x+64,270,w-74,47,size)
        arr('deduce-'+ident+'-output',[(x+w/2,319),(x+w/2,339)],'#9D87B8',2.4)
    chip('relation-midpoint','BC = AC / 2',1150,340,305,43,BLUE,BS,27)
    chip('relation-pythagoras','BC² + BD² = CD²',1481,340,306,43,BLUE,BS,26)
    chip('relation-area','S = AC × BD / 2',1813,340,301,43,BLUE,BS,26)
    arr('geometric-to-algebra',[(1632,397),(1632,408)],'#A58D5C',2.6)
    # Four atomic algebraic transformations are actual AutoGPS engine capabilities.
    sec('algebra-engine',1134,409,996,189,'','green','#FFFEF8')
    art('algebra-engine-icon','calculator',1146,414,35)
    tx('algebra-engine-heading','Algebra engine: atomic derivations',1191,410,716,40,28,True)
    kernels=[('substitute','Substitution','AC = 10 → BC = 10 / 2','align',1150,456,LILAC,LS),
             ('evaluate','Constant evaluation','BC = 10 / 2 → BC = 5','calculator',1643,456,AMBER,AS),
             ('nonlinear','Nonlinear equation solving','BD² = 144, BD > 0 → BD = 12','brain',1150,525,CYAN,CS),
             ('linear','Linear-system solving','S = 5BD, BD = 12 → S = 60','memo',1643,525,BLUE,BS)]
    for ident,title,payload,asset,x,y,fill,stroke in kernels:
        box('kernel-'+ident,x,y,471,61,fill,stroke)
        art('kernel-'+ident+'-icon',asset,x+7,y+4,53)
        tx('kernel-'+ident+'-title',title,x+71,y+2,389,27,23,True)
        tx('kernel-'+ident+'-example',payload,x+71,y+31,389,27,22)
    sec('goal-control',1134,612,996,110,'','green','#FCFEFA')
    art('target-match-icon','search',1146,632,64)
    tx('target-match-heading','Match the target',1223,623,276,35,25,True)
    tx('target-match-value','Area(△ADC)',1223,662,276,39,28)
    wire('goal-control-sep1',[(1512,625),(1512,708)],'#B5C5A9',1.3)
    art('solution-check-icon','check',1525,633,62)
    tx('solution-heading','Solution found',1598,623,251,35,25,True)
    chip('solution-literal','S = 60',1598,665,242,40,GREEN,GS,29,True)
    wire('goal-control-sep2',[(1860,625),(1860,708)],'#B5C5A9',1.3)
    art('repeat-expansion-icon','repeat',1873,634,60)
    tx('repeat-question','Otherwise',1944,623,169,35,24,True)
    tx('repeat-action','Expand again',1944,655,169,32,24)
    tx('repeat-bound','within the limit',1944,687,169,25,20,color=MUTED)
    # A compact dependency subgraph makes the discarded branch concrete.
    sec('traceback',1134,843,367,304,'','green','#FCFEFA')
    art('traceback-search','search',1146,850,37)
    tx('traceback-heading','Keep the goal proof',1195,847,294,40,26,True)
    chip('proof-start','AC = 10 · AD = CD = 13',1150,899,335,40,BLUE,BS,23)
    arr('proof-midpoint-edge',[(1226,940),(1226,955)],'#7E9A69',2.3)
    wire('proof-angle-edge',[(1395,940),(1395,955)],'#BBC1BA',1.7)
    chip('proof-midpoint','BC = 5',1150,957,150,40,LILAC,LS,25)
    chip('unused-angle','∠A = ∠C',1317,957,168,40,'#F2F2EE','#C1C5BD',23)
    arr('proof-height-edge',[(1225,998),(1225,1015)],'#7E9A69',2.3)
    wire('unused-area-edge',[(1301,977),(1308,977),(1308,1035),(1316,1035)],'#BBC1BA',1.7)
    chip('proof-height','BD = 12',1150,1017,150,40,CYAN,CS,25)
    wire('height-to-unused-area',[(1301,1037),(1316,1037)],'#BBC1BA',1.7)
    chip('unused-area','Area(△ABD)=30',1317,1017,168,40,'#F2F2EE','#C1C5BD',19)
    arr('proof-goal-edge',[(1225,1058),(1225,1080)],'#7E9A69',2.3)
    art('minimal-proof-check','check',1150,1085,47)
    chip('minimal-target','S = 60',1203,1081,282,53,GREEN,GS,29,True)
    # Each proof row now shows premises, its rule, and an explicit conclusion.
    sec('stepwise',1515,843,615,304,'','green','#FCFEFA')
    art('proof-document','memo',1525,848,42)
    tx('stepwise-heading','Premises → rule → conclusion',1575,847,540,40,26,True)
    rows=[('one','Isosceles altitude','AC = 10, AD = CD, BD ⟂ AC ⇒ BC = 5','theorems',LILAC,LS),
          ('two','Pythagorean theorem','BC = 5, CD = 13 ⇒ BD² = 144','ruler',BLUE,BS),
          ('three','Solve for a positive length','BD² = 144, BD > 0 ⇒ BD = 12','calculator',AMBER,AS),
          ('four','Area formula + substitution','AC = 10, BD = 12 ⇒ S = 60','check',GREEN,GS)]
    for n,(ident,title,payload,asset,fill,stroke) in enumerate(rows):
        y=896+n*60
        box('proof-step-'+ident,1528,y,589,55,fill,stroke)
        art('proof-step-'+ident+'-icon',asset,1537,y+4,46)
        tx('proof-step-'+ident+'-rule',title,1588,y+1,518,26,23,True)
        tx('proof-step-'+ident+'-payload',payload,1588,y+28,518,26,23)
    f.write(output)
    Path(output).with_suffix('.trace.json').write_text(json.dumps(trace(),indent=2)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('autogps.drawio'));p.add_argument('--style',type=Path)
    a=p.parse_args();build(a.out,json.loads(a.style.read_text()) if a.style else None)
