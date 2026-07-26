from pages.cart_page import CartPage
from pages.products_page import ProductsPage


def test_add_product_to_cart_from_products_page(driver, cart_test_product):
  products_page = ProductsPage(driver)
  products_page.navigate_to_products()
  products_page.add_product_to_cart_by_name(cart_test_product["name"])
  products_page.click_view_cart_in_success_modal()

  cart_page = CartPage(driver)
  assert cart_page.is_product_in_cart(cart_test_product["name"]), (
    f"{cart_test_product['name']}이 장바구니에 담겨 있어야 한다"
  )

  quantity = cart_page.get_product_quantity(cart_test_product["name"])
  assert quantity == 1, (
    f"상품 목록 페이지에는 수량 입력 UI가 없어 항상 1개만 담겨야 하나 {quantity}개가 담겼다"
  )

  price = cart_page.get_product_price(cart_test_product["name"])
  assert price == cart_test_product["expected_price"], (
    f"가격은 {cart_test_product['expected_price']}이어야 하나 {price}이다"
  )

  total = cart_page.get_product_total(cart_test_product["name"])
  assert total == price * quantity, (
    f"Total은 Price*Quantity({price * quantity})와 같아야 하나 {total}이다"
  )


def test_add_product_to_cart_from_detail_page_with_quantity(driver, cart_test_product):
  quantity_to_add = 3
  products_page = ProductsPage(driver)
  products_page.navigate_to_products()
  products_page.open_product_detail(cart_test_product["name"])
  products_page.enter_quantity(quantity_to_add)
  products_page.click_add_to_cart_button()
  products_page.click_view_cart_in_success_modal()

  cart_page = CartPage(driver)
  assert cart_page.is_product_in_cart(cart_test_product["name"]), (
    f"{cart_test_product['name']}이 장바구니에 담겨 있어야 한다"
  )

  quantity = cart_page.get_product_quantity(cart_test_product["name"])
  assert quantity == quantity_to_add, (
    f"상세 페이지에서 지정한 수량 {quantity_to_add}이 반영되어야 하나 {quantity}이다"
  )


def test_delete_product_from_cart(driver, cart_test_product):
  products_page = ProductsPage(driver)
  products_page.navigate_to_products()
  products_page.add_product_to_cart_by_name(cart_test_product["name"])
  products_page.click_view_cart_in_success_modal()

  cart_page = CartPage(driver)
  assert cart_page.is_product_in_cart(cart_test_product["name"]), (
    "삭제 시도 전에는 상품이 장바구니에 있어야 한다"
  )

  cart_page.delete_product(cart_test_product["name"])
  assert not cart_page.is_product_in_cart(cart_test_product["name"]), (
    "삭제 후에는 해당 상품이 장바구니 목록에서 사라져야 한다"
  )


def test_duplicate_add_increases_quantity(driver, cart_test_product):
  products_page = ProductsPage(driver)
  products_page.navigate_to_products()
  products_page.add_product_to_cart_by_name(cart_test_product["name"])
  products_page.navigate_to_products()
  products_page.add_product_to_cart_by_name(cart_test_product["name"])
  products_page.click_view_cart_in_success_modal()

  cart_page = CartPage(driver)
  row_count = cart_page.get_cart_row_count_for_product(cart_test_product["name"])
  assert row_count == 1, f"동일 상품을 중복으로 담아도 행은 1개여야 하나 {row_count}개다"

  quantity = cart_page.get_product_quantity(cart_test_product["name"])
  assert quantity == 2, f"중복 담기 2회 후 수량은 2여야 하나 {quantity}이다"


def test_guest_checkout_shows_login_modal(driver, cart_test_product):
  products_page = ProductsPage(driver)
  products_page.navigate_to_products()
  products_page.add_product_to_cart_by_name(cart_test_product["name"])
  products_page.click_view_cart_in_success_modal()

  cart_page = CartPage(driver)
  cart_page.click_proceed_to_checkout()

  assert cart_page.is_login_modal_displayed(), (
    "비로그인 상태에서 Proceed To Checkout 클릭 시 로그인 안내 모달이 노출되어야 한다"
  )
  assert "/view_cart" in driver.current_url, (
    f"로그인 모달 노출 후에도 URL은 /view_cart로 유지되어야 하나 {driver.current_url}이다"
  )


def test_empty_cart_shows_message(driver):
  cart_page = CartPage(driver)
  cart_page.navigate_to_cart()

  assert cart_page.is_empty_cart_message_displayed(), (
    "상품을 담지 않은 상태에서는 빈 장바구니 안내 문구가 표시되어야 한다"
  )
  assert not cart_page.is_proceed_to_checkout_button_displayed(), (
    "빈 장바구니 상태에서는 Proceed To Checkout 버튼이 노출되지 않아야 한다"
  )
