from typing import Optional, Tuple

from selenium.common.exceptions import (
  ElementClickInterceptedException,
  NoSuchElementException,
  TimeoutException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import DEFAULT_TIMEOUT
from utils.logger import get_logger

logger = get_logger(__name__)

Locator = Tuple[str, str]

_INTERCEPTING_ELEMENT_SCRIPT = """
const rect = arguments[0].getBoundingClientRect();
const x = rect.left + rect.width / 2;
const y = rect.top + rect.height / 2;
const top = document.elementFromPoint(x, y);
if (!top || top === arguments[0] || arguments[0].contains(top) || top.contains(arguments[0])) {
  return null;
}
return top;
"""


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

  def scroll_into_view(self, element: WebElement) -> None:
    self.driver.execute_script(
      "arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element
    )

  def click(self, locator: Locator) -> None:
    element = self.find_element(locator)
    self.scroll_into_view(element)
    element.click()

  def click_element(self, element: WebElement) -> None:
    self.scroll_into_view(element)
    element.click()

  def get_page_title(self) -> str:
    return self.driver.title

  def is_element_displayed(self, locator: Locator) -> bool:
    try:
      return self.find_element(locator).is_displayed()
    except NoSuchElementException:
      return False

  def find_element_visible(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
    wait = WebDriverWait(self.driver, timeout or DEFAULT_TIMEOUT)
    try:
      return wait.until(EC.visibility_of_element_located(locator))
    except TimeoutException as e:
      logger.error(f"요소가 보이기를 기다리는 중 타임아웃 발생: {locator}, {str(e)}")
      raise

  def _get_intercepting_element(self, element: WebElement) -> Optional[WebElement]:
    return self.driver.execute_script(_INTERCEPTING_ELEMENT_SCRIPT, element)

  def click_when_clickable(self, locator: Locator, timeout: Optional[int] = None) -> None:
    wait = WebDriverWait(self.driver, timeout or DEFAULT_TIMEOUT)
    try:
      element = wait.until(EC.element_to_be_clickable(locator))
    except TimeoutException as e:
      logger.error(f"요소가 클릭 가능해지기를 기다리는 중 타임아웃 발생: {locator}, {str(e)}")
      raise

    self.scroll_into_view(element)
    blocker = self._get_intercepting_element(element)
    if blocker is not None:
      logger.warning(
        f"클릭 대상을 다른 요소가 가리고 있어 JS 클릭으로 우회함: {locator}, "
        f"blocker=<{blocker.tag_name} class='{blocker.get_attribute('class')}'>"
      )
      self.driver.execute_script("arguments[0].click();", element)
      return

    try:
      element.click()
    except ElementClickInterceptedException as e:
      logger.warning(f"클릭이 다른 요소에 가로채짐, JS 클릭으로 재시도: {locator}, {str(e)}")
      self.driver.execute_script("arguments[0].click();", element)

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

  def wait_for_element_invisible(self, locator: Locator, timeout: Optional[int] = None) -> bool:
    wait = WebDriverWait(self.driver, timeout or DEFAULT_TIMEOUT)
    try:
      return wait.until(EC.invisibility_of_element_located(locator))
    except TimeoutException as e:
      logger.error(f"요소가 사라지기를 기다리는 중 타임아웃 발생: {locator}, {str(e)}")
      raise
