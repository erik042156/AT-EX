# AT-EX AI Agent 운영 규칙 (shrimp-rules.md)

이 문서는 **AI Agent 전용 운영 규칙**입니다. 일반 개발 지식이나 기능 요구사항은 포함하지 않습니다.
- 코딩 컨벤션/아키텍처 원칙 → `CLAUDE.md` 참조 (이 문서에서 재작성하지 않음)
- 기능 요구사항 → `docs/prd/project-prd.md`, `docs/prd/features/*.md` 참조
- 실행 계획/진행 상태 → `docs/ROADMAP.md` 참조

---

## 1. 프로젝트 현재 상태 (필수 인지)

- **실제 코드는 아직 하나도 존재하지 않는다.** `pages/`, `tests/`, `utils/`, `config/`, `conftest.py`, `requirements.txt` 등은 모두 미생성 상태이다.
- 존재하는 것은 문서뿐이다: `CLAUDE.md`, `docs/prd/project-prd.md`, `docs/prd/features/*.md`, `docs/ROADMAP.md`, `.claude/agents/**`.
- 코드 관련 작업을 요청받으면, 먼저 `docs/ROADMAP.md`를 열어 어느 Phase까지 실제로 완료되었는지 확인한다. ROADMAP.md의 체크박스만 신뢰하고, 체크되지 않은 항목을 이미 완료된 것으로 가정하지 않는다.

---

## 2. 문서 소유권 및 요청 라우팅 (핵심 규칙)

이 프로젝트에는 역할이 엄격히 분리된 두 개의 전담 서브에이전트가 정의되어 있다. **요청의 성격에 따라 아래 표대로 라우팅한다.**

| 요청 성격 | 담당 | 대상 파일 | 금지 사항 |
|---|---|---|---|
| 프로젝트 전체 MVP PRD 작성/수정 | `automation-prd-writer` 서브에이전트 | `docs/prd/project-prd.md` | 메인 에이전트가 이 파일을 직접 수정하지 않는다 |
| 기능별 상세 PRD 작성/수정 | `automation-prd-writer` 서브에이전트 | `docs/prd/features/{feature-name}.md` | 메인 에이전트가 이 파일을 직접 수정하지 않는다 |
| 실행 로드맵/진행 상태(착수·완료·블록) 갱신 | `roadmap-writer` 서브에이전트 | `docs/ROADMAP.md` | 메인 에이전트가 이 파일을 직접 수정하지 않는다 |
| Selenium/pytest 코드, Page Object, conftest, requirements.txt 등 실제 구현 | 메인 에이전트(또는 향후 정의될 코드 전담 서브에이전트)가 직접 수행 | `pages/`, `tests/`, `utils/`, `config/`, `conftest.py` 등 | `automation-prd-writer`, `roadmap-writer`에게 위임하지 않는다 (이 두 서브에이전트는 코드 생성 권한이 없음) |

**판단 예시**:
- "로그인 PRD에 비정상 시나리오 추가해줘" → `automation-prd-writer` 호출 (`docs/prd/features/login.md` 수정 대상).
- "Phase 1 진행 상황 업데이트해줘" / "로드맵에 새 블로커 추가해줘" → `roadmap-writer` 호출 (`docs/ROADMAP.md` 수정 대상).
- "LoginPage 클래스 구현해줘" / "test_signup.py 작성해줘" → 서브에이전트 위임 금지, CLAUDE.md 규칙에 따라 직접 구현.
- "회원가입 요구사항이 바뀌었으니 코드도 같이 고쳐줘"처럼 PRD 변경과 코드 변경이 섞인 요청은 **먼저 `automation-prd-writer`로 PRD를 갱신하고, 그 결과를 반영해 코드를 직접 수정**하는 순서로 나눈다. 두 작업을 한 번에 뭉뚱그려 처리하지 않는다.

---

## 3. 다중 파일 동기화 규칙

