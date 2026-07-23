# 회원가입 (Sign Up) 기능 상세 PRD

**작성 일자**: 2026-07-20  
**최종 수정일**: 2026-07-23 (login.md와의 테스트 계정 준비 방식 동기화)  
**버전**: 1.4  
**상태**: 초안 (회원가입 성공 흐름 중심으로 범위 확정. Locator는 Page Object 구현 착수 시 사용자가 실시간으로 공유할 예정)

---

## 1. 기능명

- **한국어명**: 회원가입
- **영문명**: Sign Up
- **기능 ID**: SIGNUP

---

## 2. 기능 목적

신규 사용자가 이메일과 비밀번호를 포함한 계정 정보를 등록하여 시스템에 신규 회원으로 가입하고, 이후 로그인을 통해 회원 전용 기능에 접근할 수 있도록 하는 기능입니다.

### 비즈니스 가치
- 신규 사용자 확보 및 계정 생성
- 개인화된 사용자 경험 제공 기반 마련
- 사용자별 데이터(주문 이력, 장바구니 등) 관리 준비
- 로그인을 통한 보안 기반 제공

---

## 3. 프로젝트 전체 PRD와의 연관성

### 기준 문서
**참고**: `docs/prd/project-prd.md`

### 연관 섹션
- **8.1 Phase 1**: 기본 사용자 인증 및 탐색 (필수 기능)
- **9.1 주요 사용자 흐름**: 단계 1 (회원가입) - Happy Path 정의
- **5.2 MVP 대상 기능**: 우선순위 1 (필수)

### 의존성
- **후행 기능**: 로그인 (Login)
  - 회원가입으로 계정을 생성한 후 로그인을 수행해야 함
  
---

## 4. 대상 URL 또는 진입 경로

**확인 완료**: 실제 사이트 방문(스크린샷) 결과, 회원가입은 아래와 같이 3단계 URL을 거치는 흐름으로 확인되었습니다.

### 관련 URL (3단계)
1. **로그인 페이지**: `https://automationexercise.com/login`
   - "New User Signup!" 영역에서 Name, Email Address를 입력하고 "Signup" 버튼을 클릭하는 진입 지점
   - **이메일 중복 검사가 이 단계(Signup 버튼 클릭 시점)에서 수행됨**: 이미 등록된 이메일이면 `/signup` 페이지로 이동하지 못하고 이 페이지에서 가입 불가 처리됨 (비즈니스 규칙, 섹션 9 "입력값 특성 / 비즈니스 규칙" 참고). 단, 이 실패 흐름 자체는 이번 자동화 범위에서 제외됩니다 (섹션 11 참고).
2. **회원가입 페이지**: `https://automationexercise.com/signup`
   - 로그인 페이지에서 미등록 이메일로 "Signup" 버튼 클릭 시에만 진입 가능
   - "ENTER ACCOUNT INFORMATION"과 "ADDRESS INFORMATION" 두 영역의 상세 정보 입력 후 "Create Account" 클릭
3. **회원가입 완료 페이지**: `https://automationexercise.com/account_created`
   - "Create Account" 클릭 성공 시 이동하는 완료 안내 페이지
   - "Continue" 버튼 클릭 시 로그인된 상태로 메인 페이지(`https://automationexercise.com/`)로 이동

### 진입 경로 (사용자 흐름)
1. **로그인 페이지에서 진입**: 로그인 페이지(`/login`)의 "New User Signup!" 영역에서 Name, Email Address 입력 후 "Signup" 버튼 클릭 → `/signup` 페이지로 이동
   - 참고: 입력한 이메일이 이미 등록된 이메일인 경우 `/signup` 페이지로 이동하지 않음 (비즈니스 규칙). 이 실패 흐름은 이번 자동화 범위(회원가입 성공 흐름)에서 제외됩니다.

---

## 5. 사용자 역할

### 대상 사용자
- **신규 사용자 (New User)**: 아직 계정을 생성하지 않은 사용자
  - 이메일 주소 보유
  - 사이트에 처음 방문하는 사용자

### 사용자 시나리오
- 첫 가입: 새로운 계정 생성 (이번 PRD의 자동화 대상)
- 재가입: 동일 이메일로는 재가입이 불가능함 (비즈니스 규칙, 확인 완료). 이 실패 흐름에 대한 테스트 케이스는 이번 자동화 범위에서 제외됩니다.

---

## 6. 사전 조건 (Precondition)

### 필수 조건
1. **로그인하지 않은 상태**: 테스트 시작 전 로그아웃 상태 또는 비회원 상태
   - 기존 로그인 상태가 없음
   - 쿠키/세션이 초기화된 상태

2. **사이트 접근**: Automation Exercise 사이트에 접근 가능
   - 인터넷 연결이 정상
   - 사이트가 운영 중 (다운타임 없음)

3. **유효한 이메일 주소**: 사용 가능한 이메일 주소 준비
   - 미등록 이메일 (새로운 계정 생성)
   - 유효한 이메일 형식

### 테스트 데이터 준비
- 회원가입 시 사용할 유효한 이메일 주소
- 회원가입 시 사용할 비밀번호
- 회원 정보 (이름, 주소 등 - 페이지에 필수 입력 항목에 따라 준비)

---

## 7. 주요 화면과 UI 요소

**확인 완료**: 아래 화면 구성은 실제 사이트 방문(스크린샷 5장) 결과를 반영하여 작성되었습니다.

### 화면 1: 로그인 페이지(`/login`) - New User Signup! 영역

```
┌─────────────────────────────────────┐
│        New User Signup!             │  (영역 제목)
│                                     │
│  Name                               │  (이름 입력 필드)
│  [____________________]            │
│                                     │
│  Email Address                      │  (이메일 입력 필드)
│  [____________________]            │
│                                     │
│  [   Signup   ]                     │  (Signup 버튼)
│                                     │
└─────────────────────────────────────┘
```

| 요소명 | 타입 | 설명 | 필수 여부 |
|--------|------|------|---------|
| **Name 입력란** | Input (Text) | 사용자 이름 입력 | 필수 |
| **Email Address 입력란** | Input (Email) | 이메일 주소 입력 | 필수 |
| **Signup 버튼** | Button | 입력한 Name/Email로 `/signup` 페이지 이동을 시도하는 버튼. 이 클릭 시점에 이메일 중복 검사가 수행됨 | 필수 |

### 화면 2: 회원가입 페이지(`/signup`) - ENTER ACCOUNT INFORMATION 영역

```
┌───────────────────────────────────────────────────┐
│           ENTER ACCOUNT INFORMATION                │  (영역 제목)
│                                                     │
│  Title                                             │  (Mr./Mrs. 선택 - 선택사항)
│    o Mr.    o Mrs.                                 │
│                                                     │
│  Name *                                            │  (기본값 채움, 수정 가능)
│  [John Doe___________]                             │
│                                                     │
│  Email *                                           │  (dim 처리, 수정 불가)
│  [newuser@example.com]                             │
│                                                     │
│  Password *                                        │  (마스킹 처리)
│  [____________________]                            │
│                                                     │
│  Date of Birth                                     │  (선택사항)
│  [Day v] [Month v] [Year v]                        │
│                                                     │
│  ☐ Sign up for our newsletter!                     │  (체크박스, 선택사항)
│  ☐ Receive special offers from our partners!       │  (체크박스, 선택사항)
└───────────────────────────────────────────────────┘
```

