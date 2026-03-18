from behave import when, then
from pages.product_page import ProductPage


@when('user opens sofa card by name "{sofa_name}"')
def step_open_sofa_card(context, sofa_name):
    context.catalog_name = context.catalog_page.get_product_name_from_catalog(sofa_name)
    context.catalog_dimensions = context.catalog_page.get_catalog_card_dimensions(sofa_name)

    assert "Ширина" in context.catalog_dimensions, (
        f"Ширина не найдена в карточке каталога: {context.catalog_dimensions}"
    )
    assert "Глубина" in context.catalog_dimensions, (
        f"Глубина не найдена в карточке каталога: {context.catalog_dimensions}"
    )

    context.catalog_page.open_product_by_name(sofa_name)

    context.product_page = ProductPage(context.page)
    context.product_page.wait_for_product_loaded()


@then('opened product title should contain "{expected_name}"')
def step_check_product_title(context, expected_name):
    actual_title = context.product_page.get_product_title()

    assert expected_name.lower() in actual_title.lower(), (
        f"Ожидали, что заголовок товара будет содержать '{expected_name}', "
        f"но получили '{actual_title}'"
    )


@when('user opens the "Характеристики" tab')
def step_open_characteristics_tab(context):
    context.product_page.open_characteristics_tab()


@then("product width should be the same as in catalog")
def step_check_product_width(context):
    page_width = context.product_page.get_characteristic_value("Ширина")
    catalog_width = context.catalog_dimensions["Ширина"]

    assert page_width is not None, "Ширина не найдена во вкладке 'Характеристики'"

    assert catalog_width == page_width, (
        f"Ширина не совпадает: в каталоге {catalog_width} мм, "
        f"в карточке товара {page_width} мм"
    )


@then("product depth should be the same as in catalog")
def step_check_product_depth(context):
    page_depth = context.product_page.get_characteristic_value("Глубина")
    catalog_depth = context.catalog_dimensions["Глубина"]

    assert page_depth is not None, "Глубина не найдена во вкладке 'Характеристики'"

    assert catalog_depth == page_depth, (
        f"Глубина не совпадает: в каталоге {catalog_depth} мм, "
        f"в карточке товара {page_depth} мм"
    )