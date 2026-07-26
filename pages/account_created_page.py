from selenium.webdriver.common.by import By

from config.settings import PAGE_LOAD_TIMEOUT
from pages.base_page import BasePage, Locator
from pages.home_page import HomePage


class AccountCreatedPage(BasePage):
  ACCOUNT_CREATED_MESSAGE: Locator = (By.CSS_SELECTOR, "h2[data-qa='account-created']")
  CONTINUE_BUTTON: Locator = (By.CSS_SELECTOR, "a[data-qa='continue-button']")

  def is_account_created_message_displayed(self) -> bool:
    return self.find_element_visible(self.ACCOUNT_CREATED_MESSAGE) is not None

  def click_continue_button(self) -> None:
    self.click_when_clickable(self.CONTINUE_BUTTON)
    # 홈페이지는 광고 로딩이 많아 리다이렉트 후 렌더링이 DEFAULT_TIMEOUT(10초)을 넘길 수 있어
    # project-prd.md §11.4의 페이지 로드 타임아웃(20초)을 적용한다.
    self.wait_for_element_presence(HomePage.LOGOUT_LINK, timeout=PAGE_LOAD_TIMEOUT)
