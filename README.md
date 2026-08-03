# AT-EX (Automation Testing - Automation Exercise)

[Automation Exercise](https://automationexercise.com/)를 대상으로 한 웹 UI 회귀 테스트 자동화 프레임워크입니다.
Python + Selenium WebDriver + pytest 기반이며, Page Object Model(POM) 설계를 따릅니다.

## 기술 스택

| 항목 | 기술/도구 |
|------|----------|
| 언어 | Python 3.9 |
| 자동화 도구 | Selenium WebDriver |
| 테스트 러너 | pytest |
| 설계 패턴 | Page Object Model (POM) |
| 리포팅 | pytest-html |
| 실행 브라우저 | Chrome (ChromeDriver) |
| CI/CD | GitHub Actions |

## 디렉터리 구조

```
AT-EX/
├── pages/          # Page Object 클래스 (Locator + 화면 조작 메서드)
├── tests/          # 테스트 케이스 (시나리오 + assertion)
├── utils/          # 공통 유틸리티 (로거, 헬퍼 함수)
├── config/         # 환경 설정 (URL, 타임아웃 등)
├── test_data/      # 테스트 데이터 (JSON)
├── screenshots/    # 테스트 실패 시 자동 저장되는 스크린샷 (git 미추적)
├── reports/        # pytest-html 리포트 (git 미추적)
├── logs/           # 실행 로그 (git 미추적)
├── conftest.py     # pytest fixture 및 훅
├── pytest.ini      # pytest 설정
├── requirements.txt
└── CLAUDE.md       # 프로젝트 공통 개발 규칙
```

## 설치

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 환경변수 설정

`.env.example`을 복사해 `.env`를 생성하고 값을 채웁니다.

```bash
cp .env.example .env
```

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `BASE_URL` | 테스트 대상 사이트 URL | `https://automationexercise.com` |
| `HEADLESS` | 헤드리스 브라우저 실행 여부 (`true`/`false`) | `false` |
| `TEST_USER_EMAIL` | 테스트 계정 이메일 | - |
| `TEST_USER_PASSWORD` | 테스트 계정 비밀번호 | - |

## 테스트 실행

```bash
# 전체 테스트 실행
pytest tests/

# 특정 파일 실행
pytest tests/test_login.py

# 특정 테스트 함수 실행
pytest tests/test_login.py::test_login_with_valid_credentials

# 스모크 테스트만 실행
pytest -m smoke

# HTML 리포트 생성
pytest tests/ --html=reports/report.html
```

테스트 실패 시 `screenshots/` 디렉터리에 `{테스트_함수명}_{상태}_{타임스탬프}.png` 형식으로 스크린샷이 자동 저장됩니다.

## 테스트 범위

| 파일 | 기능 |
|------|------|
| `tests/test_signup.py` | 회원가입 |
| `tests/test_login.py` | 로그인 |
| `tests/test_logout.py` | 로그아웃 |
| `tests/test_product_search.py` | 상품 검색 |
| `tests/test_shopping_cart.py` | 장바구니 |
| `tests/test_smoke.py` | 핵심 동작 스모크 테스트 |

## CI/CD

`.github/workflows/test.yml`에서 push 시 자동으로 pytest를 실행하고, 실패 시 Slack으로 알림을 전송합니다.
GitHub Actions 실행 환경의 일시적인 Cloudflare 봇차단에 대응하기 위해 job을 최대 3회(`attempt-1`~`attempt-3`)까지 새 러너에서 재시도하는 체이닝 구조로 구성되어 있습니다.

## 개발 규칙

프로젝트 공통 개발 규칙(POM 설계 원칙, Locator 작성 원칙, Wait 처리, 코딩 컨벤션 등)은 [`CLAUDE.md`](./CLAUDE.md)를 참고하세요.
기능별 요구사항 명세는 [`docs/prd/`](./docs/prd/) 하위 문서를, 실행 계획 및 진행 상황은 [`docs/ROADMAP.md`](./docs/ROADMAP.md)를 참고하세요.