| 요소명 | 타입 | 설명 | 필수 여부 |
|--------|------|------|---------|
| **Title 라디오 버튼** | Radio (Mr./Mrs.) | 호칭 선택 | 선택 |
| **Name 입력란** | Input (Text) - 일반 입력 필드 | 로그인 페이지에서 입력한 이름이 기본값으로 채워지며, `/signup` 페이지에서 사용자가 값을 수정할 수 있음 | 필수(자동 채움, 수정 가능) |
| **Email 입력란** | Input (Email) - dim 처리, 수정 불가 | 로그인 페이지에서 입력한 이메일이 그대로 노출되며 수정할 수 없음 | 필수(자동 채움, 수정 불가) |
| **Password 입력란** | Input (Password) | 비밀번호 입력, 입력 시 마스킹(●●●●) 처리 | 필수 |
| **Date of Birth (Day/Month/Year) 드롭다운 3종** | Select | 생년월일 선택 | 선택 |
| **Sign up for our newsletter! 체크박스** | Checkbox | 뉴스레터 수신 동의 | 선택 |
| **Receive special offers from our partners! 체크박스** | Checkbox | 특별 혜택 정보 수신 동의 | 선택 |

### 화면 3: 회원가입 페이지(`/signup`) - ADDRESS INFORMATION 영역

```
┌───────────────────────────────────────────────────┐
│              ADDRESS INFORMATION                   │  (영역 제목)
│                                                     │
│  First name *                                      │
│  [____________________]                            │
│                                                     │
│  Last name *                                        │
│  [____________________]                            │
│                                                     │
│  Company                                            │  (선택사항)
│  [____________________]                            │
│                                                     │
│  Address *                                          │
│  [____________________]                            │
│                                                     │
│  Address2                                           │  (선택사항)
│  [____________________]                            │
│                                                     │
│  Country *                                          │  (드롭다운, 기본값: India)
│  [ India v ]                                        │
│                                                     │
│  State *                                            │
│  [____________________]                            │
│                                                     │
│  City *                                             │
│  [____________________]                            │
│                                                     │
│  Zipcode *                                          │
│  [____________________]                            │
│                                                     │
│  Mobile Number *                                    │
│  [____________________]                            │
│                                                     │
│  [    Create Account    ]                           │  (버튼)
└───────────────────────────────────────────────────┘
```

| 요소명 | 타입 | 설명 | 필수 여부 |
|--------|------|------|---------|
| **First name 입력란** | Input (Text) | 이름 입력 | 필수 |
| **Last name 입력란** | Input (Text) | 성 입력 | 필수 |
| **Company 입력란** | Input (Text) | 회사명 입력 | 선택 |
| **Address 입력란** | Input (Text) | 주소1 입력 | 필수 |
| **Address2 입력란** | Input (Text) | 주소2 입력 | 선택 |
| **Country 선택란** | Select (드롭다운) | 국가 선택. **확인 완료**: 기본 선택값은 India이며, 총 7개 옵션(표시 순서: India, United States, Canada, Australia, Israel, New Zealand, Singapore) 중 선택 가능 | 필수 |
| **State 입력란** | Input (Text) | 주/도 입력 | 필수 |
| **City 입력란** | Input (Text) | 도시 입력 | 필수 |
| **Zipcode 입력란** | Input (Text) | 우편번호 입력 | 필수 |
| **Mobile Number 입력란** | Input (Text) | 휴대전화번호 입력 | 필수 |
| **Create Account 버튼** | Button | 입력 정보 제출 및 계정 생성 수행 버튼 | 필수 |

### 화면 4: 회원가입 완료 페이지(`/account_created`)

**확인 완료**: 아래는 실제 사이트에서 확인된 정확한 문구입니다.

```
┌───────────────────────────────────────────────────┐
│        Account Created!                            │  (완료 메시지 제목)
│                                                     │
│  Congratulations! Your new account has been        │  (안내 문구)
│  successfully created!                              │
│                                                     │
│  You can now take advantage of member privileges   │  (안내 문구)
│  to enhance your online shopping experience         │
│  with us.                                          │
│                                                     │
│  [   Continue   ]                                   │  (Continue 버튼)
└───────────────────────────────────────────────────┘
```

| 요소명 | 타입 | 설명 | 필수 여부 |
|--------|------|------|---------|
| **"Account Created!" 메시지** | Text | 회원가입 성공 완료 안내 문구. 제목 "Account Created!" + 본문 "Congratulations! Your new account has been successfully created!" + "You can now take advantage of member privileges to enhance your online shopping experience with us." | 조건부(성공 시 노출) |
| **Continue 버튼** | Button | 클릭 시 로그인된 상태로 메인 페이지 이동 | 필수 |

### 확인 필요
- 각 UI 요소의 HTML id, CSS 클래스, data-* 속성: Page Object 구현 착수 시 사용자가 실시간으로 공유할 예정
- 회원가입 버튼 클릭 후 로딩 표시(스피너 등) 여부

---

## 8. 정상 사용자 흐름 (Happy Path)

**확인 완료**: 아래 흐름은 실제 사이트 방문(스크린샷)으로 확인된 4단계 흐름입니다.

### 흐름 1: 유효한 정보로 회원가입

**시작 조건**: 로그인 페이지(`/login`) 방문, 미등록 이메일 사용

**단계별 행동**:

**1단계 - 로그인 페이지(`/login`)에서 Name/Email 입력**
1. 사용자가 로그인 페이지(`https://automationexercise.com/login`) 접속
2. "New User Signup!" 영역의 "Name" 입력란에 사용자 이름 입력
   - 예: `John Doe`
3. "Email Address" 입력란에 등록되지 않은 이메일 주소 입력
   - 예: `newuser@example.com`
4. "Signup" 버튼 클릭
5. 시스템이 이메일 중복 여부를 검사 (미등록 이메일이므로 통과)
6. 회원가입 페이지(`https://automationexercise.com/signup`)로 이동

**2단계 - 회원가입 페이지(`/signup`): ENTER ACCOUNT INFORMATION 입력**
7. "Name" 입력란에 1단계에서 입력한 이름이 기본값으로 노출되며, 필요 시 값을 수정할 수 있음 (일반 입력 필드)
8. "Email" 입력란에 1단계에서 입력한 이메일이 dim 처리되어 노출됨 (수정 불가)
9. 필요시 "Title" 라디오 버튼에서 Mr./Mrs. 선택 (선택사항)
10. "Password" 입력란에 비밀번호 입력 (입력값은 마스킹되어 표시됨)
    - 예: `password123`
11. 필요시 "Date of Birth"의 Day/Month/Year 드롭다운 선택 (선택사항)
12. 필요시 "Sign up for our newsletter!", "Receive special offers from our partners!" 체크박스 선택 (선택사항)

**3단계 - 회원가입 페이지(`/signup`): ADDRESS INFORMATION 입력**
13. "First name" 입력란에 이름 입력 (예: `John`)
14. "Last name" 입력란에 성 입력 (예: `Doe`)
15. 필요시 "Company" 입력란에 회사명 입력 (선택사항)
16. "Address" 입력란에 주소 입력
17. 필요시 "Address2" 입력란에 추가 주소 입력 (선택사항)
18. "Country" 드롭다운에서 국가 선택
19. "State" 입력란에 주/도 입력
20. "City" 입력란에 도시 입력
21. "Zipcode" 입력란에 우편번호 입력
22. "Mobile Number" 입력란에 휴대전화번호 입력
23. "Create Account" 버튼 클릭
24. 시스템이 입력 정보를 검증

**4단계 - 회원가입 완료 페이지(`/account_created`)**
25. 검증 성공 시 회원가입 완료 페이지(`https://automationexercise.com/account_created`)로 이동, "Account Created!" 메시지와 "Congratulations! Your new account has been successfully created! You can now take advantage of member privileges to enhance your online shopping experience with us." 안내 문구가 노출됨
26. "Continue" 버튼 클릭
27. 메인 페이지(`https://automationexercise.com/`)로 이동 → 메인 페이지 헤더(네비게이션) 영역에 "Logout"이 노출되는 것으로 로그인 상태를 확인함

