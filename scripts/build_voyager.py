"""Public Voyager mechanism example. Original schematic art and synthetic task.
No Minecraft/LLM run is claimed. Action API signatures follow public Voyager.
The shortened chest-code example adapts the released MIT-licensed trial program;
see THIRD_PARTY_NOTICES.md and references/voyager-code-license.txt.
"""
from pathlib import Path
import argparse,base64,json,math,zlib
from urllib.parse import quote
from figure import Figure
ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/'assets/streamline/ledger.json'
INK='#202A32';MUTED='#5D6469';WIRE='#939C98'
BLUE='#E3EFF9';LILAC='#E6DCF4';AMBER='#FAE5BE';ROSE='#F2D5DF';GREEN='#D9EBCB';CYAN='#D6ECE5'
BS='#8FAFC5';LS='#AB90C9';AS='#CAA064';RS='#BF8CA2';GS='#87AA72';CS='#83B3A8'
PROGRAM='''// Shortened adaptation of MineDojo/Voyager craftChest.js.
// Copyright (c) 2023 MineDojo Team. MIT license;
// see ../references/voyager-code-license.txt.
async function craftChest(bot) {
  const n = bot.inventory.count(
    mcData.itemsByName.oak_planks.id);
  if (n < 8) await craftItem(
    bot, "oak_planks", Math.ceil((8-n)/4));
  await craftItem(bot, "chest", 1);
}'''
def material_trace(planks=6,logs=1):
    batches=max(0,math.ceil((8-planks)/4));needed=max(0,8-planks)
    if logs<batches:return dict(illustrative=True,minecraft_execution=False,success=False,initial_planks=planks,initial_logs=logs,missing_planks=needed,recipe_batches=batches)
    total=planks+4*batches
    return dict(illustrative=True,minecraft_execution=False,llm_execution=False,success=True,initial_planks=planks,initial_logs=logs,missing_planks=needed,recipe_batches=batches,planks_after_conversion=total,final_planks=total-8,final_logs=logs-batches,final_chests=1)