- `docs/prd/project-prd.md`를 수정한 경우, `docs/ROADMAP.md` 상단 "기준 문서 및 버전" 표의 버전 번호가 최신 상태와 일치하는지 확인한다. 불일치하면 `roadmap-writer`에게 갱신을 제안한다 (직접 고치지 않음).
- `docs/prd/features/*.md` 중 하나를 수정해 `docs/prd/project-prd.md`의 서술과 모순이 생기면, **임의로 project-prd.md를 덮어쓰지 않는다.** 모순 내용을 사용자에게 보고하고 승인 후 `automation-prd-writer`를 통해 수정한다. (이는 `automation-prd-writer` 서브에이전트 정의에 이미 규정된 원칙이며, 메인 에이전트도 동일하게 따른다.)
- `docs/prd/features/*.md`가 갱신되었는데 `docs/ROADMAP.md`의 해당 Phase Task 목록이 이를 반영하지 못하고 있다면, `roadmap-writer`에게 갱신을 제안한다.

---

## 4. 코드 작업 착수 전 확인 규칙

- Page Object(`pages/*.py`) 또는 테스트(`tests/test_*.py`) 구현을 시작하기 전, `docs/ROADMAP.md`의 해당 기능 섹션에 명시된 **블로커** 항목(예: 실제 Locator 미공유, 테스트 계정 미생성)이 해소되었는지 확인한다. 해소되지 않았다면 사용자에게 먼저 확인을 요청하고, 추측으로 Locator나 계정 정보를 만들어내지 않는다.
- 코드 작업 시작 전 `CLAUDE.md`를 반드시 재확인한다 (디렉터리 구조, Locator 우선순위, Wait 규칙, Page/Test 계층 책임 분리, 2칸 들여쓰기 등은 `CLAUDE.md`가 유일한 기준이며 이 문서에서 반복하지 않는다).
- Phase 순서를 건너뛰지 않는다: `docs/ROADMAP.md`는 Phase 0(기반 설정) → Phase 1(인증/탐색) → Phase 2(장바구니) → Phase 3(안정화) 순서를 전제로 Task 간 선행 조건을 명시하고 있다. 예를 들어 `pages/base_page.py`(Phase 0)가 없는 상태에서 `pages/login_page.py`(Phase 1)부터 구현하지 않는다.

---

## 5. 모호한 요청 처리 기준

다음 정보가 없는 상태로 확정적인 결정이 필요한 경우, 임의로 결정하지 말고 사용자에게 질문한다:
- 자동화 대상 사이트의 실제 UI 요소(id/name/data-*/CSS selector) — 추측으로 Locator를 작성하지 않는다.
- 테스트 계정의 실제 이메일/비밀번호/이름 값.
- PRD에 "확인 필요"로 표시된 항목의 실제 값(예: 세션 타임아웃 시간).

위 항목이 없어도 진행 가능한 문서 작업(PRD 초안, 로드맵 구조화 등)은 "확인 필요"로 표시한 채 진행하되, **코드에 실제 값처럼 하드코딩하지 않는다.**

---

## 6. 금지 행위 요약

- 메인 에이전트가 `docs/prd/project-prd.md`, `docs/prd/features/*.md`, `docs/ROADMAP.md`를 직접 수정하는 행위 (반드시 해당 서브에이전트 경유).
- `automation-prd-writer`, `roadmap-writer`에게 Selenium/pytest 코드, Page Object, conftest, requirements.txt 생성을 요청하는 행위 (두 서브에이전트 모두 Read/Write/Edit 권한만 있고 코드 생성은 역할 범위 밖).
- `docs/ROADMAP.md`의 기존 체크(✅) 표시를 실제 코드/테스트 존재 여부 확인 없이 임의로 변경하는 행위.
- PRD 문서 간(project-prd.md ↔ features/*.md) 또는 PRD-ROADMAP 간 불일치를 발견하고도 사용자 보고 없이 한쪽을 임의로 맞춰 고치는 행위.
- 실제 사이트에서 확인되지 않은 Locator, 오류 메시지, URL을 확인된 사실처럼 PRD나 코드에 작성하는 행위.
