# 로그인 (Login) 기능 상세 PRD

**작성 일자**: 2026-07-20  
**최종 수정일**: 2026-07-22 ("Logged in as {username}"의 표시 형식이 회원가입 시 "Name" 필드 입력값과 일치함을 확인하여 반영)  
**버전**: 1.4  
**상태**: 초안 (로그인 성공/실패 핵심 흐름 중심으로 범위 확정. Locator는 Page Object 구현 착수 시 사용자가 실시간으로 공유할 예정)

---

## 1. 기능명

- **한국어명**: 로그인
- **영문명**: Login
- **기능 ID**: LOGIN

---

## 2. 기능 목적

사용자가 회원가입으로 생성한 계정(이메일, 비밀번호)을 사용하여 시스템에 인증하고, 회원 전용 기능(상품 검색, 장바구니, 주문 등)에 접근할 수 있도록 하는 기능입니다.

### 비즈니스 가치
- 사용자 식별 및 세션 관리
- 개인화된 사용자 경험 제공
- 주문 이력, 장바구니 등 사용자별 데이터 관리
- 보안 기반 제공

---

## 3. 프로젝트 전체 PRD와의 연관성

### 기준 문서
**참고**: `docs/prd/project-prd.md`

### 연관 섹션
- **8.1 Phase 1**: 기본 사용자 인증 및 탐색 (필수 기능)
- **9.1 주요 사용자 흐름**: 단계 2 (로그인) - Happy Path 정의
- **5.2 MVP 대상 기능**: 우선순위 1 (필수)

### 의존성
- **선행 기능**: 회원가입 (Signup)
  - 로그인하기 전에 사용자 계정이 먼저 생성되어야 함
  
---

## 4. 대상 URL 또는 진입 경로

### 로그인 페이지 URL
**확인 완료**: `https://automationexercise.com/login`

### 진입 경로 (사용자 흐름)
1. **홈 페이지에서 진입**: 홈 페이지의 "Signup / Login" 네비게이션 링크 클릭
   - **확인 완료(스크린샷 근거)**: 로그인되지 않은 상태의 헤더 네비게이션에는 "Login"이 단독으로 노출되는 것이 아니라, "Signup / Login"이라는 하나의 통합 링크로 노출됨. 이 링크를 클릭하면 로그인 페이지로 이동함
2. **로그아웃 후 진입**: 로그아웃 후에도 동일하게 "Signup / Login" 통합 링크가 노출되며, 이 링크 클릭으로 로그인 페이지 진입
3. **직접 URL 접근**: 브라우저 주소창에 로그인 페이지 URL 직접 입력

**참고**: 회원가입 완료 후에는 별도의 로그인 절차 없이 자동으로 로그인 상태가 되어 메인 페이지로 이동합니다(signup.md 섹션 4, 8 참고). 따라서 회원가입 완료 후에는 로그인 페이지를 거치지 않으며, 이 목록에서 "회원가입 후 진입" 경로는 제외합니다.

---

## 5. 사용자 역할

### 대상 사용자
- **기존 회원 (Registered User)**: 이미 회원가입을 완료한 사용자
  - 이메일과 비밀번호를 보유하고 있음
  - 가입된 계정으로 로그인하려는 사용자

### 사용자 시나리오
- 첫 로그인: 회원가입 직후 계정으로 처음 로그인
- 반복 로그인: 기존 계정으로 재로그인 (세션 만료, 브라우저 종료 후)

---

## 6. 사전 조건 (Precondition)

### 필수 조건
1. **계정 존재**: 사용자가 미리 회원가입하여 계정이 생성되어 있어야 함
   - 유효한 이메일 주소로 가입됨
   - 비밀번호가 등록되어 있음

2. **브라우저 상태**: 테스트 시작 전 상태
   - 기존 로그인 상태가 없는 상태 (로그아웃 또는 처음 방문)
   - 쿠키/세션이 초기화된 상태

3. **사이트 접근**: Automation Exercise 사이트에 접근 가능
   - 인터넷 연결이 정상
   - 사이트가 운영 중 (다운타임 없음)

### 테스트 데이터 준비
- 로그인 시 사용할 유효한 계정 정보 (이메일, 비밀번호)
- 로그인 실패 테스트용 무효한 계정 정보

---

## 7. 주요 화면과 UI 요소

### 로그인되지 않은 상태의 메인 페이지 헤더 (확인 완료, 스크린샷 근거)

```
┌───────────────────────────────────────────────────────────────────────────┐
│                          Automation Exercise                              │  (헤더)
│ Home | Products | Cart | Signup / Login | Test Cases | API Testing |      │  (네비게이션 - 비로그인 상태)
│ Video Tutorials | Contact us                                              │
└───────────────────────────────────────────────────────────────────────────┘
```

**확인 완료(스크린샷 근거)**: 로그인되지 않은 상태의 헤더 네비게이션은 `Home | Products | Cart | Signup / Login | Test Cases | API Testing | Video Tutorials | Contact us` 순서로 구성되며, "Login"이라는 텍스트가 단독으로 노출되지 않고 **"Signup / Login" 하나의 통합 링크**로 노출됩니다.

### 로그인 페이지 화면 레이아웃 (헤더는 확인 완료, 본문 레이아웃은 추정)

