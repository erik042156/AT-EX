# 로그아웃 (Logout) 기능 상세 PRD

**작성 일자**: 2026-07-22
**최종 수정일**: 2026-07-23 (v1.4: 사용자 판단에 따라 ABN-002(비로그인 상태 `/logout` URL 직접 접근 시 Django 디버그 트레이스백 페이지 노출)를 자동화 대상에서 완전히 제외함)
**버전**: 1.4
**상태**: 초안 (로그아웃 성공 흐름 중심으로 범위 확정. 비로그인 상태에서 `/logout` URL 직접 접근 시 Django 디버그 트레이스백 페이지가 노출되는 동작은 실제로 확인되었으나, Django `DEBUG` 설정에 의존하는 환경 종속적 시나리오라는 이유로 자동화 대상에서 제외하기로 결정함(구 ABN-002, 섹션 12 참고). Locator는 Page Object 구현 착수 시 사용자가 실시간으로 공유할 예정)

---

## 1. 기능명

- **한국어명**: 로그아웃
- **영문명**: Logout
- **기능 ID**: LOGOUT

---

## 2. 기능 목적

로그인 상태의 사용자가 헤더 네비게이션의 "Logout" 링크를 클릭하여 현재 세션을 종료하고, 비회원(게스트) 상태로 전환할 수 있도록 하는 기능입니다.

### 비즈니스 가치
- 사용자가 공용 PC 등에서 세션을 안전하게 종료할 수 있도록 지원
- 로그인 상태와 비로그인 상태를 명확히 구분하여 개인화된 데이터 노출을 방지
- 로그인 → 로그아웃 → 재로그인의 전체 인증 사이클을 완성하여 회귀 테스트의 기반 마련

---

## 3. 프로젝트 전체 PRD와의 연관성

### 기준 문서
**참고**: `docs/prd/project-prd.md`

### 연관 섹션
- **5.2 MVP 대상 기능**: 우선순위 1 (필수) - 회원가입, 로그인과 함께 로그아웃(세션 종료)이 명시됨 (131행)
- **7.1 MVP 스코프**: "3. 로그아웃 (Logout) - 세션 종료 및 로그아웃 확인" (185-186행)
- **8.1 Phase 1**: 기본 사용자 인증 및 탐색 - "3. 로그아웃(Logout): 로그아웃 버튼 클릭 → 로그아웃 후 홈 페이지 또는 로그인 페이지 리다이렉트 확인" 및 산출물로 `docs/prd/features/logout.md` 명시 (222-224행, 235행)

### 확인 완료 (project-prd.md와의 관계)
- project-prd.md 8.1(224행)에는 로그아웃 후 리다이렉트 대상이 "홈 페이지 또는 로그인 페이지"로 두 가지 가능성이 함께 기술되어 있습니다. 실제로는 login.md의 NOR-002 시나리오(로그아웃 → 로그인 페이지 이동 → 재로그인 성공, login.md 304-324행)를 통해 **로그인 페이지로 리다이렉트되는 것으로 확인**되었습니다. 이는 project-prd.md가 제시한 두 가능성 중 하나를 확정한 것으로, project-prd.md의 내용과 충돌하지 않으며 별도의 project-prd.md 수정은 필요하지 않다고 판단합니다.

### 의존성
- **선행 기능**: 로그인 (Login)
  - 로그아웃을 수행하려면 먼저 로그인 상태여야 함 (login.md 섹션 18, 549행 "로그아웃(Logout): 후행 기능 - 로그인하지 않으면 로그아웃을 할 수 없음" 참고)
- **선행 기능(간접)**: 회원가입 (Signup)
  - 로그인하려면 계정이 먼저 생성되어 있어야 하므로, 로그아웃 테스트 역시 유효한 계정 존재를 전제로 함

---

## 4. 대상 URL 또는 진입 경로

### 로그아웃 관련 URL
**확인 완료**: 로그아웃은 별도의 전용 페이지(화면)를 갖지 않고, 헤더 네비게이션의 "Logout" 링크를 클릭하는 즉시 세션이 종료되며 로그인 페이지로 리다이렉트되는 **액션(action) 성격의 링크**입니다 (login.md NOR-002 시나리오, 304-324행 근거).

- **로그아웃 완료 후 도착 페이지**: `https://automationexercise.com/login` (확인 완료, login.md NOR-002 참고)
- **로그아웃 링크 자체의 실제 요청 URL**: `https://automationexercise.com/logout` (확인 완료 — 실제 사이트 확인 결과, v1.2 신규 반영)
  - 단, 이 URL은 **로그인 상태에서만 정상 동작**하며, 비로그인 상태에서 이 URL에 직접 접근(예: 브라우저 주소창 입력 또는 Selenium `driver.get()` 직접 호출)하면 **Django 프레임워크의 디버그 예외 트레이스백 페이지가 그대로 노출됨**이 실제 화면 스크린샷으로 확인되었습니다 (확인 완료, v1.3). 페이지 헤딩은 `KeyError at /logout`, 예외 값은 `'user_id'`이며, Request Method(GET), Request URL(`https://automationexercise.com/logout`), Django Version(3.2.8), Exception Type(KeyError) 및 `website/views.py, line 216, in logout` → `del request.session['user_id']` 코드가 포함된 traceback이 화면에 그대로 노출됩니다. 즉 사용자 친화적인 "안내" 성격의 에러 페이지가 아니라, 서버가 세션에 없는 `user_id` 키를 삭제하려다 발생한 **미처리 예외(unhandled exception)가 디버그 모드로 그대로 노출되는 화면**입니다. 이 동작은 섹션 9 흐름 3에서 참고 사실로 다루되, Django `DEBUG` 설정에 의존하는 환경 종속적 동작이라는 이유로 자동화 대상에서는 제외합니다 (v1.4, 구 ABN-002, 섹션 12 참고).

### 진입 경로 (사용자 흐름)
1. **로그인 상태의 임의 페이지에서 진입**: 로그인 상태에서는 사이트 내 대부분의 페이지 헤더 네비게이션에 "Logout" 링크가 노출되며, 이를 클릭하여 로그아웃 수행
   - **확인 완료(v1.3)**: 헤더 네비게이션(Logout, Signup/Login, Delete Account, Logged in as {username} 포함)은 사이트 전역에서 위치가 불변인 공통 고정 컴포넌트이므로, "Logout" 링크의 위치는 메인 페이지와 다른 페이지에서 완전히 동일합니다.
   - 이번 PRD의 자동화 대상 시나리오는 **로그인 직후 메인 페이지**에서 로그아웃을 수행하는 경로를 기준으로 하되, 이는 헤더 위치가 페이지마다 달라서가 아니라 대표성 있는 단일 경로로 반복 검증 비용을 줄이기 위한 스코프 결정입니다 (다른 페이지에서의 로그아웃은 섹션 12 자동화 제외 범위 참고)

**참고**: 로그아웃은 로그인 상태에서만 진입 가능한 경로이므로(사전 조건 필수), 로그인하지 않은 상태에서 헤더 "Logout" 링크를 통한 진입 경로는 존재하지 않습니다. 다만 헤더 링크가 아닌 **URL 직접 접근**(`https://automationexercise.com/logout`)은 비로그인 상태에서도 가능하며, 이 경우 Django 디버그 트레이스백 페이지(`KeyError at /logout`)가 노출됨이 확인되었습니다 (확인 완료, 섹션 9 흐름 3 참고).

---

## 5. 사용자 역할

### 대상 사용자
- **기존 회원 (Registered User, 로그인 상태)**: 이미 로그인을 완료하여 세션이 유지 중인 사용자
  - 헤더 네비게이션에 "Logout" 링크가 노출된 상태

### 사용자 시나리오
- 정상 로그아웃: 로그인 직후 또는 임의의 로그인 상태에서 세션을 종료하려는 사용자
- 재로그인을 위한 로그아웃: 다른 계정으로 다시 로그인하기 위해 기존 세션을 종료하려는 사용자

**참고**: 비로그인 상태(Guest)의 사용자는 이 기능의 대상이 아닙니다. 헤더에 "Logout" 링크 자체가 노출되지 않으므로 로그아웃을 시도할 UI 진입점이 없습니다.

---

## 6. 사전 조건 (Precondition)

### 필수 조건
1. **로그인 상태**: 유효한 계정으로 이미 로그인되어 있어야 함 (필수)
   - 이는 로그인 기능(login.md)의 후행 기능이라는 의존성에서 비롯된 것으로, **로그인하지 않은 상태에서는 로그아웃 시나리오 자체가 성립하지 않습니다** (login.md 섹션 18, 549행 근거)
   - 헤더 네비게이션에 "Logout" 링크가 노출되어 있는 상태

2. **브라우저 상태**: 테스트 시작 전 상태
   - 로그인 성공 직후이거나, 유효한 세션이 유지되고 있는 상태

3. **사이트 접근**: Automation Exercise 사이트에 접근 가능
   - 인터넷 연결이 정상
   - 사이트가 운영 중 (다운타임 없음)

### 테스트 데이터 준비
- 로그아웃 테스트를 위해서는 **먼저 유효한 계정으로 로그인을 수행하는 절차가 선행되어야 함**
- 로그아웃 후 재로그인 검증을 위한 동일 계정의 이메일/비밀번호

**모든 로그아웃 테스트 시나리오는 "유효한 계정으로 로그인된 상태"를 사전 조건으로 합니다.** 이는 정상/비정상 시나리오 구분 없이 공통으로 적용됩니다 (섹션 13, 14 참고).

---

## 7. 주요 화면과 UI 요소

### 로그인 상태의 헤더 네비게이션 (로그아웃 직전, 확인 완료 — login.md v1.4 스크린샷 근거)

