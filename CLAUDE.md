# CLAUDE.md - AT-EX 프로젝트 공통 개발 규칙

## 📋 주의사항

이 문서는 **프로젝트 공통 개발 규칙 및 아키텍처 설계 원칙**을 정의한 문서입니다.
- **기능별 요구사항**(로그인, 회원가입, 결제 등)은 이 문서에 포함하지 않습니다.
- 기능별 요구사항은 별도의 **기능 명세 문서**로 관리합니다.
- **아직 실제 코드, 디렉터리 구조, 설정 파일은 생성되지 않았습니다.** 이 문서는 앞으로 따를 규칙을 정의합니다.

---

## 1. 프로젝트 개요와 목표

### 1.1 프로젝트 정보
- **프로젝트명**: AT-EX (Automation Testing - Automation Exercise)
- **대상 사이트**: [Automation Exercise](https://automationexercise.com/)
- **목표**: 웹 UI 회귀 테스트 자동화 프레임워크 구축
- **설계 방식**: Page Object Model (POM)
- **테스트 범위**: 대상 사이트의 주요 기능 및 사용자 시나리오

### 1.2 문서의 역할
이 문서는 프로젝트에서 **모든 자동화 코드 개발 시 Claude(AI)와 개발자가 일관되게 따를 공통 규칙**을 정의합니다.
모호한 규칙 없이 구체적인 원칙과 금지사항을 명시하여, 코드 품질과 유지보수성을 보장합니다.

---

## 2. 기술 스택

| 항목 | 기술/도구 | 상태 |
|------|---------|------|
| 언어 | Python | 확정 |
| 자동화 도구 | Selenium WebDriver | 확정 |
| 테스트 러너 | pytest | 확정 |
| 설계 패턴 | Page Object Model (POM) | 확정 |
| 리포팅 | pytest-html | 확정 |
| 실행 브라우저 | Chrome (ChromeDriver) | 확정 |
| 패키지 버전 | requirements.txt에서 관리 (미생성) | 미정 |
| CI/CD | GitHub Actions | 확정 |

---

## 3. 기본 디렉터리 구조 (예정)

```
AT-EX/
├── pages/                  # Page Object 클래스들
│   ├── base_page.py       # BasePage (공통 기능)
│   ├── home_page.py       # 홈 페이지
│   └── ...
├── tests/                  # 테스트 케이스
│   ├── test_home.py
│   ├── test_login.py
│   └── ...
├── utils/                  # 공통 유틸리티
│   ├── logger.py          # 로깅
│   ├── helpers.py         # 헬퍼 함수
│   └── ...
├── config/                 # 설정 파일
│   ├── settings.py        # 환경 설정 (미생성)
│   └── ...
├── test_data/              # 테스트 데이터
│   ├── test_accounts.json # 테스트 계정 (미생성)
│   └── ...
├── screenshots/            # 실패 시 스크린샷 저장 경로
├── reports/                # pytest-html 리포트 저장 경로
├── conftest.py            # pytest 설정 및 fixture (미생성)
├── requirements.txt       # Python 의존성 (미생성)
├── pytest.ini             # pytest 설정 (미생성)
├── .env                   # 환경변수 (git 미추적, 미생성)
├── .gitignore             # git 제외 목록 (미생성)
└── CLAUDE.md              # 이 문서
```

**각 디렉터리 역할:**
- `pages/`: Page Object 클래스 정의 - UI 요소 locator 및 화면 조작 메서드
- `tests/`: 테스트 케이스 작성 - 시나리오 검증 및 assertion
- `utils/`: 공통 유틸리티 - 로깅, 데이터 생성, 문자열 처리 등
- `config/`: 환경 설정 - URL, 타임아웃, 브라우저 옵션 등
- `test_data/`: 테스트 데이터 - JSON/YAML 형식 데이터 파일
- `screenshots/`: 테스트 실패 시 자동 저장되는 스크린샷
- `reports/`: pytest-html 생성 리포트

---

## 4. POM (Page Object Model) 설계 원칙

### 4.1 구조
- **1개 페이지 = 1개 Page 클래스**: 각 웹 페이지(또는 주요 화면 영역)마다 클래스 1개를 작성합니다.
- **BasePage 상속**: 모든 Page 클래스는 `BasePage`를 상속하여 공통 기능을 재사용합니다.
- **WebDriver 인스턴스**: Page 객체는 WebDriver 인스턴스 1개만 보유하며, 상태 변수는 최소화합니다.

### 4.2 Page 클래스 구성
```python
# 예시 구조 (실제 코드 아님)
class HomePage(BasePage):
    # Locator 정의 (상수 또는 클래스 변수)
    SEARCH_INPUT = (By.ID, "search_input")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button.search")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    # 화면 조작 메서드만 작성 (assertion 없음)
    def search_product(self, product_name):
        self.find_element(self.SEARCH_INPUT).send_keys(product_name)
        self.click(self.SEARCH_BUTTON)
    
    def get_search_results_count(self):
        # 페이지에서 값을 조회만 하고 반환 (assertion은 Test에서)
        return len(self.find_elements(self.SEARCH_RESULT))
```

---

## 5. Page Layer와 Test Layer의 책임 분리

### 5.1 Page Layer의 책임
- **Locator 정의**: 모든 UI 요소의 locator를 클래스 상수로 정의
- **화면 조작**: 클릭, 입력, 드래그, 스크롤 등의 메서드 제공
- **요소 조회**: UI 요소의 텍스트, 속성 등을 조회하여 **값을 반환**
- **절대 금지**: Assertion을 Page Layer에서 수행하지 않습니다.

### 5.2 Test Layer의 책임
- **시나리오 구성**: Page 객체의 메서드를 호출하여 테스트 시나리오를 흐름대로 작성
- **데이터 준비**: 테스트에 필요한 데이터 생성 및 정리
- **Assertion 수행**: Page에서 반환받은 값과 예상값을 검증
- **로그 및 리포트**: 테스트 결과를 로깅하고 최종 리포트에 반영

**원칙**: Page는 "어떻게 하는가?"만 알고, Test는 "무엇을 검증하는가?"를 담당합니다.

---

## 6. Locator 작성 원칙

### 6.1 Locator 선택 우선순위
Locator의 안정성 기준에 따라 **아래 순서대로 선택**합니다:

1. **id 속성** (가장 안정적)
   ```python
   BUTTON = (By.ID, "submit_button")
   ```

2. **data-* 속성** (안정적, 테스트용 속성)
   ```python
   INPUT = (By.CSS_SELECTOR, "input[data-testid='email']")
   ```

3. **name 속성**
   ```python
   FIELD = (By.NAME, "username")
   ```

4. **안정적인 CSS Selector** (변동 가능성이 적은 구조)
   ```python
   LINK = (By.CSS_SELECTOR, "a.menu-home")
   ```

5. **상대 XPath** (마지막 수단, 충분히 안정적인 경우만)
   ```python
   ROW = (By.XPATH, "//tr[@data-id='123']/td[2]")
   ```

### 6.2 금지 사항

**Full XPath 절대 금지**
```python
# ❌ 금지 - 매우 불안정
ELEMENT = (By.XPATH, "/html/body/div[1]/div[2]/section/div[3]/button")
```

**이유**: DOM 구조 변경 시 즉시 깨지므로 유지보수 불가능합니다.

### 6.3 Locator 정의 위치
- 모든 Locator는 Page 클래스의 **상단에 상수 또는 클래스 변수로 정의**합니다.
- 메서드 내에 locator를 하드코딩하지 않습니다.

```python
# ✅ 올바른 방식
class LoginPage(BasePage):
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button.login")
```

---

## 7. Wait 처리 규칙

### 7.1 time.sleep() 절대 금지
```python
# ❌ 금지 - 불안정하고 비효율적
time.sleep(5)
driver.find_element(By.ID, "element")
```

**이유**: 
- 고정 시간 대기로 인한 테스트 속도 저하
- 실제 요소 로드 시간과 무관하게 대기
- 테스트 불안정성 증가

### 7.2 Explicit Wait 기본 사용
Selenium의 `WebDriverWait` + `expected_conditions`를 사용하여 명시적 대기 구현합니다.

```python
# ✅ 올바른 방식
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, "element")))
```

### 7.3 BasePage에 공통 Wait 메서드 제공 (예정)
BasePage에서 반복되는 wait 로직을 래핑 메서드로 제공할 예정입니다.
예시 (구현 시 실제 메서드명 확정):
- `find_element_visible()`: 요소가 보이기를 대기 후 반환
- `click_when_clickable()`: 요소가 클릭 가능하기를 대기 후 클릭
- `wait_for_element_presence()`: 요소가 DOM에 나타나기를 대기
- `wait_for_text()`: 요소의 텍스트가 특정 값이 될 때까지 대기

**원칙**: 모든 요소 조작 시 적절한 Wait 조건을 명시하여 안정성을 확보합니다.

---

## 8. Assertion 작성 규칙

### 8.1 Assertion은 Test Layer에서만 수행
- **Page Layer**: 값을 조회하여 반환만 합니다.
- **Test Layer**: Page에서 받은 값과 예상값을 비교하여 검증합니다.

### 8.2 pytest assert 사용
```python
# ✅ 올바른 방식 (Test Layer)
def test_login_success(driver):
    login_page = LoginPage(driver)
    login_page.login("user@example.com", "password")
    
    dashboard_page = DashboardPage(driver)
    username = dashboard_page.get_logged_in_username()
    
    assert username == "John Doe", f"Expected 'John Doe' but got '{username}'"
```

### 8.3 실패 메시지에 기대값/실제값 포함
```python
# ✅ 명확한 메시지
assert result == expected, f"Expected {expected}, but got {result}"

# ❌ 부족한 메시지
assert result == expected
```

---

## 9. pytest Fixture 작성 규칙

### 9.1 WebDriver Fixture는 conftest.py에 배치 (예정)
`conftest.py`에 WebDriver 생성/종료를 담당하는 fixture를 정의합니다.

```python
# 예시 (구현 시 실제 구조 반영)
@pytest.fixture(scope="function")
def driver():
    # WebDriver 생성
    driver = webdriver.Chrome(...)
    yield driver
    # 테스트 후 정리
    driver.quit()
```

### 9.2 Scope 기본값: function
- **기본 scope**: `function` (각 테스트마다 새로운 드라이버 생성)
- **목표**: 테스트 간 상태 격리로 서로 영향을 주지 않도록 보장

### 9.3 Fixture는 yield 패턴으로 리소스 정리 보장
```python
# ✅ 올바른 방식
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()  # 항상 정리됨
```

### 9.4 Page Object Fixture (선택사항)
자주 사용하는 Page 객체도 fixture로 작성하여 테스트에서 재사용합니다.

```python
# 예시
@pytest.fixture
def home_page(driver):
    return HomePage(driver)
```

---

## 10. 테스트 독립성 규칙

### 10.1 테스트 간 실행 순서 의존 금지
- 각 테스트는 **단독 실행 가능**해야 합니다.
- 한 테스트의 결과가 다른 테스트에 영향을 주지 않아야 합니다.

### 10.2 각 테스트는 독립적 셋업/테어다운
```python
# ❌ 금지 - 순서 의존성
def test_login():
    login_page.login(...)

def test_dashboard():  # test_login이 먼저 실행되어야 함
    dashboard_page.verify_widgets()
```

```python
# ✅ 올바른 방식 - 각 테스트 독립적
def test_login(driver):
    login_page = LoginPage(driver)
    login_page.login(...)
    assert login_page.is_logged_in()

def test_dashboard_widgets(driver):
    login_page = LoginPage(driver)
    login_page.login(...)  # 독립적 셋업
    
    dashboard_page = DashboardPage(driver)
    assert dashboard_page.verify_widgets()
```

### 10.3 테스트가 생성한 데이터는 해당 테스트 내에서 정리
가능한 경우, fixture의 yield 후(teardown) 생성한 데이터를 삭제합니다.
(API 호출로 생성한 테스트 사용자 등)

---

## 11. 테스트 데이터 관리 규칙

### 11.1 계정 정보/테스트 데이터는 코드에 하드코딩 금지
```python
# ❌ 금지
def test_login():
    login_page.login("testuser@example.com", "password123")
```

### 11.2 테스트 데이터는 외부 소스에서 관리 (예정)
- **방식 1**: JSON/YAML 파일 (`test_data/` 디렉터리)
  ```python
  # test_data/accounts.json
  {
    "valid_user": {
      "email": "user@example.com",
      "password": "password123"
    }
  }
  ```

- **방식 2**: pytest fixture/factory
  ```python
  @pytest.fixture
  def valid_user():
      return {"email": "user@example.com", "password": "password123"}
  ```

- **방식 3**: 환경변수
  ```python
  user_email = os.getenv("TEST_USER_EMAIL")
  ```

**원칙**: 테스트 데이터를 코드와 분리하여 환경에 따라 쉽게 변경할 수 있도록 합니다.

---

## 12. 환경변수 및 민감정보 관리 규칙

### 12.1 민감정보는 환경변수로 관리
비밀번호, API 키, 토큰 등 민감한 정보는 **절대 코드에 작성하지 않습니다.**

```python
# ❌ 금지
password = "mySecurePassword123"

# ✅ 올바른 방식
password = os.getenv("TEST_PASSWORD")
```

### 12.2 .env 파일 사용 (미생성)
`python-dotenv` 라이브러리를 사용하여 `.env` 파일에서 환경변수 로드:
```python
from dotenv import load_dotenv
load_dotenv()
password = os.getenv("TEST_PASSWORD")
```

### 12.3 .env는 git 미추적 대상
`.gitignore`에 `.env` 추가하여 실수로 인한 민감정보 누출 방지:
```
.env
```

### 12.4 코드/로그/리포트에 민감정보 노출 금지
- 로그 출력 시 비밀번호는 마스킹 처리
- 실패 시 스크린샷에 민감정보가 보이지 않도록 주의
- 테스트 리포트에 계정 정보 노출 금지

---

## 13. Logging 규칙

### 13.1 Python 표준 logging 모듈 사용
```python
import logging

logger = logging.getLogger(__name__)

# ❌ 금지
print("로그인 시도")

# ✅ 올바른 방식
logger.info("로그인 시도")
```

### 13.2 로그 레벨 기준
- **DEBUG**: 상세한 진단 정보 (locator 찾기, 요소 상태 등)
- **INFO**: 주요 액션 (로그인, 페이지 이동, 버튼 클릭 등)
- **WARNING**: 경고 (재시도, 느린 응답 등)
- **ERROR**: 오류 (예외 발생, 요소를 찾지 못함 등)
- **CRITICAL**: 심각한 오류 (드라이버 크래시 등)

### 13.3 로그 포맷 및 저장 위치 (예정)
- 로그 포맷: `[시간] [레벨] [모듈명] [메시지]`
- 저장 경로: `logs/` 디렉터리 (미생성)
- 로테이션: 일일 또는 크기 기반 로테이션 적용 (구현 시 결정)

---

## 14. 테스트 실패 시 Screenshot 저장 규칙

### 14.1 자동 스크린샷 캡처 구조 (예정)
pytest hook을 사용하여 **테스트 실패 시 자동으로 스크린샷을 캡처**하도록 구현할 예정입니다.
- Hook 사용: `pytest_runtest_makereport`
- 실패(FAILED) 상태일 때만 캡처

### 14.2 파일명 규칙
```
screenshots/test_login_failure_2024-07-20_14-30-45.png
```
- 형식: `{테스트_함수명}_{상태}_{타임스탬프}.png`
- 타임스탬프: `YYYY-MM-DD_HH-MM-SS`

### 14.3 저장 경로
모든 스크린샷은 `screenshots/` 디렉터리에 저장합니다. (git 미추적)

### 14.4 민감정보 고려
스크린샷에 비밀번호, 개인정보 등 민감정보가 노출되지 않도록 주의합니다.

---

## 15. 예외 처리 규칙

### 15.1 불필요한 광범위 예외 처리 지양
```python
# ❌ 금지 - 너무 광범위
try:
    login_page.login(email, password)
except Exception:
    logger.error("로그인 실패")
```

### 15.2 구체적 예외만 처리
Selenium에서 발생하는 특정 예외를 명시적으로 처리합니다.

```python
# ✅ 올바른 방식
from selenium.common.exceptions import TimeoutException, NoSuchElementException

try:
    element = wait.until(EC.presence_of_element_located((By.ID, "element")))
except TimeoutException:
    logger.error("요소를 찾을 때까지 타임아웃 발생")
except NoSuchElementException:
    logger.error("요소를 찾을 수 없음")
```

### 15.3 Selenium 관련 예외는 로깅 필수
예외 발생 시 로그를 남겨 나중에 디버깅할 수 있도록 합니다.

```python
except TimeoutException as e:
    logger.error(f"TimeoutException 발생: {str(e)}")
```

---

## 16. Python Coding Convention

### 16.1 PEP8 준수
[Python Enhancement Proposal 8 (PEP8)](https://www.python.org/dev/peps/pep-0008/) 스타일 가이드를 준수합니다.

### 16.2 들여쓰기: 2칸
프로젝트 글로벌 설정에 따라 **2칸 들여쓰기**를 사용합니다.

```python
# ✅ 올바른 방식
class LoginPage(BasePage):
  def login(self, email, password):
    self.find_element(self.EMAIL_INPUT).send_keys(email)
```

### 16.3 타입힌트 권장
메서드 파라미터와 반환값에 타입힌트를 추가하여 코드 가독성을 높입니다.

```python
# ✅ 권장
def login(self, email: str, password: str) -> bool:
    ...

def get_user_count(self) -> int:
    return len(self.find_elements(...))
```

### 16.4 최대 라인 길이: 100자
한 줄을 100자 이내로 유지하여 가독성을 확보합니다.

```python
# ❌ 길이 초과
very_long_variable_name = self.find_element((By.CSS_SELECTOR, "div.container > ul > li:nth-child(3)"))

# ✅ 줄바꿈 처리
element = self.find_element(
    (By.CSS_SELECTOR, "div.container > ul > li:nth-child(3)")
)
```

---

## 17. 파일·클래스·메서드 Naming Convention

### 17.1 파일명: snake_case
```
pages/
├── home_page.py
├── login_page.py
└── dashboard_page.py

tests/
├── test_login.py
├── test_product_search.py
└── test_checkout.py
```

### 17.2 클래스명: PascalCase
```python
class HomePage(BasePage):
    ...

class LoginPage(BasePage):
    ...
```

### 17.3 Page 객체 클래스명 접미사: Page
모든 Page 객체 클래스는 `Page`로 끝납니다.
```python
# ✅ 올바른 방식
class HomePage(BasePage):
    ...

class LoginPage(BasePage):
    ...

# ❌ 금지
class Home(BasePage):
    ...

class LoginScreen(BasePage):
    ...
```

### 17.4 메서드명: snake_case (동사로 시작)
```python
class LoginPage(BasePage):
    def enter_email(self, email: str) -> None:
        ...
    
    def enter_password(self, password: str) -> None:
        ...
    
    def click_login_button(self) -> None:
        ...
    
    def is_login_error_displayed(self) -> bool:
        ...
```

### 17.5 테스트 함수명: test_* 접두사
```python
def test_login_with_valid_credentials():
    ...

def test_login_with_invalid_password():
    ...

def test_product_search_by_name():
    ...
```

### 17.6 변수/함수명: snake_case (영어 사용)
프로젝트 글로벌 설정에 따라 코드에서는 영어를 사용합니다.
```python
search_keyword = "laptop"
product_count = 25
is_logged_in = True
```

---

## 18. 공통 코드와 Utility 분리 기준

### 18.1 공통 화면 조작은 BasePage에 작성
```python
# base_page.py
class BasePage:
    def __init__(self, driver):
        self.driver = driver
    
    # 공통 메서드
    def find_element(self, locator):
        return self.driver.find_element(*locator)
    
    def find_elements(self, locator):
        return self.driver.find_elements(*locator)
    
    def click(self, locator):
        self.find_element(locator).click()
    
    def get_page_title(self) -> str:
        return self.driver.title
```

### 18.2 화면과 무관한 순수 로직은 utils에 분리
```python
# utils/helpers.py
def generate_random_email() -> str:
    """테스트용 임의의 이메일 주소 생성"""
    return f"test_{uuid.uuid4().hex[:8]}@example.com"

def extract_numbers_from_string(text: str) -> list:
    """문자열에서 숫자만 추출"""
    return [int(s) for s in text.split() if s.isdigit()]

def format_date(date_obj, format_string: str) -> str:
    """날짜 포맷팅"""
    return date_obj.strftime(format_string)
```

### 18.3 분리 기준
- **2회 이상 반복**: 중복 코드는 공통 메서드로 분리
- **BasePage**: 모든 Page에서 필요한 화면 조작 (클릭, 입력, 요소 찾기 등)
- **utils**: 화면과 무관한 데이터 처리, 문자열 변환, 헬퍼 함수

---

## 19. 코드 생성 후 실행 및 검증 규칙

### 19.1 코드 생성 후 반드시 테스트 실행
코드 작성을 완료한 후 **반드시 관련 테스트를 실행**하여 동작을 검증합니다.
테스트 실행 없이 "완료"로 간주하지 않습니다.

### 19.2 pytest 실행 방법 (예정)
```bash
# 특정 테스트 파일 실행
pytest tests/test_login.py

# 특정 테스트 함수 실행
pytest tests/test_login.py::test_login_with_valid_credentials

# 모든 테스트 실행
pytest tests/

# 상세 출력 옵션
pytest -v tests/

# HTML 리포트 생성
pytest tests/ --html=reports/report.html
```

### 19.3 pytest-html 리포트 확인
테스트 실행 후 `reports/` 디렉터리에 생성된 HTML 리포트를 브라우저에서 열어 시각적으로 결과를 확인합니다.

### 19.4 검증 체크리스트
- ✅ 테스트 함수가 PASSED 상태인가?
- ✅ 로그에 예상된 INFO/ERROR 메시지가 있는가?
- ✅ 실패한 테스트는 스크린샷이 저장되었는가?
- ✅ 타임아웃이나 예외는 없는가?

---

## 20. Claude 자체 리뷰 체크리스트

코드 생성 후 Claude가 다음 항목을 **자체 검토**합니다. 이 체크리스트를 통과하지 않으면 코드 수정을 진행합니다.

### 20.1 Wait 및 Sleep 관련
- [ ] `time.sleep()`이 코드에 포함되지 않았는가?
- [ ] 모든 요소 조작에 적절한 WebDriverWait가 사용되었는가?
- [ ] Implicit Wait 대신 Explicit Wait가 사용되었는가?

### 20.2 Locator 관련
- [ ] Full XPath가 사용되지 않았는가?
- [ ] 모든 locator가 Page 클래스 상단에 상수/변수로 정의되었는가?
- [ ] locator 우선순위 규칙(id > data-* > name > css > xpath)을 따랐는가?

### 20.3 POM 구조
- [ ] Page Layer에 assertion이 없는가? (assertion은 Test에서만)
- [ ] Page 메서드가 값을 반환하거나 화면을 조작만 하는가?
- [ ] 모든 Page 클래스가 BasePage를 상속하는가?

### 20.4 테스트 독립성
- [ ] 각 테스트가 단독 실행 가능한가?
- [ ] 테스트 간 순서 의존성이 없는가?
- [ ] 테스트가 생성한 데이터를 정리하는가?

### 20.5 민감정보 관리
- [ ] 계정 정보/비밀번호가 코드에 하드코딩되지 않았는가?
- [ ] 민감정보가 환경변수나 외부 파일로 관리되는가?
- [ ] 로그/리포트에 민감정보가 노출되지 않는가?

### 20.6 코딩 컨벤션
- [ ] 파일명이 snake_case인가?
- [ ] 클래스명이 PascalCase이고 Page 객체는 `~Page` 접미사인가?
- [ ] 메서드명이 snake_case이고 동사로 시작하는가?
- [ ] 테스트 함수가 `test_` 접두사로 시작하는가?
- [ ] 2칸 들여쓰기를 사용했는가?
- [ ] 라인 길이가 100자 이내인가?

### 20.7 데이터 및 로깅
- [ ] 테스트 데이터가 외부 소스에서 로드되는가?
- [ ] `print()` 대신 `logging` 모듈을 사용하는가?
- [ ] 예외는 광범위하게 처리하지 않고 구체적으로 처리하는가?

### 20.8 테스트 실행 확인
- [ ] 코드 작성 후 pytest를 실행했는가?
- [ ] 테스트 결과가 PASSED/FAILED/ERROR 상태인가?
- [ ] HTML 리포트가 생성되고 확인되었는가?

---

## 21. 참고 사항

### 21.1 추후 작업
다음 항목들은 아직 생성되지 않았으며, 실제 개발이 시작될 때 작성됩니다:
- 디렉터리 구조 생성
- `conftest.py` 작성 (pytest fixture)
- `base_page.py` 구현 (BasePage 클래스)
- `requirements.txt` 작성 (의존성 패키지)
- `.env` 파일 (환경변수, git 미추적)
- 테스트 데이터 파일 (JSON/YAML)
- GitHub Actions 워크플로우 파일 (`.github/workflows/*.yml`)
- 기능별 명세 문서

### 21.2 문서 유지보수
- 이 문서는 프로젝트 진행 중 새로운 규칙이 발견되면 업데이트합니다.
- 특정 기능의 요구사항이 결정되면 별도의 기능 명세 문서를 작성합니다.
- 모호한 부분이 있으면 Claude에 질문하여 명확히 합니다.

---

**문서 생성 일자**: 2026-07-20  
**버전**: 1.0