```
┌─────────────────────────────────────┐
│        Automation Exercise          │  (헤더)
│ ... | Signup / Login | ...          │  (네비게이션 - 비로그인 상태, 위 다이어그램 참고)
├─────────────────────────────────────┤
│                                     │
│        Login to Your Account        │  (페이지 제목)
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Email Address *               │  │  (이메일 입력 필드)
│  │ [____________________]        │  │
│  │                               │  │
│  │ Password *                    │  │  (비밀번호 입력 필드)
│  │ [____________________]        │  │
│  │                               │  │
│  │ Your email or password is    │  │  (오류 메시지, 실패 시에만 노출)
│  │ incorrect!                   │  │
│  │                               │  │
│  │  [   Login   ]                │  │  (로그인 버튼)
│  │                               │  │
│  └───────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

### 로그인된 상태의 메인 페이지 헤더 (확인 완료, 스크린샷 근거 — 참고용, 로그인 성공 후 화면)

```
┌───────────────────────────────────────────────────────────────────────────┐
│                          Automation Exercise                              │  (헤더)
│ Home | Products | Cart | Logout | Delete Account | Test Cases |           │  (네비게이션 - 로그인 상태)
│ API Testing | Video Tutorials | Contact us | Logged in as {username}      │
└───────────────────────────────────────────────────────────────────────────┘
```

**확인 완료(스크린샷 근거)**: 로그인 성공 후에는 헤더 네비게이션이 `Home | Products | Cart | Logout | Delete Account | Test Cases | API Testing | Video Tutorials | Contact us | Logged in as {username}` 순서로 구성됩니다. 로그인 전 대비 다음 3가지 요소가 달라지거나 추가로 노출됩니다.
- **"Signup / Login"** → **"Logout"**로 대체
- **"Delete Account"** 링크가 신규로 노출됨 (기존 문서에 언급 없던 요소)
- **"Logged in as {username}"** 텍스트가 신규로 노출됨 (기존 문서에 언급 없던 요소). {username}에는 회원가입 시 "Name" 필드에 입력한 값이 그대로 표시됨(확인 완료). 따라서 단순히 "Logout 노출 여부"만 확인하는 것보다 로그인 시도에 사용한 계정의 회원가입 Name 값과 실제 노출된 사용자명이 일치하는지까지 검증할 수 있는 더 강력한 검증 포인트로 활용 가능함 (섹션 16 참고)

### 주요 UI 요소

| 요소명 | 타입 | 설명 | 필수 여부 |
|--------|------|------|---------|
| **Email Address 입력란** | Input (Text) | 사용자 이메일 주소 입력 | 필수 |
| **Password 입력란** | Input (Password) | 비밀번호 입력 (마스킹 처리) | 필수 |
| **Login 버튼** | Button | 로그인 수행 버튼 | 필수 |
| **오류 메시지 영역** | Text | 로그인 실패 시 "Password" 입력 필드 하단에 "Your email or password is incorrect!" 문구 표시 (확인 완료) | 조건부 |
| **Signup / Login 링크** (헤더) | Link (네비게이션) | 로그인되지 않은 상태에서 노출되는 통합 링크. 클릭 시 로그인 페이지로 이동 (확인 완료, 스크린샷 근거) | 조건부(비로그인 상태에서 노출) |
| **Logout 링크** (헤더) | Link (네비게이션) | 로그인 상태에서 "Signup / Login"을 대체하여 노출되는 링크 (확인 완료) | 조건부(로그인 상태에서 노출) |
| **Delete Account 링크** (헤더) | Link (네비게이션) | 로그인 상태에서만 노출되는 계정 삭제 링크 (확인 완료, 스크린샷 근거 — 신규 확인) | 조건부(로그인 상태에서 노출) |
| **Logged in as {username} 텍스트** (헤더) | Text (네비게이션) | 로그인 상태에서만 노출되며, {username}에는 회원가입 시 "Name" 필드에 입력한 값이 그대로 표시됨 (확인 완료, 스크린샷 근거 — 신규 확인) | 조건부(로그인 상태에서 노출) |
| **Cart / Test Cases / API Testing / Video Tutorials / Contact us 링크** (헤더) | Link (네비게이션) | 로그인 여부와 무관하게 항상 노출되는 공통 네비게이션 항목 (확인 완료, 스크린샷 근거) | 항상 노출 |

### 확인 완료
- 로그인 실패 시 오류 메시지는 "Password" 입력 필드 하단에 "Your email or password is incorrect!" 문구로 노출됨
- 로그인 버튼 클릭 후 로딩 표시(스피너 등)는 없음
- 로그인되지 않은 상태의 헤더 네비게이션은 "Login"이 단독으로 노출되지 않고 "Signup / Login" 통합 링크로 노출됨 (스크린샷 근거)
- 로그인 상태의 헤더 네비게이션에는 "Logout", "Delete Account" 링크와 "Logged in as {username}" 텍스트가 노출됨 (스크린샷 근거)

### 확인 완료 (추가)
- **"Logged in as {username}"의 표시 형식**: {username}에는 회원가입 시 "Name" 필드에 입력한 값이 그대로 표시됨 (이메일 주소나 이메일의 로컬 파트가 아님). 즉, 로그인 후 헤더에 노출되는 사용자명은 해당 계정으로 회원가입할 때 입력한 Name 값과 정확히 일치해야 함 (섹션 10 LOGIN-REQ-008, 섹션 16, 17, 20 참고)

### 확인 필요
- 각 UI 요소의 HTML id, CSS 클래스, data-* 속성: Page Object 구현 착수 시 사용자가 실시간으로 공유할 예정이며, 별도의 사전 개발자 도구 조사는 필요하지 않음

---

## 8. 정상 사용자 흐름 (Happy Path)

**확인 완료**: 아래 흐름은 실제 사이트 확인 결과를 반영하여 작성되었습니다.

### 흐름 1: 유효한 자격증명으로 로그인

**시작 조건**: 로그인 페이지 방문, 유효한 계정 존재

**단계별 행동**:
1. 사용자가 로그인 페이지(`https://automationexercise.com/login`) 접속
2. "Email Address" 입력란에 등록된 이메일 주소 입력
   - 예: `user@example.com`
3. "Password" 입력란에 정확한 비밀번호 입력
   - 예: `password123`
4. "Login" 버튼 클릭
5. 시스템이 자격증명을 검증함 (로딩 표시 없음, 확인 완료)
6. 로그인 성공 시 메인 페이지(`https://automationexercise.com/`)로 이동
7. 메인 페이지 헤더(네비게이션) 영역에 "Logout"이 노출되는 것으로 로그인 상태를 확인함
   - 이 외에도 헤더 네비게이션에 "Delete Account" 링크와 "Logged in as {username}" 텍스트가 함께 노출됨 (확인 완료, 스크린샷 근거, 섹션 7 참고)

**기대 결과**:
- 로그인 성공 시 메인 페이지로 이동하며, 헤더(네비게이션) 영역에 "Logout", "Delete Account" 링크와 "Logged in as {username}" 텍스트가 노출됨
- 개인화된 사용자 영역 접근 가능

**소요 시간**: 약 2~3초 (네트워크 지연 포함)

---

## 9. 예외 사용자 흐름 (Exception Flow)

**확인 완료**: 로그인 실패 시 오류 메시지 문구와 위치가 실제 사이트 확인으로 확인되었습니다.

### 흐름 1: 잘못된 비밀번호 입력

**시작 조건**: 로그인 페이지, 존재하는 계정

**단계별 행동**:
1. 로그인 페이지에 올바른 이메일 입력
2. 잘못된 비밀번호 입력
3. "Login" 버튼 클릭
4. 시스템이 자격증명 검증 및 실패
5. 오류 메시지 표시 (페이지 유지)

**기대 결과**:
- 오류 메시지: "Password" 입력 필드 하단에 "Your email or password is incorrect!" 노출 (확인 완료)
- 페이지 새로고침 없이 현재 페이지 유지
- 입력한 이메일은 유지되고 비밀번호는 초기화

---

### 흐름 2: 존재하지 않는 이메일 입력

**시작 조건**: 로그인 페이지

**단계별 행동**:
1. 등록되지 않은 이메일 입력
   - 예: `nonexistent@example.com`
2. 임의의 비밀번호 입력
3. "Login" 버튼 클릭
4. 시스템이 계정 확인 및 실패
5. 오류 메시지 표시

**기대 결과**:
- 오류 메시지: "Password" 입력 필드 하단에 "Your email or password is incorrect!" 노출 (확인 완료)
- 로그인 실패, 로그인 페이지 유지

---

### 흐름 3: 필수 필드 공란 상태에서 로그인 시도 (자동화 범위에서 제외됨)

