from pages.base_page import BasePage


class ProductPage(BasePage):
    ADD_TO_CART_BUTTON = ".btnToCart:visible"
    PRODUCT_TITLE = "h1"

    def is_product_page(self):
        return self.page.locator(self.PRODUCT_TITLE).count() > 0

    def get_product_title(self):
        return self.page.locator(self.PRODUCT_TITLE).first.inner_text().strip()

    def click_add_to_cart_and_dismiss_dialog(self):
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(1500)

        self.page.once("dialog", lambda dialog: dialog.dismiss())

        button = self.page.locator(self.ADD_TO_CART_BUTTON).first
        button.wait_for(state="visible", timeout=15000)
        button.click()

        self.page.wait_for_timeout(1500)