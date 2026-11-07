# Little Deer English Trail — promotion kit

Website / QR target: https://luckydeer3776.github.io/little-deer-english-trail/

Public preview and downloads: https://luckydeer3776.github.io/little-deer-english-trail/promo/

| File | Purpose / format |
| --- | --- |
| little-deer-promo.mp4 | 45.000-second 1920×1080, 16:9, 30 fps, H.264 yuv420p video + stereo AAC 48 kHz audio; fast-start MP4; about 3.3 MB |
| qr-code.png | 900×900 high-contrast dark-green-on-white QR, error correction Q, quiet border |
| qr-code.svg | Scalable QR with a white background |
| qr-poster.png | 1080×1350 portrait QR poster |
| youtube-thumbnail.jpg | 1280×720 upload-ready thumbnail |
| captions-zh-Hant.srt | Seven Traditional Chinese caption cues, 0–45 seconds |
| captions-en.srt | Seven English subtitle cues, 0–45 seconds |
| youtube-description.txt | Suggested title and copy-ready YouTube description |

## Video content

- 0–5 s: Little Deer English Trail introduction.
- 5–14 s: Actual deer movement, wrong-answer retry, correct answer and phrase collection/library UI.
- 14–21 s: Original GEPT-style question practice. The film labels it as original preparation, not official questions.
- 21–26 s: Fish-catching game.
- 26–31 s: Picture puzzle.
- 31–37 s: Level-matched YouTube recommendation cards, without opening or playing external videos.
- 37–45 s: Static QR ending, held for scanning.

All scenes were captured from actual site interactions in fresh browser contexts containing only demonstration progress. No private account information or real learner records are shown. Designed titles, Traditional Chinese captions and an original instrumental score are included. There is no spoken narration.

The soundtrack is locally synthesized using this project's original melodic motif and arrangement. No external song recording, YouTube footage, third-party backing track or celebrity performance is included. The two puzzle/forest illustrations and layout are original project assets. Original promotional material is covered by ../LICENSE.txt and may be uploaded to YouTube or used for this event. Linked external media elsewhere in the app remain outside that license.

## Validation

- ffprobe verified the exact 45-second duration, 1920×1080 dimensions, H.264/yuv420p at 30 fps and stereo AAC 48 kHz. The complete MP4 decoded without errors.
- MP4 metadata appears before media data for web streaming. Audio analysis measured mean volume -22.6 dB and maximum -7.0 dB, with no clipping.
- An independent ZXing decoder recovered the exact website URL from the PNG, poster, thumbnail, rendered SVG, and the final encoded video's QR frame at both 1080p and 720p.
- Chromium played and sought the local preview without autoplay. The browser-downloaded MP4 matched the source SHA-256 hash. All companion downloads responded successfully, and the 390px-wide page had no horizontal overflow.
- QR tests are software decoding tests, not a claim of physical-camera testing. Actual YouTube account upload/transcoding and Safari hardware playback were not performed.

Use the Download Video button on this page to save the MP4, then choose YouTube Studio → Create → Upload videos. The film already contains Chinese text; the optional SRT files can supply selectable captions and accessibility indexing.
