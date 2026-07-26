import json
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config.settings import HEADLESS
from pages.login_page import LoginPage

ACCOUNTS_DATA_PATH = "test_data/accounts.json"
SEARCH_KEYWORDS_DATA_PATH = "test_data/search_keywords.json"
PRODUCTS_DATA_PATH = "test_data/products.json"


def pytest_addoption(parser):
  parser.addoption("--browser", action="store", default="chrome", help="chrome 또는 firefox")


@pytest.fixture(scope="function")
def driver(request):
  browser = request.config.getoption("--browser")
  if browser == "firefox":
    options = FirefoxOptions()
    if HEADLESS:
      options.add_argument("--headless")
    drv = webdriver.Firefox(options=options)
  else:
    options = webdriver.ChromeOptions()
    if HEADLESS:
      options.add_argument("--headless=new")
    drv = webdriver.Chrome(options=options)
  drv.set_window_size(1920, 1080)
  yield drv
  drv.quit()


@pytest.fixture(scope="session")
def accounts_data():
  with open(ACCOUNTS_DATA_PATH, encoding="utf-8") as f:
    return json.load(f)


@pytest.fixture
def valid_signup_data(accounts_data):
  return accounts_data["signup"]["valid_signup"]


@pytest.fixture
def relogin_signup_data(accounts_data):
  return accounts_data["signup"]["relogin_signup"]


@pytest.fixture
def valid_login_credentials(accounts_data):
  return accounts_data["shared_login_accounts"]["valid_account"]


@pytest.fixture
def relogin_credentials(accounts_data):
  return accounts_data["shared_login_accounts"]["relogin_account"]


@pytest.fixture
def invalid_login_credentials(accounts_data):
  return accounts_data["shared_login_accounts"]["invalid_password"]


@pytest.fixture
def nonexistent_login_credentials(accounts_data):
  return accounts_data["shared_login_accounts"]["nonexistent_email"]


@pytest.fixture
def logged_in_user(driver, valid_login_credentials):
  login_page = LoginPage(driver)
  login_page.navigate_to_login()
  login_page.enter_email(valid_login_credentials["email"])
  login_page.enter_password(valid_login_credentials["password"])
  login_page.click_login_button()
  return valid_login_credentials


@pytest.fixture(scope="session")
def search_keywords_data():
  with open(SEARCH_KEYWORDS_DATA_PATH, encoding="utf-8") as f:
    return json.load(f)


@pytest.fixture
def valid_search_keyword(search_keywords_data):
  return search_keywords_data["valid_keywords"][0]


@pytest.fixture
def nonexistent_search_keyword(search_keywords_data):
  return search_keywords_data["invalid_keywords"][0]


@pytest.fixture
def case_insensitive_keywords(search_keywords_data):
  return search_keywords_data["case_insensitive_check"]


@pytest.fixture(scope="session")
def products_data():
  with open(PRODUCTS_DATA_PATH, encoding="utf-8") as f:
    return json.load(f)


@pytest.fixture
def cart_test_product(products_data):
  return products_data["cart_test_product_1"]


@pytest.fixture
def cart_test_product_secondary(products_data):
  return products_data["cart_test_product_2"]


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
