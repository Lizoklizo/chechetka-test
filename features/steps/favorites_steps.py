from behave import when, then
from pages.favorites_page import FavoritesPage


@when("user adds the first sofa to favorites")
def step_add_first_sofa_to_favorites(context):
    context.selected_sofa_name = context.catalog_page.get_first_product_name()
    context.selected_sofa_link = context.catalog_page.get_first_product_link()
    context.selected_sofa_keyword = context.catalog_page.get_first_product_keyword()

    context.catalog_page.add_first_product_to_favorites()

    assert context.selected_sofa_name, "Не удалось получить название первого товара"
    assert context.selected_sofa_link, "Не удалось получить ссылку первого товара"


@when("user opens favorites page")
def step_open_favorites_page(context):
    context.favorites_page = FavoritesPage(context.page)
    context.favorites_page.open_favorites()
    context.favorites_page.wait_for_favorites_loaded()


@then("selected sofa should appear in favorites")
def step_check_selected_sofa_in_favorites(context):
    found_by_link = context.favorites_page.is_product_in_favorites_by_link(
        context.selected_sofa_link
    )

    found_by_keyword = context.favorites_page.is_product_in_favorites_by_keyword(
        context.selected_sofa_keyword
    )

    assert found_by_link or found_by_keyword, (
        f"Товар не найден в избранном. "
        f"Название в каталоге: '{context.selected_sofa_name}', "
        f"ссылка: '{context.selected_sofa_link}', "
        f"ключевое слово: '{context.selected_sofa_keyword}'"
    )