**기대 결과**:
- `/account_created` 페이지에서 "Account Created!" 메시지와 안내 문구가 표시됨
- 새 계정 생성됨 (데이터베이스에 저장)
- 입력한 이메일로 회원 계정 등록 완료
- "Continue" 버튼 클릭 시 별도의 로그인 절차 없이 로그인된 상태로 메인 페이지로 이동하며, 헤더 영역에 "Logout"이 노출됨
- 이후 로그아웃 후에도 동일한 이메일과 비밀번호로 재로그인 가능

**소요 시간**: 약 2~3초 (네트워크 지연 포함, 단계별)

---

## 9. 기능 요구사항

### 요구사항 정의

**SIGNUP-REQ-001**: 로그인 페이지(`/login`) 회원 정보 입력
- 사용자는 "New User Signup!" 영역의 "Name" 입력란에 사용자 이름을 입력할 수 있어야 한다.
- 사용자는 "Email Address" 입력란에 이메일 주소를 입력할 수 있어야 한다.

**SIGNUP-REQ-002**: 로그인 페이지(`/login`) 이메일 중복 검사
- 사용자가 이미 등록된 이메일로 "Signup" 버튼을 클릭하면, 시스템은 `/login` 페이지에서 이메일 중복 여부를 검사하고 `/signup` 페이지로 이동시키지 않아야 한다.
- 이 경우 명확한 오류 메시지가 `/login` 페이지에 표시되어야 한다. (**확인 필요**: 정확한 문구. 단, 이 흐름 자체는 이번 자동화 범위에서 제외됨)
- 사용자가 미등록 이메일로 "Signup" 버튼을 클릭하면, 시스템은 `/signup` 페이지로 이동시켜야 한다.

**SIGNUP-REQ-003**: 회원가입 페이지(`/signup`) Name/Email 자동 채움
- `/signup` 페이지 진입 시 "Name" 입력란에는 `/login`에서 입력한 이름이 기본값으로 채워져야 한다. 이 필드는 사용자가 값을 수정할 수 있어야 한다.
- `/signup` 페이지 진입 시 "Email" 입력란에는 `/login`에서 입력한 이메일이 dim 처리되어 노출되어야 한다. 이 필드는 사용자가 수정할 수 없어야 한다.

**SIGNUP-REQ-004**: 회원가입 페이지(`/signup`) ENTER ACCOUNT INFORMATION 입력
- 사용자는 "Title" 라디오 버튼에서 Mr. 또는 Mrs.를 선택할 수 있어야 한다. (선택사항)
- 사용자는 "Password" 입력란에 비밀번호를 입력할 수 있어야 하며, 입력값은 마스킹(●●●●)되어 표시되어야 한다.
- 사용자는 "Date of Birth"의 Day, Month, Year 드롭다운을 각각 선택할 수 있어야 한다. (선택사항)
- 사용자는 "Sign up for our newsletter!", "Receive special offers from our partners!" 체크박스를 각각 선택할 수 있어야 한다. (선택사항)

**SIGNUP-REQ-005**: 회원가입 페이지(`/signup`) ADDRESS INFORMATION 입력
- 사용자는 "First name", "Last name", "Address", "State", "City", "Zipcode", "Mobile Number" 입력란에 각각 값을 입력할 수 있어야 한다. (필수)
- 사용자는 "Country" 드롭다운에서 국가를 선택할 수 있어야 한다. (필수)
- 사용자는 "Company", "Address2" 입력란에 값을 입력할 수 있어야 한다. (선택사항)

**SIGNUP-REQ-006**: 필수 필드 검증
- Password, First name, Last name, Address, Country, State, City, Zipcode, Mobile Number는 필수 입력 필드이다.
- Title, Date of Birth, newsletter/offers 체크박스, Company, Address2는 선택 입력 필드이다.
- 필수 필드 중 하나 이상을 비운 상태에서 "Create Account" 버튼을 클릭하면, `/signup` 페이지에 머무르고 계정이 생성되지 않아야 한다. (**확인 필요**: 유효성 검사 메시지의 정확한 문구와 표시 방식. 단, 이 흐름에 대한 테스트 케이스는 이번 자동화 범위에서 제외됨)

**SIGNUP-REQ-007**: 유효한 정보로 회원가입 성공
- 사용자가 모든 필수 항목을 유효한 값으로 입력한 후 "Create Account" 버튼을 클릭하면, 시스템은 입력 정보를 검증해야 한다.
- 검증이 성공한 경우, 새로운 사용자 계정이 생성되고 회원가입 완료 페이지(`https://automationexercise.com/account_created`)로 이동해야 한다.
- 완료 페이지에는 "Account Created!" 메시지가 노출되어야 한다.

**SIGNUP-REQ-008**: 회원가입 완료 후 로그인 상태 전환
- 완료 페이지(`/account_created`)에서 "Continue" 버튼을 클릭하면, 사용자는 별도의 로그인 절차 없이 로그인된 상태로 메인 페이지(`https://automationexercise.com/`)로 이동해야 한다.
- 이동한 메인 페이지의 헤더(네비게이션) 영역에는 "Logout"이 노출되어야 한다.

**SIGNUP-REQ-009**: 비밀번호 요구사항
- 비밀번호는 필수 입력 필드이다.
- 비밀번호의 최소/최대 길이 제한은 없다. (확인 완료 - 섹션 9 "입력값 특성 / 비즈니스 규칙" 참고)
- 비밀번호 복잡성(대문자/숫자/특수문자 조합 등) 요구사항은 없다. (확인 완료)
- 비밀번호는 대소문자를 구분하여 저장되어야 한다.

**SIGNUP-REQ-010**: 비밀번호 보안
- 비밀번호는 HTTPS를 통해 암호화되어 전송되어야 한다.
- 비밀번호는 서버에서 암호화(해싱)되어 저장되어야 한다.
- 평문 비밀번호가 로그에 기록되지 않아야 한다.

**SIGNUP-REQ-011**: 회원 계정 활성화
- 회원가입 성공 후 계정이 즉시 활성화되어야 한다. (이메일 인증 절차 없이 로그인 가능해야 함, 확인 완료)

**SIGNUP-REQ-012**: 사용자 정보 저장
- 입력한 Name, Email, Password, First name, Last name, Address, Country, State, City, Zipcode, Mobile Number 등이 데이터베이스에 저장되어야 한다.
- 저장된 이메일/비밀번호는 이후 로그인 시 사용되어야 한다.

**SIGNUP-REQ-013**: 이메일 재사용 제한 (비즈니스 규칙)
- 회원가입에 성공하여 등록된 이메일은 이후 동일한 이메일로 재가입할 수 없다. (확인 완료, REQ-002의 중복 검사와 연결됨)
- 이 규칙에 대한 실패 테스트 케이스(중복 가입 시도)는 이번 자동화 범위(회원가입 성공 흐름)에서 제외한다.

### 입력값 특성 / 비즈니스 규칙 (확인된 사실)

실제 사이트 확인 결과, 아래 항목들은 제약사항이 없거나 동작 방식이 확인되어 더 이상 미확정 사항이 아닙니다. 이번 프로젝트 범위는 회원가입 성공 흐름이므로, 아래 사실을 검증하기 위한 별도의 실패/경계값 테스트 케이스는 작성하지 않습니다.

- ✅ 입력 항목(Password, Name 등 포함)의 글자수 최소/최대 길이 제한 없음
- ✅ 비밀번호 복잡성 요구사항 없음 (대문자/숫자/특수문자 조합 강제 없음)
- ✅ 이메일 형식 검증은 클라이언트 사이드(브라우저)에서 수행됨
- ✅ 공백 입력 가능하며, 자동 트리밍 없음
- ✅ 이메일은 대소문자를 구분하지 않음
- ✅ 회원가입 후 동일 이메일로는 재가입할 수 없음 (비즈니스 규칙)

