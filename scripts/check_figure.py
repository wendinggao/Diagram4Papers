"""Role-aware XML/style checks; optional real font advances. Not visual approval."""
from pathlib import Path
import argparse, base64, hashlib, html, json, os, re, subprocess, xml.etree.ElementTree as ET
from figure import STYLE

def font_file(family='Comic Sans MS'):
    windir=os.environ.get('WINDIR')
    options=([Path(windir)/'Fonts'/({'Comic Sans MS':'comic.ttf','Arial':'arial.ttf'}.get(family,family.replace(' ','').lower()+'.ttf'))] if windir else [])+[Path('/System/Library/Fonts/Supplemental')/(family+'.ttf')]
    for path in options:
        if path.is_file():return path
    try:
        value=subprocess.check_output(['fc-match','-f','%{family}|%{file}',family],text=True)
        found_family,path=value.split('|',1)
        if family.casefold() in found_family.casefold() and Path(path).is_file():return Path(path)
    except (FileNotFoundError,ValueError,subprocess.CalledProcessError):pass
    return None

def inspect(path,font=None,contract=None,require_font=False,assets=None):
    contract=contract or STYLE
    root=ET.parse(path).getroot();allcells=list(root.iter('mxCell'));cs={c.get('id'):c for c in allcells};errors=[];notes=[]
    if len(cs)!=len(allcells):errors.append(dict(rule='duplicate-id'))
    model=root.find('.//mxGraphModel');width=float(model.get('pageWidth'));height=float(model.get('pageHeight'))
    def style(c):return dict(v.split('=',1) for v in c.get('style','').split(';') if '='in v)
    memo={};active=set()
    def bounds(i):
        if i in memo:return memo[i]
        if i in active:raise ValueError('Parent cycle')
        active.add(i);c=cs[i];g=c.find('mxGeometry');parent=c.get('parent')
        if g is None:result=(0.,0.,0.,0.)
        else:
            ox,oy,_,_=bounds(parent) if parent in cs else (0,0,0,0)
            result=(ox+float(g.get('x',0)),oy+float(g.get('y',0)),float(g.get('width',0)),float(g.get('height',0)))
        active.remove(i);memo[i]=result;return result
    try:
        for i in cs:bounds(i)
    except ValueError:errors.append(dict(rule='parent-cycle'));return dict(passed=False,errors=errors,notes=notes)
    font=Path(font) if font else font_file(contract['font']);measure=None
    try:
        from PIL import ImageFont
        if font:
            bold_font=font.with_name(font.stem+' Bold'+font.suffix)
            measure=lambda text,size,bold=False:ImageFont.truetype(str(bold_font if bold and bold_font.exists() else font),round(size*10)).getlength(text)/10
    except ImportError:notes.append('Pillow not installed: font-advance check omitted')
    if not font:
        notes.append('Requested font not found: exact typography needs verification before final export')
        if require_font:errors.append(dict(rule='required-font-unavailable'))
    ledger={}
    if assets:
        ledger_path=Path(assets)
        entries=json.loads(ledger_path.read_text())['assets']
        for item in entries:
            aid=item['id']
            if aid in ledger:errors.append(dict(rule='duplicate-asset-id',id=aid))
            ledger[aid]=item
            base=ledger_path.resolve().parent
            file=(base/item['file']).resolve()
            if base not in file.parents or not file.is_file():errors.append(dict(rule='asset-file',id=aid));continue
            if hashlib.sha256(file.read_bytes()).hexdigest()!=item.get('sha256'):errors.append(dict(rule='asset-file-hash',id=aid))
            if item.get('origin')=='external' and any(not item.get(k) for k in ('author','source_url','license','license_url','distribution')):errors.append(dict(rule='asset-provenance',id=aid))
    for i,c in cs.items():
        parent=c.get('parent');s=style(c);role=c.get('pfRole');g=c.find('mxGeometry')
        if parent and parent not in cs:errors.append(dict(id=i,rule='missing-parent'))
        if c.get('vertex')=='1':
            x,y,w,h=bounds(i)
            if w<=0 or h<=0:errors.append(dict(id=i,rule='nonpositive-box'))
            if x<-.01 or y<-.01 or x+w>width+.01 or y+h>height+.01:errors.append(dict(id=i,rule='off-page'))
        if role=='text':
            if s.get('fontFamily')!=contract['font']:errors.append(dict(id=i,rule='font-family'))
            raw=c.get('value','');text=html.unescape(re.sub('<[^>]+>','',re.sub(r'<br\s*/?>','\n',raw)));fs=float(s.get('fontSize',26))
            bold=bool(int(s.get('fontStyle','0'))&1)
            advance=max((measure(t,fs,bold) for t in text.splitlines()),default=0) if measure else 0
            if advance>bounds(i)[2]+.5:errors.append(dict(id=i,rule='text-advance-overflow',text_width=round(advance,1),box_width=bounds(i)[2]))
        tier=c.get('pfTier')
        if role=='container' and tier in ('outer','section','local'):
            spec=contract[tier]
            expected={'strokeWidth':str(spec['stroke']),'dashPattern':spec['dash'],'fixDash':'0','strokeOpacity':'100','arcSize':str(spec['radius']*2),'rounded':'1','absoluteArcSize':'1'}
            for k,v in expected.items():
                if s.get(k)!=v:errors.append(dict(id=i,rule='frame-tier',property=k))
        if role=='container' and tier=='solid':
            if s.get('rounded')!='1' or s.get('absoluteArcSize')!='1' or float(s.get('arcSize',0)) not in [2*contract['cell']['radius'],2*contract['heading_radius']]:errors.append(dict(id=i,rule='solid-corner'))
        if role=='icon':
            src=s.get('image','')
            if not src.startswith('data:image/svg+xml,'):errors.append(dict(id=i,rule='nonembedded-vector-icon'));continue
            try:
                payload=base64.b64decode(src.split(',',1)[1]);svg=payload.decode();ET.fromstring(svg)
                if re.search(r'<(?:\w+:)?(?:image|text)\b',svg):errors.append(dict(id=i,rule='raster-or-outlined-text-icon'))
                origin=c.get('pfOrigin')
                if origin not in ('original','external'):errors.append(dict(id=i,rule='unrecorded-icon-origin'))
                if origin=='external':
                    entry=ledger.get(c.get('pfAsset'))
                    if not entry:errors.append(dict(id=i,rule='external-asset-ledger-required'))
                    elif entry.get('origin')!=origin or hashlib.sha256(payload).hexdigest()!=entry.get('sha256'):errors.append(dict(id=i,rule='embedded-asset-mismatch'))
            except Exception:errors.append(dict(id=i,rule='invalid-svg'))
        if role=='flow':
            for attr in ['pfSource','pfTarget']:
                if c.get(attr) and c.get(attr) not in cs:errors.append(dict(id=i,rule='missing-flow-endpoint'))
            pts=[(float(q.get('x')),float(q.get('y'))) for q in g.iter('mxPoint')]
            if len(pts)==2 and pts[0][0]!=pts[1][0] and pts[0][1]!=pts[1][1]:notes.append('Diagonal flow '+i+': confirm it is necessary in the native render')
    return dict(passed=not errors,errors=errors,notes=notes,vertices=sum(c.get('vertex')=='1' for c in cs.values()),text_cells=sum(c.get('pfRole')=='text' for c in cs.values()),font_metrics_measured=bool(measure),external_icon_instances=sum(c.get('pfOrigin')=='external' for c in cs.values()),visual_approval=False)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('drawio');p.add_argument('--font');p.add_argument('--style',type=Path);p.add_argument('--require-font',action='store_true');p.add_argument('--assets',type=Path);p.add_argument('--report',type=Path);a=p.parse_args();r=inspect(a.drawio,a.font,json.loads(a.style.read_text()) if a.style else None,a.require_font,a.assets)
    result=json.dumps(r,indent=2);print(result)
    if a.report:a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(result)
    raise SystemExit(not r['passed'])
