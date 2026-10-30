import tempfile,zipfile
from pathlib import Path
from epub_preflight import review
CONTAINER='<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OPS/content.opf"/></rootfiles></container>'
PACKAGE='<package xmlns="http://www.idpf.org/2007/opf"><manifest><item id="nav" href="nav.xhtml" properties="nav"/><item id="chapter" href="chapter.xhtml"/></manifest><spine><itemref idref="chapter"/></spine></package>'
def build(path,broken=False):
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('mimetype','application/epub+zip',compress_type=zipfile.ZIP_STORED)
        z.writestr('META-INF/container.xml',CONTAINER)
        z.writestr('OPS/content.opf',PACKAGE.replace('idref="chapter"','idref="missing"') if broken else PACKAGE)
        z.writestr('OPS/nav.xhtml','<html/>')
        if not broken:z.writestr('OPS/chapter.xhtml','<html/>')
with tempfile.TemporaryDirectory() as d:
    clean=Path(d)/'clean.epub'; broken=Path(d)/'broken.epub'
    build(clean);build(broken,True)
    assert review(clean)==[],review(clean)
    assert {f['code'] for f in review(broken)}=={'MISSING_RESOURCE','BROKEN_SPINE'},review(broken)
    print('PASS: clean and intentionally broken synthetic EPUBs')
