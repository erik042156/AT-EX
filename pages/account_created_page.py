from selenium.webdriver.common.by import By

from pages.base_page import BasePage, Locator
from pages.home_page import HomePage


class AccountCreatedPage(BasePage):
  ACCOUNT_CREATED_MESSAGE: Locator = (By.CSS_SELECTOR, "h2[data-qa='account-created']")
  CONTINUE_BUTTON: Locator = (By.CSS_SELECTOR, "a[data-qa='continue-button']")

  def is_account_created_message_displayed(self) -> bool:
    return self.find_element_visible(self.ACCOUNT_CREATED_MESSAGE) is not None

  def click_continue_button(self) -> None:
    self.click_when_clickable(self.CONTINUE_BUTTON)
    self.wait_for_element_presence(HomePage.LOGOUT_LINK)
