"""Bundle the static application and its original media into one HTML file."""
from pathlib import Path
import base64
import re

root = Path(__file__).resolve().parent.parent
html = (root / 'index.html').read_text()
html = re.sub(r'<link rel="stylesheet" href="style.css[^\"]*">', lambda _: '<style>' + (root / 'style.css').read_text() + '</style>', html)
html = re.sub(r'<script defer src="(?:lessons|exam-data|songs-data|videos-data|app|play).js[^\"]*"></script>', '', html)
replacements = {}
for directory, mime in [('assets/audio', 'audio/mpeg'), ('assets/art', 'image/svg+xml')]:
    for path in (root / directory).iterdir():
        if path.is_file():
            replacements[path.relative_to(root).as_posix()] = 'data:' + mime + ';base64,' + base64.b64encode(path.read_bytes()).decode()
parts = []
for name in ['lessons.js', 'exam-data.js', 'songs-data.js', 'app.js', 'videos-data.js', 'play.js']:
    code = (root / name).read_text()
    for source, data in replacements.items():
        code = code.replace(source, data)
    parts.append('<script>' + code + '</script>')
html = html.replace('</body>', ''.join(parts) + '</body>')
html = html.replace('href="AUDIO-CREDITS.md"', 'href="https://luckydeer3776.github.io/little-deer-english-trail/AUDIO-CREDITS.md"')
html = html.replace('href="promo/"', 'href="https://luckydeer3776.github.io/little-deer-english-trail/promo/"')
(root / 'single-file.html').write_text(html)
print('single-file.html built with embedded original audio and art.')
