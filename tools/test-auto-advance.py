"""Run with python3 tools/test-auto-advance.py (pip install playwright; playwright install chromium)."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
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
    print(f'PASS {"mobile touch 390x844" if mobile else "desktop"}: visible completion panel, animation, auto/manual, typing/playback/cancel, last station, exam, self-review, reload, storage errors; no console errors')
    context.close()


try:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for mobile in (False, True):
            run(browser, mobile)
        browser.close()
finally:
    server.shutdown()
