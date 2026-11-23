"""Run with python3 tools/test-auto-advance.py (pip install playwright; playwright install chromium)."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright, expect


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


root = Path(__file__).resolve().parents[1]
server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(root)))
Thread(target=server.serve_forever, daemon=True).start()
url = f'http://127.0.0.1:{server.server_port}'


def run_cross_tab(browser):
    context = browser.new_context()
    editor = context.new_page()
    errors = []

    def watch(page):
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
        page.route('**/favicon.ico', lambda route: route.fulfill(status=204))

    watch(editor)
    editor.goto(url)
    task = editor.evaluate('lessons.find(l=>l.mode==="open")')
    editor.evaluate('(id)=>openLesson(known(id))', task['id'])
    editor.locator('#response').fill('My initial draft.')
    replay = context.new_page()
    watch(replay)
    replay.goto(url)
    editor.locator('#response').fill('My newer draft must survive replay in another tab.')
    replay.evaluate('openLesson(lessons[0])')
    replay.locator('#options button').nth(0).click()
    actual = replay.evaluate('(id)=>JSON.parse(localStorage.getItem(DRAFT_KEY))[id]', task['id'])
    assert actual == 'My newer draft must survive replay in another tab.', f'Cross-tab replay lost newer draft: {actual!r}'
    replay.locator('#close').click()
    replay.evaluate('(id)=>openLesson(known(id))', task['id'])
    expect(replay.locator('#response')).to_have_value(actual)
    editor.locator('#response').fill('')
    replay.locator('#close').click()
    replay.evaluate('openLesson(lessons[0])')
    replay.locator('#options button').nth(0).click()
    assert replay.evaluate('(id)=>JSON.parse(localStorage.getItem(DRAFT_KEY))[id]', task['id']) == ''
    editor.reload()
    editor.evaluate('(id)=>openLesson(known(id))', task['id'])
    expect(editor.locator('#response')).to_have_value('')
    other = replay.evaluate('lessons.filter(l=>l.mode==="open")[1]')
    replay.locator('#close').click()
    replay.evaluate('(id)=>openLesson(known(id))', other['id'])
    replay.locator('#response').fill('An independent draft in the other tab.')
    editor.locator('#response').fill('Updated first draft.')
    assert editor.evaluate('(id)=>JSON.parse(localStorage.getItem(DRAFT_KEY))[id]', other['id']) == 'An independent draft in the other tab.'
    editor.evaluate('''()=>{
        window.realDraftSet=Storage.prototype.setItem;
        Storage.prototype.setItem=function(key,value){
            if(key===DRAFT_KEY)throw Error('blocked draft write');
            return window.realDraftSet.call(this,key,value);
        };
    }''')
    editor.locator('#response').fill('Pending draft survives a failed write.')
    expect(editor.locator('#storageNotice')).to_contain_text('匯出 JSON 備份')
    assert editor.evaluate('(id)=>JSON.parse(localStorage.getItem(DRAFT_KEY))[id]', task['id']) == 'Updated first draft.'
    editor.evaluate('()=>{Storage.prototype.setItem=window.realDraftSet}')
    assert editor.evaluate('save()')
    assert editor.evaluate('(id)=>JSON.parse(localStorage.getItem(DRAFT_KEY))[id]', task['id']) == 'Pending draft survives a failed write.'
    # Saving must also read latest progress when storage events have not arrived.
    stale = context.new_page()
    watch(stale)
    stale.add_init_script("window.addEventListener('storage',e=>e.stopImmediatePropagation())")
    stale.goto(url)
    editor.locator('#close').click()
    editor.evaluate('openLesson(lessons[1])')
    editor.locator('#options button').nth(1).click()
    assert not stale.evaluate('!!records[lessons[1].id]')
    assert stale.evaluate('save()')
    assert stale.evaluate('JSON.parse(localStorage.getItem(KEY)).records.some(r=>r.id===lessons[1].id)')
    imported = replay.evaluate('lessons.filter(l=>l.mode==="open")[2].id')
    replay.locator('#import').set_input_files({
        'name': 'backup.json', 'mimeType': 'application/json',
        'buffer': json.dumps({'version': 1, 'records': [], 'drafts': {
            task['id']: 'Do not replace the latest stored draft.', imported: 'Imported backup draft.'
        }}).encode(),
    })
    replay.wait_for_function('(id)=>JSON.parse(localStorage.getItem(DRAFT_KEY))[id]==="Imported backup draft."', arg=imported)
    assert replay.evaluate('(id)=>JSON.parse(localStorage.getItem(DRAFT_KEY))[id]', task['id']) == 'Pending draft survives a failed write.'
    assert not errors, errors
    print('PASS cross-tab: newer/empty/independent drafts survive replay and reload; stale saves preserve latest progress; no console errors')
    context.close()


def run_storage_recovery(browser):
    context = browser.new_context()
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
    page.route('**/favicon.ico', lambda route: route.fulfill(status=204))
    for key in ('little-deer-progress-v1', 'little-deer-drafts-v1'):
        for failure in ('malformed', 'unreadable'):
            page.goto(url)
            page.evaluate('localStorage.clear()')
            page.reload()
            task = page.evaluate('lessons.find(l=>l.mode==="open")')
            page.evaluate('(id)=>openLesson(known(id))', task['id'])
            page.locator('#response').fill('Keep this existing draft in memory.')
            page.locator('#close').click()
            page.evaluate('openLesson(lessons[0])')

            def break_reads():
                if failure == 'malformed':
                    page.evaluate('(key)=>localStorage.setItem(key,"{broken")', key)
                else:
                    page.evaluate('''key=>{
                        window.realGet=Storage.prototype.getItem;
                        Storage.prototype.getItem=function(k){
                            if(k===key)throw Error('blocked read');
                            return window.realGet.call(this,k);
                        };
                    }''', key)

            def restore_reads():
                if failure == 'unreadable':
                    page.evaluate('()=>{Storage.prototype.getItem=window.realGet}')

            break_reads()
            page.locator('#options button').nth(0).click()
            restore_reads()
            assert page.evaluate('JSON.parse(localStorage.getItem(KEY)).records.some(r=>r.id===lessons[0].id)')
            assert page.evaluate('(id)=>JSON.parse(localStorage.getItem(DRAFT_KEY))[id]', task['id']) == 'Keep this existing draft in memory.'
            page.locator('#close').click()
            page.evaluate('(id)=>openLesson(known(id))', task['id'])
            break_reads()
            page.locator('#response').fill('New draft saved despite bad storage reads.')
            restore_reads()
            page.reload()
            assert page.evaluate('!!records[lessons[0].id]')
            page.evaluate('(id)=>openLesson(known(id))', task['id'])
            expect(page.locator('#response')).to_have_value('New draft saved despite bad storage reads.')
    assert not errors, errors
    print('PASS storage recovery: malformed/unreadable progress and drafts do not block completion or draft writes; data survives reload; no console errors')
    context.close()


def run_import_recovery(browser):
    context = browser.new_context()
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
    page.route('**/favicon.ico', lambda route: route.fulfill(status=204))
    for failure in ('malformed progress', 'malformed drafts', 'blocked reads', 'blocked reads and writes'):
        page.goto(url)
        page.evaluate('localStorage.clear()')
        page.reload()
        task = page.evaluate('lessons.find(l=>l.mode==="open")')
        record = page.evaluate('({id:lessons[0].id,completedAt:new Date().toISOString(),method:"answer"})')
        if failure.startswith('malformed'):
            key = 'little-deer-progress-v1' if failure.endswith('progress') else 'little-deer-drafts-v1'
            page.evaluate('(key)=>localStorage.setItem(key,"{broken")', key)
        else:
            page.evaluate('''blockWrites=>{
                window.importGet=Storage.prototype.getItem;
                window.importSet=Storage.prototype.setItem;
                Storage.prototype.getItem=function(key){
                    if(key===KEY||key===DRAFT_KEY)throw Error('blocked read');
                    return window.importGet.call(this,key);
                };
                if(blockWrites)Storage.prototype.setItem=function(){throw Error('blocked write')};
            }''', failure == 'blocked reads and writes')
        page.locator('#import').set_input_files({
            'name': 'backup.json', 'mimeType': 'application/json',
            'buffer': json.dumps({'version': 1, 'records': [record], 'drafts': {
                task['id']: 'Valid backup draft survives blocked storage.'
            }}).encode(),
        })
        page.wait_for_function('(id)=>drafts[id]==="Valid backup draft survives blocked storage."', arg=task['id'])
        assert page.evaluate('(id)=>!!records[id]', record['id'])
        if failure == 'blocked reads and writes':
            expect(page.locator('#storageNotice')).to_contain_text('瀏覽器無法保存進度，請匯出 JSON 備份。')
        else:
            expect(page.locator('#storageNotice')).to_contain_text('已合併')
        page.evaluate('(id)=>openLesson(known(id))', task['id'])
        expect(page.locator('#response')).to_have_value('Valid backup draft survives blocked storage.')
        if failure.startswith('blocked'):
            page.evaluate('()=>{Storage.prototype.getItem=window.importGet;Storage.prototype.setItem=window.importSet}')
            assert page.evaluate('save()')
        page.reload()
        assert page.evaluate('(id)=>!!records[id]', record['id'])
        page.evaluate('(id)=>openLesson(known(id))', task['id'])
        expect(page.locator('#response')).to_have_value('Valid backup draft survives blocked storage.')
    assert not errors, errors
    print('PASS import recovery: malformed JSON is repaired; blocked reads/writes retain imported records and visible drafts, preserve failure notice, and recover after reload; no console errors')
    context.close()


def run(browser, mobile):
    context = browser.new_context(viewport={'width': 390, 'height': 844} if mobile else {'width': 1280, 'height': 900}, has_touch=mobile)
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
    page.route('**/favicon.ico', lambda route: route.fulfill(status=204))

    def press(selector):
        target = page.locator(selector)
        target.tap() if mobile else target.click()

    def arrive(index):
        if page.locator('#lesson').evaluate('(el)=>el.open'):
            press('#close')
        press(f'#stations .station:nth-child({index + 1}) > button:first-child')
        expect(page.locator('#lesson')).to_be_visible()
        page.wait_for_function('(i)=>position===i&&!moving', arg=index)

    def correct():
        answer = page.evaluate('current.answer')
        press(f'#options button:nth-child({answer + 1})')
        expect(page.locator('#clearCelebration')).to_be_visible()
        expect(page.locator('#advancePanel')).to_be_in_viewport(ratio=0.99)
        expect(page.locator('#nextTask')).to_be_hidden()
        expect(page.locator('#advanceActions')).to_be_visible(timeout=3000)
        expect(page.locator('#advancePanel')).to_be_in_viewport(ratio=0.99)
        expect(page.locator('#advanceNow')).to_be_in_viewport(ratio=1)

    def stayed(index):
        page.wait_for_timeout(3300)
        assert page.evaluate('position') == index
        expect(page.locator('#advanceNow')).to_have_text('前往下一關 →')

    page.goto(url)
    press('#start')
    arrive(0)
    correct()
    expect(page.locator('#advanceMessage')).to_contain_text('小鹿將前往下一關')
    expect(page.locator('#advanceCancel')).to_be_in_viewport(ratio=1)
    page.screenshot(path=f'/tmp/fix-{"mobile" if mobile else "desktop"}.png')
    page.wait_for_function('position===1 && current.id===mapLessons()[1].id && document.querySelector("#lesson").open', timeout=7000)
    press('#close')
    press('#autoAdvance')
    arrive(0)
    correct()
    stayed(0)
    press('#advanceNow')
    page.wait_for_function('position===1 && current.id===mapLessons()[1].id')
    press('#close')
    press('#autoAdvance')
    for action in ('cancel', 'typing', 'playback'):
        arrive(0)
        correct()
        if action == 'cancel':
            press('#advanceCancel')
        elif action == 'typing':
            page.evaluate("document.querySelector('#writtenResponse').hidden=false")
            page.locator('#response').fill('I want to stay here.')
        else:
            page.evaluate("Object.defineProperty(document.querySelector('#recording'),'paused',{configurable:true,get:()=>false});document.querySelector('#recording').dispatchEvent(new Event('play'))")
        stayed(0)
        if action == 'playback':
            page.evaluate("delete document.querySelector('#recording').paused")
    page.evaluate('''()=>{
        window.originalSpeechSpeak=speechSynthesis.speak;
        speechSynthesis.speak=utterance=>{window.mockPrompt=utterance};
    }''')
    for timing in ('before completion', 'before travel'):
        arrive(0)
        if timing == 'before completion':
            press('#listen')
        correct()
        if timing == 'before travel':
            page.wait_for_timeout(2700)
            page.evaluate('speak(current.en)')
        assert page.evaluate('speaking && !!window.mockPrompt')
        stayed(0)
        expect(page.locator('#lesson')).to_be_visible()
        assert page.evaluate('speaking'), 'Travel must not interrupt the spoken prompt'
    page.keyboard.press('Escape')
    expect(page.locator('#lesson')).to_be_hidden()
    assert not page.evaluate('speaking'), 'Escape must still stop spoken prompts'
    page.evaluate('()=>{speechSynthesis.speak=window.originalSpeechSpeak}')
    arrive(0)
    correct()
    page.evaluate('recognitionActive=true')
    stayed(0)
    press('#advanceNow')
    assert page.evaluate('position === 0 && recognitionActive'), 'Next must not interrupt speech recognition'
    press('#close')
    arrive(7)
    answer = page.evaluate('current.answer')
    press(f'#options button:nth-child({answer + 1})')
    expect(page.locator('#advanceMessage')).to_contain_text('本路線已全部走完', timeout=3000)
    expect(page.locator('#advanceActions')).to_be_hidden()
    arrive(0)
    page.evaluate('recordingActive=true')
    correct()
    stayed(0)
    page.evaluate('recordingActive=false')
    press('#close')
    # A library lesson that is not the current station must not move the deer.
    page.evaluate('openLesson(mapLessons()[2])')
    answer = page.evaluate('current.answer')
    press(f'#options button:nth-child({answer + 1})')
    expect(page.locator('#advanceMessage')).to_contain_text('回到目前站點', timeout=3000)
    expect(page.locator('#advanceActions')).to_be_hidden()
    press('#close')
    press('#examNav')
    press('#examTasks article:first-child button')
    page.wait_for_function('page==="mapPage" && !moving && document.querySelector("#lesson").open')
    assert page.evaluate('current.level') == 'elementary'
    press('#close')
    press('#autoAdvance')
    page.reload()
    press('#start')
    assert page.locator('#mapLevel').input_value() == 'elementary'
    assert page.evaluate('position') == 0
    expect(page.locator('#autoAdvance')).to_have_attribute('aria-pressed', 'false')
    # Self-review remains learner-controlled; no automatic scoring.
    task = page.evaluate('lessons.find(l=>l.mode==="open")')
    page.evaluate('(id)=>startExamTask(id)', task['id'])
    expect(page.locator('#lesson')).to_be_visible()
    page.locator('#response').fill(' '.join(['practice'] * max(task.get('minWords', 10), 10)))
    press('#submitResponse')
    for box in page.locator('#reviewChecks input').all():
        box.check()
    press('#completeReview')
    expect(page.locator('#clearCelebration')).to_be_visible()
    assert task['level'] != 'foundation'
    expect(page.locator('#nextTask')).to_be_visible()
    assert page.evaluate('(id)=>!!JSON.parse(localStorage.getItem(KEY)).records.find(r=>r.id===id&&r.method==="self-review")', task['id'])
    press('#close')
    press('#mapNav')
    page.locator('#mapLevel').select_option('foundation')
    arrive(3)
    press('#close')
    page.reload()
    press('#start')
    assert page.evaluate('position') == 3
    assert page.locator('#deer').evaluate('(el)=>el.style.top') == '825px'
    press('#autoAdvance')
    arrive(0)
    correct()
    press('#close')
    page.wait_for_timeout(3300)
    assert page.evaluate('position') == 0
    arrive(0)
    page.emulate_media(reduced_motion='reduce')
    answer = page.evaluate('current.answer')
    press(f'#options button:nth-child({answer + 1})')
    expect(page.locator('#clearCelebration')).to_be_visible()
    assert page.locator('.clear-deer').evaluate('(el)=>getComputedStyle(el).animationName') == 'none'
    press('#close')
    # Invalid station IDs fall back to the beginning of the valid route.
    page.evaluate("localStorage.setItem(POSITION_KEY,JSON.stringify({level:'elementary',id:'invalid'}))")
    page.reload()
    press('#start')
    assert page.evaluate('position') == 0
    assert page.locator('#mapLevel').input_value() == 'elementary'
    page.locator('#mapLevel').select_option('foundation')
    # Storage failures and silently dropped writes must never advance.
    for failure in ('throw', 'drop'):
        arrive(0)
        page.evaluate("localStorage.removeItem(KEY)")
        page.evaluate("(mode)=>{window.realSet=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k===KEY){if(mode==='throw')throw Error('blocked');return}return window.realSet.call(this,k,v)}}", failure)
        press('#options button:first-child')
        expect(page.locator('#advanceMessage')).to_contain_text('匯出 JSON 備份')
        expect(page.locator('#advanceActions')).to_be_hidden()
        page.evaluate('()=>{Storage.prototype.setItem=window.realSet}')
    assert not errors, errors
    print(f'PASS {"mobile touch 390x844" if mobile else "desktop"}: visible completion panel, animation, auto/manual, typing/playback/cancel, spoken prompt blocks countdown/travel, last station, exam, self-review, reload, storage errors; no console errors')
    context.close()


try:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        run_cross_tab(browser)
        run_storage_recovery(browser)
        run_import_recovery(browser)
        for mobile in (False, True):
            run(browser, mobile)
        browser.close()
finally:
    server.shutdown()
