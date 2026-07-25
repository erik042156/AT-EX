import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage


def test_login_with_valid_credentials(driver, valid_login_credentials):
  login_page = LoginPage(driver)
  login_page.navigate_to_login()
  login_page.enter_email(valid_login_credentials["email"])
  login_page.enter_password(valid_login_credentials["password"])
  login_page.click_login_button()

  home_page = HomePage(driver)
  assert home_page.is_logout_link_displayed(), "로그인 성공 후 헤더에 Logout이 노출되어야 한다"
  assert home_page.get_logged_in_username() == valid_login_credentials["expected_username"], (
    f"Expected logged in username {valid_login_credentials['expected_username']}, "
    f"but got {home_page.get_logged_in_username()}"
  )


def test_login_with_invalid_password(driver, invalid_login_credentials):
  login_page = LoginPage(driver)
  login_page.navigate_to_login()
  login_page.enter_email(invalid_login_credentials["email"])
  login_page.enter_password(invalid_login_credentials["password"])
  login_page.click_login_button()

  assert login_page.is_error_message_displayed(), "잘못된 비밀번호 입력 시 오류 메시지가 표시되어야 한다"
  assert "Your email or password is incorrect!" in login_page.get_error_message_text(), (
    f"Expected error text to contain 'Your email or password is incorrect!', "
    f"but got {login_page.get_error_message_text()}"
  )
  assert login_page.is_on_login_page(), "로그인 실패 시 /login 페이지에 머물러야 한다"


def test_login_with_nonexistent_email(driver, nonexistent_login_credentials):
  login_page = LoginPage(driver)
  login_page.navigate_to_login()
  login_page.enter_email(nonexistent_login_credentials["email"])
  login_page.enter_password(nonexistent_login_credentials["password"])
  login_page.click_login_button()

  assert login_page.is_error_message_displayed(), "존재하지 않는 이메일 입력 시 오류 메시지가 표시되어야 한다"
  assert "Your email or password is incorrect!" in login_page.get_error_message_text(), (
    f"Expected error text to contain 'Your email or password is incorrect!', "
    f"but got {login_page.get_error_message_text()}"
  )
  assert login_page.is_on_login_page(), "로그인 실패 시 /login 페이지에 머물러야 한다"


def test_relogin_after_logout(driver, relogin_credentials):
  login_page = LoginPage(driver)
  login_page.navigate_to_login()
  login_page.enter_email(relogin_credentials["email"])
  login_page.enter_password(relogin_credentials["password"])
  login_page.click_login_button()

  home_page = HomePage(driver)
  assert home_page.is_logout_link_displayed(), "첫 로그인 후 헤더에 Logout이 노출되어야 한다"
  home_page.click_logout_link()

  login_page_after_logout = LoginPage(driver)
  assert login_page_after_logout.is_on_login_page(), "로그아웃 후 /login 페이지로 이동해야 한다"
  assert login_page_after_logout.is_signup_login_link_displayed(), (
    "로그아웃 후 헤더에 Signup/Login 링크가 노출되어야 한다"
  )
  login_page_after_logout.enter_email(relogin_credentials["email"])
  login_page_after_logout.enter_password(relogin_credentials["password"])
  login_page_after_logout.click_login_button()

  home_page_after_relogin = HomePage(driver)
  assert home_page_after_relogin.is_logout_link_displayed(), "재로그인 후 헤더에 Logout이 노출되어야 한다"
  assert (
    home_page_after_relogin.get_logged_in_username() == relogin_credentials["expected_username"]
  ), (
    f"Expected logged in username {relogin_credentials['expected_username']}, "
    f"but got {home_page_after_relogin.get_logged_in_username()}"
  )
