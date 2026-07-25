from pages.home_page import HomePage
from pages.login_page import LoginPage


def test_logout_from_logged_in_state(driver, logged_in_user):
  home_page = HomePage(driver)
  assert home_page.is_logout_link_displayed(), "로그인 상태에서 헤더에 Logout이 노출되어야 한다"
  home_page.click_logout_link()

  login_page = LoginPage(driver)
  assert login_page.is_on_login_page(), "Logout 클릭 후 /login 페이지로 이동해야 한다"
  assert login_page.is_signup_login_link_displayed(), (
    "로그아웃 후 헤더에 Signup/Login 통합 링크가 노출되어야 한다"
  )
  assert login_page.is_delete_account_link_displayed() is False, (
    "로그아웃 후 헤더에 Delete Account가 노출되지 않아야 한다"
  )
  assert login_page.is_logged_in_username_displayed() is False, (
    "로그아웃 후 헤더에 Logged in as username이 노출되지 않아야 한다"
  )


def test_logout_then_relogin(driver, logged_in_user):
  home_page = HomePage(driver)
  assert home_page.is_logout_link_displayed(), "로그인 상태에서 헤더에 Logout이 노출되어야 한다"
  home_page.click_logout_link()

  login_page = LoginPage(driver)
  assert login_page.is_on_login_page(), "Logout 클릭 후 /login 페이지로 이동해야 한다"

  login_page.enter_email(logged_in_user["email"])
  login_page.enter_password(logged_in_user["password"])
  login_page.click_login_button()

  home_page_after_relogin = HomePage(driver)
  assert home_page_after_relogin.is_logout_link_displayed(), (
    "재로그인 후 헤더에 Logout이 노출되어야 한다"
  )
  assert (
    home_page_after_relogin.get_logged_in_username() == logged_in_user["expected_username"]
  ), (
    f"Expected logged in username {logged_in_user['expected_username']}, "
    f"but got {home_page_after_relogin.get_logged_in_username()}"
  )