이메일 또는 비밀번호 입력란을 비운 상태에서 "Login" 버튼을 클릭하는 흐름입니다. 이 흐름에 대한 실제 동작 검증(클라이언트/서버 사이드 유효성 검사 방식 등)은 이번 자동화 범위에서 제외합니다 (섹션 10 LOGIN-REQ-005, 섹션 12 참고).

---

## 10. 기능 요구사항

### 요구사항 정의

**LOGIN-REQ-001**: 이메일 및 비밀번호 입력
- 사용자는 이메일 주소를 "Email Address" 입력란에 입력할 수 있어야 한다.
- 사용자는 비밀번호를 "Password" 입력란에 입력할 수 있어야 한다.
- 입력한 비밀번호는 마스킹(●●●●)되어 표시되어야 한다.

**LOGIN-REQ-002**: 유효한 자격증명으로 로그인
- 사용자가 등록된 이메일과 정확한 비밀번호를 입력한 후 "Login" 버튼을 클릭하면, 시스템은 자격증명을 검증해야 한다.
- 자격증명이 유효한 경우, 사용자는 메인 페이지(`https://automationexercise.com/`)로 이동해야 한다.

**LOGIN-REQ-003**: 로그인 상태 표시
- 로그인 성공 후 메인 페이지 헤더(네비게이션) 영역에 "Logout"이 노출되어야 한다.
- 로그인 전에는 "Login"이 단독으로 표시되는 것이 아니라, "Signup / Login" 통합 링크가 표시되어야 한다. (확인 완료, 스크린샷 근거)

**LOGIN-REQ-004**: 로그인 실패 오류 처리
- 이메일 또는 비밀번호가 잘못된 경우, "Password" 입력 필드 하단에 "Your email or password is incorrect!" 오류 메시지가 표시되어야 한다. (확인 완료)
- 오류 발생 시 페이지가 새로고침되지 않아야 한다. (현재 페이지 유지)

**LOGIN-REQ-005**: 필수 필드 검증
- 이메일과 비밀번호는 필수 입력 필드이다.
- 필수 필드가 공란인 경우의 실제 동작 검증(클라이언트/서버 사이드 유효성 검사 방식, 오류 메시지 문구 등)은 이번 자동화 범위에서 제외한다.

**LOGIN-REQ-006**: 로그인 보안
- 비밀번호는 HTTPS를 통해 암호화되어 전송되어야 한다.

**LOGIN-REQ-007**: 로그인 후 계정 관리 링크 노출 (신규, 확인 완료)
- 로그인 성공 후 메인 페이지 헤더(네비게이션) 영역에 "Delete Account" 링크가 노출되어야 한다. (스크린샷 근거)

**LOGIN-REQ-008**: 로그인 사용자명 표시 (신규, 확인 완료)
- 로그인 성공 후 메인 페이지 헤더(네비게이션) 영역에 "Logged in as {username}" 텍스트가 노출되어야 한다. (스크린샷 근거)
- 이 {username}은 회원가입 시 "Name" 필드에 입력한 값과 정확히 일치해야 하며(확인 완료), 단순히 "Logout 노출 여부"보다 더 강력한 로그인 성공 검증 포인트로 활용할 수 있다 (섹션 16 참고).

---

## 11. 자동화 대상 범위

### 자동화 범위 (포함)

| 시나리오 | 자동화 대상 | 설명 |
|---------|-----------|------|
| **정상 로그인** | ✅ 포함 | 유효한 이메일과 비밀번호로 로그인 성공 |
| **로그인 실패 (비밀번호 오류)** | ✅ 포함 | 잘못된 비밀번호 입력 시 오류 처리 |
| **로그인 실패 (존재하지 않는 이메일)** | ✅ 포함 | 미등록 이메일 입력 시 오류 처리 |
| **로그인 상태 표시** | ✅ 포함 | 로그인 후 메인 페이지 헤더에 "Logout", "Delete Account" 링크 및 "Logged in as {username}" 텍스트 노출 확인 (확인 완료, 스크린샷 근거) |

---

## 12. 자동화 제외 범위

### 자동화 제외 사유

| 기능 | 제외 사유 |
|------|---------|
| **입력 검증/경계값 테스트(비밀번호 길이, 이메일 형식, 대소문자, 공백 트리밍 등)** | 이번 프로젝트 범위를 로그인 성공/실패 핵심 흐름으로 한정 (경계값 검증은 이번 범위에서 제외) |
| **필수 필드 공란 상태에서 로그인 시도 케이스** | 이번 자동화 범위에서 제외 (섹션 9, LOGIN-REQ-005 참고) |
| **비밀번호 암호화 방식** | 서버 내부 구현 (테스트 불필요) |
| **보안 인증서 검증** | HTTPS/TLS 인증서 검증 (인프라 수준) |
| **세션/쿠키 생성·저장·만료 검증** | 이번 범위에서 세션/쿠키 자체를 검증하지 않으며, 로그인 상태는 화면 요소(헤더의 "Logout" 노출 여부)로만 판단함 |
| **IP 기반 보안 (2FA, MFA)** | MVP 범위 외 고급 보안 기능 |
| **CAPTCHA 또는 봇 방지** | 외부 서비스 의존성, 테스트 환경 구성 복잡 |
| **Remember me 쿠키 검증** | 선택사항 기능 (MVP에서 핵심이 아님) |
| **SQL Injection 또는 XSS 공격** | 보안 테스트 (별도 전문 도구 필요) |
| **브라우저 개발자 도구 헤더 조작** | 수동 테스트 범위 |

---

## 13. 정상 시나리오 (Normal Scenarios)

### NOR-001: 유효한 이메일과 비밀번호로 로그인 성공

**시나리오명**: 기존 회원이 올바른 자격증명으로 로그인

**전제조건**:
- 로그인 페이지가 표시됨
- 테스트 계정이 사전에 생성되어 있음 (이메일: `test@example.com`, 비밀번호: `password123`)

**테스트 단계**:
1. 로그인 페이지에서 "Email Address" 입력란에 `test@example.com` 입력
2. "Password" 입력란에 `password123` 입력
3. "Login" 버튼 클릭
4. 메인 페이지로 리다이렉트 완료 확인 (로딩 표시 없음, 확인 완료)

**기대 결과**:
- URL 변경: 로그인 페이지 → 메인 페이지(`https://automationexercise.com/`)
- 메인 페이지 헤더(네비게이션) 영역에 "Logout", "Delete Account" 링크 및 "Logged in as {username}" 텍스트가 노출됨

**검증 포인트**:
- ✅ 페이지 URL이 메인 페이지로 변경되었는가?
- ✅ 메인 페이지 헤더 영역에 "Logout"이 노출되었는가?
- ✅ 메인 페이지 헤더 영역에 "Delete Account" 링크가 노출되었는가? (확인 완료, 신규 검증 포인트)
- ✅ (강화된 검증) 메인 페이지 헤더 영역에 "Logged in as {username}" 텍스트가 노출되며, 이 {username}이 로그인 시도에 사용한 계정(`test@example.com`)의 사용자명과 실제로 일치하는가? (섹션 16 참고)

