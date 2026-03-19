import re
from pages.base_page import BasePage


class CatalogPage(BasePage):
    URL = "https://mebelmart-saratov.ru/myagkaya_mebel_v_saratove/divanyi_v_saratove"

    PRODUCT_CARD = ".product-card"
    PRODUCT_NAME = ".product-card__name"
    PRODUCT_PRICE = ".product-card__now_price"
    PRODUCT_OPEN_BUTTON = "a.btn.btn-primary"
    FAVORITE_BUTTON = ".favorite-icon"

    def open_catalog(self):
        self.open(self.URL)

    def open_catalog_with_price_filter(self, price_from: int, price_to: int):
        filter_url = f"{self.URL}?filterRange=&price={price_from}-{price_to}"
        self.open(filter_url)
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_load_state("networkidle")

    def wait_for_catalog_loaded(self):
        self.page.locator(self.PRODUCT_CARD).first.wait_for(timeout=15000)

    def is_catalog_loaded(self):
        return self.page.locator(self.PRODUCT_CARD).count() > 0

    def get_product_cards_count(self):
        return self.page.locator(self.PRODUCT_CARD).count()

    def get_name_price_pairs(self, limit=15):
        cards = self.page.locator(self.PRODUCT_CARD)
        result = []

        for i in range(min(cards.count(), limit)):
            card = cards.nth(i)
            name = card.locator(self.PRODUCT_NAME).inner_text().strip()
            raw_price = card.locator(self.PRODUCT_PRICE).inner_text().strip()
            result.append((name, raw_price))

        return result

    @staticmethod
    def _extract_actual_price(raw_price: str):
        numbers = re.findall(r"\d[\d\s]*", raw_price)
        if not numbers:
            return None
        return int(numbers[-1].replace(" ", ""))

    def find_products_by_name(self, target_name: str):
        cards = self.page.locator(self.PRODUCT_CARD)
        matches = []

        for i in range(cards.count()):
            card = cards.nth(i)
            name = card.locator(self.PRODUCT_NAME).inner_text().strip()

            if target_name.lower() in name.lower():
                raw_price = card.locator(self.PRODUCT_PRICE).inner_text().strip()
                actual_price = self._extract_actual_price(raw_price)
                matches.append({
                    "card": card,
                    "name": name,
                    "raw_price": raw_price,
                    "actual_price": actual_price,
                    "index": i,
                })

        return matches

    def find_product_by_name_in_price_range(self, target_name: str, price_from: int, price_to: int):
        matches = self.find_products_by_name(target_name)

        for item in matches:
            price = item["actual_price"]
            if price is not None and price_from <= price <= price_to:
                return item

        return None

    def get_product_card_by_name(self, target_name: str):
        matches = self.find_products_by_name(target_name)

        if not matches:
            raise AssertionError(f"Товар с названием '{target_name}' не найден")

        return matches[0]["card"]

    def get_product_name_from_catalog(self, target_name: str):
        matches = self.find_products_by_name(target_name)

        if not matches:
            raise AssertionError(f"Товар с названием '{target_name}' не найден")

        return matches[0]["name"]

    def open_product_by_name(self, target_name: str):
        card = self.get_product_card_by_name(target_name)
        card.scroll_into_view_if_needed()
        card.locator(self.PRODUCT_OPEN_BUTTON).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_load_state("networkidle")

    def get_catalog_card_dimensions(self, target_name: str):
        card = self.get_product_card_by_name(target_name)
        card_text = card.inner_text()

        dimensions = {}

        width_match = re.search(r"Ширина:\s*(\d+)\s*мм", card_text, re.IGNORECASE)
        depth_match = re.search(r"Глубина:\s*(\d+)\s*мм", card_text, re.IGNORECASE)

        if width_match:
            dimensions["Ширина"] = width_match.group(1)

        if depth_match:
            dimensions["Глубина"] = depth_match.group(1)

        return dimensions

    def get_first_product_card(self):
        return self.page.locator(self.PRODUCT_CARD).first

    def get_first_product_name(self):
        card = self.get_first_product_card()
        return card.locator(self.PRODUCT_NAME).inner_text().strip()

    def add_first_product_to_favorites(self):
        card = self.get_first_product_card()
        card.scroll_into_view_if_needed()
        card.locator(self.FAVORITE_BUTTON).first.click()
        self.page.wait_for_timeout(1500)

    def highlight_product(self, product_item):
        card = product_item["card"]

        card.scroll_into_view_if_needed()
        self.page.wait_for_timeout(1200)

        card.evaluate(
            """
            el => {
                el.style.outline = '5px solid red';
                el.style.outlineOffset = '4px';
                el.style.backgroundColor = '#fff3cd';
            }
            """
        )

        self.page.wait_for_timeout(2500)

    def highlight_all_matching_products(self, target_name: str):
        matches = self.find_products_by_name(target_name)

        for item in matches:
            try:
                item["card"].evaluate(
                    """
                    el => {
                        el.style.outline = '3px dashed orange';
                        el.style.outlineOffset = '3px';
                    }
                    """
                )
            except Exception:
                pass

        return matches

    def get_first_product_link(self):
        card = self.get_first_product_card()
        return card.locator(self.PRODUCT_OPEN_BUTTON).first.get_attribute("href")

    def get_first_product_keyword(self):
        full_name = self.get_first_product_name()
        words = full_name.split()

        if len(words) > 1:
            return words[-1].strip()

        return full_name.strip()

