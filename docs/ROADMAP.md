# AT-EX 프로젝트 실행 로드맵 (ROADMAP)

## 1. 문서 개요

이 문서는 AT-EX 프로젝트(Python + Selenium + pytest 기반 웹 UI 자동화 테스트 프레임워크, 대상 사이트: [Automation Exercise](https://automationexercise.com/))의 **실행 계획서**입니다. `docs/prd/` 하위 PRD 문서에 이미 확정된 요구사항을 재정의하지 않으며, "지금 무엇을 해야 하는가"와 "그 작업의 완료 기준"에만 집중합니다. 개발팀은 이 문서를 매일 열어보며 진행 상황(착수/완료/블록)을 체크리스트로 관리합니다.

### 기준 문서 및 버전
| 문서 | 버전 |
|------|------|
| `docs/prd/project-prd.md` | v1.2 |
| `docs/prd/features/signup.md` | v1.4 |
| `docs/prd/features/login.md` | v1.4 |
| `docs/prd/features/logout.md` | v1.4 |
| `docs/prd/features/product_search.md` | v1.6 |
| `docs/prd/features/shopping_cart.md` | v1.4 |
| `CLAUDE.md` | v1.0 (프로젝트 공통 개발 규칙) |

### 작성/갱신 이력
- **작성일**: 2026-07-24
- **최종 갱신일**: 2026-07-24
- **상태**: roadmap-writer 에이전트 규칙 갱신(Phase 1/2 DoD에 Playwright MCP 보조 검증 항목 추가)에 따라 구조 일부 갱신. 현재 저장소에는 `pages/`, `tests/`, `conftest.py` 등 실제 코드가 아직 존재하지 않으므로, 모든 Phase의 진행률은 0%(⬜ 예정)에서 유지됩니다.

---

## 2. 마일스톤 요약

| Phase | 목표 | 상태 | 진행률 | 예상 기간(PRD 근거) | 완료 조건 요약 |
|-------|------|------|--------|------|----------------|
| Phase 0 | 프로젝트 기반 설정 (디렉터리/설정/공통 유틸) | ⬜ 예정 | 0% | 미정(선행 작업, project-prd.md §13.2, §21.1 근거) | 디렉터리 구조, conftest.py, base_page.py, requirements.txt 등 기본 골격 구축 |
| Phase 1 | 기본 사용자 인증 및 탐색 (회원가입/로그인/로그아웃/상품검색) | ⬜ 예정 | 0% | 1주 (project-prd.md §8.1) | 4개 기능 Page Object + 테스트 케이스 작성, 전체 테스트 PASS |
| Phase 2 | 장바구니 및 결제 진입 제약 확인 | ⬜ 예정 | 0% | 1주 (project-prd.md §8.2) | 장바구니 Page Object + 테스트 케이스 작성, 전체 테스트 PASS |
| Phase 3 | 검증 및 안정성 강화 (예외/경계값 확장 검토, 크로스브라우저, CI/CD 최종화) | ⬜ 예정 | 0% | 1주 (project-prd.md §8.3) | 확장 검토 완료, Firefox 테스트 구성, CI/CD 파이프라인 최종 점검 |

상태 범례: `⬜ 예정 / 🟨 진행중 / ✅ 완료 / 🟥 블록됨`

---

## 3. Phase별 실행 Task

### Phase 0: 프로젝트 기반 설정

**목표**: Phase 1 이후 모든 기능 자동화 작업의 전제가 되는 공통 인프라를 구축합니다.
**관련 문서**: `CLAUDE.md` §3(디렉터리 구조), §7.3(BasePage Wait 메서드), §9(Fixture), §14(스크린샷), §21.1(추후 작업 목록) / `docs/prd/project-prd.md` §13.2(코드 구조), §11.3(CI/CD)

- [ ] 디렉터리 구조 생성: `pages/`, `tests/`, `utils/`, `config/`, `test_data/`, `screenshots/`, `reports/` (CLAUDE.md §3)
- [ ] `requirements.txt` 작성: selenium, pytest, pytest-html, python-dotenv 등 (CLAUDE.md §2)
- [ ] `pytest.ini` 작성 (기본 옵션, 마커 등)
- [ ] `.env.example` 및 `.gitignore` 작성: `.env`, `screenshots/`, `reports/` 등 git 미추적 대상 정리 (CLAUDE.md §12.3, project-prd.md §12.4)
- [ ] `conftest.py` 작성: `driver` fixture (scope="function", yield 패턴으로 종료 시 `driver.quit()`) (CLAUDE.md §9)
- [ ] `pages/base_page.py` 구현: 공통 요소 조작 메서드(`find_element`, `click` 등) + 공통 Wait 메서드(`find_element_visible`, `click_when_clickable`, `wait_for_element_presence`, `wait_for_text`) (CLAUDE.md §7.3, §18.1)
- [ ] `utils/logger.py` 구현: Python `logging` 모듈 기반 로거, 로그 포맷 `[시간] [레벨] [모듈명] [메시지]`, `logs/` 디렉터리 저장 (CLAUDE.md §13)
- [ ] `utils/helpers.py` 골격 작성 (화면과 무관한 공통 로직 배치 위치 확보, CLAUDE.md §18.2)
- [ ] 테스트 실패 시 자동 스크린샷 저장 hook 구현: `pytest_runtest_makereport` 사용, 파일명 규칙 `{테스트_함수명}_{상태}_{타임스탬프}.png` (CLAUDE.md §14)
- [ ] `.github/workflows/test.yml` 초안 작성: 커밋 시 pytest 실행 + `reports/` 아티팩트 업로드 (project-prd.md §11.3, §13.4) — 최종 점검은 Phase 3에서 수행
- [ ] `test_data/accounts.json` 골격 생성 (회원가입/로그인/로그아웃 공용 계정 데이터 스키마만 우선 정의, 실제 값은 각 기능 Task에서 채움)

**참고**: 이 Phase의 Task들은 PRD상 별도 Phase로 명시되어 있지 않으나, CLAUDE.md §21.1 "추후 작업" 목록과 project-prd.md §13.2의 코드 구조를 근거로 실행 단위를 구체화한 것입니다. Phase 1 착수 전에 최소한 `conftest.py`의 `driver` fixture와 `base_page.py`의 Wait 메서드는 준비되어 있어야 합니다.

---

### Phase 1: 기본 사용자 인증 및 탐색

**목표**: 사용자 가입부터 상품 검색까지의 기본 흐름 자동화 (project-prd.md §8.1)
**선행 조건**: Phase 0의 `driver` fixture, `base_page.py` Wait 메서드 준비 완료

#### 1-A. 회원가입 (Signup)
**관련 PRD**: `docs/prd/features/signup.md` v1.4 (NOR-001, NOR-002 / SIGNUP-REQ-001~013)

- [ ] `pages/login_page.py`에 `/login` 페이지 "New User Signup!" 영역 메서드 추가: `enter_signup_name()`, `enter_signup_email()`, `click_signup_button()` (signup.md §17 권장 — 이 메서드들은 로그인 기능 PRD의 LoginPage 설계에 포함시키는 것을 signup.md가 명시적으로 권장함)
- [ ] `pages/signup_page.py` 구현: Name(조회+수정), Email(조회 전용, dim 처리), Title/Password/Date of Birth/뉴스레터 체크박스, ADDRESS INFORMATION(First name~Mobile Number), `click_create_account_button()` (signup.md §17, SIGNUP-REQ-003~006)
- [ ] `pages/account_created_page.py` 구현: `is_account_created_message_displayed()`, `click_continue_button()` (SIGNUP-REQ-007~008)
- [ ] `test_data/accounts.json`에 회원가입 테스트 데이터 반영: 정상 가입용(John Doe), 재로그인 검증용(Jane Doe), Country 기본값(India) 사용 케이스(Alex Kim) 3종 (signup.md §15)
- [ ] `tests/test_signup.py` 작성: NOR-001(유효 정보로 `/login`→`/signup`→`/account_created` 전체 흐름 회원가입 성공), NOR-002(가입 직후 로그아웃 → 동일 계정 재로그인 성공) (signup.md §12)
- [ ] **블로커**: `/login`, `/signup`, `/account_created` 각 UI 요소의 실제 id/name/data-* 속성 공유 필요 — Page Object 구현 착수 시 사용자가 실시간 공유 예정 (signup.md §18)

#### 1-B. 로그인 (Login)
**선행**: 1-A 회원가입 완료 (계정 생성 필요) 및 로그인 테스트 계정 사전 생성
**관련 PRD**: `docs/prd/features/login.md` v1.4 (NOR-001~002, ABN-001~002 / LOGIN-REQ-001~008)

- [ ] `pages/login_page.py`에 로그인 폼 메서드 추가: `enter_email()`, `enter_password()`, `click_login_button()`, `is_error_message_displayed()`, `get_error_message_text()`, `is_on_login_page()` (LOGIN-REQ-001~004)
- [ ] `pages/home_page.py`(헤더 공통 영역) 구현: `is_logout_link_displayed()`, `is_signup_login_link_displayed()`, `is_delete_account_link_displayed()`, `get_logged_in_username()` (LOGIN-REQ-003, 007, 008 — "Logged in as {username}"는 회원가입 시 입력한 Name 값과 일치해야 함에 유의, login.md §16)
- [ ] `test_data/accounts.json`에 로그인 테스트 계정(사전 생성 방식 확정, login.md §17) 반영: 정상 로그인용, 재로그인용, 비정상 테스트용(미존재 이메일)
- [ ] `tests/test_login.py` 작성: NOR-001(유효 자격증명 로그인 성공, "Logged in as {username}"이 회원가입 Name 값과 일치하는지 검증), NOR-002(로그아웃 후 재로그인), ABN-001(잘못된 비밀번호), ABN-002(존재하지 않는 이메일) (login.md §13~14)
- [ ] **블로커**: 로그인 테스트 계정(이메일/비밀번호/Name)을 실제로 사전 생성해두는 작업 필요 — 테스트 실행 전 준비 필수 (login.md §17, §22, 사전 생성 방식 확정)
- [ ] **블로커**: 로그인 폼 및 헤더 네비게이션 요소의 실제 Locator 공유 필요 (login.md §20)

#### 1-C. 로그아웃 (Logout)
**선행**: 1-B 로그인 완료 (HomePage, LoginPage 재사용)
**관련 PRD**: `docs/prd/features/logout.md` v1.4 (NOR-001~002 / LOGOUT-REQ-001~005)

- [ ] `pages/home_page.py`에 `click_logout_link()` 추가 (1-B의 `is_logout_link_displayed()` 재사용)
- [ ] `pages/login_page.py`에 로그아웃 이후 상태 조회 메서드 추가: `is_signup_login_link_displayed()`(1-B와 공유), `is_delete_account_link_displayed()`, `is_logged_in_username_displayed()` (LOGOUT-REQ-003)
- [ ] `conftest.py`에 `logged_in_user` fixture 추가: 로그인을 사전 수행한 상태를 반환 (login.md/logout.md 공용, logout.md §19 권장)
- [ ] `tests/test_logout.py` 작성: NOR-001(정상 로그아웃 → 로그인 페이지 리다이렉트, "Logout"/"Delete Account"/"Logged in as {username}" 미노출 확인), NOR-002(로그아웃 후 동일 계정 재로그인 성공) (logout.md §13)
- [ ] **참고(자동화 대상 아님)**: 로그아웃 후 브라우저 뒤로가기(구 ABN-001)와 비로그인 상태 `/logout` URL 직접 접근(구 ABN-002)은 스코프 결정에 따라 자동화 대상에서 완전히 제외되었으므로 별도 테스트 코드를 작성하지 않음 (logout.md §12, §14)

#### 1-D. 상품 검색 (Product Search)
**선행 없음(독립)**: 로그인 여부와 무관하게 이용 가능하도록 확인됨 (product_search.md §18). 단, Phase 1 실행 순서상 인증 3종 이후 착수
**관련 PRD**: `docs/prd/features/product_search.md` v1.6 (NOR-001~003, ABN-001 / SEARCH-REQ-001~010)

- [ ] `pages/products_page.py` 구현: `navigate_to_products()`, `enter_search_keyword()`, `click_search_button()`, `get_product_count()`, `get_product_names()`, `is_on_products_page()` (product_search.md §19, SEARCH-REQ-001~010)
- [ ] `test_data/search_keywords.json` 작성: 유효 키워드(`Blue`, `Top`, `Tshirt`, `Dress`, `Kids`), 무효 키워드(`mondaykiz`, `testkeyword`, `qwer`, `asdf`), 대소문자 검증용(`TOP`) (product_search.md §17)
- [ ] `tests/test_product_search.py` 작성: NOR-001(유효 키워드 검색), NOR-002(검색어 없이 전체 목록 조회, 정확히 34개 확인 — 사이트 데이터 변경 시 기대값 갱신 필요), NOR-003(대소문자 무시 검증), ABN-001(존재하지 않는 키워드, 빈 화면 확인) (product_search.md §13~14)
- [ ] **블로커**: 검색 입력란, Search 버튼, 상품 카드 등 실제 Locator 공유 필요 (product_search.md §20)

**Phase 1 산출물**: `pages/login_page.py`, `pages/signup_page.py`, `pages/account_created_page.py`, `pages/home_page.py`, `pages/products_page.py`, `tests/test_signup.py`, `tests/test_login.py`, `tests/test_logout.py`, `tests/test_product_search.py`

---

### Phase 2: 장바구니 및 결제 진입 제약 확인

**목표**: 장바구니 기능 자동화 (project-prd.md §8.2)
**선행 조건**: Phase 1의 `pages/products_page.py` 존재 (1-D에서 이미 구현됨 — 이 Phase에서는 장바구니 담기 관련 메서드로 확장)
**관련 PRD**: `docs/prd/features/shopping_cart.md` v1.4 (NOR-001~005, ABN-001~002 / CART-REQ-001~010)

- [ ] `pages/products_page.py` 확장: `add_product_to_cart_by_name()`, `open_product_detail()`, `enter_quantity()`(상품 상세 페이지 전용, 목록 페이지에는 수량 입력 UI 없음), `click_add_to_cart_button()`, `click_view_cart_in_success_modal()`, `click_continue_shopping_in_success_modal()` (shopping_cart.md §19, CART-REQ-001~002)
- [ ] `pages/cart_page.py` 신규 구현: `navigate_to_cart()`, `is_product_in_cart()`, `get_cart_row_count_for_product()`, `get_product_price()`, `get_product_quantity()`, `get_product_total()`, `delete_product()`, `is_empty_cart_message_displayed()`, `is_proceed_to_checkout_button_displayed()`, `click_proceed_to_checkout()`, `is_login_modal_displayed()` (shopping_cart.md §19, CART-REQ-003~010)
- [ ] `test_data/products.json`(장바구니 전용)에 테스트 상품 데이터 반영: Men Tshirt(Rs. 400), Printed Off Shoulder Top - White(Rs. 315) (shopping_cart.md §17)
- [ ] `tests/test_shopping_cart.py` 작성:
  - [ ] NOR-001 (상품 목록 페이지에서 장바구니 추가, 항상 1개만 담김)
  - [ ] NOR-002 (상품 상세 페이지에서 수량 지정 후 장바구니 추가)
  - [ ] NOR-003 (장바구니에서 상품 삭제, 페이지 리로드 없이 즉시 반영 확인)
  - [ ] NOR-004 (동일 상품 중복 담기 시 기존 행 수량 증가 확인)
  - [ ] NOR-005 / ABN-001 (비로그인 상태에서 "Proceed To Checkout" 클릭 시 로그인 안내 모달 노출 확인, URL이 `/view_cart`로 유지되는지 확인 — 두 시나리오는 동일 사실을 다루므로 중복 구현하지 않고 하나로 통합 구현 권장, shopping_cart.md §13 NOR-005 비고)
  - [ ] ABN-002 (빈 장바구니 상태에서 안내 문구 확인, "Proceed To Checkout" 버튼 미노출 확인)
- [ ] **블로커**: "Add to cart" 버튼, "View Product" 버튼, 삭제(X) 아이콘, 담기 성공 모달, 로그인 모달 등 실제 Locator 공유 필요 (shopping_cart.md §20)

**Phase 2 산출물**: `pages/products_page.py`(확장), `pages/cart_page.py`, `tests/test_shopping_cart.py`

---

### Phase 3: 검증 및 안정성 강화

**목표**: 예외/경계값 시나리오 확장 검토, 크로스 브라우저 지원, CI/CD 파이프라인 최종화 (project-prd.md §8.3)
**선행 조건**: Phase 1, Phase 2의 모든 정상/비정상 시나리오 테스트 PASS

- [ ] (검토) 회원가입 실패/유효성 검증 케이스(중복 이메일, 필수 필드 누락 등) 자동화 확장 여부 논의 — 현재 자동화 범위에서 명시적으로 제외됨 (signup.md §11, §20)
- [ ] (검토) 로그인 필수 필드 공란 시나리오, 경계값(비밀번호 길이 등) 자동화 확장 여부 논의 — 현재 자동화 범위에서 명시적으로 제외됨 (login.md §12, §22)
- [ ] (검토, 블로커 해소 후 착수) 로그아웃 세션 만료 관련 시나리오 자동화 검토 — **세션 타임아웃 시간이 프로젝트 전체 차원에서 아직 미확정**이므로 확정 전까지는 착수 불가 (logout.md §12, §22, project-prd.md §19.1)
- [ ] (검토) 상품 검색 카테고리/브랜드 필터링, 정렬 기능 자동화 확장 여부 논의 — 현재 자동화 범위에서 명시적으로 제외됨 (product_search.md §12)
- [ ] (검토) 장바구니 최대 담기 개수 제한, 데이터 저장 방식(세션/쿠키/DB) 검증 여부 재논의 — 사용자 판단으로 현재 자동화 범위에서 제외됨 (shopping_cart.md §12, §20)
- [ ] Firefox WebDriver 추가 및 Phase 1~2 정상 시나리오 대상 크로스 브라우저 테스트 구성 (project-prd.md §8.3, §11.2, §18.2)
- [ ] `.github/workflows/test.yml` 최종 점검: 실패 시 알림, HTML 리포트 아티팩트 저장, 매 커밋 자동 실행 안정성 확인 (project-prd.md §11.3, §13.4)
- [ ] 성능 테스트 요구사항 정의 문서화 (실제 성능 테스트 구현은 범위 밖 유지, project-prd.md §8.3, §6.1)

**Phase 3 산출물**: 확장 시나리오 반영된 기능별 PRD 업데이트(필요 시 automation-prd-writer에 요청), Firefox 테스트 구성, 최종 CI/CD 워크플로우

---

## 4. 기능 의존성 개요

| 선행 기능 | 후행 기능 | 의존 내용 |
|-----------|-----------|-----------|
| 회원가입 (Signup) | 로그인 (Login) | 로그인 전에 계정이 먼저 생성되어야 함. 특히 로그인 성공 후 헤더에 노출되는 "Logged in as {username}"의 검증값은 **회원가입 시 입력한 Name 필드 값**과 정확히 일치해야 함 (login.md §18, signup.md §16) |
| 로그인 (Login) | 로그아웃 (Logout) | 로그인 상태여야 헤더에 "Logout" 링크가 노출되며, 로그아웃 시나리오 자체가 로그인 상태를 전제로 함 (logout.md §18) |
| 로그인 (Login) | 로그아웃 (Logout), 재사용 | `pages/home_page.py`(헤더 공통 컴포넌트)와 `pages/login_page.py`는 로그인·로그아웃 기능이 공동으로 소유/재사용함 (logout.md §19 권장) |
| 상품 검색 (Product Search) | 없음 (독립) | 로그인 여부와 무관하게 이용 가능함이 확인됨 (product_search.md §18) — Phase 1 내 실행 순서는 편의상 인증 3종 이후로 배치 |
| 상품 검색/목록 조회 (Product Search) | 장바구니 (Shopping Cart) | 장바구니에 담을 상품을 먼저 찾아야 함. `pages/products_page.py`는 Phase 1(검색)에서 먼저 구현된 후 Phase 2(장바구니)에서 담기 메서드로 확장됨 (shopping_cart.md §18) |
| 장바구니 (Shopping Cart) | 결제(Checkout, MVP 범위 밖) | 비로그인 상태에서 "Proceed to Checkout" 클릭 시에만 로그인이 요구됨(로그인 모달 노출까지만 Phase 2 범위). 결제 프로세스 자체는 MVP 제외 범위 (shopping_cart.md §3, §12) |

---

## 5. 현재 블로커 / 확인 필요 항목 트래킹

| 항목 | 막고 있는 Task | 확인/해소 주체 및 시점 |
|------|----------------|------------------------|
| 전 기능 공통 UI 요소의 실제 id/name/data-* 속성 미공유 | Phase 1, 2의 모든 Page Object 구현 Task | 사용자가 각 Page Object 구현 착수 시점에 실시간 공유 예정 (signup.md §18, login.md §20, logout.md §20, product_search.md §20, shopping_cart.md §20) |
| 로그인 테스트 계정(이메일/비밀번호/Name) 사전 생성 필요 | 1-B 로그인, 1-C 로그아웃 테스트 실행 | 테스트 실행 전 준비 필요 (login.md §17, §22 — 준비 방식은 "사전 생성"으로 이미 확정됨, 실제 계정 생성 작업만 남음) |
| 세션 타임아웃 시간 미확정 | Phase 3 "로그아웃 세션 만료 시나리오" 검토 Task | 프로젝트 전체 차원의 확인 필요 사항 (project-prd.md §19.1, logout.md §20). 확정되기 전까지 해당 Task는 착수하지 않음 |
| `shopping_cart.md` §22 "project-prd.md 정합성 검토(사용자 승인 필요)" 항목 | 로드맵 진행에는 직접 영향 없음 (참고) | `project-prd.md`는 이미 v1.2에서 "장바구니 수량 변경" 서술을 "장바구니 상품 삭제"로 수정하여 `shopping_cart.md` v1.4와 동기화된 것으로 확인됨(§5.1, §8.2). 다만 `shopping_cart.md` 자체의 "다음 단계" 섹션에는 아직 미해결 항목으로 남아 있어, feature PRD 담당(automation-prd-writer)이 해당 문서의 해당 항목을 정리하는 것을 권장함 |
| 로그인 상태에서 "Proceed to Checkout" 클릭 시 결제 페이지의 상세 동작 | 결제(Checkout) 기능 PRD 착수 (MVP 범위 밖) | MVP 이후 별도 checkout PRD 작성 시점에 확인 (shopping_cart.md §20, §22) |

---

## 6. Definition of Done (Phase별 완료 조건)

### Phase 0 완료 조건
- [ ] `pages/`, `tests/`, `utils/`, `config/`, `test_data/`, `screenshots/`, `reports/` 디렉터리 존재
- [ ] `conftest.py`의 `driver` fixture가 정상 동작 (브라우저 실행/종료 확인)
- [ ] `base_page.py`의 4개 공통 Wait 메서드(`find_element_visible`, `click_when_clickable`, `wait_for_element_presence`, `wait_for_text`) 구현 및 단순 호출 테스트로 동작 확인
- [ ] `requirements.txt` 기준으로 `pip install -r requirements.txt` 정상 완료
- [ ] `.env`, `screenshots/`, `reports/` 등이 `.gitignore`에 등록되어 git 미추적 확인

### Phase 1 완료 조건
- [ ] signup, login, logout, product_search 4개 기능 PRD의 자동화 대상 정상/비정상 시나리오(NOR-001~002, NOR-001~002/ABN-001~002, NOR-001~002, NOR-001~003/ABN-001) 100% 테스트 케이스화
- [ ] 각 Page Object(SignupPage, LoginPage, HomePage, ProductsPage 등) 구현 직후 Playwright MCP로 주요 화면/시나리오의 실제 동작을 확인 (pytest 실행 전 보조 검증, pytest를 대체하지 않음)
- [ ] `pytest tests/test_signup.py tests/test_login.py tests/test_logout.py tests/test_product_search.py` 전체 PASS (실패율 0%, pytest 기준)
- [ ] 로그인 테스트 계정이 사전 생성되어 있고, 회원가입 시 입력한 Name 값과 로그인 후 "Logged in as {username}"이 일치함을 확인
- [ ] 테스트 실패 시 `screenshots/`에 스크린샷 자동 저장 확인
- [ ] `pytest-html` 리포트(`reports/report.html`) 생성 확인

### Phase 2 완료 조건
- [ ] shopping_cart.md의 자동화 대상 정상/비정상 시나리오(NOR-001~005, ABN-001~002) 100% 테스트 케이스화
- [ ] `pages/products_page.py`(확장 메서드)와 신규 `pages/cart_page.py` 구현 직후 Playwright MCP로 담기/삭제/결제 진입 등 주요 시나리오의 실제 동작을 확인 (pytest 실행 전 보조 검증, pytest를 대체하지 않음)
- [ ] `pytest tests/test_shopping_cart.py` PASS, Phase 1 테스트와 함께 실행 시에도 누적 성공률 100% (pytest 기준)
- [ ] `pages/products_page.py`와 `pages/cart_page.py` 간 책임 분리가 shopping_cart.md §19 기준과 일치 (담기 진입은 ProductsPage, 조회/삭제/결제진입은 CartPage)

### Phase 3 완료 조건
- [ ] Phase 3 "검토" Task 6건에 대한 착수 여부 결정 및 결과 문서화(착수하지 않기로 한 경우 사유 기록)
- [ ] Firefox 브라우저로 Phase 1~2 정상 시나리오 재실행 PASS
- [ ] `.github/workflows/test.yml`이 매 커밋마다 정상 실행되고 리포트 아티팩트가 저장됨을 확인
- [ ] 프로젝트 전체 성공 기준(project-prd.md §14) 충족 여부 최종 점검

---

## 7. 다음 액션 (Next Actions)

우선순위 순으로 착수를 권장하는 Task입니다.

1. **Phase 0 기반 설정 완료**: 디렉터리 구조, `requirements.txt`, `conftest.py`(`driver` fixture), `base_page.py`(공통 Wait 메서드) — 이후 모든 작업의 전제 조건
2. **로그인 테스트 계정 사전 생성**: login.md에서 이미 "사전 생성" 방식으로 확정되어 있으므로, 실제 이메일/비밀번호/Name 값을 가진 계정을 준비 (1-B, 1-C 착수 전 필요)
3. **1-A 회원가입 Page Object 및 테스트 착수**: `/login`, `/signup`, `/account_created` 실제 Locator 공유받아 `SignupPage`, `AccountCreatedPage` 구현 후 `test_signup.py`(NOR-001, NOR-002) 작성 및 실행
4. **1-B 로그인 Page Object 및 테스트 착수**: 회원가입에서 생성한 계정 기준으로 `LoginPage`, `HomePage` 구현 후 `test_login.py`(NOR-001~002, ABN-001~002) 작성 및 실행
5. **1-C, 1-D 순차 진행**: 로그아웃(`test_logout.py`)과 상품 검색(`test_product_search.py`)을 이어서 진행하여 Phase 1 완료

---

## 8. 변경 이력

- **v1.0 (2026-07-24)**: 최초 작성. `docs/prd/project-prd.md`(v1.2)의 Phase 1/2/3 구조를 뼈대로 하여, `signup.md`(v1.4), `login.md`(v1.4), `logout.md`(v1.4), `product_search.md`(v1.6), `shopping_cart.md`(v1.4)에 명시된 정상/비정상 시나리오 ID(NOR-xxx/ABN-xxx), 자동화 제외 범위, 확인 완료/확인 필요 항목, 기능 간 의존성을 실행 Task로 변환. Phase 0(프로젝트 기반 설정)을 신설하여 CLAUDE.md §21.1의 미생성 인프라 항목을 선행 작업으로 명시. 현재 저장소에 실제 코드가 없어 모든 Phase 진행률은 0%에서 시작.
- **v1.1 (2026-07-24)**: roadmap-writer 서브에이전트 정의(`.claude/agents/dev/roadmap-writer.md`)에 추가된 규칙("구현 Task가 포함된 Phase의 DoD에는 Playwright MCP 실동작 확인 항목을 pytest PASS 항목과 별도 체크박스로 포함")을 반영. Page Object 구현 Task가 포함된 Phase 1, Phase 2의 완료 조건에 "구현 직후 Playwright MCP로 주요 화면/시나리오의 실제 동작을 확인 (pytest 실행 전 보조 검증, pytest를 대체하지 않음)" 항목을 추가. 인프라 설정 위주인 Phase 0과 검토/크로스브라우저/CI 위주인 Phase 3에는 해당 항목을 추가하지 않음. Task 목록(섹션 3)과 기존 진행 상태(체크박스)는 변경하지 않음.

---

이 문서는 진행 상황이 바뀔 때(착수/완료/블록)마다 갱신됩니다. 요구사항 자체의 변경이 필요한 경우 이 문서가 아니라 `docs/prd/` 하위 PRD 문서를 automation-prd-writer 서브에이전트를 통해 수정해야 합니다.