```
┌───────────────────────────────────────────────────────────────────────────┐
│                          Automation Exercise                              │  (헤더)
│ Home | Products | Cart | Logout | Delete Account | Test Cases |           │  (네비게이션 - 로그인 상태)
│ API Testing | Video Tutorials | Contact us | Logged in as {username}      │
├───────────────────────────────────────────────────────────────────────────┤
│  (페이지 본문 - 메인 페이지 등)                                             │
└───────────────────────────────────────────────────────────────────────────┘
```

**확인 완료(login.md v1.4 스크린샷 근거)**: 로그인 상태의 헤더 네비게이션은 `Home | Products | Cart | Logout | Delete Account | Test Cases | API Testing | Video Tutorials | Contact us | Logged in as {username}` 순서로 구성됩니다. 로그아웃을 수행하면 이 중 "Logout" 링크뿐 아니라 **"Delete Account" 링크와 "Logged in as {username}" 텍스트도 함께 사라진다는 점**이 이번 문서 업데이트의 핵심 반영 사항입니다.

### 로그아웃 클릭 후 도착하는 로그인 페이지 (login.md 섹션 7 참고, 확인 완료)

```
┌───────────────────────────────────────────────────────────────────────────┐
│                          Automation Exercise                              │  (헤더)
│ Home | Products | Cart | Signup / Login | Test Cases | API Testing |      │  (네비게이션 - 로그아웃 상태)
│ Video Tutorials | Contact us                                              │
├───────────────────────────────────────────────────────────────────────────┤
│        Login to Your Account        │  (페이지 제목)
│  ┌───────────────────────────────┐  │
│  │ Email Address *               │  │
│  │ Password *                    │  │
│  │  [   Login   ]                │  │
│  └───────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────────┘
```

**확인 완료(login.md v1.3~v1.4 스크린샷 근거)**: 로그아웃 후 헤더 네비게이션에는 "Login"과 "Signup"이 각각 별도의 링크로 노출되는 것이 아니라, **"Signup / Login"이라는 하나의 통합 링크**로 노출됩니다.

### 주요 UI 요소

| 요소명 | 타입 | 설명 | 필수 여부 |
|--------|------|------|---------|
| **Logout 링크** | Link/Button (헤더 네비게이션) | 로그인 상태에서만 노출되며, 클릭 시 세션 종료 및 로그인 페이지로 이동을 트리거함 | 필수(로그인 상태에서) |
| **Signup / Login 통합 링크** | Link (헤더 네비게이션) | 로그아웃 완료 후 노출되는 **하나의 통합 링크**("Login"과 "Signup"이 별도 링크가 아님, 확인 완료). 클릭 시 로그인 페이지로 이동 | 조건부(로그아웃 상태에서 노출) |
| **Delete Account 링크** | Link (헤더 네비게이션) | 로그인 상태(로그아웃 직전)에서만 노출되며, 로그아웃 완료 후에는 더 이상 노출되지 않음 (확인 완료, login.md v1.4 스크린샷 근거 — 신규 반영) | 조건부(로그인 상태에서만 노출, 로그아웃 시 소멸) |
| **Logged in as {username} 텍스트** | Text (헤더 네비게이션) | 로그인 상태(로그아웃 직전)에서만 노출되며, 로그아웃 완료 후에는 더 이상 노출되지 않음. {username}은 회원가입 시 "Name" 필드 입력값 그대로 표시 (확인 완료, login.md v1.4 근거 — 신규 반영) | 조건부(로그인 상태에서만 노출, 로그아웃 시 소멸) |

### 확인 완료
- 로그인 상태에서는 헤더 네비게이션에 "Logout", "Delete Account" 링크와 "Logged in as {username}" 텍스트가 노출되고, 로그아웃 후에는 이 세 요소가 모두 사라지며 대신 "Signup / Login" 통합 링크가 노출됨 (login.md LOGIN-REQ-003, LOGIN-REQ-007, LOGIN-REQ-008 및 섹션 7 스크린샷 근거)
- Logout 클릭 → 로그인 페이지로 이동 (login.md NOR-002 시나리오 근거)
- 로그아웃 후 헤더에 노출되는 링크는 "Login"/"Signup" 개별 링크가 아니라 **"Signup / Login" 하나의 통합 링크**임 (login.md v1.3~v1.4 스크린샷 근거)
- Logout 클릭 시 별도의 확인(confirm) 다이얼로그는 **존재하지 않으며**, 클릭 즉시 로그아웃이 처리됨 (확인 완료 — 실제 사이트 확인 결과, v1.2 신규 반영)
- Logout 링크의 실제 요청 URL은 `https://automationexercise.com/logout`이며, 비로그인 상태에서 이 URL에 직접 접근하면 Django 프레임워크의 디버그 예외 트레이스백 페이지(`KeyError at /logout`)가 노출됨 (확인 완료 — 실제 화면 스크린샷 확인 결과, v1.3 신규 반영·정정, 섹션 4 참고)
- "Logout" 링크의 위치(헤더 내 순서)는 메인 페이지와 다른 페이지에서 완전히 동일함 — 헤더 네비게이션 자체가 사이트 전역에서 위치가 불변인 공통 고정 영역(컴포넌트)이기 때문 (확인 완료 — 실제 화면 스크린샷 확인 결과, v1.3 신규 반영)

### 확인 필요
- 각 UI 요소의 HTML id, CSS 클래스, data-* 속성: Page Object 구현 착수 시 사용자가 실시간으로 공유할 예정이며, 별도의 사전 개발자 도구 조사는 필요하지 않음

---

## 8. 정상 사용자 흐름 (Happy Path)

**확인 완료**: 아래 흐름은 login.md NOR-002 시나리오에서 확인된 실제 사이트 동작을 로그아웃 기능 관점에서 재정리한 것입니다.

### 흐름 1: 로그인 상태에서 정상 로그아웃

**시작 조건**: 유효한 계정으로 로그인 완료, 메인 페이지 헤더에 "Logout" 링크가 노출된 상태. 이때 헤더에는 "Logout" 링크뿐 아니라 **"Delete Account" 링크와 "Logged in as {username}" 텍스트도 함께 노출**되어 있음 (확인 완료, login.md v1.4 스크린샷 근거)

**단계별 행동**:
1. 사용자가 로그인 상태의 메인 페이지(`https://automationexercise.com/`)에 있음
2. 헤더 네비게이션에서 "Logout" 링크 클릭
3. 시스템이 세션을 종료함
4. 로그인 페이지(`https://automationexercise.com/login`)로 리다이렉트됨 (확인 완료)
5. 로그인 페이지 헤더 네비게이션에 "Signup / Login" 통합 링크가 노출됨 ("Logout", "Delete Account" 링크와 "Logged in as {username}" 텍스트는 더 이상 노출되지 않음)

**기대 결과**:
- URL 변경: 메인 페이지(또는 로그인 상태의 임의 페이지) → 로그인 페이지(`https://automationexercise.com/login`)
- 헤더 네비게이션에 "Signup / Login" 통합 링크 노출, "Logout", "Delete Account" 링크와 "Logged in as {username}" 텍스트는 노출되지 않음

**소요 시간**: 약 1~2초 (네트워크 지연 포함, 추정)

---

## 9. 예외 사용자 흐름 (Exception Flow)

### 흐름 1: 로그아웃 후 브라우저 뒤로가기(Back)로 이전 화면 재접근 시도 (자동화 범위에서 제외하기로 결정됨)

**설명**: 로그아웃 완료 후 브라우저의 "뒤로가기" 버튼을 눌러 로그인 상태였던 이전 화면(예: 메인 페이지, 장바구니 등)으로 돌아가려는 시도입니다. **스코프 결정(v1.2)**: 이 흐름의 실제 동작(캐시된 화면 노출 여부, 재리다이렉트 여부 등)이 무엇으로 확인되든 상관없이, 세션/쿠키 값 자체를 검증하는 영역과 맞닿아 있다는 이유로 이번 자동화 범위에서 **제외하기로 결정**하였습니다. 즉 "실제 동작을 몰라서" 제외하는 것이 아니라, "실제 동작 여부와 무관하게 자동화하지 않기로" 확정한 스코프 결정 사항입니다 (섹션 12, 섹션 14 ABN-001, 섹션 20 참고).

### 흐름 2: 세션 만료 후 로그아웃 시도 (자동화 범위에서 제외됨)

**설명**: 세션이 이미 만료된 상태에서 "Logout" 링크를 클릭하는 흐름입니다. 세션 타임아웃 시간 자체가 프로젝트 전체 차원에서 미확정이므로(project-prd.md 19.1, 813-816행), 이 흐름에 대한 실제 동작 검증은 이번 자동화 범위에서 제외합니다 (섹션 12, 섹션 20 참고).

### 흐름 3: 로그인하지 않은 상태에서 로그아웃 시도

**설명(UI 진입점 관점)**: 로그아웃은 로그인의 후행 기능이므로, 로그인하지 않은 상태에서는 헤더에 "Logout" 링크 자체가 노출되지 않아 **UI를 통한** 로그아웃 시도 진입점은 없습니다. 이 관점에서는 시나리오 자체가 성립하지 않으며, 별도의 테스트 케이스로 작성하지 않습니다 (섹션 6, 18 참고).

