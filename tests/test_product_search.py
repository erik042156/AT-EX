from pages.products_page import ProductsPage

# NOR-002의 34는 product_search.md 확정 시점 기준 전체 상품 개수이며, 사이트 데이터가
# 바뀌면 이 값도 함께 갱신해야 한다.
EXPECTED_TOTAL_PRODUCT_COUNT = 34


def test_search_with_valid_keyword(driver, valid_search_keyword):
  products_page = ProductsPage(driver)
  products_page.navigate_to_products()
  products_page.enter_search_keyword(valid_search_keyword)
  products_page.click_search_button()

  assert products_page.is_on_products_page(), "검색 후에도 /products 페이지에 머물러야 한다"
  assert products_page.get_product_count() > 0, (
    f"유효 키워드 '{valid_search_keyword}' 검색 시 1개 이상의 결과가 있어야 한다"
  )


def test_view_all_products_without_keyword(driver):
  products_page = ProductsPage(driver)
  products_page.navigate_to_products()

  product_count = products_page.get_product_count()
  assert product_count == EXPECTED_TOTAL_PRODUCT_COUNT, (
    f"검색어 없이 전체 목록 조회 시 정확히 {EXPECTED_TOTAL_PRODUCT_COUNT}개여야 하지만 "
    f"{product_count}개가 조회되었다"
  )


def test_search_case_insensitive(driver, case_insensitive_keywords):
  products_page = ProductsPage(driver)

  products_page.navigate_to_products()
  products_page.enter_search_keyword(case_insensitive_keywords["lowercase_mixed"])
  products_page.click_search_button()
  mixed_case_count = products_page.get_product_count()

  products_page.navigate_to_products()
  products_page.enter_search_keyword(case_insensitive_keywords["uppercase"])
  products_page.click_search_button()
  uppercase_count = products_page.get_product_count()

  assert mixed_case_count == uppercase_count, (
    f"'{case_insensitive_keywords['lowercase_mixed']}'와 "
    f"'{case_insensitive_keywords['uppercase']}' 검색 결과 개수가 대소문자와 무관하게 "
    f"동일해야 하지만 {mixed_case_count} != {uppercase_count} 이다"
  )
  assert mixed_case_count > 0, "대소문자 검증용 키워드는 1개 이상의 결과를 가져야 한다"


def test_search_with_nonexistent_keyword(driver, nonexistent_search_keyword):
  products_page = ProductsPage(driver)
  products_page.navigate_to_products()
  products_page.enter_search_keyword(nonexistent_search_keyword)
  products_page.click_search_button()

  product_count = products_page.get_product_count()
  assert product_count == 0, (
    f"존재하지 않는 키워드 '{nonexistent_search_keyword}' 검색 시 결과가 0개여야 하지만 "
    f"{product_count}개가 조회되었다"
  )
