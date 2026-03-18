from pages.base_page import BasePage


class CatalogPage(BasePage):

    URL = "https://mebelmart-saratov.ru/myagkaya_mebel_v_saratove/divanyi_v_saratove"

    # catalog
    PRODUCT_CARD = ".product-card"
    PRODUCT_NAME = ".product-card__name"
    PRODUCT_PRICE = ".product-card__now_price"
    BUY_BUTTON = ".product-card a.btn.btn-primary"
    FAVORITE_BUTTON = ".favorite-icon"

    # search
    SEARCH_INPUT = ".searchInput"
    SEARCH_BUTTON = "button.submit"

    # filters
    PRICE_FILTER_BLOCK = ".filter_values_range-slider"
    MIN_PRICE_SLIDER = ".min-slider-handle"
    MAX_PRICE_SLIDER = ".max-slider-handle"
    APPLY_FILTER_BUTTON = "#filterLinkContainer"

    # --------------------------------------

    def open_catalog(self):
        self.open(self.URL)

    def wait_for_catalog_loaded(self):
        self.page.locator(self.PRODUCT_CARD).first.wait_for()

    # --------------------------------------
    # products
    # --------------------------------------

    def get_product_cards(self):
        return self.page.locator(self.PRODUCT_CARD)

    def get_product_cards_count(self):
        return self.page.locator(self.PRODUCT_CARD).count()

    def get_first_product_name(self):
        return self.page.locator(self.PRODUCT_NAME).first.inner_text().strip()

    def get_first_product_price(self):
        return self.page.locator(self.PRODUCT_PRICE).first.inner_text().strip()

    def click_first_buy_button(self):
        self.page.locator(self.BUY_BUTTON).first.click()

    def click_first_favorite_button(self):
        self.page.locator(self.FAVORITE_BUTTON).first.click()

    # --------------------------------------
    # search
    # --------------------------------------

    def search_for_product(self, text):
        self.fill(self.SEARCH_INPUT, text)
        self.click(self.SEARCH_BUTTON)

    # --------------------------------------
    # filters
    # --------------------------------------

    def click_apply_filter(self):
        self.page.locator(self.APPLY_FILTER_BUTTON).click()