**설명(URL 직접 접근 관점, 확인 완료 — v1.2 반영, v1.3 세부 확정, v1.4 자동화 범위 제외 결정)**: 다만 UI 진입점 여부와 별개로, Selenium `driver.get()` 등으로 로그아웃 URL(`https://automationexercise.com/logout`)에 **직접 접근**하는 것은 일반적인 자동화 테스트 범위에 해당할 수 있습니다. 실제 화면 스크린샷 확인 결과, 비로그인 상태에서 이 URL에 직접 접근하면 사용자 친화적 에러 안내 페이지가 아니라 **Django 프레임워크의 디버그 예외 트레이스백 페이지**(헤딩 `KeyError at /logout`, 예외 값 `'user_id'`)가 그대로 노출됨이 확인되었습니다 (확인 완료, v1.3).

다만 이 화면은 Django `DEBUG` 설정 값에 따라 노출 형태가 달라지는 프레임워크 차원의 디버그 화면이며, 운영 환경에서 `DEBUG=False`로 전환되면 다른 형태(예: 일반 500 에러 페이지)가 노출될 수 있는 환경 종속적 동작입니다. 이에 따라 사용자는 이 흐름(구 ABN-002)을 **자동화 대상에서 완전히 제외하기로 결정**하였습니다 (스코프 결정, v1.4. 섹션 12, 섹션 20 참고).

---

## 10. 기능 요구사항

### 요구사항 정의

**LOGOUT-REQ-001**: 로그인 상태에서 로그아웃 진입점 제공
- 사용자가 로그인 상태인 경우, 헤더 네비게이션 영역에 "Logout" 링크가 노출되어야 한다. (login.md LOGIN-REQ-003과 연동)
- 참고: 이때 헤더 네비게이션에는 "Logout" 링크와 함께 "Delete Account" 링크, "Logged in as {username}" 텍스트도 함께 노출된다 (login.md LOGIN-REQ-007, LOGIN-REQ-008 근거, 확인 완료). 다만 이 두 요소 자체의 노출 요구사항은 로그인 기능(login.md)에서 정의하며, 이 문서에서는 로그아웃 시 이 두 요소가 사라진다는 점만 요구사항으로 다룬다(LOGOUT-REQ-003 참고).

**LOGOUT-REQ-002**: 로그아웃 수행
- 사용자가 "Logout" 링크를 클릭하면, 시스템은 현재 세션을 종료해야 한다.
- 세션 종료 후, 사용자는 로그인 페이지(`https://automationexercise.com/login`)로 이동해야 한다. (확인 완료)

**LOGOUT-REQ-003**: 로그아웃 상태 표시
- 로그아웃 완료 후 헤더 네비게이션 영역에 "Signup / Login" 통합 링크가 노출되어야 한다. ("Login"과 "Signup"이 각각 별도로 노출되는 것이 아니라 하나의 통합 링크로 노출됨, 확인 완료 — login.md v1.3~v1.4 스크린샷 근거)
- 로그아웃 완료 후에는 "Logout" 링크가 더 이상 노출되지 않아야 한다.
- 로그아웃 완료 후에는 "Delete Account" 링크와 "Logged in as {username}" 텍스트가 더 이상 노출되지 않아야 한다 (신규 반영, login.md v1.4 스크린샷 근거).

**LOGOUT-REQ-004**: 로그아웃 후 재로그인 가능
- 로그아웃 완료 후, 사용자는 동일한 이메일과 비밀번호로 다시 로그인할 수 있어야 한다.
- 재로그인 성공 시 헤더 네비게이션에 "Logout" 링크가 다시 노출되어야 한다.

**LOGOUT-REQ-005**: 세션/쿠키 값 자체는 요구사항 대상 외
- 로그아웃 시 세션/쿠키가 서버 또는 브라우저에서 실제로 어떻게 삭제·만료 처리되는지에 대한 구체적인 요구사항은 정의하지 않는다. 로그인/로그아웃 상태 판단은 오직 화면에 노출되는 텍스트/링크("Logout", "Delete Account", "Logged in as {username}" 또는 "Signup / Login")를 기준으로 한다 (섹션 12 참고).

---

## 11. 자동화 대상 범위

### 자동화 범위 (포함)

| 시나리오 | 자동화 대상 | 설명 |
|---------|-----------|------|
| **정상 로그아웃** | ✅ 포함 | 로그인 상태에서 "Logout" 클릭 → 로그인 페이지로 리다이렉트 확인 |
| **로그아웃 상태 표시** | ✅ 포함 | 로그아웃 후 헤더에 "Signup / Login" 통합 링크 노출, "Logout" 링크 미노출 확인 |
| **로그아웃 후 재로그인 가능 여부** | ✅ 포함 | 로그아웃 후 동일 계정으로 재로그인 성공 확인 |

---

## 12. 자동화 제외 범위

### 자동화 제외 사유

| 기능 | 제외 사유 |
|------|---------|
| **세션/쿠키 자체의 값 검증** | 이번 범위에서는 세션/쿠키 자체를 검증하지 않으며, 로그인/로그아웃 상태는 화면 요소(헤더의 "Logout" 또는 "Signup / Login" 통합 링크 노출 여부)로만 판단함 (login.md 섹션 12, 267행 원칙과 동일) |
| **세션 타임아웃/만료 후 동작 검증** | 세션 타임아웃 시간 자체가 프로젝트 전체 차원에서 미확정 (project-prd.md 19.1, 813-816행). 확정 전까지 자동화 대상에서 제외 |
| **로그아웃 후 브라우저 뒤로가기(Back) 동작 검증** | 실제 동작 여부와 무관하게 자동화 범위에서 제외하기로 결정함 (스코프 결정, v1.2 정정 — 세션/쿠키 검증 영역과 맞닿아 있다는 이유로 확정된 것이며, "실제 동작 미확인"이 제외 사유가 아님) |
| **로그인하지 않은 상태에서 헤더 "Logout" 링크를 통한 로그아웃 시도** | 로그아웃은 로그인의 후행 기능으로, 로그인하지 않은 상태에서는 헤더에 "Logout" 링크 자체가 노출되지 않아 UI 진입점을 통한 시나리오는 성립하지 않음 (섹션 9 흐름 3 참고) |
| **비로그인 상태에서 `/logout` URL 직접 접근 시 노출되는 화면(Django 디버그 트레이스백 페이지) 검증** | 환경 의존적(Django DEBUG 설정)이라 자동화 대상에서 제외하기로 결정 (구 ABN-002, v1.4 스코프 결정. 실제 동작 자체는 확인되었으나, 운영 환경에서 `DEBUG=False`로 전환 시 노출 형태가 달라질 수 있는 환경 종속성을 이유로 제외) |
| **다중 탭/다중 세션 로그아웃 동기화** | 여러 브라우저 탭/세션 간 로그아웃 전파 여부는 인프라 수준의 검증이며 MVP 범위 밖 |
| **로그아웃 API/서버 측 세션 삭제 로직 검증** | 백엔드 구현 세부사항으로 테스트 불필요 |
| **메인 페이지 외 다른 페이지(장바구니, 상품 상세 등)에서의 로그아웃** | (1) 헤더 네비게이션(Logout 링크 포함)이 사이트 전역에서 위치가 불변인 공통 고정 컴포넌트임이 실제 화면 스크린샷으로 확인되어(확인 완료, v1.3), "Logout" 링크 자체가 페이지마다 다르지 않으므로 페이지별 반복 클릭 테스트가 추가로 검증할 내용이 없음. (2) 이와 별개로, 장바구니 페이지에서 상품 결제를 시도하면 로그인을 안내하는 모달이 노출되는 것이 확인되어(확인 완료, v1.2), 인증이 필요한 상황에서 로그인을 유도하는 메커니즘도 페이지와 무관하게 전역적으로 일관되게 동작함을 근거로 페이지별 반복 테스트는 불필요하다고 판단함 (제외 사유 정정 — 기존 "미확인이라서"에서 "확인된 두 가지 전역 메커니즘에 근거해 불필요"로 변경) |

---

## 13. 정상 시나리오 (Normal Scenarios)

### NOR-001: 로그인 상태에서 정상 로그아웃

**시나리오명**: 로그인한 사용자가 "Logout" 링크를 클릭하여 세션 종료

**전제조건**:
- 유효한 계정(예: 이메일 `test001@example.com`, 비밀번호 `password123`)으로 로그인이 완료된 상태
- 메인 페이지 헤더 네비게이션에 "Logout" 링크가 노출됨 (이때 "Delete Account" 링크와 "Logged in as {username}" 텍스트도 함께 노출됨, 확인 완료)

**테스트 단계**:
1. (사전 준비) 유효한 계정으로 로그인 수행 (login.md NOR-001 참고)
2. 메인 페이지 헤더 네비게이션에서 "Logout" 링크 클릭
3. 페이지 전환 완료 대기

**기대 결과**:
- URL이 로그인 페이지(`https://automationexercise.com/login`)로 변경됨
- 헤더 네비게이션에 "Signup / Login" 통합 링크가 노출되고, "Logout", "Delete Account" 링크와 "Logged in as {username}" 텍스트는 노출되지 않음

**검증 포인트**:
- ✅ 페이지 URL이 로그인 페이지로 변경되었는가?
- ✅ 헤더 네비게이션에 "Signup / Login" 통합 링크가 노출되었는가?
- ✅ 헤더 네비게이션에 "Logout" 링크가 더 이상 노출되지 않는가?
- ✅ 헤더 네비게이션에 "Delete Account" 링크가 더 이상 노출되지 않는가? (신규, login.md v1.4 근거)
- ✅ 헤더 네비게이션에 "Logged in as {username}" 텍스트가 더 이상 노출되지 않는가? (신규, login.md v1.4 근거)

**예상 실행 시간**: 약 2~3초 (로그인 사전 준비 포함 시 추가 소요)

---

### NOR-002: 로그아웃 후 동일 계정으로 재로그인 성공

