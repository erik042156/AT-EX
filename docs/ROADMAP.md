# AT-EX 프로젝트 실행 로드맵 (ROADMAP)

## 1. 문서 개요

이 문서는 AT-EX 프로젝트(Python + Selenium + pytest 기반 웹 UI 자동화 테스트 프레임워크, 대상 사이트: [Automation Exercise](https://automationexercise.com/))의 **실행 계획서**입니다. `docs/prd/` 하위 PRD 문서에 이미 확정된 요구사항을 재정의하지 않으며, "지금 무엇을 해야 하는가"와 "그 작업의 완료 기준"에만 집중합니다. 개발팀은 이 문서를 매일 열어보며 진행 상황(착수/완료/블록)을 체크리스트로 관리합니다.

### 기준 문서 및 버전
| 문서 | 버전 |
|------|------|
| `docs/prd/project-prd.md` | v1.3 |
| `docs/prd/features/signup.md` | v1.4 |
| `docs/prd/features/login.md` | v1.4 |
| `docs/prd/features/logout.md` | v1.4 |
| `docs/prd/features/product_search.md` | v1.6 |
| `docs/prd/features/shopping_cart.md` | v1.4 |
| `CLAUDE.md` | v1.0 (프로젝트 공통 개발 규칙, §6 "Playwright MCP 기반 페이지 탐색 규칙" 포함) |
| `shrimp-rules.md` | 버전 미표기 (AI Agent 운영 규칙, §5 "Playwright MCP 기반 Locator 조사 절차" 포함) |

### 작성/갱신 이력
- **작성일**: 2026-07-24
- **최종 갱신일**: 2026-07-26
- **상태**: shrimp-task-manager MCP의 Task 실행 이력(T1~T19 completed)을 저장소 실제 파일 상태와 교차검증하여 진행 상태를 전면 재동기화(v1.3). Phase 0 전체와 Phase 1의 1-A/1-B/1-C가 실제로 구현·테스트 작성·PASS까지 완료되어 있음을 확인하고 체크박스·진행률·상태를 갱신했습니다. Phase 1의 1-D는 `pages/products_page.py` 구현까지만 완료되어 있어(v1.2에서 이미 확인) 아직 진행중이며, `test_data/search_keywords.json`과 `tests/test_product_search.py`는 저장소에 존재하지 않음을 확인했습니다. 이전 정책 변경(v1.2, Locator 확보 절차)에 대한 설명은 변경 이력 섹션 8을 참고하십시오. 이번 재동기화는 Phase 0/1(1-D 일부 제외)에 한정되며, Phase 2/3과 섹션 5 블로커 트래킹 표는 손대지 않았습니다.

---

## 2. 마일스톤 요약

| Phase | 목표 | 상태 | 진행률 | 예상 기간(PRD 근거) | 완료 조건 요약 |
|-------|------|------|--------|------|----------------|
| Phase 0 | 프로젝트 기반 설정 (디렉터리/설정/공통 유틸) | ✅ 완료 | 100% | 미정(선행 작업, project-prd.md §13.2, §21.1 근거) | 디렉터리 구조, conftest.py, base_page.py, requirements.txt 등 기본 골격 구축 |
| Phase 1 | 기본 사용자 인증 및 탐색 (회원가입/로그인/로그아웃/상품검색) | ✅ 완료 | 100% (1-A 회원가입/1-B 로그인/1-C 로그아웃/1-D 상품 검색 4개 기능 모두 구현·테스트 작성·PASS 완료, Phase 1 통합 검증(T22)까지 완료) | 1주 (project-prd.md §8.1) | 4개 기능 Page Object + 테스트 케이스 작성, 전체 테스트 PASS |
| Phase 2 | 장바구니 및 결제 진입 제약 확인 | ✅ 완료 | 100% | 1주 (project-prd.md §8.2) | 장바구니 Page Object + 테스트 케이스 작성, 전체 테스트 PASS |
| Phase 3 | 검증 및 안정성 강화 (예외/경계값 확장 검토, 크로스브라우저, CI/CD 최종화) | 🟨 진행중 | 약 70% (8개 항목 중 완료 5 / 부분완료 2 / 보류 1 — 아래 근거 참고) | 1주 (project-prd.md §8.3) | 확장 검토 완료, Firefox 테스트 구성, CI/CD 파이프라인 최종 점검 — **완료 아님**: shrimp-task-manager MCP로 6개 Task(Task1~6)를 순차 실행해 전부 `execute_task`→구현/조사→`verify_task`(80점 이상)로 completed 처리되었으나, 검증 과정에서 (1) GitHub Actions 실제 CI 실행(run_id 30201769656)에서 chrome/firefox 모두 대량 테스트 실패(각 16 failed/2 passed/2 errors, 로컬 Chrome 18 passed와 상반됨, 원인 미확정), (2) Firefox 로컬 100% 안정적 통과 미달성(geckodriver 인프라 불안정성으로 판명, CI 검증으로 이관), (3) 저장소 루트에 README.md 파일이 존재하지 않아 project-prd.md §14.4 미충족, (4) SLACK_WEBHOOK_URL 시크릿 미등록으로 Slack 실패 알림 미동작이라는 4건의 미해결 사항이 새로 확인되어 ✅ 완료로 표기하지 않음 (섹션 3·5·6 상세 참고) |

상태 범례: `⬜ 예정 / 🟨 진행중 / ✅ 완료 / 🟥 블록됨`

---

## 3. Phase별 실행 Task

### Phase 0: 프로젝트 기반 설정

**목표**: Phase 1 이후 모든 기능 자동화 작업의 전제가 되는 공통 인프라를 구축합니다.
**관련 문서**: `CLAUDE.md` §3(디렉터리 구조), §7.3(BasePage Wait 메서드), §9(Fixture), §14(스크린샷), §21.1(추후 작업 목록) / `docs/prd/project-prd.md` §13.2(코드 구조), §11.3(CI/CD)

- [x] 디렉터리 구조 생성: `pages/`, `tests/`, `utils/`, `config/`, `test_data/`, `screenshots/`, `reports/` (CLAUDE.md §3) — 구현 확인됨(2026-07-25)
- [x] `requirements.txt` 작성: selenium, pytest, pytest-html, python-dotenv 등 (CLAUDE.md §2) — 구현 확인됨
- [x] `pytest.ini` 작성 (기본 옵션, 마커 등) — 구현 확인됨(`smoke` 마커 포함)
- [x] `.env.example` 및 `.gitignore` 작성: `.env`, `screenshots/`, `reports/` 등 git 미추적 대상 정리 (CLAUDE.md §12.3, project-prd.md §12.4) — 구현 확인됨(`logs/`도 함께 정리됨)
- [x] `conftest.py` 작성: `driver` fixture (scope="function", yield 패턴으로 종료 시 `driver.quit()`) (CLAUDE.md §9) — 구현 확인됨
- [x] `pages/base_page.py` 구현: 공통 요소 조작 메서드(`find_element`, `click` 등) + 공통 Wait 메서드(`find_element_visible`, `click_when_clickable`, `wait_for_element_presence`, `wait_for_text`) (CLAUDE.md §7.3, §18.1) — 구현 확인됨
- [x] `utils/logger.py` 구현: Python `logging` 모듈 기반 로거, 로그 포맷 `[시간] [레벨] [모듈명] [메시지]`, `logs/` 디렉터리 저장 (CLAUDE.md §13) — 구현 확인됨
- [x] `utils/helpers.py` 골격 작성 (화면과 무관한 공통 로직 배치 위치 확보, CLAUDE.md §18.2) — 골격 파일 존재 확인됨(실제 헬퍼 함수는 필요 시점에 추가 예정)
- [x] 테스트 실패 시 자동 스크린샷 저장 hook 구현: `pytest_runtest_makereport` 사용, 파일명 규칙 `{테스트_함수명}_{상태}_{타임스탬프}.png` (CLAUDE.md §14) — `conftest.py`에 구현 확인됨
- [x] `.github/workflows/test.yml` 초안 작성: 커밋 시 pytest 실행 + `reports/` 아티팩트 업로드 (project-prd.md §11.3, §13.4) — 최종 점검은 Phase 3에서 수행 — 초안 구현 확인됨
- [x] `test_data/accounts.json` 골격 생성 (회원가입/로그인/로그아웃 공용 계정 데이터 스키마만 우선 정의, 실제 값은 각 기능 Task에서 채움) — 골격 생성 확인됨(이후 1-A/1-B에서 실제 값으로 채워짐)

**참고**: 이 Phase의 Task들은 PRD상 별도 Phase로 명시되어 있지 않으나, CLAUDE.md §21.1 "추후 작업" 목록과 project-prd.md §13.2의 코드 구조를 근거로 실행 단위를 구체화한 것입니다. Phase 1 착수 전에 최소한 `conftest.py`의 `driver` fixture와 `base_page.py`의 Wait 메서드는 준비되어 있어야 합니다.

---

### Phase 1: 기본 사용자 인증 및 탐색

**목표**: 사용자 가입부터 상품 검색까지의 기본 흐름 자동화 (project-prd.md §8.1)
**선행 조건**: Phase 0의 `driver` fixture, `base_page.py` Wait 메서드 준비 완료

#### 1-A. 회원가입 (Signup)
**관련 PRD**: `docs/prd/features/signup.md` v1.4 (NOR-001, NOR-002 / SIGNUP-REQ-001~013)

- [x] `pages/login_page.py`에 `/login` 페이지 "New User Signup!" 영역 메서드 추가: `enter_signup_name()`, `enter_signup_email()`, `click_signup_button()` (signup.md §17 권장 — 이 메서드들은 로그인 기능 PRD의 LoginPage 설계에 포함시키는 것을 signup.md가 명시적으로 권장함) — 구현 확인됨(2026-07-25)
- [x] `pages/signup_page.py` 구현: Name(조회+수정), Email(조회 전용, dim 처리), Title/Password/Date of Birth/뉴스레터 체크박스, ADDRESS INFORMATION(First name~Mobile Number), `click_create_account_button()` (signup.md §17, SIGNUP-REQ-003~006) — 구현 확인됨
- [x] `pages/account_created_page.py` 구현: `is_account_created_message_displayed()`, `click_continue_button()` (SIGNUP-REQ-007~008) — 구현 확인됨
- [x] `test_data/accounts.json`에 회원가입 테스트 데이터 반영: 정상 가입용(John Doe), 재로그인 검증용(Jane Doe), Country 기본값(India) 사용 케이스(Alex Kim) 3종 (signup.md §15) — 3종 데이터 반영 확인됨(`india_default_signup` 포함)
- [x] `tests/test_signup.py` 작성: NOR-001(유효 정보로 `/login`→`/signup`→`/account_created` 전체 흐름 회원가입 성공), NOR-002(가입 직후 로그아웃 → 동일 계정 재로그인 성공) (signup.md §12) — 작성 및 PASS 확인됨(`test_signup_with_valid_info`, `test_signup_then_logout_and_relogin`)
- [x] `/login`, `/signup`, `/account_created` 각 UI 요소의 Locator는 Playwright MCP(`browser_snapshot` 우선, 부족 시 `browser_evaluate`)로 실제 페이지를 직접 조사·검증한 뒤 확보 (CLAUDE.md §6, shrimp-rules.md §5) — 실제 Locator 미공유 자체는 더 이상 착수를 막는 블로커가 아님. MCP로 확인이 불가능한 사유(로그인 권한 없음, OTP·2FA·CAPTCHA, 다의적 해석 등, CLAUDE.md §6.4·shrimp-rules.md §5)가 있는 요소만 그 시점에 사용자 확인 요청 (signup.md §18) — 조사·확보 완료 확인됨(`data-qa` 속성 기반 Locator로 구현됨)
- [x] (계획 외 추가 산출물) `pages/delete_account_page.py` 신규 구현: `is_account_deleted_message_displayed()`, `click_continue_button()` — 회원가입 테스트가 생성한 계정을 테스트 내에서 정리(계정 삭제)하기 위해 `tests/test_signup.py` 작성 과정에서 추가로 구현됨 (CLAUDE.md §10.3 테스트 데이터 정리 원칙 근거, 원래 로드맵에는 계획되지 않았던 산출물)

#### 1-B. 로그인 (Login)
**선행**: 1-A 회원가입 완료 (계정 생성 필요) 및 로그인 테스트 계정 사전 생성
**관련 PRD**: `docs/prd/features/login.md` v1.4 (NOR-001~002, ABN-001~002 / LOGIN-REQ-001~008)

- [x] `pages/login_page.py`에 로그인 폼 메서드 추가: `enter_email()`, `enter_password()`, `click_login_button()`, `is_error_message_displayed()`, `get_error_message_text()`, `is_on_login_page()` (LOGIN-REQ-001~004) — 구현 확인됨
- [x] `pages/home_page.py`(헤더 공통 영역) 구현: `is_logout_link_displayed()`, `is_signup_login_link_displayed()`, `is_delete_account_link_displayed()`, `get_logged_in_username()` (LOGIN-REQ-003, 007, 008 — "Logged in as {username}"는 회원가입 시 입력한 Name 값과 일치해야 함에 유의, login.md §16) — 구현 확인됨
- [x] `test_data/accounts.json`에 로그인 테스트 계정(사전 생성 방식 확정, login.md §17) 반영: 정상 로그인용, 재로그인용, 비정상 테스트용(미존재 이메일) — `shared_login_accounts` 반영 확인됨
- [x] `tests/test_login.py` 작성: NOR-001(유효 자격증명 로그인 성공, "Logged in as {username}"이 회원가입 Name 값과 일치하는지 검증), NOR-002(로그아웃 후 재로그인), ABN-001(잘못된 비밀번호), ABN-002(존재하지 않는 이메일) (login.md §13~14) — 작성 및 PASS 확인됨(`test_login_with_valid_credentials`, `test_relogin_after_logout`, `test_login_with_invalid_password`, `test_login_with_nonexistent_email`)
- [ ] **블로커**: 로그인 테스트 계정(이메일/비밀번호/Name)을 실제로 사전 생성해두는 작업 필요 — 테스트 실행 전 준비 필수 (login.md §17, §22, 사전 생성 방식 확정)
- [x] 로그인 폼 및 헤더 네비게이션 요소의 Locator는 Playwright MCP로 직접 조사·검증한 뒤 확보 (CLAUDE.md §6, shrimp-rules.md §5) — 실제 Locator 미공유 자체는 더 이상 착수를 막는 블로커가 아님. MCP로 확인이 불가능한 사유(CLAUDE.md §6.4·shrimp-rules.md §5)가 있는 요소만 그 시점에 사용자 확인 요청 (login.md §20) — 조사·확보 완료 확인됨

#### 1-C. 로그아웃 (Logout)
**선행**: 1-B 로그인 완료 (HomePage, LoginPage 재사용)
**관련 PRD**: `docs/prd/features/logout.md` v1.4 (NOR-001~002 / LOGOUT-REQ-001~005)

- [x] `pages/home_page.py`에 `click_logout_link()` 추가 (1-B의 `is_logout_link_displayed()` 재사용) — 구현 확인됨
- [x] `pages/login_page.py`에 로그아웃 이후 상태 조회 메서드 추가: `is_signup_login_link_displayed()`(1-B와 공유), `is_delete_account_link_displayed()`, `is_logged_in_username_displayed()` (LOGOUT-REQ-003) — 구현 확인됨
- [x] `conftest.py`에 `logged_in_user` fixture 추가: 로그인을 사전 수행한 상태를 반환 (login.md/logout.md 공용, logout.md §19 권장) — 구현 확인됨
- [x] `tests/test_logout.py` 작성: NOR-001(정상 로그아웃 → 로그인 페이지 리다이렉트, "Logout"/"Delete Account"/"Logged in as {username}" 미노출 확인), NOR-002(로그아웃 후 동일 계정 재로그인 성공) (logout.md §13) — 작성 및 PASS 확인됨(`test_logout_from_logged_in_state`, `test_logout_then_relogin`). 이 시점에 `test_signup.py`/`test_login.py`의 NOR-002(로그아웃 의존 시나리오)도 함께 재실행하여 최종 PASS 재확인됨
- [ ] **참고(자동화 대상 아님)**: 로그아웃 후 브라우저 뒤로가기(구 ABN-001)와 비로그인 상태 `/logout` URL 직접 접근(구 ABN-002)은 스코프 결정에 따라 자동화 대상에서 완전히 제외되었으므로 별도 테스트 코드를 작성하지 않음 (logout.md §12, §14)

#### 1-D. 상품 검색 (Product Search)
**선행 없음(독립)**: 로그인 여부와 무관하게 이용 가능하도록 확인됨 (product_search.md §18). 단, Phase 1 실행 순서상 인증 3종 이후 착수
**관련 PRD**: `docs/prd/features/product_search.md` v1.6 (NOR-001~003, ABN-001 / SEARCH-REQ-001~010)

- [x] `pages/products_page.py` 구현: `navigate_to_products()`, `enter_search_keyword()`, `click_search_button()`, `get_product_count()`, `get_product_names()`, `is_on_products_page()` (product_search.md §19, SEARCH-REQ-001~010) — 사용자의 스크린샷 공유 없이 Playwright MCP `browser_evaluate`로 `/products` 페이지 DOM을 직접 조사해 `SEARCH_INPUT`, `SEARCH_BUTTON`, `PRODUCT_CARDS`, `PRODUCT_NAME` Locator를 확보하고 구현 완료를 확인함(2026-07-25). 이 사례가 CLAUDE.md §6·shrimp-rules.md §5 절차의 최초 실증 사례임
- [x] `test_data/search_keywords.json` 작성: 유효 키워드(`Blue`, `Top`, `Tshirt`, `Dress`, `Kids`), 무효 키워드(`mondaykiz`, `testkeyword`, `qwer`, `asdf`), 대소문자 검증용(`TOP`) (product_search.md §17) — T21에서 작성 완료 확인됨
- [x] `tests/test_product_search.py` 작성: NOR-001(유효 키워드 검색), NOR-002(검색어 없이 전체 목록 조회, 정확히 34개 확인 — 사이트 데이터 변경 시 기대값 갱신 필요), NOR-003(대소문자 무시 검증), ABN-001(존재하지 않는 키워드, 빈 화면 확인) (product_search.md §13~14) — T21에서 4개 테스트(`test_search_with_valid_keyword`, `test_view_all_products_without_keyword`, `test_search_case_insensitive`, `test_search_with_nonexistent_keyword`) 작성 및 PASS 확인됨, Phase 1 통합 실행(T22)에서도 재확인됨

**Phase 1 산출물**: `pages/login_page.py`, `pages/signup_page.py`, `pages/account_created_page.py`, `pages/home_page.py`, `pages/products_page.py`, `pages/delete_account_page.py`(계획 외 추가 산출물, 1-A 회원가입 테스트 계정 정리용), `tests/test_signup.py`, `tests/test_login.py`, `tests/test_logout.py`, `tests/test_product_search.py`(T21에서 작성 완료, T22 통합 실행에서 PASS 재확인됨)

---

### Phase 2: 장바구니 및 결제 진입 제약 확인

**목표**: 장바구니 기능 자동화 (project-prd.md §8.2)
**선행 조건**: Phase 1의 `pages/products_page.py` 존재 (1-D에서 이미 구현됨 — 이 Phase에서는 장바구니 담기 관련 메서드로 확장)
**관련 PRD**: `docs/prd/features/shopping_cart.md` v1.4 (NOR-001~005, ABN-001~002 / CART-REQ-001~010)

- [x] Playwright MCP로 `/products`, `/product_details/2`, `/view_cart` 3개 페이지를 실제 방문하여 장바구니 관련 UI Locator 조사·확정 (`browser_snapshot` 우선, 부족 시 `browser_evaluate`) — shrimp-task-manager Task1(95점) 완료 확인됨. 삭제(X 아이콘)와 "Proceed To Checkout" 버튼은 "되돌리기 어려운 동작"으로 분류되어 실클릭 전 AskUserQuestion으로 사용자 확인을 받았고(사용자가 "둘 다 허용" 응답), 실제 클릭으로 삭제 즉시 반영, 로그인 모달 노출 + URL(`/view_cart`) 유지, 빈 장바구니 안내 문구를 모두 확인함 (CLAUDE.md §6, shopping_cart.md §20)
- [x] `pages/base_page.py`에 `wait_for_element_invisible` 메서드 추가: 기존 4종 공통 Wait 메서드와 동일한 스타일로 구현 (shopping_cart.md §19 "재사용 가능한 메서드" 근거) — shrimp-task-manager Task2(100점) 완료 확인됨
- [x] `utils/helpers.py`에 가격 텍스트 파싱 함수 추가: `parse_price_text(price_text: str) -> int` 구현 (shopping_cart.md §19 `parse_price_text_to_number` 예시 근거) — shrimp-task-manager Task3(100점) 완료 확인됨. **(계획 외 추가 산출물)**: 실제 사이트의 광고 스크립트(`class="google-anno"`)가 상품명 텍스트에 여분의 공백을 삽입하는 문제를 Task5 실동작 검증 중 발견하여 `normalize_whitespace(text: str) -> str` 함수도 함께 추가됨
- [x] `pages/products_page.py` 확장: `add_product_to_cart_by_name()`, `open_product_detail()`, `enter_quantity()`(상품 상세 페이지 전용, 목록 페이지에는 수량 입력 UI 없음), `click_add_to_cart_button()`, `click_view_cart_in_success_modal()`, `click_continue_shopping_in_success_modal()` 6개 메서드와 비공개 헬퍼 `_find_card_by_product_name` 추가 (shopping_cart.md §19, CART-REQ-001~002) — shrimp-task-manager Task4(92점) 완료 확인됨. Phase 1에서 구현된 기존 요소(`SEARCH_INPUT`/`SEARCH_BUTTON`/`PRODUCT_CARDS`/`PRODUCT_NAME` 및 6개 메서드)는 변경 없이 유지됨. `pytest tests/test_product_search.py` 4개 테스트로 회귀 없음 재확인됨
- [x] `pages/cart_page.py` 신규 구현: `navigate_to_cart()`, `is_product_in_cart()`, `get_cart_row_count_for_product()`, `get_product_price()`, `get_product_quantity()`, `get_product_total()`, `delete_product()`, `is_empty_cart_message_displayed()`, `is_proceed_to_checkout_button_displayed()`, `click_proceed_to_checkout()`, `is_login_modal_displayed()` 11개 메서드 전부 구현 (shopping_cart.md §19, CART-REQ-003~010) — shrimp-task-manager Task5(93점) 완료 확인됨
- [x] `test_data/products.json`(장바구니 전용)에 테스트 상품 데이터 반영: Men Tshirt(Rs. 400), Printed Off Shoulder Top - White(Rs. 315) (shopping_cart.md §17) 신규 작성 완료. `conftest.py`에 기존 `accounts_data`/`search_keywords_data`와 동일한 패턴으로 `products_data`(session-scope) + `cart_test_product`/`cart_test_product_secondary` fixture 추가 — shrimp-task-manager Task6(100점) 완료 확인됨
- [x] `tests/test_shopping_cart.py` 작성: shopping_cart.md 자동화 대상 시나리오 7개(NOR-001~005, ABN-001~002)를 6개 테스트 함수로 전부 커버 — shrimp-task-manager Task7(96점) 완료 확인됨
  - [x] NOR-001 (상품 목록 페이지에서 장바구니 추가, 항상 1개만 담김) → `test_add_product_to_cart_from_products_page`
  - [x] NOR-002 (상품 상세 페이지에서 수량 지정 후 장바구니 추가) → `test_add_product_to_cart_from_detail_page_with_quantity`
  - [x] NOR-003 (장바구니에서 상품 삭제, 페이지 리로드 없이 즉시 반영 확인) → `test_delete_product_from_cart`
  - [x] NOR-004 (동일 상품 중복 담기 시 기존 행 수량 증가 확인) → `test_duplicate_add_increases_quantity`
  - [x] NOR-005 / ABN-001 (비로그인 상태에서 "Proceed To Checkout" 클릭 시 로그인 안내 모달 노출 확인, URL이 `/view_cart`로 유지되는지 확인 — 두 시나리오는 동일 사실을 다루므로 중복 구현하지 않고 하나로 통합 구현, shopping_cart.md §13 NOR-005 비고에서 권장한 방식) → `test_guest_checkout_shows_login_modal`
  - [x] ABN-002 (빈 장바구니 상태에서 안내 문구 확인, "Proceed To Checkout" 버튼 미노출 확인) → `test_empty_cart_shows_message`
- [x] "Add to cart" 버튼, "View Product" 버튼, 삭제(X) 아이콘, 담기 성공 모달, 로그인 모달 등의 Locator는 Playwright MCP(`browser_snapshot` 우선, 부족 시 `browser_evaluate`)로 직접 조사·검증한 뒤 확보 (CLAUDE.md §6, shrimp-rules.md §5) — 완료 확인됨(Task1). 삭제·결제 진입 등 "되돌리기 어려운 동작"(CLAUDE.md §6.4·shrimp-rules.md §5)에 대한 사용자 확인 절차가 실제로 정상 동작함을 이번 세션에서 실증함 (shopping_cart.md §20)

**Phase 2 산출물**: `pages/products_page.py`(확장), `pages/cart_page.py`(신규), `pages/base_page.py`(확장, `wait_for_element_invisible` 추가), `utils/helpers.py`(확장, `parse_price_text` + `normalize_whitespace` 추가 — `normalize_whitespace`는 계획 대비 추가로 발생한 산출물), `test_data/products.json`(신규), `conftest.py`(확장, `products_data`/`cart_test_product`/`cart_test_product_secondary` fixture 추가), `tests/test_shopping_cart.py`(신규)

---

### Phase 3: 검증 및 안정성 강화

**목표**: 예외/경계값 시나리오 확장 검토, 크로스 브라우저 지원, CI/CD 파이프라인 최종화 (project-prd.md §8.3)
**선행 조건**: Phase 1, Phase 2의 모든 정상/비정상 시나리오 테스트 PASS

- [x] (검토) 회원가입 실패/유효성 검증 케이스(중복 이메일, 필수 필드 누락 등) 자동화 확장 여부 논의 — shrimp-task-manager **Task1(95점)** 완료 확인됨: signup.md §11·§20을 재확인해 "이번 프로젝트 범위 한정" 스코프 사유로 이미 자동화 제외가 확정되어 있음을 원문 근거로 재검증함. **결론: 재논의 불필요, 착수하지 않음. 코드/문서 변경 없음.**
- [x] (검토) 로그인 필수 필드 공란 시나리오, 경계값(비밀번호 길이 등) 자동화 확장 여부 논의 — shrimp-task-manager **Task1(95점)** 완료 확인됨: login.md §12·§22를 재확인해 "이번 프로젝트 범위 한정" 스코프 사유로 이미 자동화 제외가 확정되어 있음을 원문 근거로 재검증함. **결론: 재논의 불필요, 착수하지 않음. 코드/문서 변경 없음.**
- [ ] (검토, 블로커 해소 후 착수) 로그아웃 세션 만료 관련 시나리오 자동화 검토 — shrimp-task-manager **Task2(90점)** 완료 확인됨: project-prd.md §19.1, logout.md §9·§12·§20·§22를 재확인해 **세션 타임아웃 값이 여전히 미확정**임을 재검증함. 이번 세션에서 사용자가 "세션 타임아웃은 작업에서 제외"라고 명시적으로 지시함. **결론: 세션 타임아웃 여전히 미확정, 착수하지 않음. 섹션 5 블로커 트래킹 표의 해당 항목은 새로운 사실이 없어 변경 없이 그대로 유지됨.**
- [x] (검토) 상품 검색 카테고리/브랜드 필터링, 정렬 기능 자동화 확장 여부 논의 — shrimp-task-manager **Task1(95점)** 완료 확인됨: product_search.md §12를 재확인해 "이번 프로젝트 범위 한정" 스코프 사유로 이미 자동화 제외가 확정되어 있음을 원문 근거로 재검증함. **결론: 재논의 불필요, 착수하지 않음. 코드/문서 변경 없음.**
- [x] (검토) 장바구니 최대 담기 개수 제한, 데이터 저장 방식(세션/쿠키/DB) 검증 여부 재논의 — shrimp-task-manager **Task1(95점)** 완료 확인됨: shopping_cart.md §12·§20를 재확인해 "사용자 판단에 따른 명시적 제외 결정"으로 이미 확정되어 있음을 원문 근거로 재검증함(4건 중 가장 확정적). **결론: 재논의 불필요, 착수하지 않음. 코드/문서 변경 없음.**
- [ ] **(부분 완료)** Firefox WebDriver 추가 및 Phase 1~2 정상 시나리오 대상 크로스 브라우저 테스트 구성 (project-prd.md §8.3, §11.2, §18.2) — shrimp-task-manager **Task3(85점)** 완료 확인됨. `conftest.py`에 `pytest_addoption`으로 `--browser`(기본값 chrome) 옵션 추가, `driver` fixture를 request 파라미터로 확장. 기존 5개 테스트 파일 무수정, `--browser` 옵션 없이 실행 시 기존과 동일하게 Chrome으로 동작(하위 호환 확인). 검증 중 실제 크로스 브라우저 버그 3건을 발견해 수정함: (1) 광고 iframe이 클릭을 가로채는 `ElementClickInterceptedException` → `pages/base_page.py`에 `scroll_into_view()`/`click_element()` 추가, `click()`/`click_when_clickable()`도 스크롤 후 클릭하도록 수정 (2) project-prd.md §11.2가 명시한 1920x1080 창 크기가 애초에 미구현이었던 결함 발견 → `conftest.py`에 `driver.set_window_size(1920, 1080)` 추가 (3) 광고 많은 페이지 전환 후 대기가 `DEFAULT_TIMEOUT`(10초) 경계에서 간헐적 실패 → `config/settings.py`에 `PAGE_LOAD_TIMEOUT`(20초, project-prd.md §11.4 기 명시값) 신설, `account_created_page.py`/`home_page.py`/`signup_page.py`/`login_page.py`/`products_page.py`의 페이지 전환 대기 지점 5곳에 일관 적용. Chrome 5개 테스트 파일 재실행 결과 18 passed로 회귀 없음 재확인. **그러나** Firefox는 로컬에서 7회 이상 반복 검증(계정 정리 포함)했으나 100% 재현 가능한 완전한 통과는 달성하지 못함 — 15회 반복 실험으로 순수 `driver.get()` 호출만으로도 geckodriver가 페이지/광고와 무관하게 WebDriver 프로토콜 레벨에서 120초간 응답하지 않는 경우(ReadTimeoutError/socket.timeout)를 확인해, 로컬 macOS에서 Firefox 세션을 반복 기동하며 생긴 geckodriver 자체의 인프라 불안정성이며 애플리케이션 코드로 해결할 문제가 아님을 실험으로 검증함. 사용자가 "현재 상태로 종료 후 CI에서 재확인"을 명시적으로 선택해 **로컬 완전 안정화는 이번 Task 범위에서 제외되고 Task4(CI)로 이관됨**
- [ ] **(부분 완료)** `.github/workflows/test.yml` 최종 점검: 실패 시 알림, HTML 리포트 아티팩트 저장, 매 커밋 자동 실행 안정성 확인 (project-prd.md §11.3, §13.4) — shrimp-task-manager **Task4(82점)** 완료 확인됨. 실제 발견한 결함(HEADLESS 환경변수 미설정으로 디스플레이 없는 GitHub Actions 환경에서 Chrome 실행 실패 가능성) 수정: "Run pytest" 스텝에 `env.HEADLESS="true"` 추가. `strategy.matrix.browser=[chrome, firefox]`(`fail-fast: false`) 도입, `pytest tests/ --browser=${{ matrix.browser }} --html=reports/report-${{ matrix.browser }}.html`로 브라우저별 리포트 분리, 아티팩트도 `reports-${{ matrix.browser }}`로 분리 업로드. 사용자가 "GitHub 기본 이메일 알림으로는 부족, 별도 Slack 알림 구축"을 명시적으로 요청해 `8398a7/action-slack@v3`로 실패 시 Slack 알림 스텝 추가(`secrets.SLACK_WEBHOOK_URL` 필요). 로컬 HEADLESS=true 검증: Chrome 19 passed/1 failed(재시도 시 즉시 PASS, 알려진 광고 로딩 플레이키니스), Firefox 16 passed/4 failed(Task3에서 파악된 동일 패턴). 3개 커밋(✨ 장바구니+Firefox 지원, 🚀 CI 워크플로우, 📝 ROADMAP)으로 origin/main에 push 완료. 사용자 승인으로 gh CLI 설치·인증 후 실제 GitHub Actions 실행(run_id 30201769656)을 직접 조회해 검증함. **워크플로우 메커니즘 자체(matrix 2개 잡 트리거, HEADLESS 적용, 브라우저별 리포트 아티팩트 2종 정상 생성·다운로드)는 정상 동작 확인됨.** 그러나 실제 테스트 결과는 chrome/firefox **둘 다** 16 failed/2 passed/2 errors로 매우 낮았고, 두 브라우저의 실패 패턴이 거의 동일(로그인 이메일 입력창부터 못 찾음, 상품 검색 결과 0개 등)해 Firefox 고유 문제가 아니라 **CI 환경(GitHub Actions 클라우드 IP 등)에서 automationexercise.com 접근이 로컬과 다르게 동작하는 별도의 심층 이슈로 추정**(원인 미확정, 추가 조사 필요). Slack 알림 스텝도 `SLACK_WEBHOOK_URL` 시크릿이 아직 등록되지 않아 "Specify secrets.SLACK_WEBHOOK_URL" 오류로 실패함(사용자가 GitHub 저장소 설정에서 직접 추가해야 하는 민감정보라 에이전트가 대신 처리하지 않음). 사용자가 "워크플로우 수정만으로 Task4 마무리, CI 대량 실패 문제는 별도 기록"을 명시적으로 선택함 — **워크플로우 수정은 완료, 실제 CI 정상 동작은 미해결**(섹션 5 신규 블로커 참고)
- [x] 성능 테스트 요구사항 정의 문서화 (실제 성능 테스트 구현은 범위 밖 유지, project-prd.md §8.3, §6.1) — shrimp-task-manager **Task5(96점, automation-prd-writer 위임)** 완료 확인됨. `docs/prd/project-prd.md` v1.2 → v1.3 갱신. §8.3(Phase 3) 산출물에 "성능 테스트 요구사항 정의 문서(§8.3.1, 참고용)" 추가. 신설된 §8.3.1 "성능 테스트 요구사항 정의(참고용 — MVP 범위 외)"에 측정 지표 범주 4종, 측정 후보 대상 6개(기존 자동화 흐름과 연결), 구현 도구 후보(Locust/k6/Lighthouse 등, 미확정) 기술. 측정 임계치는 전부 "미확정 — 확인 필요"로 명시(임의 수치 생성 없음). §6.1의 기존 "성능 테스트 MVP 제외" 서술은 한 글자도 수정하지 않고 유지, §8.3.1 본문에 두 섹션이 시점상 충돌하지 않음을 명시적으로 설명. 실제 성능 테스트 코드는 작성하지 않음(문서화만)

**참고(Task6, 최종 점검)**: shrimp-task-manager Task6은 별도의 구현 산출물을 만드는 Task가 아니라 project-prd.md §14 성공 기준 전체를 저장소 실제 상태와 대조하는 최종 점검이었습니다. 이 점검에서 새로 발견된 사실(CI 대량 실패, README.md 부재, SLACK_WEBHOOK_URL 미등록, `logs/` 파일명 문서-구현 불일치)은 위 8개 항목에는 직접 포함되지 않으며, 섹션 5(블로커 트래킹)와 섹션 6(Phase 3 완료 조건)에 반영되어 있습니다.

**Phase 3 산출물**: `conftest.py`(확장, `--browser` 옵션·`pytest_addoption`·창 크기 1920x1080 설정), `pages/base_page.py`(확장, `scroll_into_view()`/`click_element()` 추가), `config/settings.py`(확장, `PAGE_LOAD_TIMEOUT` 신설), `pages/account_created_page.py`/`home_page.py`/`signup_page.py`/`login_page.py`/`products_page.py`(대기 지점 `PAGE_LOAD_TIMEOUT` 적용), `.github/workflows/test.yml`(matrix `[chrome, firefox]`·`HEADLESS=true`·브라우저별 리포트 분리·Slack 알림 스텝 추가), `docs/prd/project-prd.md`(v1.2 → v1.3, §8.3.1 신설, automation-prd-writer 위임 산출물). **주의**: 회원가입/로그인/상품검색/장바구니 4개 검토 항목은 착수하지 않기로 결론이 났으므로 해당 기능별 PRD(`signup.md`, `login.md`, `product_search.md`, `shopping_cart.md`)는 이번 Phase 3에서 수정되지 않았습니다. README.md는 아직 산출물 목록에 없습니다(섹션 5 신규 블로커 참고).

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
| 로그인 테스트 계정(이메일/비밀번호/Name) 사전 생성 필요 | 1-B 로그인, 1-C 로그아웃 테스트 실행 | 테스트 실행 전 준비 필요 (login.md §17, §22 — 준비 방식은 "사전 생성"으로 이미 확정됨, 실제 계정 생성 작업만 남음) |
| 세션 타임아웃 시간 미확정 | Phase 3 "로그아웃 세션 만료 시나리오" 검토 Task | 프로젝트 전체 차원의 확인 필요 사항 (project-prd.md §19.1, logout.md §20). 확정되기 전까지 해당 Task는 착수하지 않음 |
| `shopping_cart.md` §22 "project-prd.md 정합성 검토(사용자 승인 필요)" 항목 | 로드맵 진행에는 직접 영향 없음 (참고) | `project-prd.md`는 이미 v1.2에서 "장바구니 수량 변경" 서술을 "장바구니 상품 삭제"로 수정하여 `shopping_cart.md` v1.4와 동기화된 것으로 확인됨(§5.1, §8.2). 다만 `shopping_cart.md` 자체의 "다음 단계" 섹션에는 아직 미해결 항목으로 남아 있어, feature PRD 담당(automation-prd-writer)이 해당 문서의 해당 항목을 정리하는 것을 권장함 |
| 로그인 상태에서 "Proceed to Checkout" 클릭 시 결제 페이지의 상세 동작 | 결제(Checkout) 기능 PRD 착수 (MVP 범위 밖) | MVP 이후 별도 checkout PRD 작성 시점에 확인 (shopping_cart.md §20, §22) |
| **(신규)** CI 환경(GitHub Actions)에서 automationexercise.com 접근 시 chrome/firefox 모두 대량 테스트 실패(각 16 failed/2 passed/2 errors, run_id 30201769656) — 로컬 Chrome은 동일 시점 18 passed로 정상이라 CI 환경 고유 이슈로 추정되나 원인 미확정 | Phase 3 "CI 최종 점검" Task의 실질적 완료, project-prd.md §14.2(테스트 성공률)·§14.5(자동화 인프라 CI/CD 정상 동작) 성공 기준 최종 충족 | 원인 미확정 — 추가 조사 필요. 담당/시점 미정(다음 세션 또는 별도 조사 Task로 착수 권장) |
| **(신규)** `SLACK_WEBHOOK_URL` 저장소 시크릿 미등록 | `.github/workflows/test.yml`의 Slack 실패 알림 스텝("Specify secrets.SLACK_WEBHOOK_URL" 오류로 현재 실패) | 사용자가 GitHub 저장소 Settings → Secrets에서 직접 등록 필요(민감정보이므로 에이전트가 대신 처리하지 않음) |
| **(신규)** 저장소 루트에 `README.md` 파일이 존재하지 않음 (Task6에서 `ls` 명령으로 직접 확인) | project-prd.md §14.4 "README.md 포함(프로젝트 개요, 실행 방법)" 성공 기준 충족 | 작성 여부·시점 사용자 확인 필요 — 필요 시 별도 Task로 착수 |

**참고(Phase 0 산출물, 이번 Phase 3 범위 밖이나 Task6에서 재확인됨)**: `utils/logger.py`의 실제 로그 파일은 `logs/test.log`(고정 파일명)인데 project-prd.md §13.3은 `logs/automation_test_*.log`(타임스탬프 패턴)로 서술하고 있어 문서-구현 간 사소한 불일치가 있습니다. 로드맵 진행에 직접 영향은 없어 이 표에 블로커 행으로 추가하지 않고 참고로만 기록합니다.

**참고(정책 변경으로 표에서 제외된 항목)**: 기존에는 "전 기능 공통 UI 요소의 실제 id/name/data-* 속성 미공유"를 이 표에 블로커로 포함했으나, `CLAUDE.md` §6·`shrimp-rules.md` §5의 Playwright MCP 조사 절차 도입에 따라 더 이상 이 표에서 다루지 않습니다. 실제 Locator 미공유 자체는 Page Object 구현 착수를 막지 않으며, 1-D 상품 검색(`pages/products_page.py`)에서 이미 이 절차로 해소된 선례가 있습니다. Playwright MCP로도 확인이 불가능한 개별 요소(CLAUDE.md §6.4, shrimp-rules.md §5의 "되돌리기 어려운 동작" 등의 사유)가 실제로 발견되는 시점에만 그 항목을 이 표에 새 행으로 추가합니다.

---

## 6. Definition of Done (Phase별 완료 조건)

### Phase 0 완료 조건
- [x] `pages/`, `tests/`, `utils/`, `config/`, `test_data/`, `screenshots/`, `reports/` 디렉터리 존재 — 확인됨
- [x] `conftest.py`의 `driver` fixture가 정상 동작 (브라우저 실행/종료 확인) — `tests/test_smoke.py::test_driver_opens_and_closes` PASS로 확인됨
- [x] `base_page.py`의 4개 공통 Wait 메서드(`find_element_visible`, `click_when_clickable`, `wait_for_element_presence`, `wait_for_text`) 구현 및 단순 호출 테스트로 동작 확인 — `tests/test_smoke.py::test_base_page_wait_methods` PASS로 확인됨
- [x] `requirements.txt` 기준으로 `pip install -r requirements.txt` 정상 완료 — 확인됨
- [x] `.env`, `screenshots/`, `reports/` 등이 `.gitignore`에 등록되어 git 미추적 확인 — 확인됨(`logs/`도 함께 등록됨)

### Phase 1 완료 조건
- [x] signup, login, logout, product_search 4개 기능 PRD의 자동화 대상 정상/비정상 시나리오(NOR-001~002, NOR-001~002/ABN-001~002, NOR-001~002, NOR-001~003/ABN-001) 100% 테스트 케이스화 — **완료 확인됨**: T21에서 `tests/test_product_search.py`가 신규 작성되어 4개 기능 전부 커버됨. signup NOR-001~002 → `test_signup_with_valid_info`, `test_signup_then_logout_and_relogin` / login NOR-001~002·ABN-001~002 → `test_login_with_valid_credentials`, `test_relogin_after_logout`, `test_login_with_invalid_password`, `test_login_with_nonexistent_email` / logout NOR-001~002 → `test_logout_from_logged_in_state`, `test_logout_then_relogin`(ABN-001~002는 logout.md §12에서 자동화 범위 제외로 이미 확정되어 미구현이 정상) / product_search NOR-001~003·ABN-001 → `test_search_with_valid_keyword`, `test_view_all_products_without_keyword`, `test_search_case_insensitive`, `test_search_with_nonexistent_keyword`. 총 12개 시나리오 = 12개 테스트 함수로 1:1 매칭 확인됨
- [x] 각 Page Object(SignupPage, LoginPage, HomePage, ProductsPage 등) 구현 직후 Playwright MCP로 주요 화면/시나리오의 실제 동작을 확인 (pytest 실행 전 보조 검증, pytest를 대체하지 않음) — **완료 확인됨**: T11~T21 전 구간에서 SignupPage, LoginPage, AccountCreatedPage, HomePage, DeleteAccountPage, ProductsPage 구현 시마다 Playwright MCP(`browser_navigate`, `browser_snapshot`, `browser_evaluate`, `browser_click`, `browser_fill_form` 등)로 로그인/회원가입/로그아웃/상품검색 흐름을 사전 또는 사후 검증함(각 shrimp-task-manager Task의 verify_task 요약에 기록됨). 예: 로그인 성공/실패 케이스, 로그아웃 후 헤더 상태, 상품 검색 결과 개수(Blue=7건, 전체=34건, TOP/Top=14건 동일, 무효 키워드=0건)를 실제 사이트에서 직접 확인함
- [x] `pytest tests/test_signup.py tests/test_login.py tests/test_logout.py tests/test_product_search.py` 전체 PASS (실패율 0%, pytest 기준) — **완료 확인됨**: 2026-07-25 `pytest tests/test_signup.py tests/test_login.py tests/test_logout.py tests/test_product_search.py --html=reports/report.html` 실행 결과 `12 passed, 1 warning in 65.84s`로 실패 0건 확인됨
- [x] 로그인 테스트 계정이 사전 생성되어 있고, 회원가입 시 입력한 Name 값과 로그인 후 "Logged in as {username}"이 일치함을 확인 — 이번 전체 실행에서도 재확인됨(`test_login_with_valid_credentials`, `test_relogin_after_logout`, `test_signup_then_logout_and_relogin`의 `get_logged_in_username() == expected_username` assertion 전부 PASS)
- [x] 테스트 실패 시 `screenshots/`에 스크린샷 자동 저장 확인 — **완료 확인됨**: 이번 세션 진행 중 실제 발생한 실패(사이트 광고 인터스티셜로 인한 계정 삭제 확인 페이지 로딩 지연 타임아웃 등, 예: `test_signup_with_valid_info`)에서 `screenshots/` 디렉터리에 `test_signup_with_valid_info_failed_2026-07-25_19-31-36.png` 등 총 6개 스크린샷이 파일명 규칙(CLAUDE.md §14.2)에 맞게 정상 저장된 것을 확인함 — 실전 발생 사례로 hook 정상 동작이 실증됨
- [x] `pytest-html` 리포트(`reports/report.html`) 생성 확인 — **완료 확인됨**: 2026-07-25 실행 직후 파일 생성 확인됨(`/Users/leeseunghwan/automation/AT-EX/reports/report.html`, 46,811 bytes, 최신 타임스탬프), pytest-html 플러그인의 "Generated html report" 로그가 매 실행마다 정상 출력됨

### Phase 2 완료 조건
- [x] shopping_cart.md의 자동화 대상 정상/비정상 시나리오(NOR-001~005, ABN-001~002) 100% 테스트 케이스화 — **완료 확인됨**: `tests/test_shopping_cart.py`의 6개 테스트 함수로 7개 시나리오가 전부 매핑됨(NOR-005/ABN-001은 shopping_cart.md §13 NOR-005 비고의 권장에 따라 `test_guest_checkout_shows_login_modal` 하나로 통합 구현)
- [x] `pages/products_page.py`(확장 메서드)와 신규 `pages/cart_page.py` 구현 직후 Playwright MCP로 담기/삭제/결제 진입 등 주요 시나리오의 실제 동작을 확인 (pytest 실행 전 보조 검증, pytest를 대체하지 않음) — **완료 확인됨**: Locator 조사 Task(Task1)에서 Playwright MCP 실클릭으로 담기/성공 모달/삭제/결제 진입/빈 장바구니 전체 흐름을 확인했고, ProductsPage 확장 Task(Task4)에서 ProductsPage+CartPage 연동 흐름을 Selenium 스모크로 추가 확인함. 삭제·결제 진입처럼 되돌리기 어려운 동작은 실클릭 전 사용자 확인(AskUserQuestion)을 거쳐 안전하게 검증됨
- [x] `pytest tests/test_shopping_cart.py` PASS, Phase 1 테스트와 함께 실행 시에도 누적 성공률 100% (pytest 기준) — **완료 확인됨**: `pytest tests/test_shopping_cart.py -v` 단독 실행 결과 6 passed(26.62s). `pytest tests/test_signup.py tests/test_login.py tests/test_logout.py tests/test_product_search.py tests/test_shopping_cart.py --html=reports/report.html` 통합 실행 결과 **18 passed, 0 failed(93.61s)**. 1차 시도에서 `test_signup_then_logout_and_relogin` 1건이 사이트 광고 인터스티셜로 인한 계정 삭제 확인 페이지 로딩 지연 타임아웃으로 실패했으나, Phase 2 변경과 무관한 Phase 1 기존 코드의 플레이키 이슈로 판명되어 단독 재실행 시 즉시 PASS로 재현됨을 확인함(위 Phase 1 완료 조건 스크린샷 항목에 이미 기록된 것과 동일 종류의 현상). `reports/report.html` 최신 타임스탬프로 재생성 확인됨
- [x] `pages/products_page.py`와 `pages/cart_page.py` 간 책임 분리가 shopping_cart.md §19 기준과 일치 (담기 진입은 ProductsPage, 조회/삭제/결제진입은 CartPage) — **완료 확인됨**: 설계 그대로 구현되어 ProductsPage는 담기 진입 메서드만, CartPage는 조회/삭제/결제진입 메서드만 보유함

### Phase 3 완료 조건
- [x] Phase 3 "검토" Task 5건(회원가입/로그인/상품검색/장바구니 자동화 확장 검토 4건 + 로그아웃 세션 만료 검토 1건)에 대한 착수 여부 결정 및 결과 문서화(착수하지 않기로 한 경우 사유 기록) — **완료 확인됨**: shrimp-task-manager Task1(95점)에서 4건 모두 각 기능 PRD 원문(signup.md §11·§20, login.md §12·§22, product_search.md §12, shopping_cart.md §12·§20)을 근거로 "착수하지 않음"으로 재검증·문서화됨. Task2(90점)에서 로그아웃 세션 만료 1건은 세션 타임아웃 미확정(project-prd.md §19.1)과 사용자의 명시적 제외 지시를 근거로 "착수하지 않음(보류)"으로 문서화됨. 5건 전부 결정과 사유가 문서화되었다는 의미에서 이 DoD 항목 자체는 충족되었으나, 보류된 1건(세션 만료)은 여전히 미해결 상태로 남아 있음(섹션 5 블로커 참고)
- [ ] Firefox 브라우저로 Phase 1~2 정상 시나리오 재실행 PASS — **미충족**: Task3(85점)에서 `--browser` 옵션 및 크로스브라우저 대응 코드(스크롤 후 클릭, 1920x1080 창 크기, `PAGE_LOAD_TIMEOUT`)는 완성되어 Chrome은 18 passed로 재확인되었으나, Firefox는 로컬 7회 이상 반복 검증에서도 100% 안정적 통과를 달성하지 못했고(geckodriver 인프라 불안정성으로 판명), Task4(82점)의 실제 GitHub Actions 실행(run_id 30201769656)에서도 Firefox는 16 failed/2 passed/2 errors로 PASS 기준을 충족하지 못함
- [ ] `.github/workflows/test.yml`이 매 커밋마다 정상 실행되고 리포트 아티팩트가 저장됨을 확인 — **미충족**: Task4(82점)에서 워크플로우 트리거·HEADLESS 적용·브라우저별 리포트 아티팩트 2종 생성/다운로드 등 **메커니즘 자체는 정상 동작**함을 실제 GitHub Actions 실행(run_id 30201769656)으로 확인했으나, 그 실행에서 나온 실제 테스트 결과가 chrome/firefox 둘 다 16 failed/2 passed/2 errors로 대량 실패해 "정상 실행"의 실질적 의미(테스트가 정상적으로 통과하며 실행됨)는 충족되지 않음. Slack 실패 알림 스텝도 `SLACK_WEBHOOK_URL` 시크릿 미등록으로 실패함
- [ ] 프로젝트 전체 성공 기준(project-prd.md §14) 충족 여부 최종 점검 — **점검은 수행했으나 결과는 미충족**: shrimp-task-manager Task6에서 §14 전 항목을 실제 저장소 상태와 대조 점검함. §14.1(테스트 코드 완성도)·§14.3(코드 품질)은 기존과 동일하게 충족 유지. §14.2(테스트 성공률, "마지막 실행 기준 실패율 0%")는 로컬 Chrome 기준으로는 충족(18 passed)되나 **실제 GitHub Actions CI 실행 기준으로는 chrome/firefox 모두 대량 실패해 미충족**. §14.4(문서 완성도, "README.md 포함")는 **저장소 루트에 README.md 파일이 존재하지 않음을 `ls` 명령으로 직접 확인해 미충족**. §14.5(자동화 인프라)는 pytest 실행·pytest-html 리포트 생성·로깅/스크린샷 자동 저장은 충족되나 "GitHub Actions CI/CD 구성 완료"는 구성 자체는 완료되었어도 정상 동작까지는 §14.2와 동일한 사유로 미확인. 종합적으로 **project-prd.md §14 전체 성공 기준은 현재 미충족**(README.md 부재, CI 대량 실패가 핵심 근거)

---

## 7. 다음 액션 (Next Actions)

우선순위 순으로 착수를 권장하는 Task입니다.

Phase 0(기반 설정), Phase 1(1-A 회원가입, 1-B 로그인, 1-C 로그아웃, 1-D 상품 검색), Phase 2(장바구니 및 결제 진입 제약 확인)는 구현·테스트 작성·PASS까지 모두 완료되었습니다. Phase 3는 shrimp-task-manager MCP로 6개 Task로 분해해 모두 completed 처리되었으나, 검증 과정에서 새로 발견된 미해결 사항이 있어 다음 액션은 그 사항들을 해소하는 데 집중합니다.

1. **CI 환경(GitHub Actions)에서의 대량 테스트 실패 원인 조사**: 실제 GitHub Actions 실행(run_id 30201769656)에서 chrome/firefox 둘 다 16 failed/2 passed/2 errors로 실패했고 두 브라우저의 실패 패턴이 거의 동일해 브라우저 고유 문제가 아니라 CI 환경(클라우드 IP 등) 자체의 이슈로 추정됨. project-prd.md §14.2·§14.5 성공 기준의 실질적 충족을 위한 최우선 블로커이므로 원인 규명이 최우선 (섹션 5 블로커 트래킹 표 참고)
2. **`SLACK_WEBHOOK_URL` 저장소 시크릿 등록 여부 결정 및 등록**: `.github/workflows/test.yml`의 Slack 실패 알림 스텝이 현재 시크릿 미등록으로 실패 중임. 사용자가 GitHub 저장소 Settings에서 직접 등록해야 하는 민감정보 작업 (섹션 5 블로커 트래킹 표 참고)
3. **README.md 작성 여부 및 시점 결정**: 저장소 루트에 README.md가 존재하지 않아 project-prd.md §14.4 문서 완성도 기준이 미충족 상태임. 작성이 필요하다고 판단되면 별도 Task로 착수 (섹션 5 블로커 트래킹 표 참고)
4. **세션 타임아웃 값 확정 여부 재확인**: project-prd.md §19.1 기준 여전히 미확정이며, 이번 세션에서는 사용자 지시로 보류된 상태. 확정되는 시점에 로그아웃 세션 만료 시나리오 검토 Task 재착수 가능 (섹션 5 블로커 트래킹 표 참고)
5. **(참고, 추가 액션 불필요)** Firefox 로컬 반복 실행 시 발생하는 geckodriver 무응답 문제는 실험적으로 애플리케이션 코드 문제가 아닌 로컬 인프라 불안정성으로 판명되었으므로, 위 1번(CI 조사)의 결과로 최종 판단을 대체하는 방향이 합리적임

---

## 8. 변경 이력

- **v1.0 (2026-07-24)**: 최초 작성. `docs/prd/project-prd.md`(v1.2)의 Phase 1/2/3 구조를 뼈대로 하여, `signup.md`(v1.4), `login.md`(v1.4), `logout.md`(v1.4), `product_search.md`(v1.6), `shopping_cart.md`(v1.4)에 명시된 정상/비정상 시나리오 ID(NOR-xxx/ABN-xxx), 자동화 제외 범위, 확인 완료/확인 필요 항목, 기능 간 의존성을 실행 Task로 변환. Phase 0(프로젝트 기반 설정)을 신설하여 CLAUDE.md §21.1의 미생성 인프라 항목을 선행 작업으로 명시. 현재 저장소에 실제 코드가 없어 모든 Phase 진행률은 0%에서 시작.
- **v1.1 (2026-07-24)**: roadmap-writer 서브에이전트 정의(`.claude/agents/dev/roadmap-writer.md`)에 추가된 규칙("구현 Task가 포함된 Phase의 DoD에는 Playwright MCP 실동작 확인 항목을 pytest PASS 항목과 별도 체크박스로 포함")을 반영. Page Object 구현 Task가 포함된 Phase 1, Phase 2의 완료 조건에 "구현 직후 Playwright MCP로 주요 화면/시나리오의 실제 동작을 확인 (pytest 실행 전 보조 검증, pytest를 대체하지 않음)" 항목을 추가. 인프라 설정 위주인 Phase 0과 검토/크로스브라우저/CI 위주인 Phase 3에는 해당 항목을 추가하지 않음. Task 목록(섹션 3)과 기존 진행 상태(체크박스)는 변경하지 않음.
- **v1.2 (2026-07-25)**: Locator 확보 정책 변경 반영. `CLAUDE.md` §6 "Playwright MCP 기반 페이지 탐색 규칙"(신설) 및 `shrimp-rules.md` §5 "Playwright MCP 기반 Locator 조사 절차"(갱신)에 따라, 실제 Locator 미공유를 즉시 사용자 확인이 필요한 블로커로 표기하던 항목들(1-A 회원가입, 1-B 로그인, 1-D 상품 검색, Phase 2 장바구니, 섹션 5 블로커 트래킹 표)을 "Playwright MCP로 우선 조사·검증하고, MCP로도 확인 불가능한 경우에만 사용자 확인 요청" 방식으로 재정리. 섹션 5 표에서 "전 기능 공통 UI 요소의 실제 Locator 미공유" 행을 제거하고 정책 변경 취지를 설명하는 참고 문구로 대체. 1-D "`pages/products_page.py` 구현" Task는 실제 저장소에서 구현이 확인되어(Playwright MCP `browser_evaluate`로 `/products` DOM을 직접 조사해 Locator 확보) 체크 완료로 갱신했으며, 이에 맞춰 Phase 1 마일스톤 상태를 ⬜ 예정 → 🟨 진행중으로 조정. Locator 미공유를 사유로 두지 않는 진짜 블로커(로그인 테스트 계정 사전 생성, 세션 타임아웃 미확정 등)는 그대로 유지. Phase 0/3은 이번 정책 변경과 무관하여 수정하지 않음.
- **v1.3 (2026-07-25)**: shrimp-task-manager MCP의 Task 실행 이력(T1~T19, 각 `execute_task` → 구현 → `verify_task` 80점 이상으로 completed 처리)을 저장소 실제 파일 상태와 교차검증하여 진행 상태를 재동기화. Phase 0(디렉터리 구조, `requirements.txt`, `pytest.ini`, `config/settings.py`, `pages/base_page.py`, `conftest.py`, `utils/logger.py`, `utils/helpers.py` 골격, `test_data/accounts.json` 골격, `.github/workflows/test.yml` 초안, `tests/test_smoke.py`)의 모든 Task를 완료로 체크하고 마일스톤 상태를 ⬜ 예정 → ✅ 완료(100%)로 갱신. Phase 1의 1-A 회원가입(`pages/login_page.py`·`signup_page.py`·`account_created_page.py`, `test_data/accounts.json` signup 데이터, `tests/test_signup.py` NOR-001~002 PASS), 1-B 로그인(`pages/login_page.py` 로그인 폼 메서드, `pages/home_page.py`, `test_data/accounts.json` shared_login_accounts, `tests/test_login.py` NOR-001~002/ABN-001~002 PASS), 1-C 로그아웃(`pages/home_page.py`·`login_page.py` 로그아웃 관련 메서드, `conftest.py`의 `logged_in_user` fixture, `tests/test_logout.py` NOR-001~002 PASS)의 Task를 모두 완료로 체크. 회원가입 테스트가 생성한 계정을 정리하기 위해 원래 로드맵에 계획되지 않았던 `pages/delete_account_page.py`가 1-A 작업 중 추가로 구현된 사실을 확인하여 1-A Task 목록과 "Phase 1 산출물" 목록에 반영. 1-D 상품 검색은 `pages/products_page.py` 구현 완료(기존 v1.2에서 이미 체크)만 유지하고, `test_data/search_keywords.json`과 `tests/test_product_search.py`는 저장소에 파일이 존재하지 않음을 확인하여 미체크로 유지. 이에 따라 Phase 1 마일스톤 진행률을 "세부 산정 필요" → "약 80%"로 구체화(상태는 여전히 🟨 진행중, 1-D 미완료로 ✅ 완료 아님). 섹션 6 Definition of Done에서 Phase 0의 5개 항목을 모두 체크(스모크 테스트 PASS 근거)하고, Phase 1은 로그인 테스트 계정·Name 일치 확인 1개 항목만 체크하고 나머지(100% 테스트 케이스화, Playwright MCP 실동작 확인, 4개 파일 전체 PASS, 스크린샷 저장 확인, HTML 리포트 생성 확인)는 실제 확인 근거가 없거나 product_search 누락으로 미체크 유지하며 각 항목에 현재 상태를 설명하는 문구를 추가. 섹션 7 "다음 액션"을 1-D 잔여 Task(`search_keywords.json` 작성, `test_product_search.py` 작성·실행) 및 Phase 1 통합 검증 중심으로 갱신. 1-B의 "로그인 테스트 계정 사전 생성" 블로커 체크박스, 1-C의 "참고(자동화 대상 아님)" 항목, 섹션 5 블로커/확인 필요 항목 트래킹 표, Phase 2·Phase 3 관련 내용은 이번 재동기화 범위에서 제외하여 그대로 유지.
- **v1.4 (2026-07-25)**: Phase 1 통합 검증(T22) 완료를 반영. 사용자가 직접 실행/확인한 검증 결과(T21에서 `tests/test_product_search.py` 신규 작성 완료로 4개 기능 12개 시나리오 전부 테스트 케이스화, T11~T21 전 구간 Playwright MCP 보조 검증 수행 기록 확인, `pytest tests/test_signup.py tests/test_login.py tests/test_logout.py tests/test_product_search.py --html=reports/report.html` 실행 결과 12 passed·실패 0건, 로그인 계정·Name 일치 재확인, 실제 실패 사례에서 `screenshots/` 자동 저장 6건 확인, `reports/report.html` 생성 확인)를 근거로 섹션 6 "Phase 1 완료 조건" 6개 항목을 모두 미체크 → 체크 완료로 갱신하고 각 항목의 설명 문구를 실제 검증 결과로 교체. 섹션 2 마일스톤 요약 표의 Phase 1 상태를 `🟨 진행중 약 80%` → `✅ 완료 100%`로 갱신. 섹션 7 "다음 액션"을 Phase 1 잔여 Task 중심에서 Phase 2(장바구니) 착수 Task(`pages/products_page.py` 확장, `pages/cart_page.py` 신규 구현, `test_data/products.json` 작성, `tests/test_shopping_cart.py` 작성·실행, Phase 2 통합 검증) 중심으로 전면 교체. 이번 갱신은 섹션 2(Phase 1 행)·섹션 6(Phase 1)·섹션 7·본 변경 이력 항목에 한정되며, 섹션 3의 Phase 1 세부 Task 체크박스(1-D의 `search_keywords.json`/`test_product_search.py` 항목, "Phase 1 산출물" 목록의 "미작성" 표기 등)와 Phase 0/2/3, 섹션 4, 섹션 5 블로커 트래킹 표는 이번 갱신 범위에서 제외되어 그대로 유지됨. **참고**: 이로 인해 섹션 3의 1-D 관련 체크박스 및 "Phase 1 산출물" 목록 문구가 섹션 6과 일시적으로 불일치하는 상태이며(예: `tests/test_product_search.py(미작성)` 표기가 아직 남아 있음), 이는 다음 갱신 시 함께 정리가 필요함.
- **v1.5 (2026-07-25)**: v1.4에서 남겨두었던 섹션 3-섹션 6 불일치를 보완. 섹션 3의 "1-D. 상품 검색" Task 목록 중 `test_data/search_keywords.json` 작성, `tests/test_product_search.py` 작성 두 항목을 `[ ]` → `[x]`로 갱신(T21에서 작성 완료 및 PASS 확인, T22 통합 실행에서 재확인된 근거 반영). "Phase 1 산출물" 목록의 `tests/test_product_search.py(미작성)` 표기를 완료된 산출물 표기로 수정. 이번 보완은 섹션 3의 해당 두 체크박스와 산출물 목록 문구에 한정되며, 그 외 섹션은 변경하지 않음.
- **v1.6 (2026-07-26)**: Phase 2(장바구니 및 결제 진입 제약 확인) 완료를 반영. shrimp-task-manager MCP로 Phase 2를 7개 Task로 분해해 순차 실행했고, 7개 Task 모두 `execute_task` → 구현 → `verify_task`(80점 이상, Task1 95점/Task2 100점/Task3 100점/Task4 92점/Task5 93점/Task6 100점/Task7 96점)로 completed 처리된 이력을 근거로 갱신함. 섹션 2 마일스톤 요약 표의 Phase 2 상태를 `⬜ 예정 0%` → `✅ 완료 100%`로 갱신. 섹션 3 "Phase 2" 하위 전 체크박스를 `[x]`로 갱신하고, `tests/test_shopping_cart.py`의 NOR-001~005/ABN-001~002 각 항목에 실제 매핑된 테스트 함수명(`test_add_product_to_cart_from_products_page`, `test_add_product_to_cart_from_detail_page_with_quantity`, `test_delete_product_from_cart`, `test_duplicate_add_increases_quantity`, `test_guest_checkout_shows_login_modal`, `test_empty_cart_shows_message`)을 추가. "Phase 2 산출물" 목록을 실제 산출물(`pages/products_page.py` 확장, `pages/cart_page.py` 신규, `pages/base_page.py` 확장, `utils/helpers.py` 확장, `test_data/products.json` 신규, `conftest.py` 확장, `tests/test_shopping_cart.py` 신규)로 갱신. 섹션 6 "Phase 2 완료 조건" 4개 항목을 모두 체크 완료 처리하고, `pytest tests/test_shopping_cart.py -v`(6 passed, 26.62s) 및 Phase 1~2 통합 실행(`pytest tests/test_signup.py tests/test_login.py tests/test_logout.py tests/test_product_search.py tests/test_shopping_cart.py --html=reports/report.html`, 18 passed·0 failed·93.61s) 결과를 근거로 명시. 섹션 7 "다음 액션"을 Phase 3(검증 및 안정성 강화) 착수 관점으로 전면 교체. **[계획 외 발견 사항]** (1) Task3 실행 중 실제 사이트의 광고 스크립트(`class="google-anno"`)가 상품명 텍스트에 여분의 공백을 삽입하는 문제를 발견하여, 계획에 없던 `utils/helpers.py`의 `normalize_whitespace(text: str) -> str` 함수가 추가로 구현됨(섹션 3 Phase 2 Task 목록·산출물에 반영). (2) 삭제(X 아이콘)·"Proceed To Checkout" 클릭처럼 "되돌리기 어려운 동작"에 대해 CLAUDE.md §6.4·shrimp-rules.md §5에 따라 실클릭 전 AskUserQuestion으로 사용자 확인을 받는 절차가 Task1에서 실제로 정상 동작함을 확인함(사용자가 "둘 다 허용" 응답 후 실클릭으로 검증 완료). (3) 통합 실행 1차 시도에서 `test_signup_then_logout_and_relogin` 1건이 사이트 광고 인터스티셜로 인한 타임아웃으로 실패했으나, Phase 2 변경과 무관한 Phase 1 기존 코드의 플레이키 이슈로 판명되어 단독 재실행 시 즉시 PASS로 재현됨을 재확인함(ROADMAP.md 기존 버전 섹션 6 Phase 1 완료 조건에 이미 기록된 것과 동일 종류의 현상). 섹션 5 블로커 트래킹 표는 이번 갱신으로 정리가 필요한 Phase 2 관련 행이 없음을 확인하여(Locator 미공유 관련 정책 변경은 v1.2에서 이미 반영됨, `shopping_cart.md` §22 project-prd.md 정합성 검토 항목은 Phase 진행에 직접 영향이 없어 그대로 유지) 변경하지 않음. 섹션 3의 Phase 0/1 내용, 섹션 4(기능 의존성 개요), 섹션 5(블로커 트래킹 표)는 이번 갱신 범위에서 제외되어 그대로 유지됨.
- **v1.7 (2026-07-26)**: Phase 3(검증 및 안정성 강화) 진행 결과를 반영. shrimp-task-manager MCP로 Phase 3를 6개 Task로 분해해 순차 실행했고, 6개 Task 모두 `execute_task` → 구현/조사 → `verify_task`(80점 이상, Task1 95점/Task2 90점/Task3 85점/Task4 82점/Task5 96점, Task6은 별도 산출물 없는 최종 점검)로 completed 처리된 이력을 근거로 갱신함. **Phase 3는 완료로 표기하지 않음** — 검증 과정에서 (1) 실제 GitHub Actions CI 실행(run_id 30201769656)에서 chrome/firefox 둘 다 대량 테스트 실패(각 16 failed/2 passed/2 errors), (2) Firefox 로컬 100% 안정적 통과 미달성(geckodriver 인프라 불안정성으로 판명, CI 검증으로 이관), (3) 저장소 루트에 README.md 파일 부재(project-prd.md §14.4 미충족), (4) `SLACK_WEBHOOK_URL` 시크릿 미등록으로 Slack 알림 미동작 등 4건의 미해결 사항이 새로 확인되었기 때문. 섹션 2 마일스톤 요약 표의 Phase 3 상태를 `⬜ 예정 0%` → `🟨 진행중 약 70%`로 갱신하고 근거를 상세 기술. 섹션 3 "Phase 3" 하위 8개 항목을 갱신: 회원가입/로그인/상품검색/장바구니 자동화 확장 검토 4건은 Task1(95점)에서 각 기능 PRD 원문 근거로 재검증되어 착수 불필요로 결론 확정되어 `[x]`로 체크, 로그아웃 세션 만료 검토 1건은 Task2(90점)에서 세션 타임아웃 여전히 미확정 + 사용자의 명시적 제외 지시로 `[ ]` 유지, Firefox 크로스 브라우저 1건은 Task3(85점)에서 코드는 완성되었으나 로컬 100% 안정성 미달성으로 "부분 완료" 표기하며 `[ ]` 유지, CI 최종 점검 1건은 Task4(82점)에서 워크플로우 수정 자체는 완료되었으나 실제 CI 대량 실패가 미해결로 "부분 완료" 표기하며 `[ ]` 유지, 성능 테스트 요구사항 정의 1건은 Task5(96점, automation-prd-writer 위임)로 project-prd.md v1.2 → v1.3 갱신·§8.3.1 신설이 완료되어 `[x]`로 체크. Task3에서 발견·수정된 크로스브라우저 버그 3건(광고 iframe 클릭 가로채기 → `scroll_into_view()`/`click_element()` 추가, 1920x1080 창 크기 미구현 결함 수정, `PAGE_LOAD_TIMEOUT`(20초) 신설 및 5개 페이지 전환 대기 지점 적용)을 "Phase 3 산출물" 목록에 반영. 섹션 5 블로커 트래킹 표에 신규 항목 3건(CI 환경 대량 실패 원인 미확정, `SLACK_WEBHOOK_URL` 시크릿 미등록, README.md 부재)을 추가하고, `logs/test.log` vs project-prd.md §13.3 `logs/automation_test_*.log` 문서-구현 불일치를 참고 각주로 추가(Phase 0 산출물이라 블로커 행으로는 추가하지 않음). 세션 타임아웃 미확정 행은 새로운 사실이 없어 변경하지 않고 그대로 유지. 섹션 6 "Phase 3 완료 조건" 4개 항목을 갱신: "검토 Task 착수 여부 결정·문서화" 항목은 5건 전부 결정·사유 문서화가 완료되어 `[x]`, 나머지 3개 항목("Firefox PASS", "CI 정상 실행 확인", "project-prd.md §14 성공 기준 최종 점검")은 모두 미충족 근거(Firefox CI 결과 16 failed/2 passed/2 errors, README.md 부재, CI 대량 실패)를 명시하며 `[ ]` 유지. 섹션 7 "다음 액션"을 신규 블로커 3건(CI 대량 실패 원인 조사, Slack 시크릿 등록, README.md 작성 여부 결정) 및 기존 블로커(세션 타임아웃 확정) 중심으로 전면 교체. 섹션 1 "기준 문서 및 버전" 표의 `project-prd.md` 버전을 v1.2 → v1.3으로 동기화(project-prd.md가 이번에 Task5로 v1.3으로 갱신되었으므로). 이번 갱신은 섹션 1(project-prd.md 버전)·섹션 2(Phase 3 행)·섹션 3(Phase 3 Task 목록·산출물)·섹션 5(블로커 표)·섹션 6(Phase 3 완료 조건)·섹션 7(다음 액션)·본 변경 이력 항목에 한정되며, Phase 0/1/2 관련 내용과 섹션 4(기능 의존성 개요)는 이번 갱신 범위에서 제외되어 그대로 유지됨.

---

이 문서는 진행 상황이 바뀔 때(착수/완료/블록)마다 갱신됩니다. 요구사항 자체의 변경이 필요한 경우 이 문서가 아니라 `docs/prd/` 하위 PRD 문서를 automation-prd-writer 서브에이전트를 통해 수정해야 합니다.
