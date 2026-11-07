# Verification — Self-paced GEPT upgrade

## Local automated Chromium: PASS

Tests ran against the static website in system Chromium with Playwright at phone and desktop sizes, including a 320px-wide layout check. All 63 original GEPT tasks were exercised in the browser. No uncaught application errors occurred in the full question-bank run.

- Existing version-1 completion for the original `help-003` ID survived reload and appeared on both the map and library.
- Original A1 stations, including those formerly scheduled in the future, were immediately available. All five GEPT levels had actual tasks and no date locks.
- Level/skill/type filters displayed the expected counts: Elementary 28, Intermediate 12, High-Intermediate 11, Advanced 10, Superior 2. All task IDs were unique and each referenced a valid level/type; choice-answer indices were in range.
- Starting from the GEPT bank selected the corresponding trail and moved the deer before opening a card. A long-distance path was tested with normal animation; no card opened during intermediate movement. Reduced-motion flow passed separately.
- Choice questions: incorrect responses showed hints and allowed repeated attempts; correct answers completed and saved. Retry hid reference answers again and preserved existing completions.
- Sentence writing: wrong text showed a retry hint; an accepted complete sentence saved completion. References were unavailable before an attempt.
- Open writing: a submitted draft exposed model material and self-review. Completion required all review checks. It was saved explicitly as self-reviewed practice, not an automatically graded correct answer. Drafts survived reload.
- Speaking: missing recording/answer notes blocked self-review. Notes enabled self-review as a microphone fallback. Actual MediaRecorder capture, stop, playback availability, re-recording and stream/URL cleanup passed with a synthetic Chromium microphone. A denied getUserMedia request produced the fallback message without breaking learning.
- New and repeated practice did not duplicate the library. A backup containing 65 test completions and text drafts exported as valid JSON; re-import added zero duplicate records.
- Speech/music callbacks were mocked for deterministic end/error tests. The user's on/off preference was respected, including turning music off during speech. Audio context initialization passed. These are logic checks, not verification of audible voice/music quality.
- The rebuilt single-file.html opened the upgraded question bank successfully. The homepage GEPT shortcut worked.

## Intended behavior and scope

No due date needs to be set. Historical completion dates remain automatic so sorting and old backups keep working. All content can be repeated without limits. Open writing and speaking are self-review exercises; no AI grading service or official score is provided.

The 63 tasks are original preparatory exercises spanning task families. They are not complete exam-length papers or comprehensive coverage of all vocabulary and difficulty at each level. Advanced and superior source inputs are shortened and the interface says so. Superior registration is commissioned; consult official specifications linked in README and the interface.

## iPhone Safari hardware acceptance — PENDING

Phone-sized Chromium tests do not establish iPhone Safari compatibility. Verify these on an actual device:

1. Open the final HTTPS URL; check portrait/landscape, scrolling map and keyboard/touch focus.
2. Enter GEPT Practice, choose levels and skills, repeat a wrong answer, then complete and revisit it.
3. Write a draft, close/reopen Safari and verify it remains. Export JSON to Files and import it back without duplicates.
4. Allow microphone permission, record, stop, listen and re-record. Close the card and verify Safari's microphone indicator clears. Also test denying permission and using answer notes.
5. Verify quiet original background music, en-US speech, muting during listening/recording/playback, and return to the current music preference. Verify unavailable audio does not block questions.
6. Enable Reduce Motion and confirm arrival gating, tap targets, VoiceOver labels and legibility.

## Publishing

The owner-created public repository is LuckyDeer3776/little-deer-english-trail. GitHub Pages serves main from the repository root. Only application source and public documentation are committed. Test recordings, completion backups and local draft data are excluded. Release status and live URL are confirmed in the delivery message after deployment.

## Picture-answer clarity fix

All three picture-listening tasks now display the complete English answer choices instead of letter-only placeholders. Both picture-answer tasks show directly clickable images with descriptive English captions. Targeted Chromium checks verified all five affected tasks: readable option content, correct choice counts, image click handling, incorrect-answer retry, hidden reference on a fresh attempt, and desktop/mobile layouts, with no JavaScript errors. These checks validate practice behavior; they do not assess official-exam equivalence.

## Rest Grove upgrade — local Chromium PASS

- Randomized optional rest markers appeared between lessons and remained stable during a trail's open session. Three distinct practiced IDs showed a dismissible invitation. Skipping did not alter progress.
- Fish targets were keyboard-focusable native buttons. Catching five won a round; replay reset it. Puzzle swaps could solve the board; reference image, number hints, keyboard focus and replay passed. Both games had no countdown and left phrase completion records unchanged. Independent win counts survived reload.
- All three actual MP3 assets decoded and played in Chromium, with valid 40–60 second durations. No song autoplay occurred on entering the grove. Lyrics highlighted, track changes worked and looping could be enabled.
- Shared audio checks verified quiet background music during song playback, automatic song pause for mocked lesson speech and open games, resumption afterward, and preservation of an explicit manual Stop Song choice. Speech callbacks were mocked for deterministic logic; these tests do not establish subjective singing quality or actual-device audio behavior.
- Phone layouts including 320px and desktop layouts passed without horizontal page overflow. No uncaught JavaScript errors in the game/song run.
- Safari hardware remains pending: specifically verify MP3 controls/looping, resume after Web Speech and microphone interruptions, direct fish touch targets, puzzle taps and reduced-motion preference on a physical iPhone.

Additional checks passed for automatic song interruption/resumption during synthetic-microphone capture and recorded-audio playback, Stop Song inside a lesson, map keyboard suppression behind a game, normal fish animation and continued answering after a forced MP3 load failure. Standalone embedded songs and puzzle art were verified over HTTP without separate asset requests. Direct file:// navigation could not be tested because the managed browser blocks that scheme by administrator policy.