---

## 10. 자동화 대상 범위

### 자동화 범위 (포함)

| 시나리오 | 자동화 대상 | 설명 |
|---------|-----------|------|
| **정상 회원가입** | ✅ 포함 | 유효한 정보로 회원가입 성공 |
| **회원가입 후 로그인 가능 여부** | ✅ 포함 | 회원가입 후 생성된 계정으로 로그인 성공 확인 |

---

## 11. 자동화 제외 범위

### 자동화 제외 사유

| 기능 | 제외 사유 |
|------|---------|
| **회원가입 실패/유효성 검증 케이스** | 이번 프로젝트 범위를 회원가입 성공 흐름으로 한정 (중복 이메일, 잘못된 이메일 형식, 빈 필드 검증 등 실패/경계값 테스트는 이번 범위에서 제외) |
| **비밀번호 암호화 방식** | 서버 내부 구현 (테스트 불필요) |
| **보안 인증서 검증** | HTTPS/TLS 인증서 검증 (인프라 수준) |
| **CAPTCHA 또는 봇 방지** | 외부 서비스 의존성, 테스트 환경 구성 복잡 |
| **SQL Injection 또는 XSS 공격** | 보안 테스트 (별도 전문 도구 필요) |
| **대용량 사용자 가입 (부하 테스트)** | 성능 테스트 (별도 도구 및 환경 필요) |
| **데이터베이스 직접 검증** | 백엔드 테스트 범위 |
---

## 12. 정상 시나리오 (Normal Scenarios)

**확인 완료**: 아래 시나리오는 `/login` → `/signup` → `/account_created` 3단계 흐름 전체를 대상으로, 회원가입 성공 흐름에 한정하여 작성되었습니다.

### NOR-001: 유효한 정보로 회원가입 성공

**시나리오명**: 신규 사용자가 올바른 정보로 회원가입

**전제조건**:
- 로그인 페이지(`/login`)가 표시됨
- 미등록 이메일 주소 사용 (예: `newuser001@example.com`)

**테스트 단계**:
1. 로그인 페이지의 "New User Signup!" 영역에서 "Name" 입력란에 `John Doe` 입력
2. "Email Address" 입력란에 `newuser001@example.com` 입력
3. "Signup" 버튼 클릭 → `/signup` 페이지로 이동 확인
4. "Password" 입력란에 `password123` 입력
5. "First name"에 `John`, "Last name"에 `Doe` 입력
6. "Address"에 `123 Test Street`, "Country"에 국가 선택, "State"에 `California`, "City"에 `Los Angeles`, "Zipcode"에 `90001`, "Mobile Number"에 `1234567890` 입력
7. "Create Account" 버튼 클릭
8. `/account_created` 페이지 노출 대기
9. "Continue" 버튼 클릭

**기대 결과**:
- 3단계 URL(`/login` → `/signup` → `/account_created`)이 순서대로 전환됨
- `/account_created` 페이지에 "Account Created!" 메시지와 안내 문구 노출
- 새 계정 생성 확인 가능
- "Continue" 클릭 시 메인 페이지(`/`)로 이동하며, 헤더 영역에 "Logout"이 노출되어 로그인 상태가 확인됨
- 입력한 이메일이 이제 "이미 등록된" 상태가 됨

**검증 포인트**:
- ✅ 각 단계에서 URL이 올바르게 전환되는가?
- ✅ `/signup` 페이지의 Name 필드에 `/login`에서 입력한 값이 기본값으로 노출되며, 수정 가능한 상태인가?
- ✅ `/signup` 페이지의 Email 필드에 `/login`에서 입력한 값이 dim 처리되어 노출되며, 수정 불가능한 상태인가?
- ✅ "Account Created!" 메시지가 표시되었는가?
- ✅ Continue 클릭 후 메인 페이지 헤더 영역에 "Logout"이 노출되는가?

**예상 실행 시간**: 약 3~5초

---

### NOR-002: 회원가입 완료 후 로그아웃 → 재로그인 성공

**시나리오명**: 신규 회원가입 직후 로그인 상태에서 로그아웃한 뒤, 동일 계정으로 재로그인

**전제조건**:
- NOR-001 시나리오가 완료되어 로그인된 상태로 메인 페이지에 있음

**테스트 단계**:
1. "Logout" 클릭하여 로그아웃
2. 로그인 페이지(`/login`) 접근
3. 회원가입에서 사용한 이메일과 비밀번호로 로그인
4. 로그인 성공 확인

**기대 결과**:
- 로그아웃 후 로그인 페이지 또는 홈 페이지로 이동
- 재로그인 성공, 사용자 이름 표시, "Logout" 버튼 표시

**검증 포인트**:
- ✅ 로그인이 성공했는가?
- ✅ 회원가입 시 등록한 이름/이메일과 일치하는 사용자로 로그인되었는가?

---

## 13. 기대 결과 (Expected Results)

**확인 완료**: 아래 표는 `/login` → `/signup` → `/account_created` 3단계 흐름과 NOR-001~002 시나리오(회원가입 성공 흐름)에 맞게 갱신되었습니다.

### 성공 케이스 기대 결과

| 시나리오 | 최종 페이지 상태 | 메시지/표시 | 계정 생성 | 로그인 가능 |
|---------|-----------|-----------|---------|----------|
| **NOR-001** | `/account_created` → Continue 클릭 후 메인 페이지(`/`), 로그인 상태 | "Account Created!" 메시지 및 안내 문구 | ✅ 생성됨 | ✅ 자동 로그인 상태 (헤더에 "Logout" 노출) |
| **NOR-002** | 로그아웃 후 `/login`에서 재로그인 → 메인 페이지 | 사용자 이름 표시, "Logout" 버튼 표시 | N/A | ✅ 재로그인 성공 |

---

## 14. 주요 검증 포인트 (Assertion Points)

**확인 완료**: 검증 흐름과 pytest 예시는 `/login`(Name/Email 입력) → `/signup`(Password/Address 입력) → `/account_created`(Continue) 3단계 흐름 중 회원가입 성공 흐름에 맞게 재작성되었습니다. 아래 코드는 실제 구현 코드가 아니라 Page Object 책임 분리를 보여주기 위한 PRD 수준의 예시입니다.

### 정상 회원가입 검증

```
테스트 흐름:
1. 로그인 페이지(/login) 방문
   → 검증: URL이 로그인 페이지 URL과 일치하는가?

2. New User Signup! 영역에 Name, Email Address 입력 후 "Signup" 버튼 클릭
   → 검증: URL이 /signup 페이지로 변경되었는가?

3. /signup 페이지에서 Name/Email 필드 확인
   → 검증: Name 필드에 1단계에서 입력한 값이 기본값으로 노출되는가?
   → 검증: Name 필드가 수정 가능한 상태인가? (필요 시 값을 변경할 수 있어야 함)
   → 검증: Email 필드에 1단계에서 입력한 값이 그대로 노출되는가? (dim 처리)
   → 검증: Email 필드가 수정 불가능한 상태인가?

4. Password 및 ADDRESS INFORMATION(First name, Last name, Address, Country, State, City,
   Zipcode, Mobile Number 등) 입력
   → 검증: 각 입력 필드에 값이 정상적으로 입력되었는가?
   → 검증: Password 입력값이 마스킹되어 표시되는가?

5. "Create Account" 버튼 클릭
   → 검증: URL이 /account_created 페이지로 변경되었는가?
   → 검증: "Account Created!" 메시지와 안내 문구가 표시되는가?

6. "Continue" 버튼 클릭
   → 검증: 메인 페이지(/)로 이동했는가?
   → 검증: 메인 페이지 헤더(네비게이션) 영역에 "Logout"이 노출되는가? (로그인 상태 확인 방법)

7. 계정 생성 확인
   → 검증: 입력한 이메일이 이제 /login 페이지에서 중복된 이메일로 인식되는가?
   → 검증: 로그아웃 후 동일 이메일/비밀번호로 재로그인 가능한가?
```

