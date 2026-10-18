"""Inspect portable release files, PNG metadata and embedded SVG. No secret list is bundled."""
from pathlib import Path
import argparse, base64, hashlib, html, json, re, struct, unicodedata, zlib
from urllib.parse import unquote

def png_text(data):
    result=[];pos=8
    while pos+12<=len(data):
        n=struct.unpack('>I',data[pos:pos+4])[0];kind=data[pos+4:pos+8];body=data[pos+8:pos+8+n];pos+=12+n
        try:
            if kind==b'tEXt':result.append(body.decode('latin1'))
            elif kind==b'zTXt':
                key,rest=body.split(b'\0',1);result.append(key.decode('latin1')+' '+zlib.decompress(rest[1:]).decode('utf-8','replace'))
            elif kind==b'iTXt':
                parts=body.split(b'\0',5);payload=parts[-1]
                if parts[1][:1]==b'\x01':payload=zlib.decompress(payload)
                result.append(payload.decode('utf-8','replace'))
        except (ValueError,zlib.error):result.append('UNREADABLE_PNG_TEXT')
    return result

def audit(root,deny=()):
    root=Path(root).resolve();findings=[];files=[]
    absolute=re.compile(r'/(?:Users|home)/[A-Za-z0-9_.-]+/|[A-Za-z]:\\(?:Users|Documents)\\|file:/'+r'/')
    for path in sorted(root.rglob('*')):
        rel=path.relative_to(root).as_posix()
        if path.is_symlink():findings.append(dict(file=rel,rule='symlink'));continue
        if not path.is_file():continue
        if '__pycache__' in path.parts or path.suffix in ('.pyc','.pyo'):findings.append(dict(file=rel,rule='cache-file'));continue
        data=path.read_bytes();files.append(dict(file=rel,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
        texts=[rel]
        if data.startswith(b'\x89PNG\r\n\x1a\n'):
            metadata=png_text(data);texts+=metadata
            if 'UNREADABLE_PNG_TEXT' in metadata:findings.append(dict(file=rel,rule='unreadable-png-metadata'))
        else:
            try:texts.append(data.decode('utf-8'))
            except UnicodeDecodeError:findings.append(dict(file=rel,rule='unreviewed-binary'));continue
        for text in list(texts):
            for payload in re.findall(r'data:image/svg\+xml(?:;base64)?,([A-Za-z0-9+/=]+)',text):
                try:texts.append(base64.b64decode(payload).decode('utf-8'))
                except Exception:findings.append(dict(file=rel,rule='unreadable-svg'))
        for text in list(texts):
            for payload in re.findall(r'stencil\(([A-Za-z0-9+/=]+)\)',text):
                try:texts.append(unquote(zlib.decompress(base64.b64decode(payload),-15).decode('utf-8')))
                except (ValueError,zlib.error,UnicodeDecodeError):findings.append(dict(file=rel,rule='unreadable-stencil'))
        normalized=[]
        for text in texts:
            normalized.append(text)
            for _ in range(2):
                text=unicodedata.normalize('NFKC',html.unescape(unquote(text)))
                text=re.sub(r'\\u([0-9a-fA-F]{4})',lambda m:chr(int(m[1],16)),text)
                normalized.append(text)
        for text in normalized:
            if absolute.search(text):findings.append(dict(file=rel,rule='absolute-workstation-path'))
            for num,term in enumerate(deny):
                if term.casefold() in text.casefold():findings.append(dict(file=rel,rule='private-deny-match',deny_entry=num+1))
        if path.suffix=='.md':
            for link in re.findall(r'\]\(([^)]+)\)',data.decode('utf-8')):
                if not re.match(r'^(?:https?://|#)',link):
                    target=(path.parent/link.split('#',1)[0]).resolve()
                    if not target.is_relative_to(root):findings.append(dict(file=rel,rule='outside-relative-link'))
                    elif not target.exists():findings.append(dict(file=rel,rule='broken-relative-link'))
    return dict(passed=not findings,files_scanned=len(files),deny_entries_checked=len(deny),findings=findings,inventory=files,scope='Text files, relative Markdown links, filenames, decoded embedded SVG, native stencils and PNG text metadata; manual semantic/artwork review still required')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root');p.add_argument('--deny-file',type=Path);p.add_argument('--report',type=Path);a=p.parse_args();deny=[]
    if a.deny_file:deny=[x.strip() for x in a.deny_file.read_text().splitlines() if x.strip()]
    if a.deny_file and a.deny_file.resolve().is_relative_to(Path(a.root).resolve()):p.error('Keep the private deny-list outside the release tree')
    r=audit(a.root,deny);out=json.dumps(r,indent=2)
    if a.report:a.report.write_text(out)
    print(json.dumps({k:v for k,v in r.items() if k!='inventory'},indent=2));raise SystemExit(not r['passed'])
