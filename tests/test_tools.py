"""Behavioral checks for grouped geometry, style violations and hidden disclosure."""
from pathlib import Path
from urllib.parse import quote
import base64, copy, hashlib, json, math, struct, sys, tempfile, unittest, zlib
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from figure import Figure, STYLE
from check_figure import inspect
from audit_release import audit
from build_demo import trace

class ToolsTest(unittest.TestCase):
    def make_asset(self, root):
        svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M1 1H23V23H1Z" fill="#88BBCC"/></svg>'
        (root/'asset.svg').write_text(svg)
        entry=dict(id='sample',file='asset.svg',sha256=hashlib.sha256(svg.encode()).hexdigest(),origin='external',author='Fixture artist',source_url='https://example.org/asset.svg',license='CC-BY-4.0',license_url='https://creativecommons.org/licenses/by/4.0/',distribution='Test fixture only')
        ledger=root/'assets.json';ledger.write_text(json.dumps({'assets':[entry]}))
        return svg,entry,ledger

    def test_external_asset_roundtrip_and_honest_origin(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);svg,entry,ledger=self.make_asset(root)
            f=Figure(200,200);cell=f.asset('picture','sample',ledger,(20,20,80,80));f.write(root/'figure.drawio')
            self.assertEqual(cell.get('pfOrigin'),'external')
            self.assertEqual(cell.get('pfAsset'),'sample')
            result=inspect(root/'figure.drawio',assets=ledger)
            self.assertTrue(result['passed']);self.assertFalse(result['visual_approval'])
            self.assertTrue(any(x['rule']=='external-asset-ledger-required' for x in inspect(root/'figure.drawio')['errors']))

    def test_asset_hash_and_escaping_path_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);svg,entry,ledger=self.make_asset(root);f=Figure(200,200)
            (root/'asset.svg').write_text(svg+' ')
            with self.assertRaises(ValueError):f.asset('bad','sample',ledger,(20,20,80,80))
            entry['file']='../outside.svg';ledger.write_text(json.dumps({'assets':[entry]}))
            with self.assertRaises(ValueError):f.asset('escape','sample',ledger,(20,20,80,80))

    def test_unrecorded_origin_is_not_automatically_original(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);svg,entry,ledger=self.make_asset(root)
            f=Figure(200,200);cell=f.icon('unknown',svg,(20,20,80,80));f.write(root/'f.drawio')
            self.assertNotEqual(cell.get('pfOrigin'),'original')
            self.assertTrue(any(x['rule']=='unrecorded-icon-origin' for x in inspect(root/'f.drawio')['errors']))

    def test_embedded_asset_provenance_mismatch_detected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);svg,entry,ledger=self.make_asset(root);f=Figure(200,200)
            cell=f.asset('picture','sample',ledger,(20,20,80,80))
            entry['origin']='original';ledger.write_text(json.dumps({'assets':[entry]}));f.write(root/'f.drawio')
            self.assertTrue(any(x['rule']=='embedded-asset-mismatch' for x in inspect(root/'f.drawio',assets=ledger)['errors']))

    def test_public_example_geometry_with_independent_area_check(self):
        result=trace()
        self.assertTrue(result['illustrative'])
        self.assertFalse(result['autogps_execution'])
        a,b,c=result['equal_sides'],result['equal_sides'],result['base']
        semiperimeter=(a+b+c)/2
        heron=math.sqrt(semiperimeter*(semiperimeter-a)*(semiperimeter-b)*(semiperimeter-c))
        self.assertAlmostEqual(result['area'],heron)
        self.assertEqual(result['height']**2+result['half_base']**2,a*a)
        self.assertTrue(all(result['checks'].values()))

    def test_group_coordinates_and_cycle(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'test.drawio';f=Figure(200,200);parent=f.vertex('g',(100,100,80,80),{},role='group');child=f.frame('c',(10,10,20,20));child.set('parent','g');f.write(p)
            self.assertTrue(inspect(p)['passed'])
            parent.set('parent','c');f.write(p);self.assertFalse(inspect(p)['passed'])
    def test_explicit_style_override(self):
        with tempfile.TemporaryDirectory() as d:
            tokens=copy.deepcopy(STYLE);tokens['font']='Arial';tokens['section']['radius']=11
            p=Path(d)/'test.drawio';f=Figure(240,180,style=tokens);f.frame('s',(10,10,220,160),tier='section');f.text('t','Custom style',(25,30,180,40),24);f.write(p)
            self.assertTrue(inspect(p,contract=tokens)['passed'])
            self.assertFalse(inspect(p)['passed'])
    def test_tier_violation(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'test.drawio';f=Figure(200,200);c=f.frame('section',(10,10,150,150),tier='section');c.set('style',c.get('style').replace('dashPattern=4 3','dashPattern=12 12'));f.write(p)
            self.assertTrue(any(e['rule']=='frame-tier' for e in inspect(p)['errors']))
    def test_decoded_svg_disclosure(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'payload.drawio';secret='UNSHARED_TEST_MARKER';payload=base64.b64encode(('<svg>'+secret+'</svg>').encode()).decode();p.write_text('data:image/svg+xml;base64,'+payload)
            self.assertFalse(audit(d,[secret])['passed'])
    def test_native_stencil_disclosure(self):
        with tempfile.TemporaryDirectory() as d:
            secret='UNSHARED_TEST_MARKER'
            co=zlib.compressobj(wbits=-15)
            payload=base64.b64encode(co.compress(quote('<shape>'+secret+'</shape>').encode())+co.flush()).decode()
            Path(d,'native.drawio').write_text('shape=stencil('+payload+');')
            self.assertFalse(audit(d,[secret])['passed'])

    def test_encoded_text_disclosure(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d,'note.txt').write_text('UNSHARED%20TEST%20MARKER')
            self.assertFalse(audit(d,['UNSHARED TEST MARKER'])['passed'])
    def test_solid_corner_violation(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'test.drawio';f=Figure(200,200);c=f.frame('cell',(10,10,100,100));c.set('style',c.get('style').replace('rounded=1','rounded=0'));f.write(p)
            self.assertTrue(any(e['rule']=='solid-corner' for e in inspect(p)['errors']))
    def test_png_compressed_metadata(self):
        with tempfile.TemporaryDirectory() as d:
            body=b'comment\0\0'+zlib.compress(b'UNSHARED_TEST_MARKER');kind=b'zTXt';chunk=struct.pack('>I',len(body))+kind+body+struct.pack('>I',zlib.crc32(kind+body));Path(d,'image.png').write_bytes(b'\x89PNG\r\n\x1a\n'+chunk)
            self.assertFalse(audit(d,['UNSHARED_TEST_MARKER'])['passed'])

if __name__=='__main__':unittest.main()
