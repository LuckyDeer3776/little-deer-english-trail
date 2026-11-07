# Little Deer English Trail

Static, mobile-first A1 American English learning trail. #DEVDAYCOMMUNITU

## Open locally

Open index.html in Chrome or Safari. No build, package installation, or external assets are required. For consistent localStorage behavior, use a local web server:

    python3 -m http.server 8000

Open http://localhost:8000. single-file.html contains the same app in one HTML file. Browser storage belongs to its origin; local file storage may vary by browser. Use JSON backup before switching to a different host or browser. The public release requires no login, download, or extraction once published.

## Public website

https://luckydeer3776.github.io/little-deer-english-trail/

This repository contains only Little Deer English Trail and its teaching materials. GitHub Pages serves the main branch from the repository root. To update the site, edit the modular files and commit to main; Pages rebuilds automatically. Keep lesson IDs stable to preserve existing learning records. No build or dependency installation is required.

## Add lessons

Edit lessons.js. Append an object with a unique permanent `id`, a Taipei opening `date` in YYYY-MM-DD format, `title`, `en`, `zh`, `context`, `question`, `options`, zero-based `answer`, `hint`, and `explain`. Keep dates unique and in ascending order to unlock one station daily. Never rename released IDs. Leave existing entries in place to preserve historical stations and searchable phrases. The first batch opens 2026-11-05 through 2026-11-12 (Asia/Taipei); there are two catch-up stations on the event day, 2026-11-07. Thereafter all opened stations stay available.

The map geometry is generated from lesson order. No manual route changes are needed. No reset occurs when all lessons are released. Completion records are stored once per ID, with an ISO timestamp. Displayed completion dates use Asia/Taipei. Imports merge valid records, retain the earliest completion timestamp, reject malformed dates, future completions and completions before opening. Unknown IDs are retained as valid records for compatibility with future catalog versions but do not appear until their lesson exists.

After editing the modular files, update single-file.html if you distribute it: replace its embedded style, lesson-data and app-script sections with the corresponding files. GitHub Pages uses index.html and does not depend on single-file.html.

## Audio and assets

Music is an original repeating 16-note instrumental melody with bass, synthesized with Web Audio sine/triangle oscillators at low gain. No third-party music, recordings, external images, external fonts, APIs or analytics are used. The background loop starts only after Music On. Speech uses the device Web Speech API, requesting en-US at a slow rate. Available voices, network needs and audible output depend on device settings. Audio failure does not block learning. System deer emoji rendering differs by device.

See LICENSE.txt for permissions, ACCEPTANCE.md for verification, and YOUTUBE.txt for description copy.
