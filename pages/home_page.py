from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config.settings import PAGE_LOAD_TIMEOUT
from pages.base_page import BasePage, Locator
from pages.delete_account_page import DeleteAccountPage


class HomePage(BasePage):
  LOGOUT_LINK: Locator = (By.CSS_SELECTOR, "a[href='/logout']")
  SIGNUP_LOGIN_LINK: Locator = (By.CSS_SELECTOR, "a[href='/login']")
  DELETE_ACCOUNT_LINK: Locator = (By.CSS_SELECTOR, "a[href='/delete_account']")
  LOGGED_IN_AS_TEXT: Locator = (By.XPATH, "//a[contains(., 'Logged in as')]")

  def is_logout_link_displayed(self) -> bool:
    return self.is_element_displayed(self.LOGOUT_LINK)

  def is_signup_login_link_displayed(self) -> bool:
    return self.is_element_displayed(self.SIGNUP_LOGIN_LINK)

  def is_delete_account_link_displayed(self) -> bool:
    return self.is_element_displayed(self.DELETE_ACCOUNT_LINK)

  def click_delete_account_link(self) -> None:
    self.click_and_wait(
      self.DELETE_ACCOUNT_LINK,
      EC.presence_of_element_located(DeleteAccountPage.ACCOUNT_DELETED_MESSAGE),
      timeout=PAGE_LOAD_TIMEOUT,
    )

  def get_logged_in_username(self) -> str:
    text = self.find_element(self.LOGGED_IN_AS_TEXT).text
    return text.replace("Logged in as", "").strip()

  def click_logout_link(self) -> None:
    self.click_and_wait(self.LOGOUT_LINK, EC.url_contains("/login"), timeout=PAGE_LOAD_TIMEOUT)
