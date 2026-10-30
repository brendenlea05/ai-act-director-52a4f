"""Offline EPUB package sanity checks; not a replacement for EPUBCheck."""
import argparse, json, posixpath, zipfile
from xml.etree import ElementTree as ET
NS={'c':'urn:oasis:names:tc:opendocument:xmlns:container','opf':'http://www.idpf.org/2007/opf'}
def review(path):
    out=[]
    def flag(code,detail): out.append({'code':code,'detail':detail})
    try:
        with zipfile.ZipFile(path) as z:
            names=set(z.namelist())
            if 'mimetype' not in names: flag('MISSING_MIMETYPE','No mimetype entry')
            else:
                if z.read('mimetype')!=b'application/epub+zip': flag('INVALID_MIMETYPE','Unexpected mimetype')
                if z.infolist()[0].filename!='mimetype' or z.getinfo('mimetype').compress_type!=zipfile.ZIP_STORED: flag('MIMETYPE_PACKAGING','mimetype must be first and stored')
            container='META-INF/container.xml'
            if container not in names: flag('MISSING_CONTAINER',container); return out
            try:
                root=ET.fromstring(z.read(container)).find('.//c:rootfile',NS)
                opf=root.attrib.get('full-path') if root is not None else None
                if not opf or opf not in names: flag('MISSING_PACKAGE','OPF path absent'); return out
                package=ET.fromstring(z.read(opf))
            except (ET.ParseError,KeyError,ValueError) as e: flag('INVALID_XML',str(e)); return out
            manifest=package.find('opf:manifest',NS); spine=package.find('opf:spine',NS)
            if manifest is None or spine is None: flag('MISSING_STRUCTURE','manifest/spine absent'); return out
            entries={}
            for item in manifest.findall('opf:item',NS):
                ident=item.attrib.get('id',''); href=item.attrib.get('href','')
                if not ident or ident in entries: flag('BAD_MANIFEST_ID',ident)
                entries[ident]=item
                if '://' not in href and not href.startswith('data:'):
                    resolved=posixpath.normpath(posixpath.join(posixpath.dirname(opf),href.split('#')[0].split('?')[0]))
                    if resolved not in names: flag('MISSING_RESOURCE',ident+': '+resolved)
            for ref in spine.findall('opf:itemref',NS):
                if ref.attrib.get('idref') not in entries: flag('BROKEN_SPINE',str(ref.attrib.get('idref')))
            if not any('nav' in x.attrib.get('properties','').split() for x in entries.values()):
                flag('MISSING_NAV','No EPUB3 navigation item (EPUB2 may use NCX)')
    except (OSError,zipfile.BadZipFile,zipfile.LargeZipFile) as e: flag('UNREADABLE_ZIP',str(e))
    return out
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('epub'); args=p.parse_args()
    findings=review(args.epub)
    print(json.dumps({'findings':findings,'count':len(findings)},indent=2))
    raise SystemExit(bool(findings))
