import re
from pages.base_page import BasePage


class CartPage(BasePage):
    ITEM_NAMES = 'a[href*="/id"]'
    TOTAL_BLOCK = "text=Итого:"

    @staticmethod
    def normalize_price(raw_price: str) -> int:
        digits = re.sub(r"[^\d]", "", raw_price)
        if not digits:
            raise AssertionError(f"Не удалось извлечь цену из строки: {raw_price}")
        return int(digits)

    def get_item_names(self):
        links = self.page.locator(self.ITEM_NAMES)
        result = []

        for i in range(links.count()):
            text = links.nth(i).inner_text().strip()
            if text:
                result.append(text)

        return result

    def get_total_price(self):
        total_text = self.page.locator(self.TOTAL_BLOCK).first.inner_text().strip()
        return self.normalize_price(total_text)