### 프로그래밍적 검증 (pytest에서 - 예시, 실제 코드 아님)

```python
# 예시 (구현 시 실제 코드는 테스트 레이어에서 작성)
# LoginPage는 /login 페이지의 Name/Email 입력 및 Signup 버튼 클릭을 담당
# SignupPage는 /signup 페이지의 Password/Address 입력 및 Create Account 클릭을 담당
# AccountCreatedPage는 /account_created 페이지의 Continue 버튼 클릭을 담당

# 성공 케이스 (전체 3단계 흐름)
login_page = LoginPage(driver)
login_page.navigate_to_login()
login_page.enter_signup_name("John Doe")
login_page.enter_signup_email("newuser@example.com")
login_page.click_signup_button()

signup_page = SignupPage(driver)
# Name은 기본값으로 노출되고 수정 가능한 일반 입력 필드
assert signup_page.get_name_value() == "John Doe"
assert signup_page.is_name_field_editable() is True
# Email은 dim 처리되어 노출되고 수정 불가능한 필드
assert signup_page.get_displayed_email() == "newuser@example.com"
assert signup_page.is_email_field_editable() is False

signup_page.enter_password("password123")
signup_page.enter_first_name("John")
signup_page.enter_last_name("Doe")
signup_page.enter_address("123 Test Street")
# select_country("United States")를 호출하지 않으면 기본값 India가 그대로 유지됨 (확인 완료)
signup_page.select_country("United States")
signup_page.enter_state("California")
signup_page.enter_city("Los Angeles")
signup_page.enter_zipcode("90001")
signup_page.enter_mobile_number("1234567890")
signup_page.click_create_account_button()

account_created_page = AccountCreatedPage(driver)
assert account_created_page.is_account_created_message_displayed() == True
account_created_page.click_continue_button()

home_page = HomePage(driver)
# 메인 페이지 헤더 영역에 "Logout"이 노출되는 것으로 로그인 상태를 확인
assert home_page.is_logout_link_displayed() == True
```

---

## 15. 필요한 테스트 데이터

**확인 완료**: 실제 필수 입력 항목 전체(Password, First name, Last name, Address, Country, State, City, Zipcode, Mobile Number 등)를 반영하여 테스트 데이터 예시를 갱신했습니다.

### 테스트 계정 및 회원 정보

| 용도 | Name | Email | Password | First name | Last name | Address | Country | State | City | Zipcode | Mobile Number | 상태 | 비고 |
|------|------|-------|----------|------------|-----------|---------|---------|-------|------|---------|--------------|------|------|
| **정상 회원가입 테스트** | John Doe | `newuser001@example.com` | `password123` | John | Doe | 123 Test Street | United States | California | Los Angeles | 90001 | 1234567890 | 미등록 | 새로 생성 |
| **재로그인 테스트** | Jane Doe | `newuser002@example.com` | `securepass456` | Jane | Doe | 456 Sample Ave | United States | New York | New York | 10001 | 9876543210 | 미등록 | 새로 생성 후 로그아웃/재로그인 |
| **기본값(India) 사용 테스트** | Alex Kim | `newuser003@example.com` | `password789` | Alex | Kim | 789 Default Road | India (기본값, 별도 선택 없이 사용) | Delhi | Delhi | 110001 | 9998887777 | 미등록 | Country 드롭다운 기본 선택값(India)을 그대로 사용하는 케이스 |

**참고**: Country 드롭다운의 옵션은 총 7개(India, United States, Canada, Australia, Israel, New Zealand, Singapore)이며, 기본 선택값은 India입니다 (확인 완료, 섹션 7 참고).

### 테스트 데이터 관리 방식

**방식 1: 환경변수 (.env 파일)**
```
TEST_USER_NAME=John Doe
TEST_USER_EMAIL=newuser001@example.com
TEST_USER_PASSWORD=password123
TEST_USER_FIRST_NAME=John
TEST_USER_LAST_NAME=Doe
TEST_USER_ADDRESS=123 Test Street
TEST_USER_COUNTRY=United States
TEST_USER_STATE=California
TEST_USER_CITY=Los Angeles
TEST_USER_ZIPCODE=90001
TEST_USER_MOBILE_NUMBER=1234567890
```

**방식 2: JSON 파일 (test_data/signup.json)**
```json
{
  "valid_signup": {
    "name": "John Doe",
    "email": "newuser001@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe",
    "address": "123 Test Street",
    "country": "United States",
    "state": "California",
    "city": "Los Angeles",
    "zipcode": "90001",
    "mobile_number": "1234567890"
  }
}
```

**방식 3: pytest Fixture (conftest.py)**
```python
@pytest.fixture
def valid_signup_data():
    return {
        "name": "John Doe",
        "email": "newuser001@example.com",
        "password": "password123",
        "first_name": "John",
        "last_name": "Doe",
        "address": "123 Test Street",
        "country": "United States",
        "state": "California",
        "city": "Los Angeles",
        "zipcode": "90001",
        "mobile_number": "1234567890",
    }
```

### 데이터 보호 규칙
- ❌ 비밀번호를 코드에 하드코딩하지 않음
- ❌ 로그 또는 리포트에 비밀번호 노출 금지
- ✅ 환경변수 또는 외부 파일에서 관리
- ✅ 민감정보는 마스킹 처리하여 로깅
- ❌ 이메일 주소도 테스트 환경에서만 사용
- ✅ **확인 완료**: 테스트로 생성한 계정(이메일)은 테스트 종료 후 별도로 정리(삭제)하지 않음. Automation Exercise가 계정 삭제 기능을 제공하지 않거나 삭제하지 않는 것이 사이트 정책으로 확인됨. (CLAUDE.md 10.3 "가능한 경우 테스트가 생성한 데이터는 정리" 원칙은 유지하되, 본 사이트는 삭제 기능 부재로 인해 적용되지 않는 예외 사례로 확인됨)

### 확인 완료 (v1.4, login.md와 동기화)
- **테스트 계정 준비 방식**: **사전 생성** (테스트 실행 전 미리 생성해둔 고정 계정 사용, 테스트 중 동적 생성 방식은 사용하지 않음). `docs/prd/features/login.md` 섹션 17/20에 이미 확정되어 있던 사실을 이 문서에 동기화하여 반영함. (새로운 사실 확인이 아니라 문서 간 정합성을 맞춘 것임)

---

## 16. 다른 기능과의 의존성

### 이 기능이 의존하는 다른 기능

| 기능 | 의존 관계 | 설명 |
|------|---------|------|
| **홈 페이지 (Home)** | 진입 경로 | 홈 페이지의 "Signup / Login" 네비게이션 링크를 통해 `/login` 페이지로 진입, 이후 `/login` 페이지의 "New User Signup!" 영역에서 회원가입 절차 시작 |

### 이 기능을 필요로 하는 다른 기능

| 기능 | 의존 관계 | 설명 |
|------|---------|------|
| **로그인 (Login)** | 후행 필수 | 회원가입으로 계정을 생성해야 로그인 가능 |
| **로그아웃 (Logout)** | 간접 의존 | 로그인 가능한 계정이 필요 → 회원가입 필수 |
| **상품 검색 (Product Search)** | 간접 의존 | 회원 전용 기능인 경우 회원가입 필수 |
| **장바구니 (Shopping Cart)** | 간접 의존 | 회원 계정 연결 시 회원가입 필수 |
| **주문 (Checkout)** | 간접 의존 | 주문 시 로그인 필수 → 회원가입 필수 |

