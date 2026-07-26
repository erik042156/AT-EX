from typing import List

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from config.settings import BASE_URL, PAGE_LOAD_TIMEOUT
from pages.base_page import BasePage, Locator
from utils.helpers import normalize_whitespace
from utils.logger import get_logger

logger = get_logger(__name__)


class ProductsPage(BasePage):
  SEARCH_INPUT: Locator = (By.ID, "search_product")
  SEARCH_BUTTON: Locator = (By.ID, "submit_search")
  PRODUCT_CARDS: Locator = (By.CSS_SELECTOR, ".features_items .product-image-wrapper")
  PRODUCT_NAME: Locator = (By.CSS_SELECTOR, ".features_items .productinfo p")
  PRODUCT_NAME_IN_CARD: Locator = (By.CSS_SELECTOR, ".productinfo p")
  ADD_TO_CART_BUTTON_IN_CARD: Locator = (By.CSS_SELECTOR, ".productinfo a.add-to-cart")
  VIEW_PRODUCT_LINK_IN_CARD: Locator = (By.CSS_SELECTOR, ".choose a")
  QUANTITY_INPUT: Locator = (By.ID, "quantity")
  ADD_TO_CART_BUTTON: Locator = (By.CSS_SELECTOR, "button.cart")
  ADD_TO_CART_SUCCESS_MODAL: Locator = (By.CSS_SELECTOR, "div.modal-content")
  VIEW_CART_LINK_IN_MODAL: Locator = (By.CSS_SELECTOR, "div.modal-content a[href='/view_cart']")
  CONTINUE_SHOPPING_BUTTON_IN_MODAL: Locator = (By.CSS_SELECTOR, "button.close-modal")

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

  def _find_card_by_product_name(self, product_name: str) -> WebElement:
    self.wait_for_element_presence(self.PRODUCT_CARDS)
    for card in self.find_elements(self.PRODUCT_CARDS):
      name = normalize_whitespace(card.find_element(*self.PRODUCT_NAME_IN_CARD).text)
      if name == product_name:
        return card
    logger.error(f"상품을 찾을 수 없음: {product_name}")
    raise NoSuchElementException(f"상품을 찾을 수 없음: {product_name}")

  def add_product_to_cart_by_name(self, product_name: str) -> None:
    card = self._find_card_by_product_name(product_name)
    self.click_element(card.find_element(*self.ADD_TO_CART_BUTTON_IN_CARD))
    self.find_element_visible(self.ADD_TO_CART_SUCCESS_MODAL)

  def open_product_detail(self, product_name: str) -> None:
    card = self._find_card_by_product_name(product_name)
    self.click_element(card.find_element(*self.VIEW_PRODUCT_LINK_IN_CARD))
    self.wait_for_element_presence(self.QUANTITY_INPUT, timeout=PAGE_LOAD_TIMEOUT)

  def enter_quantity(self, quantity: int) -> None:
    quantity_input = self.find_element_visible(self.QUANTITY_INPUT)
    quantity_input.clear()
    quantity_input.send_keys(str(quantity))

  def click_add_to_cart_button(self) -> None:
    self.click_when_clickable(self.ADD_TO_CART_BUTTON)
    self.find_element_visible(self.ADD_TO_CART_SUCCESS_MODAL)

  def click_view_cart_in_success_modal(self) -> None:
    self.click_when_clickable(self.VIEW_CART_LINK_IN_MODAL)

  def click_continue_shopping_in_success_modal(self) -> None:
    self.click_when_clickable(self.CONTINUE_SHOPPING_BUTTON_IN_MODAL)