**시나리오명**: 로그아웃한 사용자가 동일 계정으로 다시 로그인하여 정상적으로 세션이 재생성됨을 확인

**전제조건**:
- NOR-001 시나리오가 완료되어 로그인 페이지에 있는 상태

**참고**: 이 시나리오는 login.md의 NOR-002("로그아웃 후 재로그인 성공")와 동일한 사용자 흐름을 다루되, login.md에서는 **로그인 기능의 재사용성**(재로그인 성공 여부) 관점에서, 이 문서에서는 **로그아웃 기능이 재로그인이 가능한 정상 상태로 세션을 종료했는지** 관점에서 검증합니다. 실제 테스트 코드는 중복 구현하지 않고 공용 헬퍼/픽스처로 재사용하는 것을 권장합니다 (섹션 19 참고).

**테스트 단계**:
1. 로그인 페이지에서 로그아웃에 사용했던 계정의 이메일과 비밀번호로 재로그인 수행
2. 로그인 성공 확인

**기대 결과**:
- 재로그인 성공 시 메인 페이지로 이동하며, 헤더 네비게이션에 "Logout" 링크가 다시 노출됨

**검증 포인트**:
- ✅ 재로그인 후 URL이 메인 페이지로 변경되었는가?
- ✅ 재로그인 후 헤더 네비게이션에 "Logout" 링크가 다시 노출되는가?

---

## 14. 비정상 시나리오 (Abnormal Scenarios)

### ABN-001: 로그아웃 후 뒤로가기(Back)로 이전 화면 접근 시도 (자동화 범위에서 제외하기로 결정됨)

**시나리오명**: 로그아웃 완료 후 브라우저 뒤로가기 버튼을 눌러 로그인 상태였던 화면 접근을 시도

**설명**: 이 시나리오는 세션/쿠키 자체의 동작과 밀접하게 연관되어 있어, **실제 동작(캐시된 화면 노출 여부, 로그인 페이지로 재리다이렉트 여부 등) 여부와 무관하게 자동화 범위에서 제외하기로 결정**하였습니다 (스코프 결정, v1.2 정정. 섹션 9 흐름 1, 섹션 12 참고).

**비고**: 로그아웃 기능은 단일 링크 클릭으로 수행되는 액션이며 별도의 입력 필드가 없어, 로그인 기능과 같은 형태의 "잘못된 입력값" 기반 비정상 시나리오는 존재하지 않습니다. 이번 PRD에서 식별된 비정상 시나리오는 ABN-001(자동화 범위 제외로 결정됨) 및 비로그인 상태에서 `/logout` URL 직접 접근 시나리오(구 ABN-002, Django DEBUG 설정에 의존하는 환경 종속적 시나리오로 v1.4에서 자동화 대상에서 완전히 제외됨, 섹션 12 참고)이며, 결과적으로 이 기능에 대해 실제로 작성되는 자동화 테스트 케이스는 없습니다.

---

## 15. 기대 결과 (Expected Results)

### 성공 케이스 기대 결과

| 시나리오 | 페이지 상태 | 메시지/표시 |
|---------|-----------|-----------|
| **NOR-001** | 로그인 페이지(`/login`) | 헤더 네비게이션에 "Signup / Login" 통합 링크 노출, "Logout"/"Delete Account"/"Logged in as {username}"는 미노출 |
| **NOR-002** | 메인 페이지(`/`) | 헤더 네비게이션에 "Logout" 다시 노출 |

### 제외 케이스 (참고용, 자동화 대상 아님)

| 시나리오 | 상태 |
|---------|------|
| **ABN-001** | 자동화 범위에서 제외하기로 결정됨 (스코프 결정, 실제 동작 여부와 무관 — 섹션 12, 14 참고) |
| **비로그인 상태에서 `/logout` URL 직접 접근 (구 ABN-002)** | 자동화 범위에서 제외됨 (v1.4 스코프 결정). 비로그인 상태에서 이 URL에 직접 접근하면 Django 디버그 트레이스백 페이지(헤딩 "KeyError at /logout", 예외 값 `'user_id'`)가 노출됨은 실제로 확인되었으나, Django `DEBUG` 설정에 의존하는 환경 종속적 동작이라는 이유로 사용자 판단에 따라 자동화 대상에서 제외 — 섹션 12, 14 참고 |

---

## 16. 주요 검증 포인트 (Assertion Points)

### 정상 로그아웃 검증

```
테스트 흐름:
1. (사전 준비) 유효한 계정으로 로그인 수행
   → 검증: 로그인 성공 후 헤더에 "Logout" 링크가 노출되는가?

2. 헤더 네비게이션에서 "Logout" 링크 클릭
   → 확인 완료(v1.2): 별도의 확인(confirm) 다이얼로그 없이 클릭 즉시 처리됨 (로딩 표시 자체의 유무는 추정 상태 유지)

3. 페이지 리다이렉트
   → 검증: URL이 로그인 페이지(`/login`)로 변경되었는가?

4. 로그아웃 상태 확인
   → 검증: 헤더 네비게이션에 "Signup / Login" 통합 링크가 노출되었는가?
   → 검증: 헤더 네비게이션에 "Logout" 링크가 더 이상 노출되지 않는가?
   → 검증: 헤더 네비게이션에 "Delete Account" 링크가 더 이상 노출되지 않는가? (신규)
   → 검증: 헤더 네비게이션에 "Logged in as {username}" 텍스트가 더 이상 노출되지 않는가? (신규)

5. 재로그인 확인 (NOR-002)
   → 검증: 동일 계정으로 재로그인 시 메인 페이지로 이동하고 "Logout"이 다시 노출되는가?
```

### 프로그래밍적 검증 (pytest에서 - 예시, 실제 코드 아님)

```python
# 예시 (구현 시 실제 코드는 테스트 레이어에서 작성)

# 사전 준비: 로그인
login_page.enter_email("test001@example.com")
login_page.enter_password("password123")
login_page.click_login_button()

home_page = HomePage(driver)
assert home_page.is_logout_link_displayed() == True

# 로그아웃 수행
home_page.click_logout_link()

login_page_after_logout = LoginPage(driver)
# 로그아웃 후 로그인 페이지로 이동했는지 확인
assert login_page_after_logout.is_on_login_page() == True
# 로그아웃 후 Signup / Login 통합 링크가 노출되고 Logout 링크는 노출되지 않는지 확인
assert login_page_after_logout.is_signup_login_link_displayed() == True
assert login_page_after_logout.is_logout_link_displayed() == False
# 로그아웃 후 Delete Account 링크, Logged in as {username} 텍스트도 더 이상 노출되지 않는지 확인 (신규)
assert login_page_after_logout.is_delete_account_link_displayed() == False
assert login_page_after_logout.is_logged_in_username_displayed() == False

# 재로그인 확인 (NOR-002)
login_page_after_logout.enter_email("test001@example.com")
login_page_after_logout.enter_password("password123")
login_page_after_logout.click_login_button()

home_page_after_relogin = HomePage(driver)
assert home_page_after_relogin.is_logout_link_displayed() == True

# 참고: 비로그인 상태에서 `/logout` URL에 직접 접근하는 시나리오(구 ABN-002)는
# Django DEBUG 설정에 의존하는 환경 종속적 동작이라는 이유로 자동화 대상에서 제외되었으므로
# (v1.4 스코프 결정, 섹션 12, 14, 20 참고) 별도의 테스트 코드를 작성하지 않는다.
```

---

## 17. 필요한 테스트 데이터

### 테스트 계정 정보

| 용도 | 이메일 | 비밀번호 | 상태 | 비고 |
|------|--------|---------|------|------|
| **로그아웃 테스트** | `test001@example.com` | `password123` | 활성 | 사전 생성된 계정, 로그인 후 로그아웃 수행 |
| **로그아웃 후 재로그인 테스트** | `test001@example.com` | `password123` | 활성 | 위와 동일 계정을 재사용하여 재로그인 검증 |

**참고**: 로그아웃 기능은 별도의 신규 계정 정보를 필요로 하지 않으며, login.md에서 정의한 사전 생성 테스트 계정을 그대로 재사용할 수 있습니다 (login.md 섹션 17 참고).

### 테스트 데이터 관리 방식

**방식 1: 환경변수 (.env 파일)**
```
TEST_EMAIL=test001@example.com
TEST_PASSWORD=password123
```

**방식 2: JSON 파일 (test_data/accounts.json)** - login.md와 공유
```json
{
  "valid_account": {
    "email": "test001@example.com",
    "password": "password123"
  }
}
```

**방식 3: pytest Fixture (conftest.py)**
```python
@pytest.fixture
def logged_in_user(driver, valid_login_credentials):
    """로그아웃 테스트 사전 준비: 로그인을 수행한 상태를 반환"""
    login_page = LoginPage(driver)
    login_page.navigate_to_login()
    login_page.enter_email(valid_login_credentials["email"])
    login_page.enter_password(valid_login_credentials["password"])
    login_page.click_login_button()
    return valid_login_credentials
```

### 데이터 보호 규칙
- ❌ 비밀번호를 코드에 하드코딩하지 않음
- ❌ 로그 또는 리포트에 비밀번호 노출 금지
- ✅ 환경변수 또는 외부 파일에서 관리
- ✅ 민감정보는 마스킹 처리하여 로깅
- ✅ login.md에서 정의한 테스트 계정을 재사용하여 별도의 계정 관리 부담 최소화

### 확인 완료
- Automation Exercise에서 동일 이메일로 중복 가입 불가 (확인 완료, signup.md 섹션 9 참고)
- 테스트 계정 준비 방식: 사전 생성 (login.md 섹션 17 근거, 이 기능도 동일 방식 적용)