### 의존성 흐름도

```
회원가입 (Signup) ← [이 기능]
    ↓
로그인 (Login)
    ↓
홈 페이지 / 대시보드
    ├─→ 상품 검색 (Product Search)
    ├─→ 장바구니 (Shopping Cart)
    └─→ 로그아웃 (Logout)
```

---

## 17. 자동화 구현 시 고려사항

**확인 완료**: 실제 흐름상 Name/Email 입력 및 Signup 버튼은 `/login` 페이지(LoginPage의 책임)에 속하고, `/signup` 페이지의 Password/Address 입력 및 Create Account 클릭은 SignupPage의 책임, `/account_created` 페이지의 Continue 클릭은 AccountCreatedPage의 책임으로 분리하여 설계 방향을 재작성했습니다.
아래 코드는 구조 설명을 위한 예시(스텁)이며 실제 동작 코드는 아닙니다. **Locator 값은 예시이며, 실제 id/name/data-* 속성은 Page Object 구현 착수 시 사용자가 실시간으로 공유할 예정입니다.**

### Page Object 설계 방향

#### 페이지 책임 분리

| 페이지 | 담당 Page 클래스 | 책임 |
|--------|-----------------|------|
| `/login` | `LoginPage` (login.md에서 정의) | New User Signup! 영역의 Name/Email 입력, Signup 버튼 클릭 |
| `/signup` | `SignupPage` | Name(수정 가능) 값 조회/입력, Email(dim 처리, 조회 전용) 값 조회, Password/Title/Date of Birth/체크박스/ADDRESS INFORMATION 입력, Create Account 버튼 클릭 |
| `/account_created` | `AccountCreatedPage` | 완료 메시지 확인, Continue 버튼 클릭 |

**참고**: `/login` 페이지의 Name/Email 입력 및 Signup 버튼 관련 메서드(`enter_signup_name`, `enter_signup_email`, `click_signup_button` 등)는 로그인 기능 PRD(`docs/prd/features/login.md`)의 LoginPage 설계에 포함시키는 것을 권장합니다. 이 문서의 SignupPage는 `/signup` 페이지 진입 이후만을 다룹니다.

#### SignupPage 클래스 구조 (예시 - 구현은 별도 작성)

```python
# pages/signup_page.py 구조 (실제 코드 아님)
# 아래 Locator 값은 예시이며, 실제 값은 Page Object 구현 착수 시 사용자가 공유할 예정입니다.

class SignupPage(BasePage):
    # Locator 정의 (상수) - /signup 페이지 요소만 포함

    # Name은 /login 입력값이 기본값으로 채워지지만 일반 입력 필드로 수정 가능
    NAME_INPUT = (By.ID, "name")
    # Email은 dim 처리되어 노출되며 수정 불가능하므로 조회용 locator만 정의
    DISPLAYED_EMAIL = (By.ID, "email")

    TITLE_MR_RADIO = (By.ID, "id_gender1")      # Mr. 라디오 버튼
    TITLE_MRS_RADIO = (By.ID, "id_gender2")     # Mrs. 라디오 버튼
    PASSWORD_INPUT = (By.ID, "password")
    DOB_DAY_SELECT = (By.ID, "days")
    DOB_MONTH_SELECT = (By.ID, "months")
    DOB_YEAR_SELECT = (By.ID, "years")
    NEWSLETTER_CHECKBOX = (By.ID, "newsletter")
    OFFERS_CHECKBOX = (By.ID, "optin")

    FIRST_NAME_INPUT = (By.ID, "first_name")
    LAST_NAME_INPUT = (By.ID, "last_name")
    COMPANY_INPUT = (By.ID, "company")
    ADDRESS_INPUT = (By.ID, "address1")
    ADDRESS2_INPUT = (By.ID, "address2")
    COUNTRY_SELECT = (By.ID, "country")
    STATE_INPUT = (By.ID, "state")
    CITY_INPUT = (By.ID, "city")
    ZIPCODE_INPUT = (By.ID, "zipcode")
    MOBILE_NUMBER_INPUT = (By.ID, "mobile_number")
    CREATE_ACCOUNT_BUTTON = (By.CSS_SELECTOR, "button[data-qa='create-account']")

    # 값 조회 메서드
    def get_name_value(self) -> str:
        """/login에서 입력한 후 기본값으로 채워진 Name 입력란의 현재 값 조회"""
        pass

    def get_displayed_email(self) -> str:
        """/login에서 입력한 후 dim 처리되어 노출되는 Email 값 조회"""
        pass

    def is_name_field_editable(self) -> bool:
        """Name 필드가 수정 가능한 상태인지 여부 반환 (기대값: True)"""
        pass

    def is_email_field_editable(self) -> bool:
        """Email 필드가 수정 가능한 상태인지 여부 반환 (기대값: False)"""
        pass

    # 화면 조작 메서드 (값 반환 또는 상태 변경, assertion 없음)
    def enter_name(self, name: str) -> None:
        """Name 입력란 값을 입력/수정 (기본값은 /login에서 입력한 값이며, 필요 시 변경 가능)"""
        pass

    def select_title(self, title: str) -> None:
        """Title(Mr./Mrs.) 라디오 버튼 선택"""
        pass

    def enter_password(self, password: str) -> None:
        """Password 입력란에 비밀번호 입력"""
        pass

    def select_date_of_birth(self, day: str, month: str, year: str) -> None:
        """Date of Birth의 Day/Month/Year 드롭다운 선택"""
        pass

    def check_newsletter(self) -> None:
        """Sign up for our newsletter! 체크박스 선택"""
        pass

    def check_special_offers(self) -> None:
        """Receive special offers from our partners! 체크박스 선택"""
        pass

    def enter_first_name(self, first_name: str) -> None:
        pass

    def enter_last_name(self, last_name: str) -> None:
        pass

    def enter_company(self, company: str) -> None:
        pass

    def enter_address(self, address: str) -> None:
        pass

    def enter_address2(self, address2: str) -> None:
        pass

    def select_country(self, country: str) -> None:
        """Country 드롭다운에서 국가 선택
        확인 완료: 기본 선택값은 India이며, 총 7개 옵션(India, United States, Canada,
        Australia, Israel, New Zealand, Singapore) 중 선택 가능. locator 값은 예시이며
        실제 값은 Page Object 구현 착수 시 사용자가 공유할 예정."""
        pass

    def enter_state(self, state: str) -> None:
        pass

    def enter_city(self, city: str) -> None:
        pass

    def enter_zipcode(self, zipcode: str) -> None:
        pass

    def enter_mobile_number(self, mobile_number: str) -> None:
        pass

    def click_create_account_button(self) -> None:
        """Create Account 버튼 클릭"""
        pass

    def is_on_signup_page(self) -> bool:
        """현재 URL이 /signup 페이지인지 여부 반환"""
        pass
```

#### AccountCreatedPage 클래스 구조 (예시 - 구현은 별도 작성)

```python
# pages/account_created_page.py 구조 (실제 코드 아님)
# 아래 Locator 값은 예시이며, 실제 값은 Page Object 구현 착수 시 사용자가 공유할 예정입니다.

class AccountCreatedPage(BasePage):
    ACCOUNT_CREATED_MESSAGE = (By.CSS_SELECTOR, "h2[data-qa='account-created']")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "a[data-qa='continue-button']")

    def is_account_created_message_displayed(self) -> bool:
        """"Account Created!" 메시지 표시 여부 반환"""
        pass

    def click_continue_button(self) -> None:
        """Continue 버튼 클릭 (클릭 시 로그인 상태로 메인 페이지 이동)"""
        pass
```

### Locator 선택 원칙

**우선순위** (CLAUDE.md 기준):
1. **id 속성** (가장 안정적)
   ```python
   PASSWORD_INPUT = (By.ID, "password")
   FIRST_NAME_INPUT = (By.ID, "first_name")
   ```