**예상 실행 시간**: 약 3~5초

---

### NOR-002: 로그아웃 후 재로그인 성공

**시나리오명**: 로그아웃한 사용자가 다시 로그인

**전제조건**:
- 사용자가 이미 로그인한 상태 (또는 회원가입 직후)
- "Logout" 버튼이 표시됨

**테스트 단계**:
1. "Logout" 버튼 클릭하여 로그아웃
2. 로그아웃 후 로그인 페이지로 이동
3. 동일한 이메일과 비밀번호로 재로그인 수행
4. 로그인 성공 확인

**기대 결과**:
- 로그아웃 후 "Signup / Login" 통합 링크 표시 (확인 완료, 스크린샷 근거)
- 재로그인 성공, 메인 페이지 헤더에 "Logout", "Delete Account" 링크 및 "Logged in as {username}" 텍스트 다시 노출

**검증 포인트**:
- ✅ 로그아웃 후 "Signup / Login" 통합 링크가 표시되었는가?
- ✅ 재로그인 후 메인 페이지 헤더에 "Logout"이 다시 노출되는가?
- ✅ 재로그인 후 "Logged in as {username}" 텍스트가 다시 노출되며, 재로그인에 사용한 계정의 사용자명과 일치하는가? (섹션 16 참고)

---

## 14. 비정상 시나리오 (Abnormal Scenarios)

### ABN-001: 잘못된 비밀번호로 로그인 시도

**시나리오명**: 존재하는 이메일이지만 비밀번호가 틀린 경우

**전제조건**:
- 로그인 페이지가 표시됨
- 테스트 계정 존재: `test@example.com` / `password123`

**테스트 단계**:
1. "Email Address" 입력란에 `test@example.com` 입력 (올바른 이메일)
2. "Password" 입력란에 `wrongpassword` 입력 (잘못된 비밀번호)
3. "Login" 버튼 클릭

**기대 결과**:
- 페이지 유지: 로그인 페이지에 머물러 있음
- 오류 메시지 표시: "Password" 입력 필드 하단에 "Your email or password is incorrect!" 노출 (확인 완료)

**검증 포인트**:
- ✅ "Password" 필드 하단에 "Your email or password is incorrect!" 오류 메시지가 표시되었는가?
- ✅ 로그인 페이지에 머물러 있는가?
- ✅ "Logout" 버튼이 표시되지 않는가?

**예상 실행 시간**: 약 2~3초

---

### ABN-002: 존재하지 않는 이메일로 로그인 시도

**시나리오명**: 등록되지 않은 이메일로 로그인 시도

**전제조건**:
- 로그인 페이지가 표시됨
- 테스트 계정과 다른 이메일 사용

**테스트 단계**:
1. "Email Address" 입력란에 `nonexistent@example.com` 입력 (존재하지 않는 이메일)
2. "Password" 입력란에 임의의 비밀번호 입력
3. "Login" 버튼 클릭

**기대 결과**:
- 페이지 유지: 로그인 페이지에 머물러 있음
- 오류 메시지 표시: "Password" 입력 필드 하단에 "Your email or password is incorrect!" 노출 (확인 완료)

**검증 포인트**:
- ✅ "Password" 필드 하단에 "Your email or password is incorrect!" 오류 메시지가 표시되었는가?
- ✅ 로그인 페이지에 머물러 있는가?

---

## 15. 기대 결과 (Expected Results)

### 성공 케이스 기대 결과

| 시나리오 | 페이지 상태 | 메시지/표시 |
|---------|-----------|-----------|
| **NOR-001** | 메인 페이지(`/`) | 헤더(네비게이션) 영역에 "Logout", "Delete Account" 링크 및 "Logged in as {username}" 텍스트 노출 |
| **NOR-002** | 메인 페이지(`/`) | 헤더(네비게이션) 영역에 "Logout", "Delete Account" 링크 및 "Logged in as {username}" 텍스트 노출 |

### 실패 케이스 기대 결과

| 시나리오 | 페이지 상태 | 오류 메시지 | 재시도 가능 |
|---------|-----------|-----------|----------|
| **ABN-001** | 로그인 페이지 유지 | "Password" 필드 하단에 "Your email or password is incorrect!" | ✅ 가능 |
| **ABN-002** | 로그인 페이지 유지 | "Password" 필드 하단에 "Your email or password is incorrect!" | ✅ 가능 |

---

## 16. 주요 검증 포인트 (Assertion Points)

### 참고: 스크린샷으로 확인된 더 강력한 검증 포인트

기존에는 로그인 성공 여부를 "헤더에 'Logout'이 노출되는가"라는 단일 기준으로만 판단했습니다. 이번에 스크린샷으로 실제 헤더 구조를 확인한 결과, 로그인 성공 시 헤더에 **"Logged in as {username}"**라는 텍스트가 추가로 노출되며, 이는 단순히 "로그인 상태인가"를 넘어 **실제 로그인 시도에 사용한 계정과 화면에 표시된 사용자명이 일치하는지까지 검증**할 수 있는 훨씬 더 강력한 검증 포인트입니다. 아래 검증 흐름에 이를 반영합니다.

**확인 완료**: {username}에는 회원가입 시 "Name" 필드에 입력한 값이 그대로 표시됩니다(이메일 주소나 이메일의 로컬 파트가 아님). 따라서 이 검증 포인트는 "로그인 시도에 사용한 계정으로 회원가입할 때 입력했던 Name 값"과 "로그인 후 헤더에 노출된 {username}"이 정확히 일치하는지를 검증하는 방식으로 구체화됩니다.

### 정상 로그인 검증

```
테스트 흐름:
1. 로그인 페이지 방문
   → 검증: URL이 로그인 페이지 URL과 일치하는가?
   → 검증: 페이지 제목이 "Login" 또는 유사한가?

2. 이메일과 비밀번호 입력
   → 검증: 입력 필드에 값이 입력되었는가?

3. "Login" 버튼 클릭
   → (로딩 표시 없음, 확인 완료 - 별도의 로딩 대기 로직 불필요)

4. 페이지 리다이렉트
   → 검증: URL이 메인 페이지(`/`)로 변경되었는가?
   → 검증: 페이지 로딩이 완료되었는가?

5. 로그인 상태 확인
   → 검증: 메인 페이지 헤더(네비게이션) 영역에 "Logout"이 노출되었는가?
   → 검증: "Signup / Login" 통합 링크가 더 이상 표시되지 않는가?
   → 검증: 메인 페이지 헤더(네비게이션) 영역에 "Delete Account" 링크가 노출되었는가? (확인 완료, 신규 검증 포인트)
   → 검증(강화): 메인 페이지 헤더(네비게이션) 영역에 "Logged in as {username}" 텍스트가 노출되며, 이 {username}이 로그인 시도에 사용한 계정으로 회원가입할 때 입력한 "Name" 값과 정확히 일치하는가? (확인 완료)
```

### 로그인 실패 검증

