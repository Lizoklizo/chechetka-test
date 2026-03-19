from behave import when, then
from pages.catalog_page import CatalogPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


@when("user adds first product to cart and dismisses dialog")
def step_add_first_product_to_cart(context):
    context.catalog_page = CatalogPage(context.page)
    context.product_page = ProductPage(context.page)

    context.expected_product_name = context.catalog_page.get_first_product_name()
    context.expected_product_keyword = context.catalog_page.get_first_product_keyword()

    raw_price = (
        context.catalog_page.get_first_product_card()
        .locator(context.catalog_page.PRODUCT_PRICE)
        .inner_text()
        .strip()
    )
    context.expected_product_price = context.catalog_page._extract_actual_price(raw_price)

    context.catalog_page.open_product_by_index(0)
    assert context.product_page.is_product_page(), "Страница товара не открылась"

    context.product_page.click_add_to_cart_and_dismiss_dialog()


@when("user opens cart from header")
def step_open_cart(context):
    context.catalog_page = CatalogPage(context.page)
    context.catalog_page.open_cart()
    context.cart_page = CartPage(context.page)


@then("added product should be displayed in cart")
def step_check_product_in_cart(context):
    cart_names = context.cart_page.get_item_names()

    assert cart_names, "Корзина пуста"

    expected_keyword = context.expected_product_keyword.lower()

    found = any(expected_keyword in name.lower() for name in cart_names)

    assert found, (
        f"Товар с ключевым словом '{expected_keyword}' не найден в корзине. "
        f"Ожидалось имя из каталога: '{context.expected_product_name}'. "
        f"Найдены: {cart_names}"
    )


@then("cart price should match catalog price")
def step_check_cart_price(context):
    actual_total = context.cart_page.get_total_price()

    assert context.expected_product_price is not None, "Не удалось получить цену товара из каталога"
    assert actual_total is not None, "Не удалось получить цену в корзине"
    assert actual_total == context.expected_product_price, (
        f"Цена в корзине {actual_total}, а в каталоге {context.expected_product_price}"
    )