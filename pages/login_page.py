from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import BASE_URL, DEFAULT_TIMEOUT
from pages.base_page import BasePage, Locator
from pages.home_page import HomePage
from pages.signup_page import SignupPage
from utils.logger import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
  SIGNUP_NAME_INPUT: Locator = (By.CSS_SELECTOR, "input[data-qa='signup-name']")
  SIGNUP_EMAIL_INPUT: Locator = (By.CSS_SELECTOR, "input[data-qa='signup-email']")
  SIGNUP_BUTTON: Locator = (By.CSS_SELECTOR, "button[data-qa='signup-button']")
  LOGIN_EMAIL_INPUT: Locator = (By.CSS_SELECTOR, "input[data-qa='login-email']")
  LOGIN_PASSWORD_INPUT: Locator = (By.CSS_SELECTOR, "input[data-qa='login-password']")
  LOGIN_BUTTON: Locator = (By.CSS_SELECTOR, "button[data-qa='login-button']")
  LOGIN_ERROR_MESSAGE: Locator = (By.CSS_SELECTOR, ".login-form p")

  def navigate_to_login(self) -> None:
    self.driver.get(f"{BASE_URL}/login")

  def enter_signup_name(self, name: str) -> None:
    self.find_element_visible(self.SIGNUP_NAME_INPUT).send_keys(name)

  def enter_signup_email(self, email: str) -> None:
    self.find_element_visible(self.SIGNUP_EMAIL_INPUT).send_keys(email)

  def click_signup_button(self) -> None:
    self.click_when_clickable(self.SIGNUP_BUTTON)
    self.wait_for_element_presence(SignupPage.NAME_INPUT)

  def enter_email(self, email: str) -> None:
    self.find_element_visible(self.LOGIN_EMAIL_INPUT).send_keys(email)

  def enter_password(self, password: str) -> None:
    self.find_element_visible(self.LOGIN_PASSWORD_INPUT).send_keys(password)

  def click_login_button(self) -> None:
    self.click_when_clickable(self.LOGIN_BUTTON)
    wait = WebDriverWait(self.driver, DEFAULT_TIMEOUT)
    try:
      wait.until(
        EC.any_of(
          EC.presence_of_element_located(HomePage.LOGOUT_LINK),
          EC.visibility_of_element_located(self.LOGIN_ERROR_MESSAGE),
        )
      )
    except TimeoutException as e:
      logger.error(f"로그인 결과(홈 이동 또는 오류 메시지)를 기다리는 중 타임아웃 발생: {str(e)}")
      raise

  def is_error_message_displayed(self) -> bool:
    return self.is_element_displayed(self.LOGIN_ERROR_MESSAGE)

  def get_error_message_text(self) -> str:
    return self.find_element(self.LOGIN_ERROR_MESSAGE).text

  def is_on_login_page(self) -> bool:
    return "/login" in self.driver.current_url

  def is_signup_login_link_displayed(self) -> bool:
    return self.is_element_displayed(HomePage.SIGNUP_LOGIN_LINK)

  def is_delete_account_link_displayed(self) -> bool:
    return self.is_element_displayed(HomePage.DELETE_ACCOUNT_LINK)

  def is_logged_in_username_displayed(self) -> bool:
    return self.is_element_displayed(HomePage.LOGGED_IN_AS_TEXT)