```
테스트 흐름:
1. 로그인 페이지 방문

2. 잘못된 자격증명 입력

3. "Login" 버튼 클릭

4. 오류 메시지 확인
   → 검증: "Password" 입력 필드 하단에 "Your email or password is incorrect!" 메시지가 표시되었는가?

5. 페이지 상태
   → 검증: 로그인 페이지에 머물러 있는가?
   → 검증: 페이지가 새로고침되지 않았는가?
   → 검증: 입력한 이메일이 유지되거나 초기화되었는가?
   → 검증: "Logout" 버튼이 표시되지 않는가?
```

### 프로그래밍적 검증 (pytest에서)

```python
# 예시 (구현 시 실제 코드는 테스트 레이어에서 작성)

# 성공 케이스
login_page.enter_email("test@example.com")
login_page.enter_password("password123")
login_page.click_login_button()

home_page = HomePage(driver)
# 메인 페이지 헤더 영역에 "Logout"이 노출되는 것으로 로그인 상태를 확인
assert home_page.is_logout_link_displayed() == True
# "Logged in as {username}" 텍스트로 실제 로그인한 계정과 일치하는지 확인 (더 강력한 검증, 확인 완료)
# {username}에는 회원가입 시 "Name" 필드에 입력한 값이 그대로 표시됨 (확인 완료, 섹션 7, 20 참고)
assert home_page.get_logged_in_username() == "Test User"  # 예시 값: 해당 계정 회원가입 시 입력한 Name 값

# 실패 케이스
login_page.enter_email("test@example.com")
login_page.enter_password("wrongpassword")
login_page.click_login_button()

assert login_page.is_error_message_displayed() == True
assert "Your email or password is incorrect!" in login_page.get_error_message_text()
```

---

## 17. 필요한 테스트 데이터

### 테스트 계정 정보

| 용도 | 이메일 | 비밀번호 | Name (회원가입 시 입력값) | 상태 | 비고 |
|------|--------|---------|--------------------------|------|------|
| **정상 로그인 테스트** | `test001@example.com` | `password123` | `Test User 001` | 활성 | 미리 생성된 계정 |
| **재로그인 테스트** | `test002@example.com` | `securepass456` | `Test User 002` | 활성 | 미리 생성된 계정 |
| **비정상 테스트용** | `invalid@example.com` | 임의 | - | 미존재 | 고의로 미생성 |

**확인 완료**: "Logged in as {username}" 텍스트 검증(섹션 16 강화된 검증 포인트)을 위해서는 각 테스트 계정에 대해 회원가입 시 사용한 "Name" 값을 그대로 `expected_username`으로 사용하면 됩니다. {username}에는 이메일이나 이메일의 로컬 파트가 아니라 회원가입 폼의 "Name" 필드 입력값이 그대로 표시되는 것으로 확인되었으므로(섹션 7, 20 참고), 위 표의 "Name (회원가입 시 입력값)" 컬럼 값을 각 테스트 계정의 `expected_username`으로 관리합니다.

### 테스트 데이터 관리 방식

**방식 1: 환경변수 (.env 파일)**
```
TEST_EMAIL=test001@example.com
TEST_PASSWORD=password123
TEST_INVALID_EMAIL=invalid@example.com
TEST_INVALID_PASSWORD=wrongpassword
```

**방식 2: JSON 파일 (test_data/accounts.json)**
```json
{
  "valid_account": {
    "email": "test001@example.com",
    "password": "password123",
    "expected_username": "Test User 001"
  },
  "invalid_password": {
    "email": "test001@example.com",
    "password": "wrongpassword"
  },
  "nonexistent_email": {
    "email": "invalid@example.com",
    "password": "anypassword"
  }
}
```

**참고**: `expected_username`은 해당 계정으로 회원가입할 때 "Name" 필드에 입력한 값을 그대로 사용합니다(확인 완료).

**방식 3: pytest Fixture (conftest.py)**
```python
@pytest.fixture
def valid_login_credentials():
    return {
        "email": "test001@example.com",
        "password": "password123",
        "expected_username": "Test User 001"  # 회원가입 시 Name 필드에 입력한 값
    }

@pytest.fixture
def invalid_login_credentials():
    return {
        "email": "test001@example.com",
        "password": "wrongpassword"
    }
```

### 데이터 보호 규칙
- ❌ 비밀번호를 코드에 하드코딩하지 않음
- ❌ 로그 또는 리포트에 비밀번호 노출 금지
- ✅ 환경변수 또는 외부 파일에서 관리
- ✅ 민감정보는 마스킹 처리하여 로깅

### 확인 완료
- Automation Exercise에서 동일 이메일로 중복 가입 불가 (확인 완료, signup.md 섹션 9 참고)
- 이메일 인증 절차 불필요 (확인 완료)
- 테스트 환경에서 사이트 접근 제약 없음 (확인 완료)
- 테스트 계정 준비 방식: 사전 생성 (테스트 실행 전 미리 생성해둔 고정 계정 사용) (확정)

---

## 18. 다른 기능과의 의존성

### 이 기능이 의존하는 다른 기능

| 기능 | 의존 관계 | 설명 |
|------|---------|------|
| **회원가입 (Signup)** | 선행 필수 | 로그인 전에 계정이 먼저 생성되어야 함. 특히 회원가입 시 "Name" 필드에 입력한 값이 로그인 성공 후 메인 페이지 헤더의 "Logged in as {username}" 텍스트로 그대로 노출되므로(확인 완료), 로그인 기능의 사용자명 검증(LOGIN-REQ-008, 섹션 16)은 회원가입 시 입력한 Name 값에 직접 의존함 |
| **홈 페이지 (Home)** | 진입 경로 | 홈 페이지의 "Signup / Login" 통합 링크를 통해 로그인 페이지 진입 (확인 완료, 스크린샷 근거) |

### 이 기능을 필요로 하는 다른 기능

| 기능 | 의존 관계 | 설명 |
|------|---------|------|
| **로그아웃 (Logout)** | 후행 기능 | 로그인하지 않으면 로그아웃을 할 수 없음 |
| **상품 검색 (Product Search)** | 로그인 후 기능 | 로그인 상태에서 개인화된 검색 기능 사용 (선택사항) |
| **장바구니 (Shopping Cart)** | 로그인 후 기능 | 로그인 후 장바구니 기능 활용 (일부 기능) |
| **주문 (Checkout)** | 로그인 필수 | 주문 시 로그인이 필수 (일반적) |

**참고(logout.md와의 정합성)**: 현재 `docs/prd/features/logout.md`는 "로그아웃 후 헤더에 'Login'/'Signup' 링크가 각각 노출된다"는 표현을 사용하고 있으나, 이번에 스크린샷으로 확인된 바에 따르면 실제로는 "Login"과 "Signup"이 별도 링크가 아니라 **하나의 "Signup / Login" 통합 링크**로 노출됩니다. 이는 이번 login.md 수정 범위에서 함께 정정하지 않았으며, logout.md 쪽도 추후 동일한 내용으로 정정이 필요함을 참고사항으로 남깁니다 (logout.md 자체 수정은 이번 작업 범위 밖).

