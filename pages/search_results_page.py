from pages.base_page import BasePage


class SearchResultsPage(BasePage):
    SEARCH_INPUT = ".searchInput"
    SEARCH_BUTTON = "button.submit"
    PRODUCT_CARD = ".product-card"
    PRODUCT_NAME = ".product-card__name"

    def search(self, query: str):
        search_input = self.page.locator(self.SEARCH_INPUT).last

        search_input.wait_for(state="visible", timeout=10000)
        search_input.click()
        search_input.fill(query)
        search_input.press("Enter")

        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_load_state("networkidle")

    def is_loaded(self):
        return self.page.locator(self.PRODUCT_CARD).count() > 0

    def get_first_product_name(self):
        cards = self.page.locator(self.PRODUCT_CARD)
        if cards.count() == 0:
            return None

        return cards.first.locator(self.PRODUCT_NAME).inner_text().strip()

    def get_product_names(self):
        names = self.page.locator(self.PRODUCT_NAME)
        result = []

        for i in range(names.count()):
            result.append(names.nth(i).inner_text().strip())

        return result

    def get_heading(self):
        headings = self.page.locator("h1")
        if headings.count() == 0:
            return ""

        return headings.first.inner_text().strip()

    def get_items_count_text(self):
        body_text = self.page.locator("body").inner_text()

        for line in body_text.splitlines():
            line = line.strip()
            if "Показаны записи" in line:
                return line

        return ""