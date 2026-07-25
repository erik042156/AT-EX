from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import DEFAULT_TIMEOUT
from pages.base_page import BasePage, Locator
from pages.delete_account_page import DeleteAccountPage
from utils.logger import get_logger

logger = get_logger(__name__)


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
    self.click_when_clickable(self.DELETE_ACCOUNT_LINK)
    self.wait_for_element_presence(DeleteAccountPage.ACCOUNT_DELETED_MESSAGE)

  def get_logged_in_username(self) -> str:
    text = self.find_element(self.LOGGED_IN_AS_TEXT).text
    return text.replace("Logged in as", "").strip()

  def click_logout_link(self) -> None:
    self.click_when_clickable(self.LOGOUT_LINK)
    wait = WebDriverWait(self.driver, DEFAULT_TIMEOUT)
    try:
      wait.until(EC.url_contains("/login"))
    except TimeoutException as e:
      logger.error(f"로그아웃 후 /login 이동을 기다리는 중 타임아웃 발생: {str(e)}")
      raise
