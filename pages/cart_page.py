from typing import List

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from config.settings import BASE_URL
from pages.base_page import BasePage, Locator
from utils.helpers import normalize_whitespace, parse_price_text
from utils.logger import get_logger

logger = get_logger(__name__)


class CartPage(BasePage):
  CART_ROW: Locator = (By.CSS_SELECTOR, "#cart_info_table tbody tr")
  PRODUCT_DESCRIPTION_CELL: Locator = (By.CSS_SELECTOR, "td.cart_description h4 a")
  PRODUCT_PRICE_CELL: Locator = (By.CSS_SELECTOR, "td.cart_price p")
  PRODUCT_QUANTITY_CELL: Locator = (By.CSS_SELECTOR, "td.cart_quantity button")
  PRODUCT_TOTAL_CELL: Locator = (By.CSS_SELECTOR, "td.cart_total p.cart_total_price")
  DELETE_ICON: Locator = (By.CSS_SELECTOR, "td.cart_delete a.cart_quantity_delete")
  EMPTY_CART_MESSAGE: Locator = (By.ID, "empty_cart")
  PROCEED_TO_CHECKOUT_BUTTON: Locator = (By.CSS_SELECTOR, "a.check_out")
  LOGIN_MODAL: Locator = (By.ID, "checkoutModal")

  def navigate_to_cart(self) -> None:
    self.driver.get(f"{BASE_URL}/view_cart")

  def _find_rows_by_product_name(self, product_name: str) -> List[WebElement]:
    return [
      row
      for row in self.find_elements(self.CART_ROW)
      if normalize_whitespace(row.find_element(*self.PRODUCT_DESCRIPTION_CELL).text) == product_name
    ]

  def _get_row_by_product_name(self, product_name: str) -> WebElement:
    rows = self._find_rows_by_product_name(product_name)
    if not rows:
      logger.error(f"장바구니에서 상품을 찾을 수 없음: {product_name}")
      raise NoSuchElementException(f"장바구니에서 상품을 찾을 수 없음: {product_name}")
    return rows[0]

  def is_product_in_cart(self, product_name: str) -> bool:
    return len(self._find_rows_by_product_name(product_name)) > 0

  def get_cart_row_count_for_product(self, product_name: str) -> int:
    return len(self._find_rows_by_product_name(product_name))

  def get_product_price(self, product_name: str) -> int:
    row = self._get_row_by_product_name(product_name)
    return parse_price_text(row.find_element(*self.PRODUCT_PRICE_CELL).text)

  def get_product_quantity(self, product_name: str) -> int:
    row = self._get_row_by_product_name(product_name)
    return int(row.find_element(*self.PRODUCT_QUANTITY_CELL).text)

  def get_product_total(self, product_name: str) -> int:
    row = self._get_row_by_product_name(product_name)
    return parse_price_text(row.find_element(*self.PRODUCT_TOTAL_CELL).text)

  def delete_product(self, product_name: str) -> None:
    row = self._get_row_by_product_name(product_name)
    row_id = row.get_attribute("id")
    self.click_element(row.find_element(*self.DELETE_ICON))
    self.wait_for_element_invisible((By.ID, row_id))

  def is_empty_cart_message_displayed(self) -> bool:
    return self.is_element_displayed(self.EMPTY_CART_MESSAGE)

  def is_proceed_to_checkout_button_displayed(self) -> bool:
    return self.is_element_displayed(self.PROCEED_TO_CHECKOUT_BUTTON)

  def click_proceed_to_checkout(self) -> None:
    self.click_when_clickable(self.PROCEED_TO_CHECKOUT_BUTTON)

  def is_login_modal_displayed(self) -> bool:
    try:
      self.find_element_visible(self.LOGIN_MODAL)
      return True
    except TimeoutException:
      return False
