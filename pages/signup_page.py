from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from config.settings import PAGE_LOAD_TIMEOUT
from pages.account_created_page import AccountCreatedPage
from pages.base_page import BasePage, Locator


class SignupPage(BasePage):
  TITLE_MR_RADIO: Locator = (By.ID, "id_gender1")
  TITLE_MRS_RADIO: Locator = (By.ID, "id_gender2")
  NAME_INPUT: Locator = (By.ID, "name")
  DISPLAYED_EMAIL: Locator = (By.ID, "email")
  PASSWORD_INPUT: Locator = (By.ID, "password")
  DOB_DAY_SELECT: Locator = (By.ID, "days")
  DOB_MONTH_SELECT: Locator = (By.ID, "months")
  DOB_YEAR_SELECT: Locator = (By.ID, "years")
  NEWSLETTER_CHECKBOX: Locator = (By.ID, "newsletter")
  OFFERS_CHECKBOX: Locator = (By.ID, "optin")
  FIRST_NAME_INPUT: Locator = (By.ID, "first_name")
  LAST_NAME_INPUT: Locator = (By.ID, "last_name")
  COMPANY_INPUT: Locator = (By.ID, "company")
  ADDRESS_INPUT: Locator = (By.ID, "address1")
  ADDRESS2_INPUT: Locator = (By.ID, "address2")
  COUNTRY_SELECT: Locator = (By.ID, "country")
  STATE_INPUT: Locator = (By.ID, "state")
  CITY_INPUT: Locator = (By.ID, "city")
  ZIPCODE_INPUT: Locator = (By.ID, "zipcode")
  MOBILE_NUMBER_INPUT: Locator = (By.ID, "mobile_number")
  CREATE_ACCOUNT_BUTTON: Locator = (By.CSS_SELECTOR, "button[data-qa='create-account']")

  def get_name_value(self) -> str:
    return self.find_element(self.NAME_INPUT).get_attribute("value")

  def is_name_field_editable(self) -> bool:
    return self.find_element(self.NAME_INPUT).get_attribute("disabled") is None

  def get_displayed_email(self) -> str:
    return self.find_element(self.DISPLAYED_EMAIL).get_attribute("value")

  def is_email_field_editable(self) -> bool:
    return self.find_element(self.DISPLAYED_EMAIL).get_attribute("disabled") is None

  def select_title(self, title: str) -> None:
    locator = self.TITLE_MR_RADIO if title == "Mr" else self.TITLE_MRS_RADIO
    self.click(locator)

  def enter_name(self, name: str) -> None:
    element = self.find_element_visible(self.NAME_INPUT)
    element.clear()
    element.send_keys(name)

  def enter_password(self, password: str) -> None:
    self.find_element_visible(self.PASSWORD_INPUT).send_keys(password)

  def select_date_of_birth(self, day: str, month: str, year: str) -> None:
    Select(self.find_element(self.DOB_DAY_SELECT)).select_by_visible_text(day)
    Select(self.find_element(self.DOB_MONTH_SELECT)).select_by_visible_text(month)
    Select(self.find_element(self.DOB_YEAR_SELECT)).select_by_visible_text(year)

  def check_newsletter(self) -> None:
    self.click(self.NEWSLETTER_CHECKBOX)

  def check_special_offers(self) -> None:
    self.click(self.OFFERS_CHECKBOX)

  def enter_first_name(self, first_name: str) -> None:
    self.find_element_visible(self.FIRST_NAME_INPUT).send_keys(first_name)

  def enter_last_name(self, last_name: str) -> None:
    self.find_element_visible(self.LAST_NAME_INPUT).send_keys(last_name)

  def enter_company(self, company: str) -> None:
    self.find_element_visible(self.COMPANY_INPUT).send_keys(company)

  def enter_address(self, address: str) -> None:
    self.find_element_visible(self.ADDRESS_INPUT).send_keys(address)

  def enter_address2(self, address2: str) -> None:
    self.find_element_visible(self.ADDRESS2_INPUT).send_keys(address2)

  def select_country(self, country: str) -> None:
    country_select = self.find_element(self.COUNTRY_SELECT)
    self.scroll_into_view(country_select)
    Select(country_select).select_by_visible_text(country)

  def enter_state(self, state: str) -> None:
    self.find_element_visible(self.STATE_INPUT).send_keys(state)

  def enter_city(self, city: str) -> None:
    self.find_element_visible(self.CITY_INPUT).send_keys(city)

  def enter_zipcode(self, zipcode: str) -> None:
    self.find_element_visible(self.ZIPCODE_INPUT).send_keys(zipcode)

  def enter_mobile_number(self, mobile_number: str) -> None:
    self.find_element_visible(self.MOBILE_NUMBER_INPUT).send_keys(mobile_number)

  def click_create_account_button(self) -> None:
    self.click_when_clickable(self.CREATE_ACCOUNT_BUTTON)
    self.wait_for_element_presence(AccountCreatedPage.ACCOUNT_CREATED_MESSAGE, timeout=PAGE_LOAD_TIMEOUT)

  def is_on_signup_page(self) -> bool:
    return "/signup" in self.driver.current_url
