from pages.account_created_page import AccountCreatedPage
from pages.delete_account_page import DeleteAccountPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.signup_page import SignupPage


def test_signup_with_valid_info(driver, valid_signup_data):
  login_page = LoginPage(driver)
  login_page.navigate_to_login()
  login_page.enter_signup_name(valid_signup_data["name"])
  login_page.enter_signup_email(valid_signup_data["email"])
  login_page.click_signup_button()

  signup_page = SignupPage(driver)
  assert signup_page.is_on_signup_page(), "Signup 클릭 후 /signup 페이지로 이동해야 한다"
  assert signup_page.get_name_value() == valid_signup_data["name"], (
    f"Expected name field value {valid_signup_data['name']}, but got {signup_page.get_name_value()}"
  )
  assert signup_page.is_name_field_editable() is True, "Name 필드는 수정 가능해야 한다"
  assert signup_page.get_displayed_email() == valid_signup_data["email"], (
    f"Expected displayed email {valid_signup_data['email']}, "
    f"but got {signup_page.get_displayed_email()}"
  )
  assert signup_page.is_email_field_editable() is False, "Email 필드는 수정 불가능해야 한다"

  signup_page.enter_password(valid_signup_data["password"])
  signup_page.enter_first_name(valid_signup_data["first_name"])
  signup_page.enter_last_name(valid_signup_data["last_name"])
  signup_page.enter_address(valid_signup_data["address"])
  signup_page.select_country(valid_signup_data["country"])
  signup_page.enter_state(valid_signup_data["state"])
  signup_page.enter_city(valid_signup_data["city"])
  signup_page.enter_zipcode(valid_signup_data["zipcode"])
  signup_page.enter_mobile_number(valid_signup_data["mobile_number"])
  signup_page.click_create_account_button()

  account_created_page = AccountCreatedPage(driver)
  assert account_created_page.is_account_created_message_displayed(), (
    "Account Created! 메시지가 표시되어야 한다"
  )
  account_created_page.click_continue_button()

  home_page = HomePage(driver)
  assert home_page.is_logout_link_displayed(), "Continue 클릭 후 헤더에 Logout이 노출되어야 한다"
  assert home_page.get_logged_in_username() == valid_signup_data["name"], (
    f"Expected logged in username {valid_signup_data['name']}, "
    f"but got {home_page.get_logged_in_username()}"
  )

  home_page.click_delete_account_link()
  delete_account_page = DeleteAccountPage(driver)
  assert delete_account_page.is_account_deleted_message_displayed(), (
    "테스트 종료 후 계정 정리를 위해 Account Deleted! 메시지가 표시되어야 한다"
  )


def test_signup_then_logout_and_relogin(driver, relogin_signup_data):
  login_page = LoginPage(driver)
  login_page.navigate_to_login()
  login_page.enter_signup_name(relogin_signup_data["name"])
  login_page.enter_signup_email(relogin_signup_data["email"])
  login_page.click_signup_button()

  signup_page = SignupPage(driver)
  signup_page.enter_password(relogin_signup_data["password"])
  signup_page.enter_first_name(relogin_signup_data["first_name"])
  signup_page.enter_last_name(relogin_signup_data["last_name"])
  signup_page.enter_address(relogin_signup_data["address"])
  signup_page.select_country(relogin_signup_data["country"])
  signup_page.enter_state(relogin_signup_data["state"])
  signup_page.enter_city(relogin_signup_data["city"])
  signup_page.enter_zipcode(relogin_signup_data["zipcode"])
  signup_page.enter_mobile_number(relogin_signup_data["mobile_number"])
  signup_page.click_create_account_button()

  account_created_page = AccountCreatedPage(driver)
  account_created_page.click_continue_button()

  home_page = HomePage(driver)
  assert home_page.is_logout_link_displayed(), "회원가입 직후 헤더에 Logout이 노출되어야 한다"
  home_page.click_logout_link()

  login_page_after_logout = LoginPage(driver)
  assert login_page_after_logout.is_on_login_page(), "로그아웃 후 /login 페이지로 이동해야 한다"
  login_page_after_logout.enter_email(relogin_signup_data["email"])
  login_page_after_logout.enter_password(relogin_signup_data["password"])
  login_page_after_logout.click_login_button()

  home_page_after_relogin = HomePage(driver)
  assert home_page_after_relogin.is_logout_link_displayed(), "재로그인 후 헤더에 Logout이 노출되어야 한다"
  assert home_page_after_relogin.get_logged_in_username() == relogin_signup_data["name"], (
    f"Expected logged in username {relogin_signup_data['name']}, "
    f"but got {home_page_after_relogin.get_logged_in_username()}"
  )

  home_page_after_relogin.click_delete_account_link()
  delete_account_page = DeleteAccountPage(driver)
  assert delete_account_page.is_account_deleted_message_displayed(), (
    "테스트 종료 후 계정 정리를 위해 Account Deleted! 메시지가 표시되어야 한다"
  )
