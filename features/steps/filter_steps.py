import logging
from behave import given, when, then
from pages.catalog_page import CatalogPage

logger = logging.getLogger(__name__)

PRICE_FROM = 10000
PRICE_TO = 15000
TARGET_SOFA = "Диван Кларити"


@given("open sofas catalog")
def step_open_sofas_catalog(context):
    logger.info("Opening sofas catalog")
    context.catalog_page = CatalogPage(context.page)
    context.catalog_page.open_catalog()
    context.catalog_page.wait_for_catalog_loaded()

    assert context.catalog_page.is_catalog_loaded(), "Sofas catalog page did not load"

    count = context.catalog_page.get_product_cards_count()
    logger.info("Catalog loaded. Cards found: %s", count)

    context.page.wait_for_timeout(2000)


@when("apply price filter")
def step_apply_filter(context):
    logger.info("Applying GET filter %s-%s", PRICE_FROM, PRICE_TO)

    context.catalog_page.open_catalog_with_price_filter(PRICE_FROM, PRICE_TO)
    context.catalog_page.wait_for_catalog_loaded()

    logger.info("First products after filter:")
    for i, (name, price) in enumerate(context.catalog_page.get_name_price_pairs(limit=15), start=1):
        logger.info("%s. %s — %s", i, name, price)

    context.page.wait_for_timeout(2000)
    logger.info("GET filter applied")


@then("sofa with name should appear in results")
def step_check_sofa(context):
    logger.info("Searching for sofa: %s", TARGET_SOFA)

    all_matches = context.catalog_page.highlight_all_matching_products(TARGET_SOFA)
    logger.info("Total matches for '%s': %s", TARGET_SOFA, len(all_matches))

    for idx, item in enumerate(all_matches, start=1):
        logger.info(
            "%s. %s — %s -> actual: %s",
            idx,
            item["name"],
            item["raw_price"],
            item["actual_price"],
        )

    product = context.catalog_page.find_product_by_name_in_price_range(
        TARGET_SOFA,
        PRICE_FROM,
        PRICE_TO
    )

    assert product is not None, (
        f"No '{TARGET_SOFA}' sofa was found with price in range {PRICE_FROM}-{PRICE_TO}"
    )

    context.catalog_page.highlight_product(product)

    logger.info("Found sofa: %s", product["name"])
    logger.info("Actual price: %s", product["actual_price"])

    assert PRICE_FROM <= product["actual_price"] <= PRICE_TO, (
        f"Price {product['actual_price']} is not in filter range {PRICE_FROM}-{PRICE_TO}"
    )

    logger.info("Success: %s found and price is within filter range", product["name"])

    context.page.wait_for_timeout(3000)