"""Run with Python Playwright and Chrome; optionally pass a screenshot directory."""
from pathlib import Path
import re
import shutil
import sys

from playwright.sync_api import expect, sync_playwright


ROOT = Path(__file__).resolve().parent.parent
EXPECTED = [
    ("A person is giving someone water.", "有個人正在把水遞給另一個人。", "A", "water"),
    ("They are waiting for the bus.", "他們正在等公車。", "B", "bus"),
    ("At nine in the morning.", "早上九點。", "A", None),
    ("Yes, please.", "好，麻煩你了。", "B", None),
    ("Next to the bakery.", "在麵包店旁邊。", "A", None),
    ("Ten dollars.", "十美元。", "B", None),
    ("A bus stop", "公車站", "B", "bus"),
    ("A bottle of water", "一瓶水", "A", "bottle"),
]
CARD_LABELS = ["① 聽力原文與中文翻譯", "② 正確答案", "③ 重要單字與片語", "④ 答案解析"]
EXPECTED_LINE_COUNTS = [3, 3, 1, 1, 3, 4, 3, 3]
HAN = r"[\u3400-\u9fff]"
GLOSSED_ENGLISH = rf"[a-zA-Z]+(?:[ ’'\-]+[a-zA-Z]+)*\s*（[^）]*{HAN}[^）]*）"


def check_transcript_and_vocabulary(task, number):
    lines = task["transcript"]
    assert len(lines) == EXPECTED_LINE_COUNTS[number - 1]
    assert all(en.strip() and re.search(HAN, zh) for en, zh in lines)
    assert any(task["zh"].rstrip("。") in zh for _, zh in lines)
    for en, zh in lines:
        label = re.match(r"^([A-C])[:.]", en)
        if label:
            assert zh.startswith(label[1] + "："), task["id"]
        if en.startswith("Question:"):
            assert zh.startswith("問題："), task["id"]
    spoken_lines = [re.sub(r"^[A-C]: ", "", en) for en, _ in lines]
    assert " ".join(spoken_lines) == task["audio"]
    if number == 5:
        assert [zh for _, zh in lines] == ["A：圖書館在哪裡？", "B：它就在麵包店旁邊。", "問題：圖書館在哪裡？"]
    assert task["vocabulary"] and all(
        re.search(r"[A-Za-z]", en) and re.search(HAN, zh) for en, zh in task["vocabulary"]
    )
    assert not re.search(r"[A-Za-z]", re.sub(GLOSSED_ENGLISH, "", task["explain"])), task["id"]


def open_bank(page, source):
    page.goto((ROOT / source).as_uri())
    page.locator("#examNav").click()
    page.locator("#examSkill").select_option("listening")
    return page.locator("#examTasks [data-task-id]")


