from typing import List

from selenium.webdriver.common.by import By

from config.settings import BASE_URL
from pages.base_page import BasePage, Locator


class ProductsPage(BasePage):
  SEARCH_INPUT: Locator = (By.ID, "search_product")
  SEARCH_BUTTON: Locator = (By.ID, "submit_search")
  PRODUCT_CARDS: Locator = (By.CSS_SELECTOR, ".features_items .product-image-wrapper")
  PRODUCT_NAME: Locator = (By.CSS_SELECTOR, ".features_items .productinfo p")

  def navigate_to_products(self) -> None:
    self.driver.get(f"{BASE_URL}/products")

  def enter_search_keyword(self, keyword: str) -> None:
    self.find_element_visible(self.SEARCH_INPUT).send_keys(keyword)

  def click_search_button(self) -> None:
    self.click_when_clickable(self.SEARCH_BUTTON)

  def get_product_count(self) -> int:
    return len(self.find_elements(self.PRODUCT_CARDS))

  def get_product_names(self) -> List[str]:
    return [element.text for element in self.find_elements(self.PRODUCT_NAME)]

  def is_on_products_page(self) -> bool:
    return "/products" in self.driver.current_url