---

## 18. 다른 기능과의 의존성

### 이 기능이 의존하는 다른 기능

| 기능 | 의존 관계 | 설명 |
|------|---------|------|
| **로그인 (Login)** | 선행 필수 | 로그아웃을 수행하려면 먼저 로그인 상태여야 함. **로그인하지 않은 상태에서는 로그아웃 시나리오 자체가 성립하지 않음** (login.md 섹션 18, 549행 근거) |
| **회원가입 (Signup)** | 간접 선행 필수 | 로그인하려면 계정이 먼저 생성되어 있어야 하므로, 로그아웃 테스트도 회원가입된 계정 존재를 전제로 함 |

### 이 기능을 필요로 하는 다른 기능

| 기능 | 의존 관계 | 설명 |
|------|---------|------|
| **로그인 (Login)** | 재검증 관계 | 로그아웃 후 재로그인 성공 여부를 검증하는 데 로그아웃 기능이 필요함 (login.md NOR-002와 상호 참조) |
| **통합 회귀 테스트** | 전체 흐름 구성 요소 | 회원가입 → 로그인 → 로그아웃 → 재로그인의 전체 인증 사이클 테스트에 필요 |

### login.md와의 정합성 확보 (확인 완료)

login.md는 v1.3~v1.4 업데이트에서 실제 사이트 스크린샷을 근거로 (1) 로그인되지 않은 상태의 헤더에는 "Login"/"Signup"이 각각 노출되는 것이 아니라 "Signup / Login" 하나의 통합 링크로 노출된다는 점, (2) 로그인 상태의 헤더에는 "Logout" 외에도 "Delete Account" 링크와 "Logged in as {username}" 텍스트가 함께 노출된다는 점을 확정하였습니다. login.md 섹션 18에는 이 문서(logout.md)가 아직 이 사실을 반영하지 못했다는 점이 참고사항으로 남아있었으며, 이번 업데이트(v1.1)로 해당 지적사항을 모두 반영하여 **login.md와의 정합성을 확보하였습니다** (섹션 7, 8, 10, 13, 15, 16, 19, 20 전반에 반영).

### 의존성 흐름도

```
회원가입 (Signup)
    ↓
로그인 (Login)
    ↓
홈 페이지 (메인 페이지, 헤더에 "Logout", "Delete Account" 링크와 "Logged in as {username}" 텍스트 노출)
    ↓
로그아웃 (Logout) ← [이 기능]
    ↓
로그인 페이지 (헤더에 "Signup / Login" 통합 링크 노출, "Logout"/"Delete Account"/"Logged in as {username}"는 사라짐)
    ↓
재로그인 (Login, NOR-002)
```

---

## 19. 자동화 구현 시 고려사항

**안내**: 아래 코드는 구조 설명을 위한 예시(스텁)이며 실제 동작 코드는 아닙니다. **Locator 값은 예시이며, 실제 id/name/data-* 속성은 Page Object 구현 착수 시 사용자가 실시간으로 공유할 예정입니다.**

### Page Object 설계 방향

#### 페이지/책임 분리

| 화면 | 담당 Page 클래스 | 책임 |
|------|-----------------|------|
| 로그인 상태의 헤더(메인 페이지 등) | `HomePage` (또는 공통 헤더를 다루는 BasePage 확장) | "Logout" 링크 클릭, "Logout"/"Delete Account" 링크 및 "Logged in as {username}" 텍스트 노출 여부 조회 |
| 로그아웃 완료 후 이동하는 로그인 페이지 | `LoginPage` (login.md에서 정의) | "Signup / Login" 통합 링크 노출 여부 조회, 재로그인 수행 |

**참고**: "Logout" 링크는 로그인 상태의 여러 페이지 헤더에 공통으로 노출되는 요소이므로, `HomePage`에 국한하지 않고 `BasePage`(또는 헤더 전용 컴포넌트 클래스)에 `click_logout_link()`, `is_logout_link_displayed()` 메서드를 두어 어느 페이지에서든 재사용 가능하도록 설계하는 것을 권장합니다. 마찬가지로 "Delete Account" 링크, "Logged in as {username}" 텍스트 조회 메서드도 로그인 상태 헤더에서 공통으로 사용되므로 동일한 위치에 두는 것을 권장합니다 (login.md v1.4 섹션 19 네이밍 권고와 일관). **이 권장 사항은 v1.3에서 실제 화면 스크린샷으로 헤더 네비게이션이 사이트 전역에서 위치가 불변인 공통 고정 컴포넌트임이 확정됨에 따라, 더 이상 추정이 아니라 확인된 사실에 근거한 설계 방향입니다.**

#### HomePage(헤더 공통 영역) 클래스 구조 예시 (예시 - 구현은 별도 작성)

```python
# pages/home_page.py 구조 (실제 코드 아님)
# 아래 Locator 값은 예시이며, 실제 값은 Page Object 구현 착수 시 사용자가 공유할 예정입니다.

class HomePage(BasePage):
    # Locator 정의 (상수) - 헤더 네비게이션 공통 요소
    LOGOUT_LINK = (By.CSS_SELECTOR, "a[href*='logout']")
    # "Login"과 "Signup"은 별도 링크가 아니라 하나의 통합 링크이므로 Locator도 하나로 통합 (확인 완료)
    SIGNUP_LOGIN_LINK = (By.CSS_SELECTOR, "a[href*='login']")
    DELETE_ACCOUNT_LINK = (By.CSS_SELECTOR, "a[href*='delete_account']")
    LOGGED_IN_AS_TEXT = (By.CSS_SELECTOR, "li a.dropdown-toggle")

    def click_logout_link(self) -> None:
        """헤더 네비게이션의 Logout 링크 클릭"""
        pass

    def is_logout_link_displayed(self) -> bool:
        """헤더 네비게이션에 Logout 링크가 노출되는지 여부 반환"""
        pass

    def is_signup_login_link_displayed(self) -> bool:
        """헤더 네비게이션에 Signup / Login 통합 링크가 노출되는지 여부 반환
        (기존 is_login_link_displayed()/is_signup_link_displayed() 2개 메서드를
        하나로 통합. login.md v1.4 네이밍 권고 반영)"""
        pass

    def is_delete_account_link_displayed(self) -> bool:
        """헤더 네비게이션에 Delete Account 링크가 노출되는지 여부 반환 (신규)"""
        pass

    def is_logged_in_username_displayed(self) -> bool:
        """헤더 네비게이션에 'Logged in as {username}' 텍스트가 노출되는지 여부 반환 (신규)"""
        pass

    def get_logged_in_username(self) -> str:
        """'Logged in as {username}' 텍스트에서 {username} 부분만 추출하여 반환 (신규,
        login.md의 HomePage.get_logged_in_username()과 동일한 메서드를 공유하는 것을 권장)"""
        pass
```

#### LoginPage 확장 (login.md 기준, 로그아웃 관점 메서드 추가)

```python
# pages/login_page.py 구조 (실제 코드 아님, login.md의 LoginPage에 아래 메서드 추가를 권장)

class LoginPage(BasePage):
    # ... login.md에서 정의한 기존 Locator/메서드 ...

    def is_on_login_page(self) -> bool:
        """현재 URL이 로그인 페이지인지 여부 반환 (login.md에서 이미 정의됨)"""
        pass

    def is_signup_login_link_displayed(self) -> bool:
        """로그아웃 완료 후 헤더에 Signup / Login 통합 링크가 노출되는지 여부 반환
        (login.md v1.4 네이밍 권고에 따라 is_login_link_displayed()에서 이름 변경)"""
        pass

    def is_delete_account_link_displayed(self) -> bool:
        """로그아웃 완료 후 헤더에 Delete Account 링크가 노출되지 않아야 함을 확인하기 위한 조회 메서드 (신규)"""
        pass

    def is_logged_in_username_displayed(self) -> bool:
        """로그아웃 완료 후 헤더에 'Logged in as {username}' 텍스트가 노출되지 않아야 함을 확인하기 위한 조회 메서드 (신규)"""
        pass
```

### Locator 선택 원칙

**우선순위** (CLAUDE.md 기준):
1. **id 속성** (가장 안정적)
   ```python
   LOGOUT_LINK = (By.ID, "logout-link")
   ```

2. **data-* 속성** (테스트용)
   ```python
   LOGOUT_LINK = (By.CSS_SELECTOR, "a[data-qa='logout-link']")
   ```

3. **name 속성**
   ```python
   LOGOUT_LINK = (By.NAME, "logout")
   ```

4. **안정적인 CSS Selector**
   ```python
   LOGOUT_LINK = (By.CSS_SELECTOR, "ul.nav li a[href*='logout']")
   ```

5. **상대 XPath** (마지막 수단)
   ```python
   LOGOUT_LINK = (By.XPATH, "//ul[@class='nav']//a[contains(text(), 'Logout')]")
   ```

**금지**: Full XPath 절대 금지
```python
# ❌ 금지
LOGOUT_LINK = (By.XPATH, "/html/body/header/div/nav/ul/li[5]/a")
```

**안내**: 위 Locator는 모두 예시 값입니다. 실제 id/name/data-* 속성은 Page Object 구현 착수 시 사용자가 실시간으로 공유할 예정이며, 별도의 사전 개발자 도구 조사는 필요하지 않습니다.

### Wait 처리 전략

**명시적 Wait 사용** (time.sleep() 절대 금지):

```python
# ✅ 올바른 방식 (예시 - 실제 코드 아님)
def click_logout_link(self):
    wait.until(EC.element_to_be_clickable(self.LOGOUT_LINK))
    self.click(self.LOGOUT_LINK)

    # 로그인 페이지로 전환될 때까지 대기
    wait.until(EC.presence_of_element_located(LoginPage.LOGIN_BUTTON))
```

