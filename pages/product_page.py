from pages.base_page import BasePage
import re


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

    def open_characteristics_tab(self):
        tab = self.page.locator("text=Характеристики").first
        tab.wait_for(state="visible", timeout=10000)
        tab.click()
        self.page.locator("text=Ширина").first.wait_for(state="visible", timeout=10000)

    def get_characteristic_value(self, name: str):
        candidates = [
            self.page.locator(f"xpath=//*[contains(normalize-space(.), '{name}') and contains(normalize-space(.), 'мм')]").first,
            self.page.locator(f"text={name}").first,
        ]

        for locator in candidates:
            try:
                if locator.count() > 0:
                    text = locator.inner_text().strip()
                    match = re.search(rf"{name}\D*(\d+)", text)
                    if match:
                        return match.group(1)

                    parent_text = locator.locator("xpath=ancestor::*[self::li or self::tr or self::div][1]").inner_text().strip()
                    match = re.search(rf"{name}\D*(\d+)", parent_text)
                    if match:
                        return match.group(1)
            except Exception:
                continue
