"""Small, dependency-free draw.io authoring primitives. Original MIT code."""
from pathlib import Path
from xml.etree import ElementTree as ET
import base64, hashlib, html, json

STYLE = json.loads((Path(__file__).resolve().parents[1] / 'assets' / 'style.json').read_text())

class Figure:
    def __init__(self, width, height, name='Research figure', style=None):
        self.tokens = style or STYLE
        self.width, self.height = width, height
        self.root = ET.Element('mxfile', host='app.diagrams.net', agent='diagram4papers', pages='1')
        page = ET.SubElement(self.root, 'diagram', name=name, id='figure')
        model = ET.SubElement(page, 'mxGraphModel', page='1', pageWidth=str(width), pageHeight=str(height), grid='0', math='0', background='#FFFFFF')
        self.cells = ET.SubElement(model, 'root')
        ET.SubElement(self.cells, 'mxCell', id='0')
        ET.SubElement(self.cells, 'mxCell', id='1', parent='0')
        self.records = []
        self.frame('page', (0, 0, width, height), fill='#FFFFFF', stroke='none', radius=0, role='background', weight=0)

    @staticmethod
    def styles(values):
        return ';'.join(f'{k}={v}' for k,v in values.items()) + ';'

    def vertex(self, ident, bounds, styles, value='', role='geometry', **attrs):
        x,y,w,h = bounds
        cell = ET.SubElement(self.cells, 'mxCell', id=ident, parent='1', vertex='1', value=value, style=self.styles(styles), pfRole=role, **{k:str(v) for k,v in attrs.items()})
        ET.SubElement(cell, 'mxGeometry', x=str(x), y=str(y), width=str(w), height=str(h), **{'as':'geometry'})
        self.records.append(dict(id=ident, role=role, box=list(bounds)))
        return cell

    def frame(self, ident, bounds, fill='#FFFFFF', stroke='#AAB8C1', radius=7, weight=1.45, tier=None, family='blue', role='container'):
        values=dict(rounded=int(radius>0), absoluteArcSize=1, arcSize=2*radius, fillColor=fill, strokeColor=stroke, strokeWidth=weight, shadow=0, strokeOpacity=100)
        if tier:
            spec=self.tokens[tier];values.update(rounded=1,arcSize=2*spec['radius'],strokeWidth=spec['stroke'],dashed=1,dashPattern=spec['dash'],fixDash=0)
            values['strokeColor']=self.tokens['families'][family][tier]
        return self.vertex(ident,bounds,values,role=role,pfTier=tier or 'solid')

    def text(self, ident, value, bounds, size=26, align='left', heavy=False, color='#17212B'):
        content=html.escape(value).replace('\n','<br>')
        return self.vertex(ident,bounds,dict(text=1,html=1,whiteSpace='nowrap',overflow='visible',fillColor='none',strokeColor='none',fontFamily=self.tokens['font'],fontSize=size,fontColor=color,fontStyle=1 if heavy else 0,align=align,verticalAlign='middle',spacing=0,shadow=0),content,role='text')

    def icon(self, ident, svg, bounds, origin='unrecorded', asset_id=None):
        encoded=base64.b64encode(svg.encode()).decode()
        attrs={'pfOrigin':origin,'pfAsset':asset_id or ''}
        cell=self.vertex(ident,bounds,dict(shape='image',image='data:image/svg+xml,'+encoded,imageAspect=1,aspect='fixed',strokeColor='none',fillColor='none',shadow=0),role='icon',**attrs)
        self.records[-1].update(origin=origin,asset_id=asset_id,sha256=hashlib.sha256(svg.encode()).hexdigest())
        return cell

    def asset(self, ident, asset_id, ledger_path, bounds):
        ledger_path=Path(ledger_path)
        data=json.loads(ledger_path.read_text())
        entries={v['id']:v for v in data['assets']}
        entry=entries[asset_id]
        root=ledger_path.resolve().parent
        path=(root/entry['file']).resolve()
        if root not in path.parents:
            raise ValueError('Asset path escapes ledger directory')
        payload=path.read_bytes()
        if hashlib.sha256(payload).hexdigest()!=entry['sha256']:
            raise ValueError('Asset hash differs from ledger: '+asset_id)
        origin=entry.get('origin')
        if origin not in ('original','external'):
            raise ValueError('Asset origin must be explicit')
        if origin=='external' and any(not entry.get(k) for k in ('author','source_url','license','license_url','distribution')):
            raise ValueError('Incomplete external asset provenance: '+asset_id)
        return self.icon(ident,payload.decode('utf-8'),bounds,origin=origin,asset_id=asset_id)

    def line(self, ident, points, arrow=False, color='#87918B', weight=2.5, source=None, target=None):
        if len(points)<2:raise ValueError('A line needs at least two points')
        cell=ET.SubElement(self.cells,'mxCell',id=ident,parent='1',edge='1',value='',pfRole='flow' if arrow else 'relation',style=self.styles(dict(edgeStyle='none',rounded=0,strokeColor=color,strokeWidth=weight,endArrow='block' if arrow else 'none',endFill=1,endSize=8,startArrow='none',shadow=0)))
        if source:cell.set('pfSource',source)
        if target:cell.set('pfTarget',target)
        geom=ET.SubElement(cell,'mxGeometry',relative='1',**{'as':'geometry'})
        for (x,y),key in [(points[0],'sourcePoint'),(points[-1],'targetPoint')]:ET.SubElement(geom,'mxPoint',x=str(x),y=str(y),**{'as':key})
        if len(points)>2:
            arr=ET.SubElement(geom,'Array',**{'as':'points'})
            for x,y in points[1:-1]:ET.SubElement(arr,'mxPoint',x=str(x),y=str(y))
        self.records.append(dict(id=ident,role='flow' if arrow else 'relation',points=[list(p) for p in points],source=source,target=target))

    def shape(self, ident, bounds, shape='ellipse', fill='#6CB7E8', stroke='#365A77'):
        return self.vertex(ident,bounds,dict(shape=shape,fillColor=fill,strokeColor=stroke,strokeWidth=2,shadow=0),role='illustration')

    def write(self, path):
        path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
        ET.indent(self.root,space='  ')
        ET.ElementTree(self.root).write(path,encoding='utf-8',xml_declaration=True)
        path.with_suffix('.manifest.json').write_text(json.dumps(dict(canvas=[self.width,self.height],objects=self.records),indent=2))
