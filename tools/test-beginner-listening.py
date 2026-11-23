"""Run with Python Playwright and Chrome; optionally pass a screenshot directory."""
from pathlib import Path
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
        assert task["zh"].rstrip("。") in task["audioZh"] and letter in task["explain"]
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
            expect(sections.locator("h4")).to_have_text(["題目", "你的答案", "正確答案", "中文解釋"])
            expect(sections.nth(1).locator("strong")).to_have_text(f"{chr(65 + selected)}. {option}")
            expect(sections.nth(2).locator("strong")).to_have_text(f"{letter}. {answer}")
            expect(sections.nth(2).locator("p").nth(1)).to_have_text(translation)
            expect(sections.nth(0).locator("p").nth(1)).to_have_text(task["audio"])
            expect(sections.nth(0).locator("p").nth(2)).to_have_text(task["audioZh"])
            expect(sections.nth(3).locator("p")).to_have_text(task["explain"])

        options.nth(task["answer"]).click()
        expect(page.locator("#feedback")).to_contain_text("答對了")
        expect(sections.nth(1).locator("strong")).to_have_text(f"{letter}. {answer}")
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


def check_layout(browser, screenshot_dir):
    for width, height in ((320, 568), (375, 900), (390, 844), (1366, 900)):
        page = browser.new_page(viewport={"width": width, "height": height}, reduced_motion="reduce")
        tiles = open_bank(page, "single-file.html")
        tiles.nth(5).click()
        page.locator("#options button").nth(0).click()
        panel = page.locator("#reference")
        expect(panel.locator("strong").nth(1)).to_have_text("B. Ten dollars.")
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
                let bottom = 0;
                return left >= 0 && right <= innerWidth &&
                    dialog.scrollWidth <= dialog.clientWidth &&
                    [node, ...node.querySelectorAll('section, h4, p')].every(el => {
                        if (el.scrollWidth > el.clientWidth) return false;
                        if (el.tagName !== 'SECTION') return true;
                        const box = el.getBoundingClientRect();
                        const nonoverlapping = box.top >= bottom;
                        bottom = box.bottom;
                        return nonoverlapping;
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
        check_layout(browser, shots)
        browser.close()
