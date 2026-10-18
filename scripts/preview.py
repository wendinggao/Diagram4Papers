"""Loopback-only native diagrams.net preview/export, no external Python packages."""
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import argparse, base64, json, sys

HTML='''<!doctype html><meta charset="utf-8"><title>Diagram4Papers preview</title>
<style>html,body{margin:0;height:100%;background:white;font:14px sans-serif}header{height:40px;padding:0 12px;display:flex;align-items:center;gap:12px;background:#eef2f5}iframe{position:absolute;top:40px;left:0;width:100%;height:calc(100% - 40px);border:0}img{display:none;position:absolute;top:40px;width:100%;height:calc(100% - 40px);object-fit:contain;object-position:left top;background:white}</style>
<header><b>Diagram4Papers</b><button id="export">Render PNG</button><button id="edit">Edit view</button><span id="status">Loading</span></header>
<iframe id="frame" src="https://embed.diagrams.net/?embed=1&proto=json&configure=1&ui=atlas&libraries=0"></iframe><img id="png" alt="Native figure preview">
<script>const frame=document.getElementById('frame'),status=document.getElementById('status'),png=document.getElementById('png'),origin='https://embed.diagrams.net';let rendered=false;
const send=m=>frame.contentWindow.postMessage(JSON.stringify(m),origin);
function render(){status.textContent='Rendering';send({action:'export',format:'png',scale:SCALE,border:0,background:'#ffffff',transparent:false,grid:false,shadow:false})}
document.getElementById('export').onclick=render;document.getElementById('edit').onclick=()=>png.style.display='none';
window.addEventListener('message',async e=>{if(e.origin!==origin||e.source!==frame.contentWindow)return;let m;try{m=typeof e.data==='string'?JSON.parse(e.data):e.data}catch{return}
if(m.event==='configure')send({action:'configure',config:{defaultFonts:['Comic Sans MS'],enableGrid:false}});
if(m.event==='init'){const xml=await fetch('/figure.drawio?cache='+Date.now()).then(r=>r.text());send({action:'load',xml,title:'Research figure',autosave:0})}
if(m.event==='load'&&!rendered){rendered=true;render()}
if(m.event==='export'&&m.data){const r=await fetch('/render',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({data:m.data})});status.textContent=r.ok?'Rendered':'Export save failed';png.src=m.data;png.style.display='block'}
if(m.event==='error')status.textContent='Render error: '+m.message;
});</script>'''

def run(path,port,scale,output):
    source=Path(path).resolve();target=Path(output).resolve() if output else source.with_suffix('.png')
    if not source.is_file():raise FileNotFoundError(source.name)
    class Handler(BaseHTTPRequestHandler):
        def reply(self,data,mime):
            self.send_response(200);self.send_header('Content-Type',mime);self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
        def do_GET(self):
            route=self.path.split('?',1)[0]
            if route=='/':self.reply(HTML.replace('SCALE',str(scale)).encode(),'text/html; charset=utf-8')
            elif route=='/figure.drawio':self.reply(source.read_bytes(),'application/xml')
            elif route=='/preview.png' and target.exists():self.reply(target.read_bytes(),'image/png')
            else:self.send_error(404)
        def do_POST(self):
            if self.path!='/render':self.send_error(404);return
            try:
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<50_000_000:raise ValueError('Invalid size')
                payload=json.loads(self.rfile.read(length))['data'];prefix,data=payload.split(',',1)
                if 'image/png' not in prefix:raise ValueError('Expected PNG')
                decoded=base64.b64decode(data,validate=True)
                if not decoded.startswith(b'\x89PNG\r\n\x1a\n'):raise ValueError('Invalid PNG')
                target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(decoded);self.reply(b'ok','text/plain')
            except Exception:self.send_error(400,'PNG export rejected')
        def log_message(self,*args):pass
    server=ThreadingHTTPServer(('127.0.0.1',port),Handler)
    print(f'Open http://127.0.0.1:{server.server_address[1]}/ ; native export writes {target.name}',flush=True)
    server.serve_forever()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('drawio');p.add_argument('--port',type=int,default=8765);p.add_argument('--scale',type=float,default=2);p.add_argument('--output',type=Path);a=p.parse_args()
    if not 0<a.scale<=8:p.error('scale must be in (0,8]')
    run(a.drawio,a.port,a.scale,a.output)