2. **data-* 속성** (테스트용)
   ```python
   CREATE_ACCOUNT_BUTTON = (By.CSS_SELECTOR, "button[data-qa='create-account']")
   ```

3. **name 속성**
   ```python
   COUNTRY_SELECT = (By.NAME, "country")
   ```

4. **안정적인 CSS Selector**
   ```python
   NAME_INPUT = (By.CSS_SELECTOR, "form.signup-form input[name='name']")
   ```

5. **상대 XPath** (마지막 수단)
   ```python
   NAME_INPUT = (By.XPATH, "//form[@action='/signup']//input[@name='name']")
   ```

**금지**: Full XPath 절대 금지
```python
# ❌ 금지
NAME_INPUT = (By.XPATH, "/html/body/div[1]/div[2]/form/div[4]/input")
```

**안내**: 위 Locator는 모두 예시 값입니다. 실제 id/name/data-* 속성은 Page Object 구현 착수 시 사용자가 실시간으로 공유할 예정이며, 별도의 사전 개발자 도구 조사는 필요하지 않습니다.

### Wait 처리 전략

**명시적 Wait 사용** (time.sleep() 절대 금지):

```python
# ✅ 올바른 방식 (예시 - 실제 코드 아님)
def click_create_account_button(self):
    wait.until(EC.element_to_be_clickable(self.CREATE_ACCOUNT_BUTTON))
    self.click(self.CREATE_ACCOUNT_BUTTON)

    # /account_created 페이지로 전환될 때까지 대기
    wait.until(
        EC.presence_of_element_located(AccountCreatedPage.ACCOUNT_CREATED_MESSAGE)
    )
```

### 동적 요소 처리

- **페이지 전환**: `/login` → `/signup` → `/account_created` 각 단계 전환 시 새 페이지 로드 완료까지 명시적 대기
- **자동 채움 필드**: Name/Email 필드는 `/login` 입력값으로 채워진 상태로 렌더링됨. Email은 dim 처리되어 수정 불가하므로 조회만 수행하고, Name은 일반 입력 필드이므로 필요 시 clear 후 재입력 가능
- **드롭다운(Country, Date of Birth)**: 옵션 목록 로드 완료 후 클릭/선택
- **로그인 상태 확인**: Continue 클릭 후 메인 페이지 헤더의 "Logout" 요소가 나타날 때까지 대기 후 조회

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

    def select_dropdown_option_by_value(self, locator, value: str) -> None:
        """드롭다운(select)에서 값으로 옵션 선택 (Country, Date of Birth 등에 재사용)"""
        pass

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

    def get_element_text(self, locator) -> str:
        """요소 텍스트 조회"""
        pass
```

### 네트워크 지연 고려

- **타임아웃 설정**: 기본 10초, 페이지 로드는 20초 (프로젝트 PRD 기준)
- **재시도 로직**: 네트워크 오류 시 1회 재시도 (선택사항)
- **느린 네트워크**: 타임아웃을 충분히 설정하여 안정성 확보

### 예시: 회원가입 테스트 구현 방향

```python
# tests/test_signup.py 구조 (실제 코드 아님)

def test_signup_with_valid_data(driver, valid_signup_data):
    # 1. 로그인 페이지에서 Name/Email 입력 후 Signup 클릭 (LoginPage 책임)
    login_page = LoginPage(driver)
    login_page.navigate_to_login()
    login_page.enter_signup_name(valid_signup_data["name"])
    login_page.enter_signup_email(valid_signup_data["email"])
    login_page.click_signup_button()

    # 2. /signup 페이지에서 Name/Email 필드 확인 (SignupPage 책임)
    signup_page = SignupPage(driver)
    assert signup_page.get_name_value() == valid_signup_data["name"]        # 기본값 노출 확인
    assert signup_page.is_name_field_editable() is True                    # 수정 가능 상태 확인
    assert signup_page.get_displayed_email() == valid_signup_data["email"]
    assert signup_page.is_email_field_editable() is False                  # 수정 불가 상태 확인

    # Name은 수정 가능하므로 필요 시 값을 변경할 수 있음 (이번 시나리오에서는 기본값을 그대로 사용)
    # signup_page.enter_name("Johnathan Doe")  # 예: 기본값을 수정하고 싶은 경우

    # 3. Password 및 ADDRESS INFORMATION 입력 후 Create Account 클릭
    signup_page.enter_password(valid_signup_data["password"])
    signup_page.enter_first_name(valid_signup_data["first_name"])
    signup_page.enter_last_name(valid_signup_data["last_name"])
    signup_page.enter_address(valid_signup_data["address"])
    signup_page.select_country(valid_signup_data["country"])
    signup_page.enter_state(valid_signup_data["state"])
    signup_page.enter_city(valid_signup_data["city"])
    signup_page.enter_zipcode(valid_signup_data["zipcode"])
    signup_page.enter_mobile_number(valid_signup_data["mobile_number"])
    signup_page.click_create_account_button()

    # 4. /account_created 페이지 확인 후 Continue 클릭 (AccountCreatedPage 책임)
    account_created_page = AccountCreatedPage(driver)
    assert account_created_page.is_account_created_message_displayed()
    account_created_page.click_continue_button()

    # 5. 메인 페이지 헤더 영역에 "Logout"이 노출되는 것으로 로그인 상태 확인
    home_page = HomePage(driver)
    assert home_page.is_logout_link_displayed()
