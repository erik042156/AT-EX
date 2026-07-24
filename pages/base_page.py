from typing import Optional, Tuple

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import DEFAULT_TIMEOUT
from utils.logger import get_logger

logger = get_logger(__name__)

Locator = Tuple[str, str]


class BasePage:
  def __init__(self, driver: WebDriver) -> None:
    self.driver = driver
    self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

  def find_element(self, locator: Locator) -> WebElement:
    try:
      return self.driver.find_element(*locator)
    except NoSuchElementException as e:
      logger.error(f"요소를 찾을 수 없음: {locator}, {str(e)}")
      raise

  def find_elements(self, locator: Locator) -> list[WebElement]:
    return self.driver.find_elements(*locator)

  def click(self, locator: Locator) -> None:
    self.find_element(locator).click()

  def get_page_title(self) -> str:
    return self.driver.title

  def find_element_visible(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
    wait = WebDriverWait(self.driver, timeout or DEFAULT_TIMEOUT)
    try:
      return wait.until(EC.visibility_of_element_located(locator))
    except TimeoutException as e:
      logger.error(f"요소가 보이기를 기다리는 중 타임아웃 발생: {locator}, {str(e)}")
      raise

  def click_when_clickable(self, locator: Locator, timeout: Optional[int] = None) -> None:
    wait = WebDriverWait(self.driver, timeout or DEFAULT_TIMEOUT)
    try:
      wait.until(EC.element_to_be_clickable(locator)).click()
    except TimeoutException as e:
      logger.error(f"요소가 클릭 가능해지기를 기다리는 중 타임아웃 발생: {locator}, {str(e)}")
      raise

  def wait_for_element_presence(
    self, locator: Locator, timeout: Optional[int] = None
  ) -> WebElement:
    wait = WebDriverWait(self.driver, timeout or DEFAULT_TIMEOUT)
    try:
      return wait.until(EC.presence_of_element_located(locator))
    except TimeoutException as e:
      logger.error(f"요소가 DOM에 나타나기를 기다리는 중 타임아웃 발생: {locator}, {str(e)}")
      raise

  def wait_for_text(self, locator: Locator, text: str, timeout: Optional[int] = None) -> bool:
    wait = WebDriverWait(self.driver, timeout or DEFAULT_TIMEOUT)
    try:
      return wait.until(EC.text_to_be_present_in_element(locator, text))
    except TimeoutException as e:
      logger.error(f"요소의 텍스트가 '{text}'가 되기를 기다리는 중 타임아웃 발생: {locator}, {str(e)}")
      raise
