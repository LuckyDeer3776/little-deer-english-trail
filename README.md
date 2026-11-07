# Little Deer English Trail

A self-paced American English trail with original GEPT practice. #DEVDAYCOMMUNITU

Public website: https://luckydeer3776.github.io/little-deer-english-trail/

## What changed

All lessons are available immediately. There are no opening dates, daily locks, due dates, or limits on retries. Previous completions remain saved under the original browser storage key and the original eight phrase IDs. Completion dates are automatic historical timestamps, not deadlines and not dates the learner needs to set.

The site contains 8 original A1 phrase stations and 63 original GEPT preparatory tasks:

| Level | Tasks | Scope |
| --- | ---: | --- |
| Elementary 初級 | 28 | Two tasks for each of 14 task families across listening, reading, writing and speaking |
| Intermediate 中級 | 12 | Picture listening, responses, dialogue, talks, vocabulary, cloze, reading, translation, essay, read-aloud, questions and picture description |
| High-Intermediate 中高級 | 11 | Responses, dialogue, talks, vocabulary, cloze, reading, translation, essay, questions, picture description and presentation |
| Advanced 高級 | 10 | Short/long conversations and talks, scanning, careful reading, synthesis, charts, interview, information exchange and presentation |
| Superior 優級 | 2 | Integrated writing and speaking, with shortened reading/listening inputs |

