from pages.base_page import BasePage


class FavoritesPage(BasePage):
    URL = "https://mebelmart-saratov.ru/favorite"

    PRODUCT_CARD = ".product-card"
    PRODUCT_NAME = ".product-card__name"

    def open_favorites(self):
        self.open(self.URL)
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_load_state("networkidle")

    def wait_for_favorites_loaded(self):
        self.page.locator("body").wait_for(timeout=15000)

    def get_favorite_product_names(self):
        names = self.page.locator(self.PRODUCT_NAME)
        result = []

        for i in range(names.count()):
            result.append(names.nth(i).inner_text().strip())

        return result

    def get_favorite_product_links(self):
        links = self.page.locator(self.PRODUCT_NAME)
        result = []

        for i in range(links.count()):
            href = links.nth(i).get_attribute("href")
            if href:
                result.append(href.strip())

        return result

    def is_product_in_favorites_by_link(self, expected_link: str):
        links = self.get_favorite_product_links()
        return expected_link in links

    def is_product_in_favorites_by_keyword(self, keyword: str):
        names = self.get_favorite_product_names()
        return any(keyword.lower() in name.lower() for name in names)