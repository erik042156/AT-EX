from selenium.webdriver.common.by import By

from config.settings import BASE_URL
from pages.base_page import BasePage


def test_driver_opens_and_closes(driver):
  driver.get(BASE_URL)
  assert driver.title != ""


def test_base_page_wait_methods(driver):
  driver.get(BASE_URL)
  page = BasePage(driver)
  element = page.wait_for_element_presence((By.TAG_NAME, "body"))
  assert element is not None
