from behave import given, when, then
from pages.catalog_page import CatalogPage
import re
import allure
from behave import given, when, then


TARGET_SOFA = "Диван Шенилл"


@given("open sofas catalog")
def step_open_catalog(context):

    print("\n[STEP] Opening sofas catalog")

    context.catalog = CatalogPage(context.page)

    context.catalog.open_catalog()
    context.catalog.wait_for_catalog_loaded()

    print("[OK] Catalog loaded")


@when("apply price filter")
def step_apply_filter(context):

    print("\n[STEP] Applying price filter 10000-15000")

    context.catalog.click_apply_filter()

    context.page.wait_for_timeout(2000)

    print("[OK] Filter applied")


@then("sofa with name should appear in results")
def step_check_sofa(context):

    print(f"\n[STEP] Searching for sofa: {TARGET_SOFA}")

    cards = context.page.locator(".product-card")

    found = False

    for i in range(cards.count()):

        card = cards.nth(i)

        name = card.locator(".product-card__name").inner_text().strip()

        if TARGET_SOFA in name:

            price_text = card.locator(".product-card__now_price").inner_text()

            numbers = re.findall(r"\d+", price_text)

            if len(numbers) >= 2:
                price = int(numbers[-2] + numbers[-1])
            else:
                price = int(numbers[0])

            print(f"Found sofa: {name}")
            print(f"Price: {price}")

            assert 10000 <= price <= 15000, f"Price {price} not in filter range"

            found = True
            break

    assert found, f"{TARGET_SOFA} not found in filtered results"

    print(f"[SUCCESS] {TARGET_SOFA} found and price is within filter range")