from datetime import datetime

import pytest
from selenium import webdriver

from config.settings import HEADLESS


@pytest.fixture(scope="function")
def driver():
  options = webdriver.ChromeOptions()
  if HEADLESS:
    options.add_argument("--headless=new")
  drv = webdriver.Chrome(options=options)
  yield drv
  drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
  outcome = yield
  report = outcome.get_result()
  if report.when == "call" and report.failed:
    driver_fixture = item.funcargs.get("driver")
    if driver_fixture:
      timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
      filename = f"screenshots/{item.name}_failed_{timestamp}.png"
      driver_fixture.save_screenshot(filename)
