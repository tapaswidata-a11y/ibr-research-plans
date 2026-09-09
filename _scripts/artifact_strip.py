"""Strip the standalone-HTML wrapper so a page can be published as a Claude Artifact.

The repo copies are full HTML5 documents, because GitHub Pages serves them directly.
The Artifact publisher wraps page content in its own <!doctype html><head></head><body>
skeleton, so publishing a wrapped file would nest one document inside another.

    python3 _scripts/artifact_strip.py das_primer.html        # -> /tmp/.../das_primer.artifact.html

Then publish the printed path with the artifact's existing `url`, so the link is preserved.
"""
import os, re, sys, tempfile

def strip(html: str) -> str:
    # keep everything from <title> onwards - the platform supplies charset/viewport
    i = html.find('<title>')
    if i == -1:
        sys.exit('no <title> found; is this one of the page files?')
    body = html[i:]
    # the platform opens <body> itself
    body = re.sub(r'</head>\s*<body[^>]*>\s*', '', body, count=1)
    # ... and closes the document itself
    body = re.sub(r'\s*</body>\s*</html>\s*$', '\n', body)
    return body

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = sys.argv[1]
    out = os.path.join(tempfile.gettempdir(),
                       os.path.basename(src).replace('.html', '.artifact.html'))
    text = strip(open(src).read())
    open(out, 'w').write(text)
    bad = [t for t in ('<!DOCTYPE', '<html', '</head>', '<body') if t.lower() in text.lower()]
    print(f'{src} -> {out}  ({len(text)} bytes)')
    print('leftover document tags:', bad or 'none')