### 동적 요소 처리

- **페이지 전환**: "Logout" 클릭 후 로그인 페이지로 전환될 때까지 명시적 대기
- **헤더 상태 변화**: 로그아웃 전/후 헤더 네비게이션의 링크 구성이 달라지므로("Logout"/"Delete Account"/"Logged in as {username}" ↔ "Signup / Login" 통합 링크), 요소 존재 여부(presence) 및 표시 여부(visibility)를 함께 대기 조건으로 활용
- **로딩 표시**: 로그인 기능과 마찬가지로 로그아웃 클릭 후 별도의 로딩 스피너는 없는 것으로 추정 (login.md 참고, 로그아웃 자체는 미확인이므로 구현 시 재확인 권장)

### 재사용 가능한 메서드

**BasePage에 추가할 공통 메서드** (login.md에서 이미 제안한 메서드와 통합 권장):

```python
# base_page.py (예시)

class BasePage:
    # 대기 메서드
    def wait_for_element_clickable(self, locator, timeout=10) -> WebElement:
        """요소가 클릭 가능해질 때까지 대기"""
        pass

    def wait_for_element_presence(self, locator, timeout=10) -> WebElement:
        """요소가 DOM에 나타날 때까지 대기"""
        pass

    # 검증 메서드
    def is_element_displayed(self, locator) -> bool:
        """요소 표시 여부"""
        pass
```

### 테스트 코드 재사용 전략

- 로그아웃 테스트는 반드시 "로그인 완료 상태"를 사전 준비해야 하므로, `conftest.py`에 로그인을 미리 수행해주는 `logged_in_user` 또는 `authenticated_driver`류의 fixture를 정의하여 로그인 관련 테스트(login.md)와 로그아웃 테스트(이 문서) 양쪽에서 공유하는 것을 권장합니다.
- login.md의 NOR-002("로그아웃 후 재로그인 성공")와 이 문서의 NOR-002는 동일한 사용자 행동을 다루므로, 실제 pytest 구현 시 중복 테스트 함수를 각각 작성하기보다 공통 헬퍼 함수(예: `perform_logout(driver)`, `perform_login(driver, credentials)`)로 추출하여 재사용하는 것을 권장합니다.

### 예시: 로그아웃 테스트 구현 방향

```python
# tests/test_logout.py 구조 (실제 코드 아님)

def test_logout_success(driver, logged_in_user):
    # 1. 사전 준비: logged_in_user fixture로 로그인 완료 상태 확보
    home_page = HomePage(driver)
    assert home_page.is_logout_link_displayed()

    # 2. 로그아웃 수행
    home_page.click_logout_link()

    # 3. 로그아웃 결과 확인
    login_page = LoginPage(driver)
    assert login_page.is_on_login_page()
    assert login_page.is_signup_login_link_displayed()
    assert login_page.is_logout_link_displayed() is False
    # Delete Account 링크, Logged in as {username} 텍스트도 더 이상 노출되지 않아야 함 (신규)
    assert login_page.is_delete_account_link_displayed() is False
    assert login_page.is_logged_in_username_displayed() is False


def test_logout_then_relogin(driver, logged_in_user):
    home_page = HomePage(driver)
    home_page.click_logout_link()

    login_page = LoginPage(driver)
    login_page.enter_email(logged_in_user["email"])
    login_page.enter_password(logged_in_user["password"])
    login_page.click_login_button()

    home_page_after_relogin = HomePage(driver)
    assert home_page_after_relogin.is_logout_link_displayed()
```

---

## 20. 확인이 필요한 미확정 사항

### 확인 완료 항목 (login.md 등 관련 문서에서 확인됨)

다음 항목들은 관련 기능(로그인) PRD 작성 과정에서 실제 사이트 확인으로 이미 확인이 완료되어 더 이상 미확정 사항이 아닙니다:

- ✅ 로그인 상태에서는 헤더 네비게이션에 "Logout"이 노출되고, 로그인 전(또는 로그아웃 후)에는 "Signup / Login" 통합 링크가 노출됨 (login.md LOGIN-REQ-003 근거, "Login"/"Signup" 개별 노출이 아님을 확정)
- ✅ Logout 클릭 → 로그인 페이지 이동 → 재로그인 성공 (login.md NOR-002 시나리오 근거)
- ✅ Automation Exercise에서 동일 이메일로 중복 가입 불가, 이메일 인증 절차 불필요 (signup.md, login.md 근거)
- ✅ 테스트 계정 준비 방식: 사전 생성 (login.md 섹션 17 근거)
- ✅ **(신규, login.md v1.4 스크린샷 근거)** 로그인 상태의 헤더 네비게이션에는 "Logout" 외에 "Delete Account" 링크와 "Logged in as {username}" 텍스트가 함께 노출되며, 로그아웃을 수행하면 이 두 요소도 "Logout" 링크와 함께 모두 사라짐
- ✅ **(신규, login.md v1.3~v1.4 스크린샷 근거)** 로그아웃 후 헤더에 노출되는 링크는 "Login"과 "Signup"이 각각 별도로 노출되는 것이 아니라 "Signup / Login" 하나의 통합 링크임

### 확인 완료 항목 (v1.2, 이번 문서 업데이트에서 실제 사이트 확인으로 신규 확정)

- ✅ **Logout 링크의 실제 요청 URL**: `https://automationexercise.com/logout` (실제 사이트 확인 완료). 로그인 상태에서만 정상 동작하며, 비로그인 상태에서 이 URL에 직접 접근하면 **Django 디버그 트레이스백 페이지가 노출됨**이 확인됨 (섹션 4, 9 흐름 3 반영, 세부 내용은 v1.3에서 확정. 단 이 흐름 자체는 v1.4에서 자동화 대상에서 제외됨 — 아래 "조사 대상에서 제외하기로 확정한 항목" 참고)
- ✅ **Logout 클릭 시 확인(confirm) 다이얼로그 부재**: 별도의 확인 다이얼로그 없이 클릭 즉시 로그아웃이 처리됨 (실제 사이트 확인 완료, 섹션 7, 16 반영)
- ✅ **다른 페이지에서의 인증 유도 메커니즘**: 장바구니 페이지에서 상품 결제를 시도하면 로그인을 안내하는 모달이 노출되는 것이 확인됨. 다만 이는 "페이지별로 Logout 버튼을 클릭했을 때 완전히 동일한 리다이렉트 UI(로그인 페이지로 이동)까지 보장한다"는 의미가 아니라, **인증이 필요한 상황에서 로그인을 유도하는 전역적 메커니즘이 페이지와 무관하게 일관되게 동작함을 확인**했다는 의미입니다. 이 근거로 섹션 12에서 페이지별 반복 테스트는 자동화 제외 범위로 유지하되, 제외 사유를 "미확인이라서"에서 "확인된 전역 메커니즘에 근거해 불필요"로 정정함

### 확인 완료 항목 (v1.3, 이번 문서 업데이트에서 실제 화면 스크린샷 확인으로 신규 확정)

- ✅ **비로그인 상태 `/logout` URL 직접 접근 시 노출 화면의 세부 내용**: 사용자 친화적 에러 안내 페이지가 아니라 **Django 프레임워크의 디버그 예외 트레이스백 페이지**가 그대로 노출됨. 페이지 헤딩은 `KeyError at /logout`, 예외 값은 `'user_id'`이며, Request Method(GET), Request URL(`https://automationexercise.com/logout`), Django Version(3.2.8), Exception Type(KeyError), 그리고 `website/views.py, line 216, in logout` → `del request.session['user_id']` 코드가 포함된 traceback이 화면에 노출됨. 즉 이는 "안내" 성격의 에러 화면이 아니라 서버 측 미처리 예외(unhandled exception)가 그대로 노출되는 디버그 화면임 (실제 화면 스크린샷 근거, 섹션 4, 9 흐름 3, 15, 16 반영). 다만 이 화면은 Django `DEBUG` 설정 값에 따라 노출 형태가 달라질 수 있는 프레임워크 차원의 디버그 화면이므로, 운영 환경(`DEBUG=False`) 전환 시 노출 형태가 달라질 가능성이 있다는 점을 이유로 이 흐름 자체가 v1.4에서 자동화 대상에서 완전히 제외되었음(아래 "조사 대상에서 제외하기로 확정한 항목" 참고)
- ✅ **"Logout" 링크의 페이지별 위치**: 다른 페이지에서의 "Logout" 링크 위치는 메인 페이지와 완전히 동일함. 헤더 네비게이션(Logout, Signup/Login, Delete Account, Logged in as {username} 포함)이 사이트 전역에서 위치가 불변인 공통 고정 컴포넌트임이 실제 화면 스크린샷으로 확인됨 (섹션 4, 7, 12, 19 반영)

### 조사 대상에서 제외하기로 확정한 항목 (스코프 결정 — 위 "확인 완료" 항목과 구분됨)

다음 항목은 실제 동작을 "몰라서" 여전히 확인이 필요한 상태가 아니라, **실제 동작이 무엇으로 확인되든 상관없이 자동화 범위에서 제외하기로 스코프를 확정**한 항목입니다. "확인 완료" 목록과 혼동하지 않도록 별도로 구분하여 명시합니다.