def build(output,style=None):
    f=Figure(2160,1180,'Voyager — embodied lifelong learning',style=style)
    def tx(i,s,x,y,w,h=36,size=26,bold=False,align='left',color=INK):return f.text(i,s,(x,y,w,h),size,align,bold,color)
    def box(i,x,y,w,h,fill='#FFFFFF',stroke='#AAB8C1',tier=None,family='blue',radius=7,role='container'):return f.frame(i,(x,y,w,h),fill,stroke,radius=radius,tier=tier,family=family,role=role)
    def art(i,name,x,y,w=58,h=None):return f.asset(i,name,LEDGER,(x,y,w,h or w))
    def wire(i,pts,color=WIRE,weight=2.3,arrow=False):return f.line(i,pts,arrow,color,weight)
    def arr(i,pts,color=WIRE,weight=3):return wire(i,pts,color,weight,True)
    def chip(i,s,x,y,w,h=44,fill=BLUE,stroke=BS,size=26,bold=False):
        box(i,x,y,w,h,fill,stroke);tx(i+'-text',s,x+6,y+1,w-12,h-2,size,bold,'center')
    def panel(i,x,y,w,h,title,family,icon,titlew):
        p=f.tokens['families'][family];box(i,x,y,w,h,p['ground'],tier='outer',family=family)
        art(i+'-icon',icon,x+12,y+10,70)
        box(i+'-ribbon',x+91,y+13,titlew,59,p['band'],'none',radius=8)
        tx(i+'-title',title,x+103,y+12,w-118,60,36,True)
    def sec(i,x,y,w,h,title,family,fill='#FFFFFF',icon=None):
        box(i,x,y,w,h,fill,tier='section',family=family);off=12
        if icon:art(i+'-icon',icon,x+10,y+8,42);off=62
        if title:tx(i+'-title',title,x+off,y+6,w-off-10,42,28,True)
    def poly(i,points,fill,stroke='#60776B',weight=1.4):
        x=min(v[0] for v in points);y=min(v[1] for v in points);w=max(v[0] for v in points)-x;h=max(v[1] for v in points)-y
        cmds='<move x="%s" y="%s"/>'%((points[0][0]-x)*100/w,(points[0][1]-y)*100/h)
        cmds+=''.join('<line x="%s" y="%s"/>'%((a-x)*100/w,(b-y)*100/h) for a,b in points[1:])+'<close/>'
        xml='<shape w="100" h="100" aspect="variable" strokewidth="inherit"><foreground><path>'+cmds+'</path><fillstroke/></foreground></shape>'
        co=zlib.compressobj(wbits=-15);payload=co.compress(quote(xml,safe='').encode())+co.flush();shape='stencil('+base64.b64encode(payload).decode()+')'
        return f.vertex(i,(x,y,w,h),dict(shape=shape,fillColor=fill,strokeColor=stroke,strokeWidth=weight),role='geometry')
    def cube(i,x,y,w=46,h=28,top='#B2D5A3',left='#B69672',right='#907453'):
        # Original native stencil faces; a data scene, not a stock icon.
        poly(i+'-left',[(x-w/2,y),(x,y+w/4),(x,y+w/4+h),(x-w/2,y+h)],left)
        poly(i+'-right',[(x,y+w/4),(x+w/2,y),(x+w/2,y+h),(x,y+w/4+h)],right)
        poly(i+'-top',[(x,y-w/4),(x+w/2,y),(x,y+w/4),(x-w/2,y)],top)
    def bars(i,x,y,width=153,height=37):
        values=[.38,.74,.52,.94,.62,.44,.81,.55]
        for n,value in enumerate(values):
            ww=(width-7*5)/8;hh=height*value
            box(i+str(n),x+n*(ww+5),y+height-hh,ww,hh,[LILAC,CYAN,BLUE,AMBER][n%4],'#A0AAA6',radius=3,role='geometry')
    panel('curriculum',14,14,2132,254,'1. Automatic curriculum','apricot','curriculum',548)
    panel('practice',14,284,1410,882,'2. Iterative prompting','lavender','code-window',481)
    panel('memory',1440,284,706,882,'3. Lifelong skill memory','teal','memory',587)
    # A compact loop uses the otherwise idle wide header to explain recurrence.
    for n,(label,asset,x) in enumerate([('Code','robot',698),('Run','cube',916),('Verify','check',1114)]):
        art('learning-loop-icon'+str(n),asset,x,305,46)
        tx('learning-loop-label'+str(n),label,x+57,310,107,39,27,True)
        if n<2:arr('learning-loop-forward'+str(n),[(x+164,329),(x+198,329)],'#A78DBE',2.8)
    arr('learning-loop-return',[(1282,329),(1300,329),(1300,358),(720,358),(720,353)],'#A78DBE',2.1)
    box('learning-loop-return-label',911,345,220,26,'#F8F5FF','none')
    tx('learning-loop-return-text','Refine when needed',918,345,206,26,21,False,'center')
    # Top-level learning frontier: completed skills make a new task feasible.
    tx('frontier-heading','Exploration frontier',723,25,310,52,29,True)
    for n,(label,asset,x,fill) in enumerate([('Gather wood','globe',1063,BLUE),('Make planks','cube',1432,LILAC),('Craft a chest','chest',1799,CYAN)]):
        art('frontier-icon'+str(n),asset,x,27,49)
        chip('frontier-label'+str(n),label,x+59,29,254,46,fill,[BS,LS,CS][n],27,n==2)
        if n<2:arr('frontier-arrow'+str(n),[(x+323,52),(x+352,52)],'#B29877',2.8)
    sec('world',30,105,620,147,'Current world','apricot','#FFFDFA',icon='globe')
    # A small, schematic voxel forest scene, independently drawn.
    for row in range(2):
        for col in range(3):cube('ground-%s-%s'%(row,col),82+col*39+row*20,205+row*19-col*5,39,18)
    cube('tree-trunk',121,184,23,34,'#B28A5E','#C39B6D','#92704E')
    cube('tree-crown',121,166,65,28,'#CCE0A9','#9FC68E','#83AD81')
    cube('crafting-block',192,209,40,25,'#D8B47A','#C59A60','#A97B48')
    tx('biome','Forest · daytime',252,149,380,36,27)
    tx('inventory-start','1 log · 6 planks · 0 chests',252,186,380,33,25)
    tx('table-state','Crafting table nearby',252,217,380,29,24)
    sec('progress',664,105,400,147,'Exploration progress','apricot','#FFFDFA',icon='clipboard')
    tx('past-wood','✓ Gather wood',684,158,360,34,27)
    tx('past-planks','✓ Make planks',684,197,360,34,27)
    sec('next-task',1078,105,500,147,'GPT-4 task proposal','apricot','#FFFDFA',icon='brain')
    art('task-flag','trophy',1090,168,58)
    tx('new-task','Craft a chest',1161,161,398,48,33,True)
    tx('task-principle','Novel and feasible',1161,211,398,31,25)
    sec('additional-context',1592,105,538,147,'Extra context · GPT-3.5','apricot','#FFFDFA',icon='question')
    tx('context-q','What does a chest require?',1608,158,505,38,25)
    tx('context-a','8 planks + a crafting table.',1608,203,505,38,27)
    # Context is provided to the action agent; retrieved skills arrive from memory.
    sec('prompt-context',30,374,1378,75,'','lavender','#FFFDFF')
    art('prompt-tools','tools',42,385,52)
    tx('prompt-inputs','State + task + control APIs',108,381,560,35,28,True)
    tx('prompt-input-details','craftItem · mineBlock · placeItem',108,417,560,27,23)
    art('prompt-library','theorems',740,385,53)
    tx('retrieved-context','Retrieved skill programs',808,384,475,34,28,True)
    tx('retrieved-context-detail','Read as reusable code context',808,419,475,27,23)
    arr('memory-context-read',[(1453,412),(1409,412)],'#6F9C93',3.2)
    # Explicit failed attempt and resource-aware correction.
    sec('program',30,463,650,367,'GPT-4 action agent','lavender','#FFFDFF',icon='robot')
    chip('initial-tag','Initial attempt',46,518,194,31,ROSE,RS,22,True)
    tx('initial-program','await craftItem(bot, "chest", 1);',46,555,616,37,25)
    wire('code-separator',[(46,600),(664,600)],'#C5B8D5',1.3)
    chip('revised-tag','Revised code',46,611,194,31,CYAN,CS,22,True)
    lines=['const n = bot.inventory.count(', '  mcData.itemsByName.oak_planks.id);','if (n < 8) await craftItem(', '  bot, "oak_planks", Math.ceil((8-n)/4));','await craftItem(bot, "chest", 1);']
    for n,line in enumerate(lines):tx('program-line'+str(n),line.replace('  ','\u00a0\u00a0'),46,650+n*31,616,32,23)
    # Environment interaction is shown through a recipe and resource-state changes.
    sec('environment',694,463,714,367,'Minecraft environment','lavender','#FFFDFF',icon='cube')
    chip('after-revision-tag','After revision',1207,477,185,31,CYAN,CS,21,True)
    tx('recipe-label','Chest recipe',711,514,213,36,27,True)
    for row in range(3):
        for col in range(3):
            x=711+col*58;y=556+row*58
            box('recipe-cell-%s-%s'%(row,col),x,y,51,51,'#F5F1E9','#CBBFA9',radius=7)
            if (row,col)!=(1,1):
                f.vertex('plank-%s-%s'%(row,col),(x+7,y+8,37,35),dict(fillColor='#DDBB80',strokeColor='#A4824F',strokeWidth=1.4,rounded=0),role='geometry')
                for k in range(2):wire('grain-%s-%s-%s'%(row,col,k),[(x+9,y+19+k*10),(x+42,y+19+k*10)],'#B5925B',1.2)
    tx('recipe-amount','8 planks',714,738,165,34,26,False,'center')
    arr('recipe-output',[(895,638),(950,638)],'#9E8CB6',3.8)
    art('crafted-chest','chest',969,568,135)
    chip('chest-output','1 chest',966,726,145,48,CYAN,CS,29,True)
    wire('environment-separator',[(1131,519),(1131,807)],'#C9BED8',1.3)
    tx('inventory-title','Inventory change',1150,514,240,38,26,True)
    art('planks-state-icon','cube',1153,566,39)
    tx('planks-state-label','Planks',1204,567,183,35,25)
    chip('planks-state','6 → 10 → 2',1150,613,238,45,AMBER,AS,28)
    tx('log-conversion','1 log → 4 planks',1150,667,238,34,24)
    art('chest-state-icon','check',1153,724,39)
    tx('chests-state-label','Chest',1204,725,183,35,25)
    chip('chests-state','0 → 1',1150,769,238,43,GREEN,GS,29,True)
    # Three distinct feedback channels, all from the initial attempt.
    feedbacks=[('env','Attempt 1 · environment','speech',30,ROSE,RS),('errors','Attempt 1 · interpreter','warning',494,AMBER,AS),('critic','Attempt 1 · GPT-4 critic','check',958,CYAN,CS)]
    for ident,title,asset,x,fill,stroke in feedbacks:
        sec('feedback-'+ident,x,844,450,182,'','lavender','#FFFDFF')
        art('feedback-'+ident+'-icon',asset,x+12,856,50)
        tx('feedback-'+ident+'-title',title,x+74,855,363,39,26,True)
        box('feedback-'+ident+'-band',x+12,905,426,105,fill,stroke)
    tx('env-response','Need 2 more oak planks.',54,912,400,37,27)
    tx('env-state','Available: 6 · required: 8',54,960,400,35,25)
    tx('error-response','No exception on this attempt.',518,912,400,37,25)
    tx('error-channel','The chest is still missing.',518,960,400,35,25)
    tx('critic-false','success: false',982,910,400,37,28,True)
    tx('critic-advice','Make more planks, then retry.',982,960,400,35,24)
    sec('control',30,1040,1378,110,'','lavender','#FFFDFF')
    art('retry-icon','repeat',43,1061,58)
    tx('retry-label','Failure → revise',114,1052,330,37,27,True)
    tx('retry-details','Reuse all feedback channels',114,1095,330,33,23)
    wire('control-divider1',[(459,1054),(459,1137)],'#C7BAD7',1.3)
    art('budget-icon','question',475,1061,56)
    tx('budget-label','4 failed attempts',546,1052,358,37,27,True)
    tx('budget-details','Move to another task',546,1095,358,33,24)
    wire('control-divider2',[(919,1054),(919,1137)],'#C7BAD7',1.3)
    art('success-icon','trophy',934,1061,58)
    tx('success-label','Attempt 2: success',1005,1052,383,37,27,True)
    tx('success-details','Save skill · choose next task',1005,1095,383,33,23)
    # The memory shows retrieval, key/value indexing, and the write boundary.
    sec('retrieval',1456,374,674,356,'Retrieve relevant programs','teal','#FCFEFC',icon='search')
    tx('retrieval-query','Task + GPT-3.5 plan + feedback',1472,426,642,36,27)
    bars('query-embedding-',1480,475,191,34)
    arr('query-to-retrieval',[(1690,491),(1746,491)],'#719D92',3)
    art('search-vector','search',1760,470,44)
    chip('top-k','Top-5 skills',1820,471,293,44,LILAC,LS,28,True)
    names=[('Collect logs','globe'),('Craft planks','cube'),('Make a crafting table','tools'),('Craft sticks','memo'),('Make wooden tools','tools')]
    for n,(name,asset) in enumerate(names):
        y=527+n*37
        box('retrieved-skill-'+str(n),1472,y,642,32,CYAN if n==1 else '#F5FAF7',CS if n==1 else '#B3C7BC')
        art('retrieved-skill-icon-'+str(n),asset,1482,y+1,30)
        tx('retrieved-skill-name-'+str(n),name,1528,y,570,32,24,n==1)
    sec('index',1456,746,674,223,'Description → embedding → code','teal','#FCFEFC',icon='memory')
    art('describe-code-icon','robot',1472,803,48)
    tx('describe-code-label','GPT-3.5 describes the program',1534,805,578,36,26)
    chip('program-description','Craft a chest from available wood',1472,851,642,43,AMBER,AS,27)
    tx('embedding-key-label','Key: description vector',1472,903,339,31,23,True)
    bars('stored-key-',1472,937,278,20)
    arr('key-value-map',[(1774,928),(1817,928)],'#719D92',2.7)
    chip('program-value','craftChest(bot)',1833,906,281,48,CYAN,CS,27,True)
    sec('write',1456,985,674,166,'Store a verified skill','teal','#FCFEFC',icon='check')
    tx('store-code','Description key + executable program',1472,1036,642,37,27)
    art('stored-artifact','memo',1472,1081,51)
    chip('new-memory-entry','+ craftChest(bot)',1542,1081,572,51,CYAN,CS,29,True)
    arr('success-write',[(1409,1105),(1455,1105)],'#5C9D8D',3.2)
    f.write(output)
    out=Path(output);out.with_suffix('.trace.json').write_text(json.dumps(material_trace(),indent=2)+'\n')
    out.with_suffix('.program.js').write_text(PROGRAM+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('voyager.drawio'));p.add_argument('--style',type=Path)
    a=p.parse_args();build(a.out,json.loads(a.style.read_text()) if a.style else None)