### 의존성 흐름도

```
회원가입 (Signup)
    ↓
로그인 (Login) ← [이 기능]
    ↓
홈 페이지 (메인 페이지)
    ├─→ 상품 검색 (Product Search)
    ├─→ 장바구니 (Shopping Cart)
    └─→ 로그아웃 (Logout)
```

---

## 19. 자동화 구현 시 고려사항

**안내**: 아래 코드는 구조 설명을 위한 예시(스텁)이며 실제 동작 코드는 아닙니다. **Locator 값은 예시이며, 실제 id/name/data-* 속성은 Page Object 구현 착수 시 사용자가 실시간으로 공유할 예정입니다.**

### Page Object 설계 방향

#### LoginPage 클래스 구조 (예시 - 구현은 별도 작성)

```python
# pages/login_page.py 구조 (실제 코드 아님)
# 아래 Locator 값은 예시이며, 실제 값은 Page Object 구현 착수 시 사용자가 공유할 예정입니다.

class LoginPage(BasePage):
    # Locator 정의 (상수)
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button.login")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "p.error-message")  # Password 필드 하단에 노출되는 오류 메시지

    # 화면 조작 메서드 (값 반환 또는 상태 변경)
    def enter_email(self, email: str) -> None:
        """이메일 입력란에 이메일 입력"""
        pass
    
    def enter_password(self, password: str) -> None:
        """비밀번호 입력란에 비밀번호 입력"""
        pass
    
    def click_login_button(self) -> None:
        """로그인 버튼 클릭"""
        pass
    
    def is_error_message_displayed(self) -> bool:
        """오류 메시지("Your email or password is incorrect!") 표시 여부 반환"""
        pass
    
    def get_error_message_text(self) -> str:
        """오류 메시지 텍스트 반환"""
        pass
    
    def is_on_login_page(self) -> bool:
        """현재 URL이 로그인 페이지인지 여부 반환"""
        pass
```

#### 참고: 헤더 네비게이션(HomePage) 관련 메서드 네이밍 고려사항

섹션 16의 예시 코드에서 사용된 `home_page.is_logout_link_displayed()`, `home_page.get_logged_in_username()` 등은 헤더 공통 영역을 다루는 `HomePage`(또는 공통 헤더 컴포넌트) 클래스에 구현될 것으로 예상되는 메서드이며, 이 문서(login.md)에서 상세 구현을 정의하지는 않습니다. 다만 이번에 헤더 네비게이션의 실제 구조가 "Signup / Login" 통합 링크임이 확인되었으므로, 향후 Page Object 구현 시 다음을 참고할 것을 권장합니다.
- 비로그인 상태의 통합 링크를 조회하는 메서드는 `is_login_link_displayed()`처럼 "Login"만 가리키는 이름 대신, `is_signup_login_link_displayed()` 등 "Signup / Login" 통합 링크임을 명확히 드러내는 이름을 사용하는 것을 검토
- 로그인 사용자명을 조회하는 메서드(`get_logged_in_username()`)는 "Logged in as {username}" 텍스트에서 {username} 부분만 추출하여 반환하도록 설계 (텍스트 파싱 로직은 utils 또는 BasePage 공통 메서드로 분리 검토). {username}은 회원가입 시 "Name" 필드에 입력한 값이 그대로 표시되는 것으로 확인되었으므로(확인 완료), 테스트 코드에서는 이 메서드의 반환값을 해당 계정 회원가입 시 사용한 Name 값(`expected_username`)과 비교하여 검증하는 방식을 권장
- HomePage 클래스 자체의 상세 설계는 이 문서(login.md)의 범위가 아니며, 홈 페이지 기능 PRD 또는 로그아웃 기능 PRD(`docs/prd/features/logout.md`)에서 구체화될 수 있습니다.

### Locator 선택 원칙

**우선순위** (CLAUDE.md 기준):
1. **id 속성** (가장 안정적)
   ```python
   EMAIL_INPUT = (By.ID, "email")
   PASSWORD_INPUT = (By.ID, "password")
   ```

2. **data-* 속성** (테스트용)
   ```python
   LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-qa='login-button']")
   ```

3. **name 속성**
   ```python
   EMAIL_INPUT = (By.NAME, "email")
   ```

4. **안정적인 CSS Selector**
   ```python
   ERROR_MESSAGE = (By.CSS_SELECTOR, "form.login-form p")
   ```

5. **상대 XPath** (마지막 수단)
   ```python
   ERROR_MESSAGE = (By.XPATH, "//form[@action='/login']//p")
   ```

**금지**: Full XPath 절대 금지
```python
# ❌ 금지
ERROR_MESSAGE = (By.XPATH, "/html/body/div[1]/div[2]/form/div[3]/p")
```

**안내**: 위 Locator는 모두 예시 값입니다. 실제 id/name/data-* 속성은 Page Object 구현 착수 시 사용자가 실시간으로 공유할 예정이며, 별도의 사전 개발자 도구 조사는 필요하지 않습니다.

### Wait 처리 전략

**명시적 Wait 사용** (time.sleep() 절대 금지):

```python
# ✅ 올바른 방식 (예시 - 실제 코드 아님)
def login(self, email: str, password: str):
    # 이메일 입력 가능 상태 대기
    wait.until(EC.element_to_be_clickable(self.EMAIL_INPUT))
    self.find_element(self.EMAIL_INPUT).send_keys(email)
    
    # 비밀번호 입력
    self.find_element(self.PASSWORD_INPUT).send_keys(password)
    
    # 로그인 버튼 클릭 가능 상태 대기
    wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
    self.click(self.LOGIN_BUTTON)
    
    # 메인 페이지로 전환될 때까지 대기 (로딩 표시 없음, 확인 완료)
    wait.until(EC.presence_of_element_located(HomePage.LOGOUT_LINK))
```

### 동적 요소 처리

- **오류 메시지**: 오류 메시지가 나타날 때까지 대기 (최대 5~10초)
- **페이지 전환**: 새 페이지 로드 완료까지 명시적 대기
- **로딩 표시**: 로그인 버튼 클릭 후 스피너 등 로딩 표시는 없는 것으로 확인됨 (별도 대기 로직 불필요)

### 재사용 가능한 메서드

**BasePage에 추가할 공통 메서드**:

```python
# base_page.py (예시)

class BasePage:
    # 입력 필드 처리
    def send_keys_to_element(self, locator, text: str) -> None:
        """요소에 텍스트 입력 (명시적 대기 포함)"""
        pass
    
    def clear_and_send_keys(self, locator, text: str) -> None:
        """입력 필드 초기화 후 텍스트 입력"""
        pass
    
    # 대기 메서드
    def wait_for_element_clickable(self, locator, timeout=10) -> WebElement:
        """요소가 클릭 가능해질 때까지 대기"""
        pass
    
    def wait_for_element_presence(self, locator, timeout=10) -> WebElement:
        """요소가 DOM에 나타날 때까지 대기"""
        pass
    
    def wait_for_text_change(self, locator, expected_text, timeout=10) -> bool:
        """요소 텍스트가 특정 값으로 변경될 때까지 대기"""
        pass
    
    # 검증 메서드
    def is_element_displayed(self, locator) -> bool:
        """요소 표시 여부"""
        pass
    
    def get_element_text(self, locator) -> str:
        """요소 텍스트 조회"""
        pass
```