- **로그아웃 완료 후 브라우저 뒤로가기(Back) 시 실제 동작** (캐시된 화면 노출 여부, 재리다이렉트 여부 등): 세션/쿠키 검증 영역과 맞닿아 있다는 이유로 자동화 범위에서 제외하기로 결정함 (스코프 결정, v1.2. 섹션 9 흐름 1, 섹션 12, 섹션 14 ABN-001 참고). 이 결정은 실제 사이트에서 어떤 동작이 확인되더라도 번복되지 않는 스코프 결정입니다.
- **비로그인 상태에서 `/logout` URL 직접 접근 시 노출되는 화면 검증 (구 ABN-002)**: 실제 동작(Django 디버그 트레이스백 페이지 노출)은 확인되었으나, 이 화면이 Django `DEBUG` 설정 값에 따라 노출 형태가 달라지는 프레임워크 차원의 디버그 화면이라는 환경 종속성을 이유로 자동화 범위에서 제외하기로 결정함 (스코프 결정, v1.4. 섹션 9 흐름 3, 섹션 12, 섹션 14 참고). 운영 환경(`DEBUG=False`)에서는 다른 형태(예: 일반 500 에러 페이지)가 노출될 수 있어, 이 검증 기준 자체가 환경에 따라 달라질 수 있다는 점이 제외 사유이며, 실제 환경 설정 확인 대신 사용자 판단으로 범위에서 제외되었습니다.

### 여전히 확인이 필요한 항목

#### 프로젝트 전체 차원의 미확정 사항
- **세션 타임아웃 시간**: 로그인 후 세션이 유지되는 시간이 얼마인지 프로젝트 전체 차원에서 아직 확정되지 않음 (project-prd.md 19.1, 813-816행). 이 값이 확정되기 전까지는 세션 만료 관련 로그아웃 동작(섹션 9 흐름 2, 섹션 12 참고)은 자동화 대상에서 제외함

#### 로그아웃 기능 고유의 확인 필요 사항
- 해당 없음 (비로그인 상태 `/logout` URL 직접 접근 관련 확인 필요 사항은 v1.4에서 해당 시나리오 자체가 자동화 대상에서 제외됨에 따라 더 이상 자동화 관점의 확인 필요 항목이 아님 — 위 "조사 대상에서 제외하기로 확정한 항목" 참고)

#### UI 요소 Locator (개발 착수 시 공유 예정)
- "Logout" 링크, "Signup / Login" 통합 링크, "Delete Account" 링크, "Logged in as {username}" 텍스트의 실제 HTML id, name, CSS 클래스, data-* 속성은 Page Object 구현 착수 시 사용자가 실시간으로 공유할 예정입니다. 별도의 사전 개발자 도구 조사는 필요하지 않습니다.

---

## 21. 완료 조건

### 로그아웃 기능 자동화 완료 기준

**정상 시나리오 완료**:
- ✅ NOR-001 (로그인 상태에서 정상 로그아웃): 테스트 PASS
- ✅ NOR-002 (로그아웃 후 동일 계정으로 재로그인 성공): 테스트 PASS

**비정상 시나리오 완료**:
- ✅ ABN-001은 자동화 범위에서 제외하기로 결정되었음을 문서화 완료 (스코프 결정, 별도 테스트 코드 작성 없음)
- ✅ 비로그인 상태에서 `/logout` URL 직접 접근 시나리오(구 ABN-002)는 v1.4에서 자동화 범위에서 완전히 제외되었음을 문서화 완료 (스코프 결정, 별도 테스트 코드 작성 없음)

**코드 품질 기준** (CLAUDE.md 준수):
- ✅ Page Object 설계: HomePage(또는 공통 헤더 컴포넌트)의 Logout 관련 메서드, LoginPage의 로그아웃 이후 상태 조회 메서드 구현 완료
  - 모든 Locator가 상수/클래스 변수로 정의됨
  - 화면 조작 메서드와 값 조회 메서드만 포함
  - Assertion 없음 (Test 계층에서만 수행)

- ✅ Locator 안정성:
  - id/data-*/name 속성 우선 사용
  - Full XPath 사용 안 함

- ✅ Wait 처리:
  - time.sleep() 사용 안 함
  - Explicit Wait (WebDriverWait) 사용

- ✅ 테스트 독립성:
  - 각 테스트가 단독 실행 가능 (로그인 사전 준비를 각 테스트 내 fixture로 수행)
  - 테스트 간 순서 의존성 없음
  - 각 테스트에서 필요한 데이터(로그인 상태) 준비

- ✅ 코딩 컨벤션:
  - 파일명: snake_case (home_page.py, login_page.py, test_logout.py)
  - 클래스명: PascalCase + Page 접미사 (HomePage, LoginPage)
  - 메서드명: snake_case, 동사로 시작 (click_logout_link, is_logout_link_displayed)
  - 테스트 함수명: test_ 접두사 (test_logout_success)
  - 2칸 들여쓰기

- ✅ 민감정보 보호:
  - 계정 정보 환경변수 또는 외부 파일로 관리 (login.md와 공유)
  - 코드에 비밀번호 하드코딩 안 함
  - 로그에서 비밀번호 마스킹

**테스트 실행 기준**:
- ✅ 모든 테스트 PASS (성공률 100%)
- ✅ 실패 시 스크린샷 저장 확인
- ✅ pytest-html 리포트 생성 확인
- ✅ 로그 파일 생성 확인

**문서 기준**:
- ✅ 이 PRD가 완성되고 검토됨
- ✅ Page Object 구현 착수 시 Locator 공유 프로세스가 합의됨 (login.md와 동일한 프로세스 적용)
- ✅ 섹션 20의 "여전히 확인이 필요한 항목"들이 실제 사이트 방문으로 검증됨

**배포 기준**:
- ✅ 모든 테스트 코드 완성
- ✅ 코드 리뷰 완료
- ✅ GitHub Actions CI/CD 테스트 통과
- ✅ 로그인 기능 PRD(`docs/prd/features/login.md`)와의 일관성 검증 (특히 로그인/로그아웃 상태 판단 기준의 일치 여부)

---

## 22. 다음 단계

### 즉시 작업 (이 PRD 이후)
1. **테스트 계정 확인**: login.md에서 정의한 사전 생성 테스트 계정(`test001@example.com` 등)을 로그아웃 테스트에도 재사용할 수 있도록 준비 상태 재확인
2. **Locator 공유 대기**: Page Object 구현 착수 시 사용자로부터 "Logout" 링크, "Signup / Login" 통합 링크, "Delete Account" 링크, "Logged in as {username}" 텍스트의 id, name, CSS 클래스, data-* 속성을 실시간으로 공유받기
3. **Page Object 구현**: HomePage(또는 공통 헤더 컴포넌트)에 Logout 관련 메서드 추가, LoginPage에 로그아웃 이후 상태 조회 메서드 추가
4. **테스트 코드 작성**: 로그아웃 기능 테스트 케이스 작성 (tests/test_logout.py) — 정상 시나리오(NOR-001, NOR-002)만 포함, 로그인 사전 준비용 공용 fixture 정의. 비로그인 상태 `/logout` URL 직접 접근 시나리오(구 ABN-002)는 v1.4에서 자동화 대상에서 제외되어 테스트 코드를 작성하지 않음
5. **테스트 실행**: pytest를 사용하여 정상 시나리오(NOR-001, NOR-002) 테스트 실행
6. **오류 수정**: 실패한 테스트 분석 및 수정

### 추후 작업 (이 기능 완료 후)
1. **통합 테스트**: 회원가입 → 로그인 → 로그아웃 → 재로그인의 전체 흐름 테스트 구성
2. **다른 기능**: Phase 1 나머지 기능 (상품 검색) 자동화
3. **세션 타임아웃 확정 후 확장 검토**: 프로젝트 전체 차원에서 세션 타임아웃 시간이 확정되면, 세션 만료 후 로그아웃 동작(섹션 9 흐름 2) 시나리오를 추후 별도 범위로 추가할지 검토
4. **뒤로가기 시나리오 스코프 재검토(필요 시에만)**: 로그아웃 후 브라우저 뒤로가기 동작(섹션 9 흐름 1, ABN-001)은 실제 동작 여부와 무관하게 자동화 범위에서 제외하기로 확정(v1.2, 스코프 결정)되었으므로, 향후 이 결정 자체를 재논의할 필요가 생길 경우에만 별도로 검토
5. **`/logout` URL 직접 접근 시나리오 재검토(필요 시에만)**: 비로그인 상태 `/logout` URL 직접 접근 시나리오(구 ABN-002)는 Django DEBUG 설정에 의존하는 환경 종속적 특성을 이유로 자동화 범위에서 제외하기로 확정(v1.4, 스코프 결정)되었으므로, 향후 운영 환경의 DEBUG 설정이 명확히 확인되는 등 상황 변화가 있을 경우에만 재검토

---

## 23. 참고 자료

### 관련 문서
- **프로젝트 전체 PRD**: `docs/prd/project-prd.md`
- **로그인 기능 PRD**: `docs/prd/features/login.md`
- **회원가입 기능 PRD**: `docs/prd/features/signup.md`
- **프로젝트 개발 규칙**: `CLAUDE.md`
- **기능별 PRD 작성 가이드**: `docs/PRD_PROMPT.md` (있는 경우)

### 외부 참고
- **Automation Exercise 공식**: https://automationexercise.com/
- **Selenium 문서**: https://selenium.dev/documentation/
- **pytest 문서**: https://docs.pytest.org/

### 버전 관리
- **이 PRD 버전**: 1.4 (ABN-002를 자동화 대상에서 완전히 제외함)
- **작성일**: 2026-07-22
- **최종 검토일**: 2026-07-22
- **최종 승인일**: (예정)

