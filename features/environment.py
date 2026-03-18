from playwright.sync_api import sync_playwright
import os
import sys
import logging


def before_all(context):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )

    context.logger = logging.getLogger("behave")
    context.logger.info("Starting Playwright")

    context.playwright = sync_playwright().start()


def before_scenario(context, scenario):
    context.scenario = scenario
    context.logger = logging.getLogger(f"behave.{scenario.name}")

    headless_value = context.config.userdata.get("headless", "").lower()

    if headless_value in ("true", "1", "yes"):
        is_headless = True
    elif headless_value in ("false", "0", "no"):
        is_headless = False
    else:
        is_ci = os.getenv("CI", "").lower() == "true"
        is_headless = is_ci

    context.logger.info("Starting scenario: %s", scenario.name)
    context.logger.info("Headless mode: %s", is_headless)

    context.browser = context.playwright.chromium.launch(
        headless=is_headless,
        slow_mo=0 if is_headless else 800
    )
    context.page = context.browser.new_page()

    context.logger.info("Browser launched")


def after_step(context, step):
    if step.status == "failed":
        os.makedirs("screenshots", exist_ok=True)
        os.makedirs("page_source", exist_ok=True)

        scenario_name = context.scenario.name.replace(" ", "_")
        step_name = step.name.replace(" ", "_")
        filename = f"{scenario_name}__{step_name}"

        error_text = str(step.exception) if step.exception else "Step failed"

        context.logger.error("Step failed: %s", step.name)
        context.logger.error("Error: %s", error_text)

        try:
            context.page.evaluate(
                """
                (errorText) => {
                    const div = document.createElement("div");
                    div.style.position = "fixed";
                    div.style.top = "10px";
                    div.style.left = "10px";
                    div.style.background = "red";
                    div.style.color = "white";
                    div.style.padding = "15px";
                    div.style.zIndex = "9999";
                    div.style.fontSize = "20px";
                    div.style.fontFamily = "Arial";
                    div.style.maxWidth = "700px";
                    div.style.borderRadius = "5px";
                    div.innerHTML = "TEST FAILED<br>" + errorText;
                    document.body.appendChild(div);
                }
                """,
                error_text
            )
        except Exception as e:
            context.logger.warning("Could not draw error overlay: %s", e)

        try:
            context.page.locator(".product-card").first.evaluate(
                "el => el.style.border='5px solid red'"
            )
        except Exception as e:
            context.logger.warning("Could not highlight first product card: %s", e)

        try:
            screenshot_path = f"screenshots/{filename}.png"
            context.page.screenshot(
                path=screenshot_path,
                full_page=True
            )
            context.logger.info("Screenshot saved: %s", screenshot_path)
        except Exception as e:
            context.logger.warning("Could not save screenshot: %s", e)

        try:
            html_path = f"page_source/{filename}.html"
            html = context.page.content()
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html)
            context.logger.info("Page source saved: %s", html_path)
        except Exception as e:
            context.logger.warning("Could not save page source: %s", e)


def after_scenario(context, scenario):
    if scenario.status == "failed":
        context.logger.error("Scenario failed: %s", scenario.name)
        print("Test failed — browser left open for debugging")
    else:
        context.logger.info("Scenario passed: %s", scenario.name)
        if hasattr(context, "browser") and context.browser:
            context.browser.close()
            context.logger.info("Browser closed")


def after_all(context):
    if hasattr(context, "playwright") and context.playwright:
        context.playwright.stop()
        logging.getLogger("behave").info("Playwright stopped")