```

---

## 18. 확인이 필요한 미확정 사항

### 확인 완료 항목 (스크린샷 검토 및 실제 사이트 재확인으로 확인됨)

다음 항목들은 실제 사이트 방문(스크린샷 5장 및 재확인) 결과로 확인이 완료되어 더 이상 미확정 사항이 아닙니다:

- ✅ 회원가입 관련 URL은 `/login` → `/signup` → `/account_created` 3단계로 구성됨
- ✅ `/signup` 페이지의 필드 목록: Title, Name, Email(dim), Password, Date of Birth(Day/Month/Year), newsletter 체크박스 2종, First name, Last name, Company, Address, Address2, Country, State, City, Zipcode, Mobile Number, Create Account 버튼
- ✅ 필수(*) 항목: Name, Email, Password, First name, Last name, Address, Country, State, City, Zipcode, Mobile Number
- ✅ 선택 항목: Title, Date of Birth, newsletter 체크박스 2종, Company, Address2
- ✅ Name 필드는 `/login`에서 입력한 값이 기본값으로 채워지며, `/signup` 페이지에서 사용자가 수정 가능한 일반 입력 필드임
- ✅ Email 필드는 `/login`에서 입력한 값이 dim 처리되어 노출되며 `/signup` 페이지에서 수정 불가능함
- ✅ Password 입력값은 마스킹되어 표시됨
- ✅ 이메일 중복 검사는 `/signup` 페이지가 아니라 `/login` 페이지의 Signup 버튼 클릭 시점에 발생함
- ✅ 회원가입 완료 후 `/account_created` 페이지에서 "Account Created!" 메시지와 "Congratulations! Your new account has been successfully created! You can now take advantage of member privileges to enhance your online shopping experience with us." 안내 문구가 노출됨
- ✅ Continue 버튼 클릭 시 별도 로그인 절차 없이 로그인된 상태로 메인 페이지로 이동함 (자동 로그인). 로그인 상태는 메인 페이지 헤더 영역에 "Logout"이 노출되는 것으로 확인함
- ✅ 이메일 인증 절차는 없음 (Continue 클릭 즉시 로그인 상태로 전환되는 것으로 확인됨)
- ✅ 입력 항목(Password, Name 등)의 글자수 최소/최대 길이 제한 없음
- ✅ 비밀번호 복잡성 요구사항 없음
- ✅ 이메일 형식 검증은 클라이언트 사이드에서 수행됨
- ✅ 공백 입력 가능하며 자동 트리밍 없음
- ✅ 이메일 대소문자 구분 안 함
- ✅ 회원가입 후 동일 이메일로 재가입 불가 (비즈니스 규칙)
- ✅ Country 드롭다운의 기본 선택값은 India이며, 총 7개 옵션(표시 순서: India, United States, Canada, Australia, Israel, New Zealand, Singapore)이 제공됨 (실제 사이트 스크린샷으로 확인 완료)
- ✅ Automation Exercise에서 테스트 계정 생성이 가능함 (실제 확인 완료)
- ✅ 테스트 환경에서 사이트 접근에 제약이 없음 (실제 확인 완료)
- ✅ 테스트 후 계정을 별도로 정리(삭제)하지 않음 (실제 확인 완료: Automation Exercise가 계정 삭제 기능을 제공하지 않거나 삭제하지 않는 것이 사이트 정책으로 확인됨. 기존에 "예상: 필요"로 서술되었던 부분을 정정함)

### 여전히 확인이 필요한 항목

#### UI 요소 Locator (개발 착수 시 공유 예정)
- 각 필드(Title, Name, Email, Password, Date of Birth 3종, 체크박스 2종, First name, Last name, Company, Address, Address2, Country, State, City, Zipcode, Mobile Number, Create Account 버튼, Continue 버튼)의 실제 HTML id, name, data-* 속성은 Page Object 구현 착수 시 사용자가 실시간으로 공유할 예정입니다. 별도의 사전 개발자 도구 조사는 필요하지 않습니다.

---

## 19. 완료 조건

### 회원가입 기능 자동화 완료 기준

**정상 시나리오 완료**:
- ✅ NOR-001 (`/login` → `/signup` → `/account_created` 전체 흐름으로 유효한 정보 회원가입): 테스트 PASS
- ✅ NOR-002 (회원가입 완료 후 로그아웃 → 재로그인): 테스트 PASS

**코드 품질 기준** (CLAUDE.md 준수):
- ✅ Page Object 설계: SignupPage(`/signup`), AccountCreatedPage(`/account_created`) 클래스 구현 완료, LoginPage(`/login`)의 Signup 관련 메서드는 login.md 기준으로 구현 완료
  - 모든 Locator가 상수/클래스 변수로 정의됨
  - 화면 조작 메서드와 값 조회 메서드만 포함
  - Name 필드는 조회/입력 메서드 모두 제공, Email(dim) 필드는 조회 전용 메서드만 제공
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
  - 파일명: snake_case (signup_page.py, account_created_page.py, test_signup.py)
  - 클래스명: PascalCase + Page 접미사 (SignupPage, AccountCreatedPage)
  - 메서드명: snake_case, 동사로 시작 (enter_password, click_create_account_button)
  - 테스트 함수명: test_ 접두사 (test_signup_with_valid_data)
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
- ✅ 이 PRD가 완성되고 검토됨 (`/login` → `/signup` → `/account_created` 3단계 흐름, 전체 필드 목록, 회원가입 성공 흐름 범위 반영)
- ✅ Page Object 구현 착수 시 Locator 공유 프로세스가 합의됨
- ✅ 섹션 18의 "여전히 확인이 필요한 항목"들이 실제 사이트 방문으로 검증됨

**배포 기준**:
- ✅ 모든 테스트 코드 완성
- ✅ 코드 리뷰 완료
- ✅ GitHub Actions CI/CD 테스트 통과
- ✅ 로그인 기능 PRD(`docs/prd/features/login.md`)와의 일관성 검증 (특히 `/login` 페이지의 Signup 관련 책임 분리)

---

## 20. 다음 단계

### 즉시 작업 (이 PRD 이후)
1. **테스트 이메일 준비**: 회원가입 테스트용 미등록 이메일 주소 생성/확인
2. **Locator 공유 대기**: Page Object 구현 착수 시 사용자로부터 각 UI 요소(`/login`의 Name/Email/Signup 버튼, `/signup`의 Title/Name/Password/Date of Birth/체크박스/ADDRESS INFORMATION/Create Account 버튼, `/account_created`의 메시지/Continue 버튼)의 id, name, CSS 클래스, data-* 속성을 실시간으로 공유받기
3. **Page Object 구현**: LoginPage의 Signup 관련 메서드(login.md 기준), SignupPage, AccountCreatedPage 클래스 작성
4. **테스트 코드 작성**: 회원가입 성공 흐름 테스트 케이스 작성 (tests/test_signup.py)
5. **테스트 실행**: pytest를 사용하여 정상 시나리오(NOR-001, NOR-002) 테스트 실행
6. **오류 수정**: 실패한 테스트 분석 및 수정

### 추후 작업 (이 기능 완료 후)
1. **로그인 (Login) 기능**: 회원가입과 통합한 로그인 테스트 (login.md의 `/login` 페이지 Signup 영역 요구사항과의 일관성 확인)
2. **로그아웃 (Logout) 기능**: 로그인 계정의 로그아웃 테스트
3. **통합 테스트**: 회원가입(`/login`→`/signup`→`/account_created`) → 로그아웃 → 재로그인의 전체 흐름 테스트
4. **회원가입 실패/경계값 테스트 확장 검토**: 이번 범위에서 제외한 중복 이메일, 잘못된 이메일 형식, 필수 필드 누락 등의 실패/경계값 시나리오를 추후 별도 범위로 추가할지 검토
5. **다른 기능**: Phase 1 나머지 기능 (상품 검색) 자동화

---

## 21. 참고 자료

### 관련 문서
- **프로젝트 전체 PRD**: `docs/prd/project-prd.md`
- **로그인 기능 PRD**: `docs/prd/features/login.md`
- **프로젝트 개발 규칙**: `CLAUDE.md`
- **기능별 PRD 작성 가이드**: `docs/PRD_PROMPT.md` (있는 경우)

### 외부 참고
- **Automation Exercise 공식**: https://automationexercise.com/
- **Selenium 문서**: https://selenium.dev/documentation/
- **pytest 문서**: https://docs.pytest.org/

### 버전 관리
- **이 PRD 버전**: 1.4 (login.md와의 테스트 계정 준비 방식 동기화)
- **작성일**: 2026-07-20
- **최종 검토일**: 2026-07-23
- **최종 승인일**: (예정)

**변경 이력**:
- v1.4 (2026-07-23): 문서 간 정합성 동기화. `login.md` 섹션 17/20에 이미 확정되어 있던 "테스트 계정 준비 방식: 사전 생성" 사실을 섹션 15에 반영(기존 "확인 필요 - 사전 생성 vs 동적 생성" 상태를 해소). 새로운 사실 확인은 없으며, 기존 문서 간 불일치를 해소한 순수 동기화 변경임.
- v1.3 (2026-07-21): Country 드롭다운 기본값(India) 및 전체 옵션(7개) 확인 완료 반영, 테스트 환경 확인 3개 항목(계정 생성 가능 여부, 사이트 접근 제약, 계정 정리 정책) 확인 완료로 전환, "테스트 후 계정 정리 필요" → "정리하지 않음"으로 정정
- v1.2 (2026-07-21): 회원가입 성공 흐름으로 범위 한정, 실패/경계값 시나리오 제외, Name 필드 수정 가능 오류 정정, Account Created 실제 문구 반영

---

**작성자**: Automation Testing Framework Lead  
**최종 검토자**: (예정)  
**승인 상태**: 초안 (검토 대기 중)

이 문서는 회원가입 기능의 자동화 테스트 작성 시 기준이 되는 요구사항 명세입니다.  
실제 구현 과정에서 새로운 정보가 발견되면 이 문서를 업데이트합니다.