### 네트워크 지연 고려

- **타임아웃 설정**: 기본 10초, 페이지 로드는 20초 (프로젝트 PRD 기준)
- **재시도 로직**: 네트워크 오류 시 1회 재시도 (선택사항)
- **느린 네트워크**: 타임아웃을 충분히 설정하여 안정성 확보

### 예시: 로그인 테스트 구현 방향

```python
# tests/test_login.py 구조 (실제 코드 아님)

def test_login_with_valid_credentials(driver, valid_credentials):
    # 1. 로그인 페이지 진입
    login_page = LoginPage(driver)
    login_page.navigate_to_login()
    
    # 2. 로그인 수행
    login_page.enter_email(valid_credentials["email"])
    login_page.enter_password(valid_credentials["password"])
    login_page.click_login_button()
    
    # 3. 로그인 성공 확인 (메인 페이지 헤더에 "Logout" 노출로 확인)
    home_page = HomePage(driver)
    assert home_page.is_logout_link_displayed()
    # 4. (강화된 검증) "Logged in as {username}" 텍스트가 회원가입 시 입력한 Name 값과 일치하는지 확인 (확인 완료)
    # valid_credentials["expected_username"]은 해당 계정 회원가입 시 "Name" 필드에 입력한 값
    assert home_page.get_logged_in_username() == valid_credentials["expected_username"]

def test_login_with_invalid_password(driver, valid_email):
    login_page = LoginPage(driver)
    login_page.navigate_to_login()
    
    # 잘못된 비밀번호로 로그인 시도
    login_page.enter_email(valid_email)
    login_page.enter_password("wrongpassword")
    login_page.click_login_button()
    
    # 오류 메시지 확인
    assert login_page.is_error_message_displayed()
    assert "Your email or password is incorrect!" in login_page.get_error_message_text()
    assert login_page.is_on_login_page()
```

---

## 20. 확인이 필요한 미확정 사항

### 확인 완료 항목 (실제 사이트 확인으로 확인됨)

다음 항목들은 실제 사이트 방문 결과로 확인이 완료되어 더 이상 미확정 사항이 아닙니다:

- ✅ 로그인 페이지의 정확한 URL은 `https://automationexercise.com/login`
- ✅ 로그인 실패 시 오류 메시지는 "Password" 입력 필드 하단에 "Your email or password is incorrect!" 문구로 노출됨
- ✅ 로그인 버튼 클릭 후 로딩 표시(스피너 등)는 없음
- ✅ 로그인 성공 시 메인 페이지(`https://automationexercise.com/`)로 이동하며, 헤더(네비게이션) 영역에 "Logout"이 노출되는 것으로 로그인 상태를 확인함
- ✅ 로그인 실패 시 페이지 새로고침 없이 로그인 페이지가 유지되며 오류 메시지가 노출됨
- ✅ Automation Exercise에서 동일 이메일로 중복 가입 불가 (확인 완료, signup.md 섹션 9 참고)
- ✅ 이메일 인증 절차 불필요 (확인 완료)
- ✅ 테스트 환경에서 사이트 접근 제약 없음 (확인 완료)
- ✅ 테스트 계정 준비 방식: 사전 생성 (테스트 실행 전 미리 생성해둔 고정 계정 사용) (확정)
- ✅ **(신규, 스크린샷 근거)** 로그인되지 않은 상태의 헤더 네비게이션은 `Home | Products | Cart | Signup / Login | Test Cases | API Testing | Video Tutorials | Contact us` 순서로 구성되며, "Login"이 단독 노출되지 않고 "Signup / Login" 하나의 통합 링크로 노출됨
- ✅ **(신규, 스크린샷 근거)** 로그인 상태의 헤더 네비게이션은 `Home | Products | Cart | Logout | Delete Account | Test Cases | API Testing | Video Tutorials | Contact us | Logged in as {username}` 순서로 구성되며, "Delete Account" 링크와 "Logged in as {username}" 텍스트가 추가로 노출됨
- ✅ **(신규)** "Logged in as {username}"의 표시 형식: {username}에는 회원가입 시 "Name" 필드에 입력한 값이 그대로 표시됨 (이메일 주소나 이메일의 로컬 파트가 아님). 이에 따라 섹션 16의 강화된 검증 포인트(계정 일치 여부 검증)와 섹션 17의 `expected_username` 테스트 데이터가 구체적으로 확정됨

### 여전히 확인이 필요한 항목

#### UI 요소 Locator (개발 착수 시 공유 예정)
- "Email Address", "Password" 입력 필드, "Login" 버튼, 오류 메시지 요소의 실제 HTML id, name, data-* 속성은 Page Object 구현 착수 시 사용자가 실시간으로 공유할 예정입니다. 별도의 사전 개발자 도구 조사는 필요하지 않습니다.

---

## 21. 완료 조건

### 로그인 기능 자동화 완료 기준

**정상 시나리오 완료**:
- ✅ NOR-001 (유효한 자격증명으로 로그인): 테스트 PASS
- ✅ NOR-002 (로그아웃 후 재로그인): 테스트 PASS

**비정상 시나리오 완료**:
- ✅ ABN-001 (잘못된 비밀번호): 테스트 PASS
- ✅ ABN-002 (존재하지 않는 이메일): 테스트 PASS

**코드 품질 기준** (CLAUDE.md 준수):
- ✅ Page Object 설계: LoginPage 클래스 구현 완료
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
  - 각 테스트가 단독 실행 가능
  - 테스트 간 순서 의존성 없음
  - 각 테스트에서 필요한 데이터 준비
  
- ✅ 코딩 컨벤션:
  - 파일명: snake_case (login_page.py, test_login.py)
  - 클래스명: PascalCase + Page 접미사 (LoginPage)
  - 메서드명: snake_case, 동사로 시작 (enter_email, click_login_button)
  - 테스트 함수명: test_ 접두사 (test_login_with_valid_credentials)
  - 2칸 들여쓰기

- ✅ 민감정보 보호:
  - 계정 정보 환경변수 또는 외부 파일로 관리
  - 코드에 비밀번호 하드코딩 안 함
  - 로그에서 비밀번호 마스킹

**테스트 실행 기준**:
- ✅ 모든 테스트 PASS (성공률 100%)
- ✅ 실패 시 스크린샷 저장 확인
- ✅ pytest-html 리포트 생성 확인
- ✅ 로그 파일 생성 확인

