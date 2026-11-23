## Feature A — read-aloud speech recognition feedback

Windows Chrome manual checks (open single-file.html or serve localhost): open a read-aloud task, tap Check Reading, allow permissions, read with omitted/extra words, stop, and check live transcript, highlighted target, recognition match count and slow missed-word buttons. Intermediate task 010 must compare the full sample, not its short heading. Try again; notes must remain unchanged. Open answers show transcript only. Verify Record/Listen/Slow cannot overlap recognition, recording and recognition remain separate, music ducks, closing/reopening clears recognition, and a transcript of three English words enables self-review. This is 語音辨識參考，不是專業發音評分.

iPhone Safari hardware plan (pending): iOS 14.5+, Siri and Dictation must be on. Use HTTPS; accept first-use microphone and speech-recognition permission prompts. Check interim results, Stop, slow reading, repeat-task audio, retry and dialog cancel. Deny permissions and expect Traditional Chinese permission guidance; disable Siri/Dictation and expect service-not-allowed guidance; test no speech, unavailable microphone and offline/network fallback. Unsupported browsers such as Firefox must hide Check Reading and retain recording/notes. Confirm the mic indicator clears after stopping/closing and no transcript is saved to localStorage. Recording stays local to the page; recognition sends audio to the browser's speech service (Chrome/Google, Safari/Apple) only after tapping; the site does not upload or save recognition audio or transcripts.

Options: Web Speech API is free and used here. In-browser Whisper is free but requires roughly 40–150 MB of model downloads and can be slow on phones; not used. Paid APIs are not enabled. Mocked Chromium checks do not verify actual speech quality, Windows permissions or iPhone hardware.

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

## Level-matched YouTube recommendations — local Chromium PASS

- Catalog schema contained 13 unique recommendations with direct HTTPS YouTube watch URLs, valid 11-character video IDs, creator/source metadata and original study guidance. All six level groups provided both song and story/short-film choices. Level/type filters, All Levels and Match My Trail returned the expected cards.
- Clicking a recommendation opened its direct watch URL in a new tab with noopener/noreferrer. No YouTube iframe, thumbnail or third-party media request occurred before a click. Popup content was stubbed in this test: external YouTube video playback is NOT claimed as verified; source checks and the environment's 403/throttling limits are recorded in MEDIA-SOURCES.md.
- Opening an external viewing link paused the original local song and temporarily suppressed instrumental music while retaining the user's Music On preference. Resume Site Audio restored that preference. Learning completions remained unchanged.
- The original song player remained reachable and playable. The rebuilt standalone included all 13 recommendation cards plus embedded original audio. Existing fish/puzzle/song tests passed after the new catalog was integrated.
- Phone layout down to 320px and desktop layout passed with no horizontal page overflow or uncaught JavaScript errors. Safari hardware remains pending, especially new-tab focus return and media resume behavior.

## Mobile experience batch — iOS Simulator Safari + local Chromium PASS

- iPhone 17 Simulator Safari (402px wide): the page was 40px wider than the screen on every page because of the hidden Import JSON file input. After the fix the page width matches the screen exactly on Home, Map, Library, GEPT and Rest Grove. Chromium at 320, 375, 402 and 1280px also showed no horizontal overflow.
- Simulator Safari: every select used 13px text before the fix (iOS zooms in on focus below 16px). After the fix every select, search box and textarea is 16px on touch screens. Desktop sizes are unchanged.
- Chromium with a synthetic microphone: pressing Record while a song was paused for read-aloud briefly restarted the song before recording began. After the fix the song stays paused while recording and resumes once recording stops.
- Chromium tab switch: before the fix the song and background music kept playing in a hidden tab. After the fix the song pauses and the instrumental scheduler and gain go silent while the tab is hidden; both resume when the tab is visible again, keeping the Music On choice. The AudioContext is not suspended explicitly, because in Simulator Safari an explicit suspend stayed suspended after Home → Safari while iOS's own interruption recovers by itself; a tap while Music On also resumes it.
- No autoplay on load, a completion survived reload, the fish game reached 5/5, the puzzle had 9 tiles, and no uncaught JavaScript errors occurred.
- Safari blocks scripted playback without a tap, so audio resume after recording and after a tab switch still needs a check on a physical iPhone.


## 完成練習後自動前進

- 地圖新增「自動前進 / 手動前進」切換，預設自動，設定與到站位置分別保存在本機。重新載入會還原路線、站點與小鹿位置；無效站點回到該路線第 1 站。
- 完成選擇題、單句題或自評後，只有成功寫入並讀回進度，才顯示約 1.2 秒「過關！進度已保存」動畫。自動模式顯示約 3 秒倒數，可立即前往或取消；手動模式只顯示「前往下一關 →」。只走到目前站的下一站，不略過已完成站點，末站不再前進。
- 編輯、點擊、按鍵、聽錄音或錄音中會停止倒數，改用手動按鈕；離開教材或頁面會清除待執行動作。儲存失敗時不前進，提示匯出 JSON 備份。減少動態效果時不播放跳躍動畫。

### Windows Chrome 操作步驟（硬體結果待驗）

1. 用 Chrome 開啟 `single-file.html`（`file://`），或執行 `python3 -m http.server 8000` 開啟 `http://localhost:8000`。兩種來源的本機資料各自獨立；若瀏覽器限制 file 儲存，改用 localhost。
2. 從地圖第一站答對，確認過關動畫、倒數、步行到緊鄰下一站並開啟教材；重做已完成站仍只前進一站。點「立即前往」應立即步行；「留在這題 / 取消」應保留教材並顯示手動按鈕。
3. 切至手動，完成練習後等候至少 5 秒，確認不移動，再按下一關。換路線、走到其他站、重整，確認路線選單、小鹿與設定一致。
4. 倒數期間編輯回答／筆記、點 Listen、Retry、自評核取方塊或關閉教材，等待 5 秒確認沒有延遲跳轉。末站完成應提示「本路線已全部走完」。從考題庫開始與開放式題目自評收藏仍應正常。
5. 封鎖網站儲存後答對，確認提示匯出備份而不自動前進。

### iPhone Safari 手動測試計畫（實機硬體結果待驗）

1. 從 localhost 的區網網址或可用網站載入，以觸控點站、切換自動／手動、立即前往與取消；確認按鈕可點且文字不遮擋。
2. 在不同級別與站點重新載入，確認小鹿、選單、設定還原。檢查直向窄螢幕與教材捲動。
3. 開啟 iOS「減少動態效果」，完成練習應顯示靜態過關訊息而沒有跳躍。
4. 允許麥克風，錄音、停止、回放、自評完成；回放不得被自動關閉教材或跳站中斷。倒數時開始回放或編輯筆記，確認改用手動按鈕；切換分頁後不得偷偷前進。

自動化：`python3 tools/test-auto-advance.py` 使用本機 Playwright Chromium，涵蓋桌面及 390×844 觸控模擬、成功／手動／取消／編輯／模擬錄音回放、末站、重載、自評與儲存錯誤。Linux 模擬結果不代表 Windows 或 iPhone 實機結果；真實麥克風與 Safari 音訊行為仍待實機驗證。
## Promotion kit

The promo/ download page includes a 45-second 1080p H.264/AAC film, a PNG/SVG website QR, a portrait QR poster, a YouTube thumbnail, Chinese/English SRT files and suggested description text. Independent QR decoding, full movie decoding, browser playback/seek, download hash matching and responsive preview checks passed. Details and actual-device/platform limits are recorded in promo/README.md. Only original site footage and original music are included; external YouTube performances are not part of the film.
