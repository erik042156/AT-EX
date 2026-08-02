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

_OVERLAY_HEURISTIC_SCRIPT = """
const CLOSE_TEXT_PATTERN = /^(close|\\u00d7|x|skip|no,? thanks|\\uB2eb\\uae30)$/i;

function isOverlayPositioned(el) {
  const style = window.getComputedStyle(el);
  return style.position === 'fixed' || style.position === 'absolute' || style.position === 'sticky';
}

function isLargeFixedOrAbsolute(el) {
  if (!isOverlayPositioned(el)) return false;
  const rect = el.getBoundingClientRect();
  return rect.width >= window.innerWidth * 0.5 && rect.height >= window.innerHeight * 0.5;
}

function hasHighZIndex(el) {
  if (!isOverlayPositioned(el)) return false;
  const zIndex = parseInt(window.getComputedStyle(el).zIndex, 10);
  return !Number.isNaN(zIndex) && zIndex > 999;
}

function isLargeIframe(el) {
  if (el.tagName !== 'IFRAME') return false;
  const rect = el.getBoundingClientRect();
  return rect.width * rect.height >= window.innerWidth * window.innerHeight * 0.3;
}

function findCloseButton(container) {
  const candidates = container.querySelectorAll('*');
  for (const el of candidates) {
    const text = (el.textContent || '').trim();
    if (text && text.length <= 20 && CLOSE_TEXT_PATTERN.test(text)) {
      return el;
    }
  }
  return null;
}

const elements = document.body.querySelectorAll('*');
let handled = 0;
for (const el of elements) {
  if (!isLargeFixedOrAbsolute(el) && !hasHighZIndex(el) && !isLargeIframe(el)) continue;
  const closeButton = findCloseButton(el);
  if (closeButton) {
    closeButton.click();
    handled += 1;
    continue;
  }
  el.remove();
  handled += 1;
}
return handled;
"""

_MAX_OVERLAY_DISMISS_ATTEMPTS = 20
_MIN_CHUNK_SECONDS = 0.5


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

  def _dismiss_overlays(self) -> int:
    handled = self.driver.execute_script(_OVERLAY_HEURISTIC_SCRIPT)
    if handled:
      logger.warning(f"오버레이로 추정되는 요소 {handled}개를 닫거나 제거함(광고/설문 등으로 추정)")
    return handled

  def _wait_with_overlay_retry(self, condition, timeout: Optional[int] = None):
    total = timeout or DEFAULT_TIMEOUT
    chunk = max(total / _MAX_OVERLAY_DISMISS_ATTEMPTS, _MIN_CHUNK_SECONDS)
    remaining = total
    attempts = 0
    last_exception: Optional[TimeoutException] = None
    while remaining > 0 and attempts < _MAX_OVERLAY_DISMISS_ATTEMPTS:
      step = min(chunk, remaining)
      wait = WebDriverWait(self.driver, step)
      try:
        return wait.until(condition)
      except TimeoutException as e:
        last_exception = e
        self._dismiss_overlays()
        remaining -= step
        attempts += 1
    logger.error(
      f"오버레이 대응 재시도({_MAX_OVERLAY_DISMISS_ATTEMPTS}회)에도 조건이 충족되지 않아 "
      f"타임아웃 발생: {str(last_exception)}"
    )
    raise last_exception

  def find_element_visible(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
    return self._wait_with_overlay_retry(EC.visibility_of_element_located(locator), timeout)

  def _get_intercepting_element(self, element: WebElement) -> Optional[WebElement]:
    return self.driver.execute_script(_INTERCEPTING_ELEMENT_SCRIPT, element)

  def click_when_clickable(self, locator: Locator, timeout: Optional[int] = None) -> None:
    element = self._wait_with_overlay_retry(EC.element_to_be_clickable(locator), timeout)

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
    return self._wait_with_overlay_retry(EC.presence_of_element_located(locator), timeout)

  def wait_for_text(self, locator: Locator, text: str, timeout: Optional[int] = None) -> bool:
    return self._wait_with_overlay_retry(EC.text_to_be_present_in_element(locator, text), timeout)

  def wait_for_element_invisible(self, locator: Locator, timeout: Optional[int] = None) -> bool:
    return self._wait_with_overlay_retry(EC.invisibility_of_element_located(locator), timeout)

  def click_and_wait(self, click_locator: Locator, condition, timeout: Optional[int] = None):
    total = timeout or DEFAULT_TIMEOUT
    chunk = max(total / _MAX_OVERLAY_DISMISS_ATTEMPTS, _MIN_CHUNK_SECONDS)
    remaining = total
    attempts = 0
    last_exception: Optional[TimeoutException] = None
    while remaining > 0 and attempts < _MAX_OVERLAY_DISMISS_ATTEMPTS:
      step = min(chunk, remaining)
      self._dismiss_overlays()
      self.click_when_clickable(click_locator, timeout=step)
      try:
        return WebDriverWait(self.driver, step).until(condition)
      except TimeoutException as e:
        last_exception = e
        remaining -= step
        attempts += 1
    logger.error(
      f"클릭 후 조건 충족 대기 재시도({_MAX_OVERLAY_DISMISS_ATTEMPTS}회)에도 실패함(광고 등에 의해 "
      f"클릭 효과가 유실됐을 가능성): {click_locator}, {str(last_exception)}"
    )
    raise last_exception
