from selenium.webdriver.common.by import By

from pages.base_page import BasePage, Locator


class DeleteAccountPage(BasePage):
  ACCOUNT_DELETED_MESSAGE: Locator = (By.CSS_SELECTOR, "h2[data-qa='account-deleted']")
  CONTINUE_BUTTON: Locator = (By.CSS_SELECTOR, "a[data-qa='continue-button']")

  def is_account_deleted_message_displayed(self) -> bool:
    return self.find_element_visible(self.ACCOUNT_DELETED_MESSAGE) is not None

  def click_continue_button(self) -> None:
    self.click_when_clickable(self.CONTINUE_BUTTON)