def check_grading(browser):
    page = browser.new_page(reduced_motion="reduce")
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    tiles = open_bank(page, "index.html")
    expect(tiles).to_have_count(len(EXPECTED))
    tasks = page.evaluate("EXAM_TASKS.filter(t => t.level === 'elementary' && t.skill === 'listening')")
    assert len(tasks) == len(EXPECTED)
    page.evaluate("""() => {
        window.spoken = null;
        speechSynthesis.speak = utterance => {
            window.spoken = utterance.text;
            utterance.onend();
        };
    }""")
    for number, (task, (answer, translation, letter, scene)) in enumerate(zip(tasks, EXPECTED), 1):
        task_id = f"gept-elementary-{number:03}"
        assert task["id"] == task_id and task["mode"] == "choice"
        assert type(task["answer"]) is int and 0 <= task["answer"] < len(task["options"])
        assert chr(65 + task["answer"]) == letter and task["options"][task["answer"]] == answer
        assert len(task["optionsZh"]) == len(task["options"]) and all(task["optionsZh"])
        assert task["optionsZh"][task["answer"]] == translation
        check_transcript_and_vocabulary(task, number)
        if task["type"] == "picture":
            assert task["audio"] == " ".join(f"{chr(65 + i)}. {option}" for i, option in enumerate(task["options"]))
            assert task["picture"] == scene and task["en"] == answer
        else:
            assert task["en"].rstrip(".") in task["audio"], task_id
        if task["type"] == "short-talk-picture":
            assert task["pictureOptions"] == ["bottle", "bus", "book"]
            assert task["pictureOptions"][task["answer"]] == scene

        page.locator(f'[data-task-id="{task_id}"]').click()
        page.locator("#listen").click()
        assert page.evaluate("spoken") == task["audio"], task_id
        panel = page.locator("#reference")
        expect(panel).to_be_hidden()
        options = page.locator("#options button")
        sections = panel.locator(".review-block")
        for selected, option in enumerate(task["options"]):
            if selected == task["answer"]:
                continue
            options.nth(selected).click()
            expect(page.locator("#feedback")).to_contain_text("再試一次")
            expect(page.locator("#nextTask")).to_be_hidden()
            assert not page.evaluate(
                """id => JSON.parse(localStorage.getItem('little-deer-progress-v1') || '{"records":[]}')
                           .records.some(record => record.id === id)""", task_id
            )
            expect(sections.locator("h4")).to_have_text(CARD_LABELS)
            answer_card = sections.nth(1)
            expect(answer_card.locator("strong")).to_have_text([f"{letter}. {answer}", f"{chr(65 + selected)}. {option}"])
            expect(answer_card.locator(".review-answer-label")).to_have_text("你的答案")
            expect(answer_card.locator("p[lang=en]")).to_have_count(2)
            expect(answer_card.locator(".review-row").first.locator("p").nth(1)).to_have_text(translation)
            expect(answer_card.locator(".review-row").last.locator("p").last).to_have_text(task["optionsZh"][selected])
            expect(sections.nth(0).locator(".review-row p")).to_have_text(
                [line for pair in task["transcript"] for line in pair]
            )
            expect(sections.nth(0).locator(".review-row p[lang=en]")).to_have_count(len(task["transcript"]))
            expect(sections.nth(2).locator("dt[lang=en]")).to_have_text([en for en, _ in task["vocabulary"]])
            expect(sections.nth(2).locator("dd")).to_have_text([zh for _, zh in task["vocabulary"]])
            expect(sections.nth(3).locator("p")).to_have_text(task["explain"])

        options.nth(task["answer"]).click()
        expect(page.locator("#feedback")).to_contain_text("答對了")
        expect(sections.nth(1).locator("strong")).to_have_text(f"{letter}. {answer}")
        expect(sections.nth(1).locator(".review-answer-label")).to_have_count(0)
        expect(page.locator("#nextTask")).to_be_visible()
        assert page.evaluate(
            """id => JSON.parse(localStorage.getItem('little-deer-progress-v1'))
                       .records.some(record => record.id === id && record.method === 'answer')""", task_id
        )
        page.locator("#retry").click()
        expect(panel).to_be_hidden()
        expect(page.locator("#backMap")).to_be_hidden()
        page.locator("#close").click()
        page.locator("#examNav").click()
    assert not errors, errors
    page.close()
    print("PASS: 8 elementary items, 8 correct and 16 incorrect attempts, TTS input and answer review.")
    print("PASS: 8 bilingual transcripts, vocabulary lists, explanations and four distinct review cards.")


def check_reference_keyboard(browser):
    page = browser.new_page(reduced_motion="reduce")
    open_bank(page, "index.html")
    page.locator("#examSkill").select_option("reading")
    page.locator('[data-task-id="gept-elementary-013"]').click()
    page.locator("#options button").first.click()
    button = page.locator("#showReference")
    button.focus()
    expect(button).to_be_focused()
    button.press("Enter")
    panel = page.get_by_role("region", name="作答解析")
    expect(panel).to_be_focused()
    expect(button).to_be_hidden()
    page.keyboard.press("Tab")
    expect(page.locator("#retry")).to_be_focused()

    def review_language(text):
        return panel.get_by_text(text, exact=True).evaluate("el => el.closest('[lang]').lang")

    assert review_language("What time does the shop close on Friday?") == "en"
    assert review_language("A. At five.") == "en"
    assert review_language("B. At six.") == "en"
    assert review_language("商店六點關門。") == "zh-Hant"
    page.locator("#close").click()
    page.evaluate("openLesson(known('water-002'))")
    page.locator("#options button").nth(1).click()
    assert review_language("這句話是在做什麼？") == "zh-Hant"
    assert panel.get_by_text("B. 主動提供水", exact=True).evaluate_all(
        "nodes => nodes.map(node => node.closest('[lang]').lang)"
    ) == ["zh-Hant", "zh-Hant"]
    page.close()
    print("PASS: keyboard focus moves from Show Reference to the answer review, then to Try Again.")
    print("PASS: English review questions and answers identify as English; Chinese text retains zh-Hant.")


