from playwright.sync_api import sync_playwright
import os


def before_all(context):
    context.playwright = sync_playwright().start()


def before_scenario(context, scenario):
    context.scenario = scenario

    is_ci = os.getenv("CI", "").lower() == "true"

    context.browser = context.playwright.chromium.launch(
        headless=is_ci,
        slow_mo=0 if is_ci else 800
    )
    context.page = context.browser.new_page()


def after_step(context, step):
    if step.status == "failed":
        os.makedirs("screenshots", exist_ok=True)
        os.makedirs("page_source", exist_ok=True)

        scenario_name = context.scenario.name.replace(" ", "_")
        step_name = step.name.replace(" ", "_")
        filename = f"{scenario_name}__{step_name}"

        error_text = str(step.exception) if step.exception else "Step failed"

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
        except Exception:
            pass

        try:
            context.page.locator(".product-card").first.evaluate(
                "el => el.style.border='5px solid red'"
            )
        except Exception:
            pass

        try:
            context.page.screenshot(
                path=f"screenshots/{filename}.png",
                full_page=True
            )
        except Exception:
            pass

        try:
            html = context.page.content()
            with open(f"page_source/{filename}.html", "w", encoding="utf-8") as f:
                f.write(html)
        except Exception:
            pass


def after_scenario(context, scenario):
    if scenario.status == "failed":
        print("Test failed — browser left open for debugging")
    else:
        if hasattr(context, "browser") and context.browser:
            context.browser.close()


def after_all(context):
    if hasattr(context, "playwright") and context.playwright:
        context.playwright.stop()