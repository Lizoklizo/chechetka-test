from pages.base_page import BasePage


class ProductPage(BasePage):
    PRODUCT_TITLE = "h1"
    CHARACTERISTICS_TAB = "text=Характеристики"
    CHARACTERISTICS_TABLE_ROWS = "table tr"

    def wait_for_product_loaded(self):
        self.page.locator(self.PRODUCT_TITLE).first.wait_for(timeout=15000)

    def get_product_title(self):
        return self.page.locator(self.PRODUCT_TITLE).first.inner_text().strip()

    def is_product_page(self):
        return self.page.locator(self.PRODUCT_TITLE).count() > 0

    def open_characteristics_tab(self):
        self.page.locator(self.CHARACTERISTICS_TAB).first.click()
        self.page.wait_for_timeout(1000)

    def get_characteristic_value(self, characteristic_name: str):
        rows = self.page.locator(self.CHARACTERISTICS_TABLE_ROWS)
        count = rows.count()

        for i in range(count):
            row = rows.nth(i)
            cells = row.locator("td")

            if cells.count() < 2:
                continue

            key = cells.nth(0).inner_text().strip().lower()
            value = cells.nth(1).inner_text().strip()

            normalized_key = key.replace(",", "").replace(".", "").strip()

            if characteristic_name.lower() in normalized_key:
                return value

        return None