These are original, separate practice exercises, not official exam questions, complete full-length papers, a certification service, or a guarantee of passing. Advanced and superior inputs are intentionally shortened. Consult official GEPT specifications for full-length examinations and registration. Superior is offered on a commissioned basis. Official sources: [Elementary](https://www.gept.org.tw/Exam_Intro/t01_introduction.asp), [Intermediate](https://www.gept.org.tw/Exam_Intro/t02_introduction.asp), [High-Intermediate](https://www.gept.org.tw/Exam_Intro/t03_introduction.asp), [Advanced](https://www.gept.org.tw/Exam_Intro/t04_introduction.asp), [Superior](https://www.gept.org.tw/Exam_Intro/t05_introduction.asp).

## How to practice

- Start Learning opens the generated map. Choose a trail level and a station. The deer travels along the route and opens the card at arrival.
- GEPT Practice / Explore GEPT opens the question bank. Filter by level, skill and task family. Every question is available without a schedule.
- Wrong choice or sentence answer: read the hint and try again without limit. After an attempt you can reveal reference material, then retry. Revealing a reference alone does not complete a task.
- Correct choice or matching sentence: completion is saved once. Retry starts a fresh attempt with answers hidden and keeps the earlier completion.
- Free writing: save a draft, submit for self-review, compare the model and check content, structure and language. This is not automatic essay grading. Sentence checks are reference matches, including listed variants; they are not a general grammar engine. Sentence rewriting tasks check capitalization and punctuation.
- Speaking: listen/read the prompt, record and replay, then self-review. Grant microphone access if prompted. On unsupported devices or denied permission, speak aloud and enter answer notes before reviewing. There is no automatic pronunciation score or official grade. Recordings stay in the page and are discarded when leaving the card. A single recording is capped at ten minutes to bound device resource use; re-recording is unlimited.
- My Phrase Library uses the same completion records. Search English/Chinese, sort by historical completion date, listen or practice again. Self-reviewed tasks are labelled accordingly.

## Local use and deployment

No dependencies or build step are required. Serve this folder with:

    python3 -m http.server 8000

Open http://localhost:8000. GitHub Pages serves `main` from `/(root)` and republishes pushes. The `index.html` asset query version should be updated after relevant releases so returning visitors receive matching assets. No private projects or user progress belong in this repository.

`single-file.html` is a bundled alternative. Local file storage and microphone availability vary by browser, so HTTPS hosting is recommended.

## Edit content

- `lessons.js`: the original 8 A1 phrase stations.
- `exam-data.js`: 63 original GEPT preparatory tasks. Add a task with a permanent unique `id`, `level`, `skill`, `type`, `title`, `en`, `zh`, `context`, `question`, and `mode`. No dates are required. Do not rename existing IDs or remove old content.
- Modes: `choice` uses `options` and a zero-based `answer`; `text` uses `accepted` answer variants; `open` and `speak` use a `sample` reference and self-review. Optional fields include `passage`, `audio`, `picture`, `pictureOptions`, `hint`, `explain`, `minWords`, `targetWords`.
- `app.js`: level/type labels, rendering, persistence, audio and practice behavior. Map geometry and question filters derive from content data.
- To add a new type or level, add its label/description to `TYPES` or `LEVELS` in `app.js` along with the corresponding task data.

After modular or media changes, run `python3 tools/build-standalone.py` to rebuild the standalone HTML with styles, scripts, original puzzle images and song MP3s embedded.

## Storage and backup

Completions use `little-deer-progress-v1`. Text drafts use `little-deer-drafts-v1`. Old version-1 backups remain supported. Export includes completion records and text drafts, but no microphone recordings. Import merges valid ISO timestamps, preserves earliest completion per ID, deduplicates, rejects future/malformed completion timestamps, and retains existing drafts. Records with unknown IDs are retained but only appear once the matching content exists. No release-date restrictions apply.

Progress and drafts are local to this browser and origin. Export before clearing data or changing devices. Storage failure shows a message; practicing remains possible. No accounts, analytics, APIs, server database, or recording uploads are used.

## Audio and art

Background music is an original quiet instrumental loop synthesized locally with Web Audio; starts only after Music On. Music mutes during speech, microphone recording and recorded-audio playback and follows the current on/off preference afterward. Speech requests the device's en-US voice. Unsupported audio does not prevent learning. Picture tasks use original inline SVG art. No external music, images or fonts are bundled. See LICENSE.txt and ACCEPTANCE.md.

## The Rest Grove — games and songs

`Play & Songs` opens optional breaks without changing learning completion records:

- **Little Fish Pond:** six large, softly animated fish; catch any five with touch, mouse or keyboard. No timer, score penalty, or learning gate. Replay freely. Reduced-motion preference stops the swimming animation.
- **Forest Picture Puzzle:** a 3×3 swap puzzle using one of two original pictures. Select any two pieces to swap; every shuffle is solvable. Keyboard arrows move focus, Enter/Space selects. Show the reference image or piece numbers at any time. No dragging or countdown required.
- **Little English Songs:** three original short songs with synthesized vocals, original instrumental arrangements and synchronized English/Traditional Chinese lyrics. Native audio controls offer play/pause/seek/volume, and the page adds track selection and optional looping. No autoplay. See AUDIO-CREDITS.md and FLITE-NOTICE.txt.

The map generates optional rest markers between lessons at randomized intervals and varies fish, puzzle and song stops. A plan stays stable for that trail during the open session; reopening can produce different stops. After practicing three different lesson IDs in a session, a dismissible invitation offers a break. It never blocks answers or opens a game automatically. `Surprise Break` can start either game without waiting.

Songs may continue between website sections after the user starts playback. Background instrumental music is muted while a song plays. Songs pause for lesson speech, microphone recording, recorded-audio playback and games; they resume only if the user still wants the song on. A Stop Song control is available on learning cards. Media failure leaves learning and the other activities available.

`play.js` manages rest markers, games and song coordination. `songs-data.js` contains song metadata, audio paths and bilingual lyric timings. MP3s are in `assets/audio/`; puzzle SVGs are in `assets/art/`. Add future songs using the same metadata schema, with a verified license and credits. Game win counts use the separate local key `little-deer-rest-v1`. They are independent from phrase completions and are not part of the learning JSON backup.

The standalone HTML embeds the two puzzle images and three MP3s so it can play them without downloading adjacent files. This makes that optional file larger than the modular website.
