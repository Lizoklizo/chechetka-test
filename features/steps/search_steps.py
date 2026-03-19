import logging
from behave import when, then
from pages.search_results_page import SearchResultsPage

logger = logging.getLogger(__name__)


@when('user searches for "{query}"')
def step_search_for_product(context, query):
    context.search_query = query
    context.search_page = SearchResultsPage(context.page)
    context.search_page.search(query)

    logger.info("Search executed for query: %s", query)


@then("search results page should be loaded")
def step_check_search_results_loaded(context):
    assert context.search_page.is_loaded(), "Search results page did not load"

    heading = context.search_page.get_heading()
    items_text = context.search_page.get_items_count_text()

    logger.info("Search heading: %s", heading)
    logger.info("Search summary: %s", items_text)

    if heading:
        assert context.search_query.lower() in heading.lower() or "поиск" in heading.lower(), (
            f"Search heading does not look correct: '{heading}'"
        )


@then('first search result should contain "{expected_text}"')
def step_check_first_search_result(context, expected_text):
    first_name = context.search_page.get_first_product_name()

    logger.info("Result: %s", first_name)

    assert first_name is not None, "No products found in search results"
    assert expected_text.lower() in first_name.lower(), (
        f"First result '{first_name}' does not contain '{expected_text}'"
    )