def check_spoken_review(browser):
    page = browser.new_page(reduced_motion="reduce")
    page.add_init_script("""window.SpeechRecognition = class {
        start() {
            this.emit('I visit friends', false);
        }
        stop() {
            this.emit(window.shortFinal ? 'visit family' : 'I visit my family', true);
            this.onend();
        }
        emit(transcript, isFinal) {
            const result = [{transcript}];
            result.isFinal = isFinal;
            this.onresult({results: [result]});
        }
        abort() {}
    };""")
    open_bank(page, "index.html")
    page.locator("#examSkill").select_option("speaking")
    page.locator('[data-task-id="gept-elementary-027"]').click()
    expect(page.locator("#checkReading")).to_be_visible()
    page.clock.install()
    page.evaluate("window.shortFinal = true")
    page.locator("#checkReading").click()
    page.clock.fast_forward(21_000)
    expect(page.locator("#stopRecognition")).to_be_visible()
    page.clock.fast_forward(99_000)
    expect(page.locator("#stopRecognition")).to_be_hidden()
    page.locator("#reviewSpeaking").click()
    expect(page.locator("#selfReview")).to_be_hidden()
    page.evaluate("window.shortFinal = false")
    page.locator("#checkReading").click()
    page.locator("#stopRecognition").click()
    page.locator("#reviewSpeaking").click()
    answer = page.locator("#reference .review-block").filter(
        has=page.get_by_role("heading", name="你的答案", exact=True)
    ).locator("strong")
    expect(answer).to_have_text("I visit my family")
    assert answer.evaluate("el => el.closest('[lang]').lang") == "en"
    page.locator("#spokenNotes").fill("I go to the park")
    page.locator("#reviewSpeaking").click()
    expect(answer).to_have_text("I go to the park")
    assert answer.evaluate("el => el.closest('[lang]').lang") == "zh-Hant"
    page.locator("#spokenNotes").fill("")
    page.locator("#retry").click()
    page.evaluate("recorded = true")
    page.locator("#reviewSpeaking").click()
    expect(answer).to_have_text("請回放你的錄音。")
    page.locator("#checkReading").click()
    page.locator("#stopRecognition").click()
    page.locator("#reviewSpeaking").click()
    expect(answer).to_have_text("I visit my family")
    page.locator("#close").click()
    expect(page.locator("#reference")).to_be_empty()
    page.close()
    print("PASS: open-answer recognition runs past 20 seconds, and a short final transcript cannot unlock self-review.")
    print("PASS: speaking review shows notes, latest recognition transcript, or recording fallback in that order.")
    print("PASS: closing the speaking lesson clears the rendered answer review.")


def check_layout(browser, screenshot_dir):
    for width, height in ((320, 568), (375, 900), (390, 844), (1366, 900)):
        page = browser.new_page(viewport={"width": width, "height": height}, reduced_motion="reduce")
        tiles = open_bank(page, "single-file.html")
        tiles.nth(5).click()
        page.locator("#options button").nth(0).click()
        panel = page.locator("#reference")
        expect(panel.locator("strong").first).to_have_text("B. Ten dollars.")
        panel.evaluate("node => node.scrollIntoView({block: 'start'})")
        if screenshot_dir and width in (375, 1366):
            page.screenshot(path=screenshot_dir / f"beginner-listening-{width}.png")
        for text in (None, "這是用來確認多行說明可捲動的長文字。" * 30 + "X" * 200):
            if text:
                panel.locator(".review-block").last.locator("p").evaluate(
                    "(node, text) => node.textContent = text", text
                )
            assert panel.evaluate("""node => {
                const dialog = node.closest('dialog');
                const {left, right} = dialog.getBoundingClientRect();
                const zh = node.querySelector('.review-row p:not([lang])');
                const type = getComputedStyle(zh);
                let bottom = -Infinity;
                return left >= 0 && right <= innerWidth &&
                    dialog.scrollWidth <= dialog.clientWidth &&
                    parseFloat(type.fontSize) >= 17 && parseFloat(type.lineHeight) >= 1.8 * 17 &&
                    [node, ...node.querySelectorAll('section, h4, p, dt, dd')].every(el => {
                        if (el.scrollWidth > el.clientWidth) return false;
                        if (el.tagName !== 'SECTION') return true;
                        const box = el.getBoundingClientRect();
                        const style = getComputedStyle(el);
                        const separated = box.top - bottom >= 16 && parseFloat(style.borderTopWidth) > 0 &&
                            style.backgroundColor !== getComputedStyle(node).backgroundColor;
                        bottom = box.bottom;
                        return separated;
                    });
            }"""), (width, "long text" if text else "actual review")
        page.locator("#feedback").scroll_into_view_if_needed()
        expect(page.locator("#feedback")).to_be_in_viewport()
        page.close()
        print(f"PASS: standalone review fits, wraps and scrolls at {width}px in Chrome.")


if __name__ == "__main__":
    shots = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=shutil.which("google-chrome"))
        check_grading(browser)
        check_reference_keyboard(browser)
        check_spoken_review(browser)
        check_layout(browser, shots)
        browser.close()
