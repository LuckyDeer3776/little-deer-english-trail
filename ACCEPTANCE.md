# Verification — 2026-11-07

## Automated Chromium results: PASS

Executed against the actual static site using system Chromium via Playwright, at 390 × 844 (phone simulation) and 1440 × 1000 (desktop). Browser console had no uncaught application errors in the primary end-to-end run. No iPhone hardware or desktop Google Chrome binary was used.

- Start Learning → map → select station → animated deer follows generated route → card opens only after arrival.
- Non-reduced movement verified by intermediate deer coordinates and absence of an open card during movement. Reduced-motion flow also passed.
- Keyboard left arrow moves to previous station; touch-oriented buttons and mouse station clicks use the same movement function.
- Flip card shows Traditional Chinese. Listen invokes browser speech. Incorrect answer shows hint and allows retry. Correct answer reveals explanation and records completion.
- Back to Map shows dated sentence marker; library shows the same completed sentence.
- Repeated practice and page reload retain exactly one record per lesson. English and Traditional Chinese search passed.
- JSON export produced a downloadable, parseable backup. Re-importing duplicates added zero records; merging two valid new records added two. Invalid JSON was rejected and a premature future lesson completion was excluded.
- Simulated Taipei 2026-11-07 23:59:40 → 2026-11-08 00:00:10 in the still-open page: the next lesson became Today. Returning to the tab also refreshes availability.
- Older station catch-up passed. Moving date beyond the final release unlocked all stations and preserved three existing completion markers.
- Web Audio context initialized after a Music On click. Speech callbacks were mocked to deterministically test music ducking state and recovery: end restores the current on preference; turning music off during speech keeps it off; speech error leaves learning usable. Actual sound/voice quality is NOT confirmed by these tests.

## iPhone Safari hardware acceptance — PENDING, separate from simulation

1. Open the final HTTPS Pages URL in iPhone Safari. Confirm landscape/portrait layouts, scrolling map, tappable controls and readable cards.
2. Click Music On and verify quiet, instrumental looping playback. Leave it on while switching map / cards / library.
3. Tap Listen: music must mute for the whole spoken sentence, then return. Switch Music Off during speech and confirm it stays off afterward. Verify the installed voice speaks American English intelligibly. Test with silent mode / device volume set appropriately.
4. Complete one station, close/reopen Safari and the site, verify progress. Export to Files and import back; check deduplication.
5. Enable iOS Reduce Motion; confirm movement remains understandable and the card opens at the destination.
6. Verify external keyboard focus / VoiceOver labels where available. Test JSON file picker and download behavior.
7. With a test device clock around Taipei midnight, leave page open then background/foreground it; verify next station unlocks and previous history remains.
8. Test audio unavailable / offline behavior: reading, answering and local progress must remain usable; device speech availability can vary.

## Deployment

The owner created a new independent public repository, LuckyDeer3776/little-deer-english-trail, after the integration could not create one. Only this standalone website and its documentation are uploaded. GitHub Pages is configured for main at the repository root. Local Chromium results above precede deployment; live deployment verification is recorded separately below.

## Known platform limits

Browser-local records do not automatically travel between devices, private windows or origins. Back up before clearing browser data or moving from local to hosted. Local file origin persistence is browser-dependent; use the local HTTP server or HTTPS hosting for stable behavior. Speech depends on installed platform voices; background audio can be interrupted by operating system policies. No third-party music assets are included.
