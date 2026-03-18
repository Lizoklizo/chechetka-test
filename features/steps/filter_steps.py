from behave import given, when, then
from pages.catalog_page import CatalogPage

PRICE_FROM = 10000
PRICE_TO = 15000
TARGET_SOFA = "Диван Кларити"


@given("open sofas catalog")
def step_open_catalog(context):
    print("\n[STEP] Opening sofas catalog")

    context.catalog = CatalogPage(context.page)
    context.catalog.open_catalog()
    context.catalog.wait_for_catalog_loaded()

    assert context.catalog.is_catalog_loaded(), "Sofas catalog page did not load"

    count = context.catalog.get_product_cards_count()
    print(f"[OK] Catalog loaded. Cards found: {count}")

    context.page.wait_for_timeout(2000)


@when("apply price filter")
def step_apply_filter(context):
    print(f"\n[STEP] Applying GET filter {PRICE_FROM}-{PRICE_TO}")

    context.catalog.open_catalog_with_price_filter(PRICE_FROM, PRICE_TO)
    context.catalog.wait_for_catalog_loaded()

    print("[INFO] First products after filter:")
    for i, (name, price) in enumerate(context.catalog.get_name_price_pairs(limit=15), start=1):
        print(f"  {i}. {name} — {price}")

    context.page.wait_for_timeout(2000)
    print("[OK] GET filter applied")


@then("sofa with name should appear in results")
def step_check_sofa(context):
    print(f"\n[STEP] Searching for sofa: {TARGET_SOFA}")

    all_matches = context.catalog.highlight_all_matching_products(TARGET_SOFA)
    print(f"[INFO] Total matches for '{TARGET_SOFA}': {len(all_matches)}")

    for idx, item in enumerate(all_matches, start=1):
        print(f"  {idx}. {item['name']} — {item['raw_price']} -> actual: {item['actual_price']}")

    product = context.catalog.find_product_by_name_in_price_range(
        TARGET_SOFA,
        PRICE_FROM,
        PRICE_TO
    )

    assert product is not None, (
        f"No '{TARGET_SOFA}' sofa was found with price in range {PRICE_FROM}-{PRICE_TO}"
    )

    context.catalog.highlight_product(product)

    print(f"[INFO] Found sofa: {product['name']}")
    print(f"[INFO] Actual price: {product['actual_price']}")

    assert PRICE_FROM <= product["actual_price"] <= PRICE_TO, (
        f"Price {product['actual_price']} is not in filter range {PRICE_FROM}-{PRICE_TO}"
    )

    print(f"[SUCCESS] {product['name']} found and price is within filter range")

    context.page.wait_for_timeout(3000)