**문서 기준**:
- ✅ 이 PRD가 완성되고 검토됨
- ✅ Page Object 구현 착수 시 Locator 공유 프로세스가 합의됨
- ✅ 섹션 20의 "여전히 확인이 필요한 항목"들이 실제 사이트 방문으로 검증됨

**배포 기준**:
- ✅ 모든 테스트 코드 완성
- ✅ 코드 리뷰 완료
- ✅ GitHub Actions CI/CD 테스트 통과
- ✅ 회원가입 기능 PRD(`docs/prd/features/signup.md`)와의 일관성 검증

---

## 22. 다음 단계

### 즉시 작업 (이 PRD 이후)
1. **테스트 계정 준비**: 사전 생성 방식으로 테스트용 이메일, 비밀번호, Name(=`expected_username`) 값을 생성/확인 (테스트 실행 중 동적 생성 방식은 사용하지 않음)
2. **Locator 공유 대기**: Page Object 구현 착수 시 사용자로부터 각 UI 요소("Email Address", "Password" 입력란, "Login" 버튼, 오류 메시지 요소, 헤더의 "Signup / Login"/"Logout"/"Delete Account" 링크, "Logged in as {username}" 텍스트)의 id, name, CSS 클래스, data-* 속성을 실시간으로 공유받기
3. **Page Object 구현**: LoginPage 클래스 작성 (pages/login_page.py)
4. **테스트 코드 작성**: 로그인 기능 테스트 케이스 작성 (tests/test_login.py)
5. **테스트 실행**: pytest를 사용하여 정상/비정상 시나리오(NOR-001~002, ABN-001~002) 테스트 실행
6. **오류 수정**: 실패한 테스트 분석 및 수정

### 추후 작업 (이 기능 완료 후)
1. **로그아웃 (Logout) 기능**: 로그아웃 기능의 PRD 및 테스트 작성
2. **통합 테스트**: 회원가입 → 로그인 → 로그아웃의 전체 흐름 테스트
3. **다른 기능**: Phase 1 나머지 기능 (상품 검색) 자동화
4. **로그인 실패/경계값 테스트 확장 검토**: 이번 범위에서 제외한 빈 필드 입력, 경계값(비밀번호 길이, 이메일 형식 등) 시나리오를 추후 별도 범위로 추가할지 검토

---

## 23. 참고 자료

### 관련 문서
- **프로젝트 전체 PRD**: `docs/prd/project-prd.md`
- **회원가입 기능 PRD**: `docs/prd/features/signup.md`
- **프로젝트 개발 규칙**: `CLAUDE.md`
- **기능별 PRD 작성 가이드**: `docs/PRD_PROMPT.md` (있는 경우)

### 외부 참고
- **Automation Exercise 공식**: https://automationexercise.com/
- **Selenium 문서**: https://selenium.dev/documentation/
- **pytest 문서**: https://docs.pytest.org/

### 버전 관리
- **이 PRD 버전**: 1.4 ("Logged in as {username}" 표시 형식 확인 완료 반영)
- **작성일**: 2026-07-20
- **최종 검토일**: 2026-07-22
- **최종 승인일**: (예정)

**변경 이력**:
- v1.4 (2026-07-22): "Logged in as {username}"에 실제로 표시되는 문자열의 형식이 확인됨 — 회원가입 시 "Name" 필드에 입력한 값이 그대로 표시되며, 이메일 주소나 이메일의 로컬 파트가 아님을 확정. 이에 따라 섹션 7(UI 요소, "확인 필요" → "확인 완료" 전환), 섹션 10(LOGIN-REQ-008 구체화), 섹션 16(강화된 검증 포인트 및 예시 코드에서 "확인 필요" 문구 제거, Name 값과의 일치 검증으로 구체화), 섹션 17(테스트 계정 표에 Name 컬럼 추가, `expected_username`을 회원가입 Name 값으로 확정), 섹션 18(회원가입 기능과의 의존 관계에 Name→{username} 연결 관계 추가), 섹션 19(`get_logged_in_username()` 관련 설명 및 예시 코드 보강), 섹션 20(관련 미확정 항목을 확인 완료로 이동), 섹션 22(관련 확인 작업 항목 제거)를 모두 갱신
- v1.3 (2026-07-22): 실제 사이트 스크린샷으로 확인된 헤더 네비게이션 구조를 반영. 로그인되지 않은 상태의 헤더가 "Login" 단독 링크가 아니라 "Signup / Login" 통합 링크로 노출됨을 확정하고, 관련 서술(섹션 4, 7, 10, 13, 16, 18) 전체 정정. 로그인 상태의 헤더에 "Delete Account" 링크와 "Logged in as {username}" 텍스트가 추가로 노출됨을 신규 확인하여 LOGIN-REQ-007/008 요구사항 신설, 섹션 7 UI 요소 표 및 헤더 목업 보강, 섹션 8·13·16의 정상 흐름/시나리오/검증 포인트에 반영. 특히 "Logged in as {username}"을 활용해 로그인 시도 계정과 실제 노출된 사용자명의 일치 여부까지 검증하는 강화된 검증 포인트를 섹션 16에 추가하고, 이에 따른 테스트 데이터 요구사항(섹션 17)과 미확정 사항(username 표시 형식, 섹션 20)을 추가. logout.md와의 표현 불일치(참고사항)를 섹션 18에 기록(logout.md 자체는 이번 범위에서 수정하지 않음)
- v1.2 (2026-07-21): 테스트 계정 준비 방식을 사전 생성으로 확정 (테스트 실행 전 미리 생성해둔 고정 계정 사용, 테스트 중 동적 생성 방식은 사용하지 않음). 섹션 17, 20의 "확인 필요" 항목을 "확인 완료"로 전환, 섹션 22 "다음 단계"의 테스트 계정 준비 항목 문구 구체화
- v1.1 (2026-07-21): 실사이트 확인 결과를 반영해 범위 확정. 로그인 실패 오류 메시지를 "Your email or password is incorrect!"(Password 필드 하단 노출)로 확정, 로딩 스피너 없음 확인, 로그인 성공 확인 방법을 "메인 페이지 헤더의 Logout 노출"로 통일(대시보드 표현 삭제), 세션/쿠키 관련 요구사항·검증 항목(LOGIN-REQ-006, 세션 생성 확인 등) 전체 제거, 경계값 시나리오(BND-001~005) 섹션 삭제 및 자동화 제외 범위로 이관, 필수 필드 공란 케이스(ABN-003, ABN-004) 자동화 범위에서 제외, 회원가입 후 진입 경로 삭제(회원가입 완료 시 로그인 페이지를 거치지 않음), Locator는 Page Object 구현 착수 시 사용자가 공유하는 방식으로 통일
- v1.0 (2026-07-20): 최초 작성 (초안)

---

**작성자**: Automation Testing Framework Lead  
**최종 검토자**: (예정)  
**승인 상태**: 초안 (검토 대기 중)

이 문서는 로그인 기능의 자동화 테스트 작성 시 기준이 되는 요구사항 명세입니다.  
실제 구현 과정에서 새로운 정보가 발견되면 이 문서를 업데이트합니다.