**변경 이력**:
- v1.4 (2026-07-23): ABN-002를 자동화 대상에서 제외함 (Django DEBUG 설정에 의존하는 환경 종속적 시나리오로, 실제 환경 설정 확인 대신 사용자 판단으로 범위에서 제외). 구체적으로 (1) 섹션 4의 URL 설명, 섹션 9 흐름 3의 결론을 "비정상 시나리오로 자동화 대상에 포함"에서 "환경 종속적 동작이라는 이유로 자동화 대상에서 제외"로 수정. (2) 섹션 11 자동화 대상 범위 표에서 ABN-002 행 삭제. (3) 섹션 12 자동화 제외 범위 표에 "비로그인 상태에서 `/logout` URL 직접 접근 시 노출되는 화면(Django 디버그 트레이스백 페이지) 검증" 행을 사유 "환경 의존적(Django DEBUG 설정)이라 자동화 대상에서 제외하기로 결정"으로 신규 추가. (4) 섹션 14에서 ABN-002 하위 섹션(시나리오명/전제조건/테스트단계/기대결과/검증포인트/리스크) 전체 삭제, 비고 문단을 "이 기능에 대해 실제로 작성되는 자동화 테스트 케이스는 없음"으로 수정. (5) 섹션 15 "비정상 케이스 기대 결과" 표(ABN-002 단독)를 삭제하고, ABN-002를 "제외 케이스" 표에 ABN-001과 함께 기록. (6) 섹션 16에서 "비정상 시나리오(ABN-002) 검증" 절 및 프로그래밍적 검증 예시 코드의 ABN-002 블록 삭제. (7) 섹션 20에서 ABN-002 관련 인용을 정리하고, "Django DEBUG 설정에 따른 화면 노출 형태 변화 가능성"/"HTTP 상태 코드" 확인 필요 항목을 "조사 대상에서 제외하기로 확정한 항목"으로 이동(더 이상 자동화를 위해 해소해야 할 확인 필요 사항이 아니므로). (8) 섹션 21 완료 조건에서 "ABN-002 테스트 PASS" 항목을 "구 ABN-002는 자동화 범위에서 제외되었음을 문서화 완료"로 수정. (9) 섹션 22 다음 단계에서 ABN-002 테스트 작성/실행 관련 서술을 제거하고 재검토 조건부 항목으로 대체. 이번 개정은 실제 환경(Django DEBUG 설정 값) 확인 결과가 아니라 사용자의 스코프 결정에 따른 것이며, Selenium/pytest 실제 동작 코드는 추가하지 않음.
- v1.3 (2026-07-22): 섹션 20 "여전히 확인이 필요한 항목" 중 로그아웃 기능 고유의 확인 필요 사항 2건에 대해 실제 화면 스크린샷 확인 결과를 반영함. (1) **비로그인 상태 `/logout` URL 직접 접근 시 노출 화면 세부 확정**: 기존에 막연히 "에러 페이지가 노출됨"으로만 서술되어 있던 부분을, 실제로는 사용자 친화적 안내 페이지가 아니라 **Django 프레임워크의 디버그 예외 트레이스백 페이지**(헤딩 `KeyError at /logout`, 예외 값 `'user_id'`, Request Method/URL, Django Version 3.2.8, Exception Type: KeyError, `website/views.py` line 216 `del request.session['user_id']` traceback 포함)임으로 구체화·정정 (섹션 4, 7 확인 완료로 이동, 섹션 9 흐름 3, 섹션 11, 섹션 14 ABN-002 기대 결과·검증 포인트, 섹션 15·16 표 및 예시 코드, 섹션 20 확인 완료 항목 반영). 이 화면이 Django `DEBUG` 설정에 따라 노출 형태가 달라질 수 있는 프레임워크 차원의 디버그 화면이라는 점과, 운영 환경에서 `DEBUG=False`로 전환 시 일반 500 에러 페이지로 대체될 수 있다는 점을 리스크로 신규 명시하고 섹션 20 "여전히 확인이 필요한 항목"에 반영. (2) **"Logout" 링크의 페이지별 위치 확정**: 다른 페이지에서의 "Logout" 링크 위치가 메인 페이지와 완전히 동일함을 확정 — 헤더 네비게이션이 사이트 전역에서 위치가 불변인 공통 고정 컴포넌트임을 확인 (섹션 4, 7 확인 완료로 이동, 섹션 12 제외 근거에 직접적 근거 추가, 섹션 19 Page Object 설계 권장이 추정이 아닌 확정된 사실에 근거함을 보강, 섹션 20 확인 완료 항목 반영). login.md, signup.md는 이 두 사실과 무관함을 확인하여 수정하지 않음. 전부 문서(PRD) 수정이며 Selenium/pytest 실제 동작 코드는 추가하지 않음(기존 스텁 수준 예시만 확장·구체화).
- v1.2 (2026-07-22): 섹션 20 "로그아웃 기능 고유의 확인 필요 사항" 4건에 대해 실제 사이트 확인 결과를 반영함. (1) **Logout 링크 URL 확정**: 실제 요청 URL을 `https://automationexercise.com/logout`으로 확정하고, 비로그인 상태에서 이 URL에 직접 접근하면 에러 페이지가 노출됨을 확인 (섹션 4 URL 정정, 섹션 9 흐름 3에 URL 직접 접근 관점 추가, 섹션 11에 신규 자동화 대상 행 추가, 섹션 14에 **ABN-002(신규 비정상 시나리오)** 추가, 섹션 15·16에 ABN-002 기대 결과/검증 포인트/예시 코드 추가, 섹션 20 확인 완료로 이동). (2) **Confirm 다이얼로그 없음 확정**: Logout 클릭 시 별도의 확인 다이얼로그가 존재하지 않음을 확정 (섹션 7 확인 완료 항목으로 이동, 섹션 16 "추정" 표현을 "확인 완료"로 정정, 섹션 20 확인 완료로 이동). (3) **브라우저 뒤로가기 자동화 제외를 "확인 필요"에서 "스코프 결정"으로 뉘앙스 정정**: 실제 동작을 몰라서 제외하는 것이 아니라 실제 동작 여부와 무관하게 제외하기로 결정한 것임을 명확화 (섹션 9 흐름 1, 섹션 12, 섹션 14 ABN-001, 섹션 21·22 문구 정정, 섹션 20에 "확인 완료"와 구분되는 별도의 "조사 대상에서 제외하기로 확정한 항목" 항목 신설). (4) **다른 페이지에서의 로그아웃 관련 확인**: 장바구니 페이지에서 결제 시도 시 로그인 안내 모달이 노출되는 것을 확인하여, 인증이 필요한 상황에서 로그인을 유도하는 전역 메커니즘이 페이지와 무관하게 일관되게 동작함을 확인 (단, 페이지별 완전히 동일한 리다이렉트까지 보장한다는 의미는 아님으로 과장 없이 서술). 이를 근거로 섹션 12의 제외 사유를 "미확인이라서"에서 "확인된 전역 메커니즘에 근거해 불필요"로 정정하고, 섹션 20 확인 완료로 이동. 전부 문서(PRD) 수정이며 Selenium/pytest 실제 동작 코드는 추가하지 않음(기존 스텁 수준 예시만 확장).
- v1.1 (2026-07-22): login.md v1.3~v1.4에서 실제 사이트 스크린샷 근거로 확정된 사실을 반영하여 정합성을 확보함. (1) 로그아웃 완료 후 헤더에 노출되는 링크를 "Login"/"Signup" 개별 표기에서 **"Signup / Login" 통합 링크**로 정정 (섹션 7 헤더 목업·UI 요소 표, 섹션 8 정상 흐름, 섹션 10 LOGOUT-REQ-003, 섹션 13 NOR-001, 섹션 15·16 기대 결과/검증 포인트/예시 코드, 섹션 18 의존성 흐름도, 섹션 19 Page Object 예시, 섹션 20 확인 완료 항목). (2) 로그인 상태(로그아웃 직전) 헤더에는 "Logout" 외에 **"Delete Account" 링크**와 **"Logged in as {username}" 텍스트**가 함께 노출되며, 로그아웃 시 이 두 요소도 모두 사라진다는 사실을 신규 반영 (섹션 7 UI 요소 표·헤더 목업 신규 행 추가, 섹션 8 시작조건/기대결과 보강, 섹션 10 LOGOUT-REQ-001 참고·LOGOUT-REQ-003 요구사항 추가, 섹션 13 NOR-001 검증 포인트 2건 추가, 섹션 15·16 표·예시 코드 보강, 섹션 20 확인 완료 항목 추가). (3) 섹션 18에 login.md와의 정합성이 이번 업데이트로 확보되었음을 명시. (4) 섹션 19 Page Object 예시 코드의 Locator/메서드명을 login.md v1.4 네이밍 권고와 일관되게 조정 (`is_login_link_displayed()`/`is_signup_link_displayed()` → `is_signup_login_link_displayed()` 통합, `is_delete_account_link_displayed()`, `is_logged_in_username_displayed()`, `get_logged_in_username()` 스텁 신규 추가). 전부 스텁 수준 예시 코드이며 실제 동작 코드는 아님.
- v1.0 (2026-07-22): 최초 작성. 로그아웃 성공 흐름(NOR-001, NOR-002) 중심으로 범위 확정, 세션/쿠키 자체 검증 및 세션 타임아웃 관련 동작을 자동화 제외 범위로 명시, 로그인 기능(login.md)에 대한 후행 의존성을 사전 조건 및 의존성 섹션에 명시

---

**작성자**: Automation Testing Framework Lead
**최종 검토자**: (예정)
**승인 상태**: 초안 (검토 대기 중)

이 문서는 로그아웃 기능의 자동화 테스트 작성 시 기준이 되는 요구사항 명세입니다.
실제 구현 과정에서 새로운 정보가 발견되면 이 문서를 업데이트합니다.
