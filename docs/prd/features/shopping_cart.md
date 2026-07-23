# 장바구니 (Shopping Cart) 기능 상세 PRD

**작성 일자**: 2026-07-22
**최종 수정일**: 2026-07-23 (v1.4 - "Add to cart" 버튼 노출 위치, "Continue Shopping" 버튼 동작, 상품 목록 페이지에서의 수량 지정 불가 여부를 실제 사이트 확인을 통해 확정 반영. "Product review platform" 버튼 관련 서술은 문서 범위에서 전체 삭제)
**버전**: 1.4
**상태**: 개정판. v1.4에서 사용자가 실제 사이트를 확인하여 제공한 4가지 확정/결정 사항을 반영했습니다: (1) "Add to cart" 버튼이 상품 목록 카드와 상품 상세 페이지 양쪽 모두에 노출된다는 사실을 확정으로 전환, (2) 담기 성공 안내 모달의 "Continue Shopping" 버튼 클릭 시 모달이 닫히고 현재 페이지(모달을 띄웠던 상품 목록 또는 상품 상세 페이지)가 그대로 유지됨을 확정, (3) "Product review platform" 버튼 관련 서술을 자동화 범위와 무관하다는 사용자 판단에 따라 문서 전체에서 삭제, (4) 상품 목록 페이지에서는 수량 지정 UI가 없어 항상 1개만 담기고, 수량 지정은 상품 상세 페이지에서만 가능함을 확정. v1.3에서 반영된 테스트 상품 데이터, 상품 상세 페이지 URL/진입 경로, 삭제 즉시 반영, 로그인 모달 노출 시 URL 유지, 페이지 전체 합계 요소 부재, 담기 성공 모달 레이아웃, 빈 장바구니 "here" 링크 목적지, 새로고침 후 유지 여부 등은 이번 버전에서도 그대로 유지됩니다. "Add to cart" 버튼의 정확한 id/class 등 Locator 값은 여전히 **확인 필요**로 남아 있으며, Page Object 구현 착수 시 사용자가 실시간으로 공유할 예정입니다.

---

## 1. 기능명

- **한국어명**: 장바구니
- **영문명**: Shopping Cart
- **기능 ID**: CART

---

## 2. 기능 목적

사용자가 상품 목록 또는 상품 상세 페이지에서 관심 있는 상품을 장바구니에 담고, 장바구니 페이지에서 담긴 상품 목록과 가격/수량/합계를 확인하며, 불필요한 상품은 삭제하고, 결제(Checkout) 단계로 진입하기 전 주문 내용을 최종 검토할 수 있도록 하는 기능입니다.

### 비즈니스 가치
- 사용자가 여러 상품을 한 번에 검토하고 구매를 결정할 수 있는 중간 단계 제공
- 상품별 가격, 수량, 합계(Total)를 투명하게 제공하여 구매 결정을 지원
- 담아둔 상품 중 불필요한 항목을 삭제하여 최종 구매 목록을 정리할 수 있는 기능 제공
- 결제(Checkout) 이전 단계에서 주문 내용을 최종 검토할 수 있는 지점 제공
- 상품 검색/조회 기능과 결제 기능을 연결하는 핵심 중간 기능으로서 전체 구매 흐름의 완결성 확보

---

## 3. 프로젝트 전체 PRD와의 연관성

### 기준 문서
**참고**: `docs/prd/project-prd.md`

### 연관 섹션
- **7.1 MVP 스코프**: "5. 장바구니 (Shopping Cart) - 상품을 장바구니에 추가, 장바구니 내용 확인" (192-194행)
- **8.2 Phase 2**: 장바구니 및 고급 기능 - "장바구니 추가(Add to Cart)", "장바구니 조회(View Cart)", "장바구니 수량 변경" 3개 세부 기능과 산출물로 `docs/prd/features/shopping_cart.md` 명시 (240-260행)

  **[중요 - 실제 사이트 확인 결과 반영]** project-prd.md 8.2(254-256행)에는 "장바구니 수량 변경"이 Phase 2 목표로 명시되어 있으나, 실제 사이트(https://automationexercise.com/view_cart) 확인 결과 **장바구니 페이지에서는 수량을 직접 변경할 수 없는 것으로 확인**되었습니다(섹션 7, 10 참고). 이 문서는 실제 사이트 동작을 우선하여 "수량 변경" 관련 요구사항을 제거하고, 대신 실제로 존재함이 확인된 "상품 삭제" 기능을 자동화 범위에 포함하는 방향으로 개정합니다. project-prd.md 5.1/8.2의 해당 서술은 이번 확인 결과와 불일치하므로, project-prd.md 자체의 갱신 여부는 사용자 승인을 거쳐 별도로 진행되어야 하며 이 문서의 개정 범위에는 포함하지 않습니다.
- **9.1 주요 사용자 흐름**: 단계 4(장바구니에 상품 추가, 322-330행), 단계 5(장바구니 확인, 332-339행) - 큰 흐름은 여전히 유효하나 "장바구니 아이콘 개수 반영"(326행), "수량 표시"(336행) 등 세부 서술 일부는 이번 확인 결과와 다르므로 이 문서의 확정 사실을 우선합니다.
- **5.2 MVP 대상 기능**: 우선순위 2 (높음) - "장바구니에 제품 추가", "장바구니 조회" (133-137행)
- **5.1 주요 기능 (전체 대상 사이트)**: "장바구니에 제품 추가", "장바구니 조회", "장바구니 수량 변경", "장바구니에서 제품 삭제" 4개 세부 기능이 나열되어 있음(108-112행). 이번 확인으로 "수량 변경"은 실제 사이트에 존재하지 않고, "제품 삭제"는 실제로 존재함이 확인되어, 이 문서는 5.1의 "제품 삭제" 항목을 자동화 범위에 포함하는 근거로 삼습니다(섹션 11 참고).

### 의존성
- **선행 기능**: 상품 검색(Product Search) 또는 상품 목록 조회 - 장바구니에 담을 상품을 먼저 찾아야 함 (project-prd.md 8.1, 226-230행)
- **후행 기능(결제 프로세스 자체는 범위 밖)**: 결제(Checkout) - project-prd.md 6.1에서 MVP 제외 대상으로 명시됨(158행). 결제 프로세스 자체(배송지/결제 정보 입력, 주문 완료 등)는 이 문서 범위 밖이나, "Proceed to Checkout 클릭 및 그 직후 분기(로그인 모달 노출)"까지는 장바구니 기능의 경계로 포함합니다(섹션 9, 11 참고).
- **로그인(Login) 기능과의 관계 (확정)**: 비로그인 상태에서도 장바구니 담기/조회/삭제는 모두 가능합니다. 로그인이 요구되는 지점은 장바구니 자체가 아니라 **"Proceed to Checkout" 클릭(결제 진입 시도) 시점**입니다 - 비로그인 상태에서 클릭하면 로그인 안내 모달이 노출됨을 확인했습니다(섹션 6, 9 참고). login.md 섹션 18의 "장바구니(Shopping Cart): 로그인 후 기능 활용(일부 기능)" 서술은 이 결제 진입 제약을 가리키는 것으로 해석 가능하나, 정확한 표현 정합은 향후 login.md 개정 시 함께 검토가 필요합니다. 로그인 이후 결제 페이지에서의 상세 동작은 향후 checkout PRD에서 다룹니다.

---

## 4. 대상 URL 또는 진입 경로

### 관련 URL

- **장바구니 페이지**: `https://automationexercise.com/view_cart` (확정)
- **상품 목록 페이지**: `https://automationexercise.com/products` (확정 - `product_search.md` 섹션 4에서 이미 확정된 사실을 이 문서에 동기화 반영, v1.2)
- **상품 상세 페이지**: `https://automationexercise.com/product_details/{id}` (확정, v1.3 - `id`는 1~8 범위의 정수이며 상품별 고유 ID. 상품 목록에서 특정 상품의 상세 페이지로 이동할 때 이 URL 패턴이 사용됨)

### 진입 경로 (확정)

1. **헤더 "Cart" 클릭**: 헤더 영역의 "Cart" 클릭 → 장바구니 페이지(`https://automationexercise.com/view_cart`)로 이동
2. **담기 성공 안내 모달의 "View Cart" 클릭**: 상품을 장바구니에 담는 데 성공하면 안내 모달이 노출되고, 모달 내 "View Cart" 버튼을 클릭하면 장바구니 페이지로 이동
   - 이 안내 모달은 아래 두 진입 지점 모두에서 "Add to cart" 클릭 시 공통으로 노출됨:
     - 상품 목록/검색 결과 페이지 > 상품 카드에서 "Add to cart" 클릭 시
     - 상품 상세 페이지에서 "Add to cart" 클릭 시
   - 담기 성공 안내는 모달 형태이며, 모달 안에 "View Cart" 버튼이 존재함 (기존 "모달인지 토스트인지 확인 필요" 상태를 **모달로 확정**)
3. **상품 목록 페이지에서 "View Product" 클릭 → 상품 상세 페이지 이동** (확정, v1.3): 상품 목록 페이지에서 상품 카드의 **"View Product"** 버튼을 클릭하면 해당 상품 ID를 포함한 `/product_details/{id}` URL의 상품 상세 페이지로 이동함. 이는 같은 카드 내 "Add to cart" 버튼과는 별개의 버튼임 (섹션 19 Page Object 설명 참고)

### 확인 완료 (v1.4)
- 담기 성공 안내 모달 내 "Continue Shopping" 버튼 클릭 시 동작: **모달이 닫히고, 현재 페이지(모달을 띄웠던 상품 목록 또는 상품 상세 페이지)가 그대로 유지됨** (페이지 이동이나 새로고침 없음, 확정)
- 상품 목록 페이지에서의 수량 지정 가능 여부: **상품 목록 페이지에는 수량 입력 UI가 없어 항상 1개만 담기며, 수량 지정은 상품 상세 페이지에서만 가능함** (확정)

### 확인 필요
- "Add to cart" 버튼의 정확한 id/class/data-* 속성 (버튼 문구 "Add to cart" 자체, 그리고 상품 목록 카드와 상품 상세 페이지 양쪽에 노출된다는 사실은 확정)

---

## 5. 사용자 역할

### 대상 사용자
- **비회원(Guest)**: 로그인 없이 장바구니 담기/조회/삭제가 모두 가능함 (확정)
- **기존 회원(Registered User)**: 로그인한 상태에서도 동일하게 이용 가능. 로그인 상태에서 "Proceed to Checkout" 클릭 시 로그인 모달 없이 바로 다음 단계로 진행되는지 여부는 결제 기능 PRD 영역이며 **확인 필요**

### 사용자 시나리오
- 상품을 검색/조회한 후 장바구니에 담아 구매를 검토하는 사용자 (회원/비회원 무관하게 가능, 확정)
- 담아둔 상품 중 일부를 삭제하려는 사용자
- 장바구니 검토를 마치고 결제를 진행하려는 사용자(비회원인 경우 로그인 안내를 받게 됨, 섹션 9 참고)

---

## 6. 사전 조건 (Precondition)

### 필수 조건
1. **상품 존재**: 장바구니에 담을 수 있는 상품이 상품 목록/상세 페이지에 최소 1개 이상 존재해야 함
2. **사이트 접근**: Automation Exercise 사이트에 접근 가능
   - 인터넷 연결이 정상
   - 사이트가 운영 중 (다운타임 없음)
3. **브라우저 상태**: 테스트 시작 전 장바구니가 비어 있는 상태 (또는 테스트 목적에 맞게 사전 정의된 상태)

### 로그인 관련 (확정)
- 장바구니 담기/조회/삭제는 **로그인이 필요하지 않습니다** (확정)
- **비로그인 상태에서 "Proceed to Checkout" 클릭 시 로그인 안내 모달이 노출됩니다** (확정). 즉 로그인이 필요한 지점은 장바구니 자체가 아니라 결제 진입 시점입니다.

### 테스트 데이터 준비
- 장바구니에 담을 대상 상품 정보 (상품명 또는 식별자, 예상 가격)
- 상품 삭제 테스트를 위해 최소 1개 이상 담긴 상태
- 동일 상품 중복 담기 테스트를 위해 동일한 상품명을 2회 이상 담을 수 있는 시나리오 데이터

---

## 7. 주요 화면과 UI 요소

### 화면 1: 상품 목록/상세 페이지의 담기 영역 및 담기 성공 모달

| 요소명 | 타입 | 설명 | 필수 여부 | 확인 상태 |
|--------|------|------|---------|---------|
| **상품명/가격 표시 영역** | Text | 상품명과 가격 표시 | 필수 | 확인 필요(구체 레이아웃) |
| **Add to cart 버튼** | Button | 문구 "Add to cart"로 확정. **상품 목록 카드와 상품 상세 페이지 양쪽 모두에 노출됨** (확정, v1.4 - 기존 추정을 확정으로 전환) | 필수 | 노출 위치 확정, locator 확인 필요 |
| **View Product 버튼** | Button/Link | 상품 목록 카드에서 상품 상세 페이지(`/product_details/{id}`)로 이동하는 버튼. "Add to cart"와는 별개의 버튼 (확정, v1.3) | 필수 | 확정 (존재, 이동 대상 URL 패턴), locator 확인 필요 |
| **담기 성공 안내 모달** | Modal | 담기 성공 시 노출되는 모달. 초록색 원형 체크마크 아이콘, 제목 "Added!", 본문 "Your product has been added to cart.", 파란색 텍스트 링크 "View Cart"(클릭 시 `/view_cart` 이동), 초록색 버튼 "Continue Shopping"으로 구성 (레이아웃 확정, v1.3, 스크린샷 근거) | 필수 | 레이아웃 확정. "Continue Shopping" 클릭 시 **모달이 닫히고 현재 페이지(모달을 띄웠던 페이지)가 그대로 유지됨** (확정, v1.4) |

### 화면 2: 장바구니 페이지 (실제 레이아웃, 스크린샷 근거로 확정)

```
Home > Shopping Cart                                            (breadcrumb)

                                          [ Proceed To Checkout ]  (상품 목록 위, 우측 정렬)

┌────────┬──────────────────────────────┬─────────┬──────────┬──────────┬─────┐
│ Item   │ Description                  │ Price   │ Quantity │ Total    │     │
├────────┼──────────────────────────────┼─────────┼──────────┼──────────┼─────┤
│ [이미지]│ Blue Top                     │ Rs. 500 │   [ 6 ]  │ Rs. 3000 │  X  │
│        │ Women > Tops                 │         │ (표시전용)│          │(삭제)│
└────────┴──────────────────────────────┴─────────┴──────────┴──────────┴─────┘
```

| 요소명 | 타입 | 설명 | 필수 여부 | 확인 상태 |
|--------|------|------|---------|---------|
| **breadcrumb** | Text/Link | "Home > Shopping Cart" 형태로 페이지 상단에 노출 | 필수 | 확정 |
| **Proceed To Checkout 버튼** | Button | 상품 목록 위쪽, 오른쪽 정렬로 위치. 장바구니에 상품이 있을 때만 노출됨(빈 장바구니 상태에서는 노출되지 않음, 섹션 9 참고) | 필수 | 확정 |
| **상품 목록 테이블** | Table | 컬럼 구성: Item(이미지) \| Description(상품명 + 카테고리 경로) \| Price \| Quantity \| Total. 각 행 오른쪽 끝에 삭제(X) 아이콘 존재 | 필수 | 확정 |
| **Item 컬럼** | Image | 상품 이미지 | 필수 | 확정 |
| **Description 컬럼** | Text | 상품명과 카테고리 경로가 함께 표시됨 (예: "Blue Top" / "Women > Tops") | 필수 | 확정 |
| **Price 컬럼** | Text | 가격 표시. 형식은 "Rs. 500"과 같이 "Rs." 통화 단위 사용 | 필수 | 확정 |
| **Quantity 컬럼** | 표시 전용 박스 | 숫자가 박스 형태로 표시되나 **사용자가 직접 값을 변경할 수 없음** (표시 전용으로 확정) | 필수 | 확정 |
| **Total 컬럼** | Text | Price × Quantity (예: Rs.500 × 6 = Rs.3000) | 필수 | 확정 |
| **삭제(X) 아이콘** | Button/Icon | 각 상품 행 오른쪽 끝에 위치, 클릭 시 해당 상품을 장바구니에서 즉시 제거함(페이지 리로드 없이 해당 행이 즉시 사라짐, 확정 v1.3) | 필수 | 확정 (존재 및 즉시 삭제 동작) |
| **페이지 전체 합계(총액) 표시 요소** | Text | 모든 상품 Total의 합을 별도로 보여주는 요소는 장바구니 페이지에 **존재하지 않음** (확인 완료, v1.3). 각 행의 개별 Total만 존재함 | 해당 없음 | 확인 완료: 존재하지 않음 |
| **빈 장바구니 안내 메시지** | Text + Link | "Cart is empty! Click here to buy products." 문구, 문구 내 "here" 링크는 클릭 시 상품 목록 페이지(`/products`)로 이동(확정, v1.3) | 조건부(빈 상태에서 노출) | 문구 및 "here" 링크 이동 대상 모두 확정 |

### 헤더 네비게이션 (확정)
- 헤더의 장바구니(Cart) 아이콘에는 담긴 상품 개수가 표시되지 않습니다 (확정). 기존 "장바구니 아이콘에 개수가 반영됨" 추정은 정정되었습니다.

### 확인 필요 (종합)
- 상품 목록/상세 페이지에서 담기 버튼 및 View Product 버튼의 정확한 id, CSS 클래스, data-* 속성 (노출 위치 자체는 확정)

---

## 8. 정상 사용자 흐름 (Happy Path)

### 흐름 1: 상품 목록 페이지에서 장바구니에 상품 추가

**시작 조건**: 상품 목록 또는 검색 결과 페이지 방문, 담을 상품 존재

**단계별 행동**:
1. 사용자가 상품 목록(또는 검색 결과) 페이지에 접속
2. 원하는 상품 카드의 "Add to cart" 버튼 클릭 (상품 목록 페이지에는 수량 입력 UI가 없으므로 항상 1개만 담김, 확정 v1.4)
3. 담기 성공 안내 모달 노출 (확정, 모달 내 "View Cart" 버튼 포함)
4. 모달의 "View Cart" 버튼 클릭 → 장바구니 페이지(`/view_cart`)로 이동

**기대 결과**:
- 상품이 장바구니에 1개 추가됨 (상품 목록 페이지에서는 수량 지정이 불가능하여 항상 1개만 담김, 확정 v1.4)
- 헤더의 장바구니 아이콘에는 개수가 표시되지 않음 (확정)

---

### 흐름 2: 상품 상세 페이지에서 장바구니에 상품 추가

**시작 조건**: 특정 상품의 상세 페이지 방문

**단계별 행동**:
1. 사용자가 상품 목록에서 특정 상품을 클릭하여 상세 페이지로 이동
2. 상세 페이지에서 수량을 지정 (**수량 지정은 상품 상세 페이지에서만 가능함, 확정 v1.4**. 별도로 지정하지 않으면 기본값 1)
3. "Add to cart" 버튼 클릭
4. 담기 성공 안내 모달 노출 → "View Cart" 클릭 → 장바구니 페이지로 이동

**기대 결과**:
- 지정한 수량만큼 상품이 장바구니에 추가됨 (수량 지정은 상세 페이지에서만 가능, 확정 v1.4)
- 헤더의 장바구니 아이콘에는 개수가 표시되지 않음 (확정)

---

### 흐름 3: 장바구니 조회 및 상품 삭제

**시작 조건**: 장바구니에 1개 이상의 상품이 담긴 상태

**단계별 행동**:
1. 헤더의 "Cart" 클릭 (또는 담기 성공 모달의 "View Cart" 클릭)
2. 장바구니 페이지(`/view_cart`)로 이동, 담긴 상품 목록(Item/Description/Price/Quantity/Total)을 확인
3. 특정 상품 행의 삭제(X) 아이콘 클릭
4. 별도 페이지 리로드 없이 해당 상품 행이 즉시 사라짐 (확정, v1.3)

**기대 결과**:
- 장바구니에 담긴 상품들의 이미지, 상품명, 카테고리 경로, 가격, 수량, Total이 정확히 표시됨
- 삭제 후 해당 상품 행이 페이지 새로고침 없이 즉시 목록에서 사라짐 (확정)

**참고**: 장바구니 내 수량은 표시 전용이며 변경할 수 없으므로(확정), 이 문서에서는 "수량 변경에 따른 재계산" 흐름을 다루지 않습니다.

---

### 흐름 4: 동일 상품을 중복으로 장바구니에 담기

**시작 조건**: 장바구니에 특정 상품이 이미 1개 이상 담긴 상태

**단계별 행동**:
1. 이미 장바구니에 담겨 있는 상품을 상품 목록 또는 상세 페이지에서 다시 "Add to cart" 클릭
2. 장바구니 페이지에서 해당 상품의 행 확인

**기대 결과**:
- 별도의 행이 추가되지 않고, **기존 행의 수량(Quantity)이 증가**함 (확정)
- Total은 증가한 수량 기준으로 재계산되어 표시됨

---

### 흐름 5: 비로그인 상태에서 결제(Checkout) 진입 시도

**시작 조건**: 비로그인 상태, 장바구니에 1개 이상의 상품이 담긴 상태

**단계별 행동**:
1. 장바구니 페이지에서 "Proceed To Checkout" 버튼 클릭
2. 로그인 안내 모달이 노출됨 (확정). 이때 현재 URL은 변경되지 않고 계속 `/view_cart`에 머무름 (확정, v1.3)

**기대 결과**:
- 결제 페이지로 바로 이동하지 않고, 로그인을 안내하는 모달이 노출됨
- 모달 노출 후에도 URL은 `/view_cart`로 유지됨 (확정)
- 결제 프로세스 자체(로그인 이후 흐름)는 이 문서 범위 밖이며, 이 흐름은 "모달 노출 확인"까지만 이 기능의 정상 분기 시나리오로 다룸(섹션 13 NOR-005 참고)

---

## 9. 예외 사용자 흐름 (Exception Flow)

### 흐름 1: 빈 장바구니 상태에서 장바구니 페이지 조회

**설명**: 아직 아무 상품도 담지 않은 상태에서 장바구니 페이지에 접근하는 흐름입니다.

**단계별 행동**:
1. 상품을 하나도 담지 않은 상태에서 헤더의 "Cart" 클릭
2. 장바구니 페이지(`/view_cart`)로 이동

**기대 결과** (확정):
- "Cart is empty! Click here to buy products." 안내 문구가 표시됨 (문구 내 "here" 링크 클릭 시 상품 목록 페이지(`/products`)로 이동함, 확정 v1.3)
- "Proceed To Checkout" 버튼은 노출되지 않음 (확정)

---

### 흐름 2: 비로그인 상태에서 결제 진입 시도 (예외적 분기로도 해석 가능)

**설명**: 장바구니 자체는 비로그인으로도 완전히 이용 가능하지만, 결제 진입 시점에는 로그인이 필요합니다. 이 흐름은 섹션 8 흐름 5와 동일한 사실을 다루되, "장바구니를 정상적으로 이용했지만 결제 직전에 막히는 경우"라는 관점에서 예외 흐름으로도 기록합니다.

**단계별 행동**:
1. 비로그인 상태에서 장바구니에 상품을 담고 장바구니 페이지 방문
2. "Proceed To Checkout" 버튼 클릭

**기대 결과**:
- 로그인 안내 모달 노출 (확정)
- 이 시나리오는 섹션 13 NOR-005(정상 분기) 및 섹션 14 ABN-001(비정상/제약 관점)에서 각각 자동화 대상으로 다룸(중복 구현이 아니라 동일 시나리오를 어느 시나리오 유형으로 우선 분류할지는 구현 시 택일)

---

## 10. 기능 요구사항

### 요구사항 정의

**CART-REQ-001**: 상품 목록 페이지에서 장바구니 추가
- 사용자는 상품 목록(또는 검색 결과) 페이지에서 "Add to cart" 버튼을 클릭하여 해당 상품을 장바구니에 추가할 수 있어야 한다.

**CART-REQ-002**: 상품 상세 페이지에서 장바구니 추가
- 사용자는 상품 상세 페이지에서 "Add to cart" 버튼을 클릭하여 해당 상품을 장바구니에 추가할 수 있어야 한다.

**CART-REQ-003**: 장바구니 조회
- 사용자는 헤더의 "Cart" 클릭 또는 담기 성공 모달의 "View Cart" 클릭을 통해 장바구니 페이지(`/view_cart`)에 접근하여, 담긴 상품들의 이미지(Item), 상품명 및 카테고리 경로(Description), 가격(Price), 수량(Quantity), 합계(Total)를 확인할 수 있어야 한다.

**CART-REQ-004**: 상품별 Total 계산 및 표시
- 장바구니 페이지의 각 상품 행은 Price × Quantity로 계산된 Total 값을 표시해야 한다. (예: Rs.500 × 6 = Rs.3000)
- 장바구니 페이지에는 페이지 전체 합계(모든 상품 Total의 합)를 표시하는 요소가 존재하지 않는다 (확인 완료, v1.3). 따라서 이 요구사항은 행 단위 Total 계산 정확성만을 검증 대상으로 하며, 페이지 전체 합계 요소에 대한 검증은 대상이 아니다.

**CART-REQ-005**: 장바구니 내 수량은 표시 전용 (확정)
- 장바구니 페이지의 Quantity 컬럼은 값이 박스 형태로 표시되나, 사용자가 이 값을 직접 변경할 수 있는 UI를 제공하지 않는다. 즉 장바구니 내에서는 수량 변경이 불가능하다. (v1.0의 "CART-REQ-005 장바구니 수량 변경" 요구사항을 대체함)

**CART-REQ-006**: 상품 삭제
- 사용자는 장바구니 페이지에서 각 상품 행의 삭제(X) 아이콘을 클릭하여 해당 상품을 장바구니에서 제거할 수 있어야 한다.
- 삭제 후 해당 상품 행은 별도의 페이지 리로드 없이 즉시 목록에서 사라져야 한다 (확정, v1.3).

**CART-REQ-007**: 빈 장바구니 상태 처리
- 장바구니에 담긴 상품이 없는 경우, 장바구니 페이지는 "Cart is empty! Click here to buy products." 문구를 표시해야 하며, "Proceed To Checkout" 버튼은 노출하지 않아야 한다.

**CART-REQ-008**: 동일 상품 중복 담기 시 수량 증가
- 이미 장바구니에 담긴 상품을 다시 "Add to cart"로 담을 경우, 별도의 행이 추가되는 대신 기존 행의 수량이 증가해야 한다.

**CART-REQ-009**: 비로그인 상태에서 결제 진입 시 로그인 안내
- 비로그인 상태에서 "Proceed To Checkout" 버튼을 클릭하면 로그인 안내 모달이 노출되어야 한다.
- 모달 노출 후에도 현재 URL은 `/view_cart`로 유지되어야 한다 (확정, v1.3).

**CART-REQ-010**: 장바구니 상태 유지 (확정)
- 장바구니에 담긴 상품 목록은 새로고침 후에도 유지되어야 한다 (확인 완료, v1.3). 저장 방식(세션/쿠키/DB)의 내부 구현 자체는 자동화 검증 대상이 아니다 (섹션 12 참고).

---

## 11. 자동화 대상 범위

### 자동화 범위 (포함)

| 시나리오 | 자동화 대상 | 설명 |
|---------|-----------|------|
| **상품 목록 페이지에서 장바구니 추가** | ✅ 포함 | 상품 목록에서 "Add to cart" 클릭 → 모달 노출 → "View Cart" 클릭 → 장바구니에 정상 반영되는지 확인 |
| **상품 상세 페이지에서 장바구니 추가** | ✅ 포함 | 상품 상세 페이지에서 "Add to cart" 클릭 후 장바구니에 정상 반영되는지 확인 |
| **장바구니 조회** | ✅ 포함 | 담긴 상품의 Item/Description/Price/Quantity/Total이 정확히 표시되는지 확인 |
| **상품 삭제** | ✅ 포함 (v1.1 신규) | 삭제(X) 아이콘 클릭 후 해당 상품 행이 목록에서 제거되는지 확인. 실제 사이트 확인 결과 삭제는 장바구니의 핵심 동작으로 확인되어 이번 개정에서 자동화 범위에 새로 포함함(섹션 3 근거) |
| **동일 상품 중복 담기 시 수량 증가 확인** | ✅ 포함 (v1.1 신규) | 동일 상품을 재차 담을 경우 기존 행의 수량이 증가하는지 확인 (project-prd.md 19.1에서 미확정이던 사항이 확정됨) |
| **빈 장바구니 상태 확인** | ✅ 포함 | 상품을 담지 않은 상태에서 장바구니 페이지 접근 시 안내 문구 및 Proceed To Checkout 버튼 미노출 확인 |
| **비로그인 상태에서 결제 진입 시도** | ✅ 포함 (v1.1 신규) | "Proceed To Checkout" 클릭 시 로그인 안내 모달이 노출되는지 확인. 모달 노출까지만 대상이며, 로그인 처리 자체 및 결제 프로세스는 제외 |

### v1.0 대비 제거된 항목
- ~~장바구니 수량 변경 및 총액 재계산~~: 실제 사이트에 수량 변경 UI가 존재하지 않는 것으로 확인되어 제거
- ~~수량을 0 이하로 변경 시도~~: 위와 동일한 사유로 전제 자체가 성립하지 않아 제거

---

## 12. 자동화 제외 범위

### 자동화 제외 사유

| 기능 | 제외 사유 |
|------|---------|
| **결제(Checkout) 프로세스 자체(로그인 이후 흐름)** | project-prd.md 6.1(158행)에서 MVP 제외 대상으로 명시됨. 로그인 이후의 배송지/결제 정보 입력, 주문 완료 등은 별도 기능(향후 checkout.md 등)으로 분리될 수 있음. 이 문서는 "Proceed To Checkout 클릭 시 로그인 모달이 노출되는지"까지만 다룸 |
| **로그인 안내 모달의 상세 동작(로그인 폼 제출, 회원가입 유도 등)** | 모달 내부의 로그인/가입 기능 자체는 login.md/signup.md 영역이며, 이 문서는 모달의 노출 여부만 검증 대상으로 함 |
| **장바구니 최대 담을 수 있는 상품 개수 제한 검증** | 사용자 판단에 따라 테스트 범위에서 제외 (실제 동작 미확인, v1.3 결정) |
| **장바구니 데이터의 세션/쿠키/DB 저장 방식 자체 검증** | 사용자 판단에 따라 테스트 범위에서 제외 (실제 동작 미확인, v1.3 결정) |
| **가격/통화 형식의 정밀 검증(소수점 처리 등)** | "Rs." 통화 단위 표기는 확정되었으나, 소수점 등 세부 형식 규칙은 미확인 상태이며, Total 계산의 산술적 정확성만 검증 대상으로 하고 형식 자체의 세부 검증은 제외 |
| **다중 탭/다중 세션 간 장바구니 동기화** | 인프라 수준의 검증으로 MVP 범위 밖 |
| **성능/부하 테스트(대량 상품 담기 등)** | 별도 전문 도구 필요, project-prd.md 6.1(161행) 근거 |

---

## 13. 정상 시나리오 (Normal Scenarios)

### NOR-001: 상품 목록 페이지에서 장바구니에 상품 추가 성공

**전제조건**: 상품 목록 페이지가 표시됨, 장바구니가 비어 있는 상태

**테스트 단계**:
1. 상품 목록 페이지 방문
2. 특정 상품 카드의 "Add to cart" 버튼 클릭
3. 담기 성공 안내 모달의 "View Cart" 버튼 클릭
4. 장바구니 페이지(`/view_cart`)에서 담긴 상품 확인

**기대 결과**:
- 장바구니에 해당 상품이 1개 추가됨 (상품 목록 페이지에는 수량 지정 UI가 없어 항상 1개만 담김, 확정 v1.4)
- 장바구니 페이지에서 해당 상품의 Description(상품명+카테고리), Price, Quantity, Total이 정확히 표시됨

**검증 포인트**:
- ✅ 장바구니 페이지에 해당 상품이 노출되는가?
- ✅ 상품의 수량이 기대한 값(기본값 1 또는 지정값)과 일치하는가?
- ✅ Total = Price × Quantity 가 성립하는가?

---

### NOR-002: 상품 상세 페이지에서 장바구니에 상품 추가 성공

**전제조건**: 특정 상품의 상세 페이지가 표시됨

**테스트 단계**:
1. 상품 상세 페이지 방문
2. 수량 입력(상품 상세 페이지에서만 가능, 확정 v1.4) 후 "Add to cart" 버튼 클릭
3. 담기 성공 안내 모달의 "View Cart" 버튼 클릭
4. 장바구니 페이지에서 담긴 상품 및 수량 확인

**기대 결과**:
- 장바구니에 해당 상품이 지정한 수량만큼 추가됨 (수량 지정은 상세 페이지에서만 가능, 확정 v1.4)

**검증 포인트**:
- ✅ 장바구니 페이지에 해당 상품이 노출되는가?
- ✅ 상품의 수량이 상세 페이지에서 지정한 값과 일치하는가?

---

### NOR-003: 장바구니에서 상품 삭제 성공

**전제조건**: 장바구니에 최소 1개 이상의 상품이 담긴 상태

**테스트 단계**:
1. 장바구니 페이지 방문
2. 삭제 대상 상품의 행이 목록에 존재하는지 확인
3. 해당 행의 삭제(X) 아이콘 클릭
4. 목록 재확인

**기대 결과**:
- 삭제한 상품의 행이 더 이상 목록에 표시되지 않음
- 삭제 후에도 나머지 상품(있는 경우)은 정상적으로 표시됨

**검증 포인트**:
- ✅ 삭제 전 해당 상품이 목록에 존재했는가?
- ✅ 삭제 후 해당 상품이 목록에서 사라졌는가?
- ✅ 장바구니에 남은 상품이 없는 경우, 빈 장바구니 안내(ABN-002 참고)가 노출되는가?

---

### NOR-004: 동일 상품 중복 담기 시 기존 행 수량 증가 확인

**전제조건**: 특정 상품이 이미 장바구니에 담긴 상태(수량 N)

**테스트 단계**:
1. 동일한 상품을 상품 목록 또는 상세 페이지에서 다시 "Add to cart" 클릭
2. 장바구니 페이지에서 해당 상품의 행 개수와 수량 확인

**기대 결과**:
- 별도의 행이 추가되지 않고, 기존 행의 Quantity가 증가함
- Total이 증가한 수량 기준으로 재계산되어 표시됨

**검증 포인트**:
- ✅ 장바구니 내 해당 상품의 행이 1개만 존재하는가? (별도 행 미생성)
- ✅ Quantity가 담기 전 대비 증가했는가?
- ✅ Total = Price × 증가한 Quantity 가 성립하는가?

---

### NOR-005: 비로그인 상태에서 결제 진입 시도 시 로그인 안내 모달 노출

**전제조건**: 비로그인 상태, 장바구니에 1개 이상의 상품이 담긴 상태

**테스트 단계**:
1. 장바구니 페이지에서 "Proceed To Checkout" 버튼 클릭
2. 화면 반응 확인

**기대 결과**:
- 로그인 안내 모달이 노출됨
- 결제 페이지로 직접 이동하지 않음

**검증 포인트**:
- ✅ 로그인 안내 모달이 노출되는가?
- ✅ 모달 노출 후 현재 URL이 `/view_cart`로 유지되는가? (확정, v1.3)

**참고**: 이 시나리오는 관점에 따라 섹션 14 ABN-001과 동일한 사실을 다루며, 구현 시 정상/비정상 중 하나로만 자동화(중복 구현 지양)하는 것을 권장합니다.

---

## 14. 비정상 시나리오 (Abnormal Scenarios)

### ABN-001: 비로그인 상태에서 결제 진입 제약 확인

**시나리오명**: 로그인하지 않은 사용자가 장바구니에서 바로 결제를 진행하려는 시도가 제약되는지 확인

**전제조건**: 비로그인 상태, 장바구니에 1개 이상의 상품이 담긴 상태

**테스트 단계**:
1. 장바구니 페이지에서 "Proceed To Checkout" 버튼 클릭
2. 결제 페이지로 진행되지 않고 로그인 안내 모달이 노출되는지 확인

**기대 결과** (확정):
- 결제 페이지로 이동하지 않고 로그인 안내 모달이 노출됨

**검증 포인트**:
- ✅ 로그인 안내 모달이 노출되는가?
- ✅ 결제 페이지(향후 checkout PRD 대상)로 이동하지 않는가?
- ✅ 현재 URL이 `/view_cart`로 유지되는가? (확정, v1.3)

**참고**: v1.0의 ABN-001("수량을 0 이하로 변경 시도")은 장바구니 내 수량 변경 UI 자체가 존재하지 않는 것으로 확인되어 이번 개정에서 이 시나리오로 대체되었습니다.

---

### ABN-002: 빈 장바구니 상태에서 장바구니 페이지 조회

**시나리오명**: 상품을 하나도 담지 않은 상태에서 장바구니 페이지 접근

**전제조건**: 장바구니가 비어 있는 상태 (신규 세션 또는 아무 상품도 담지 않은 상태)

**테스트 단계**:
1. 상품을 담지 않은 상태에서 헤더의 "Cart" 클릭
2. 장바구니 페이지 로드 완료 대기

**기대 결과** (확정):
- "Cart is empty! Click here to buy products." 안내 문구가 표시됨
- 상품 목록 테이블은 표시되지 않음
- "Proceed To Checkout" 버튼은 노출되지 않음

**검증 포인트**:
- ✅ 빈 장바구니 안내 문구("Cart is empty! Click here to buy products.")가 정확히 표시되는가?
- ✅ 상품 목록 영역에 담긴 상품이 하나도 표시되지 않는가?
- ✅ "Proceed To Checkout" 버튼이 노출되지 않는가?

---

## 15. 기대 결과 (Expected Results)

### 성공 케이스 기대 결과

| 시나리오 | 페이지 상태 | 메시지/표시 |
|---------|-----------|-----------|
| **NOR-001** | 상품 목록 → 모달 → 장바구니 페이지 | 담기 성공 모달("View Cart" 버튼 포함), 장바구니 페이지에 Item/Description/Price/Quantity/Total 표시 |
| **NOR-002** | 상품 상세 → 모달 → 장바구니 페이지 | 담기 성공 모달, 지정한 수량으로 장바구니에 반영 |
| **NOR-003** | 장바구니 페이지 유지 | 삭제 후 해당 상품 행이 목록에서 사라짐 |
| **NOR-004** | 장바구니 페이지 유지 | 기존 행의 Quantity 증가, Total 재계산 |
| **NOR-005** | 장바구니 페이지 → 로그인 모달 | 로그인 안내 모달 노출 |

### 비정상 케이스 기대 결과

| 시나리오 | 페이지 상태 | 메시지/표시 | 확정 여부 |
|---------|-----------|-----------|---------|
| **ABN-001** | 장바구니 페이지 → 로그인 모달 | 로그인 안내 모달 노출, 결제 페이지 미이동 | 확정 |
| **ABN-002** | 장바구니 페이지 | "Cart is empty! Click here to buy products.", Proceed To Checkout 미노출 | 확정 |

---

## 16. 주요 검증 포인트 (Assertion Points)

### 장바구니 추가 검증

```
테스트 흐름:
1. 상품 목록(또는 상세) 페이지 방문
   → 검증: 담을 상품이 화면에 표시되는가?

2. "Add to cart" 버튼 클릭
   → 검증: 담기 성공 모달이 노출되는가? ("View Cart" 버튼 포함)

3. 모달의 "View Cart" 클릭 → 장바구니 페이지 이동
   → 검증: 담긴 상품이 목록에 노출되는가?
   → 검증: Description(상품명+카테고리), Price, Quantity가 예상값과 일치하는가?
   → 검증: Total = Price × Quantity 가 성립하는가?
```

### 상품 삭제 검증

```
테스트 흐름:
1. 장바구니 페이지에서 삭제 대상 상품 존재 확인

2. 삭제(X) 아이콘 클릭
   → 검증: 해당 상품 행이 목록에서 사라졌는가?
   → 검증: 남은 상품이 있다면 정상적으로 유지되는가?
```

### 결제 진입 시 로그인 모달 검증

```
테스트 흐름:
1. 비로그인 상태에서 장바구니에 상품이 담긴 상태 준비

2. "Proceed To Checkout" 클릭
   → 검증: 로그인 안내 모달이 노출되는가?
   → 검증: 결제 페이지로 이동하지 않는가?
```

### 프로그래밍적 검증 (pytest에서 - 예시, 실제 코드 아님)

```python
# 예시 (구현 시 실제 코드는 테스트 레이어에서 작성)
# ProductsPage는 상품 목록/상세 페이지의 담기 진입을 담당
# CartPage는 장바구니 페이지의 조회/삭제/결제 진입을 담당

# NOR-001: 상품 목록에서 장바구니 추가
products_page = ProductsPage(driver)
products_page.navigate_to_products()
products_page.add_product_to_cart_by_name("Blue Top")  # 메서드명/동작은 예시
products_page.click_view_cart_in_success_modal()

cart_page = CartPage(driver)
assert cart_page.is_product_in_cart("Blue Top") is True
assert cart_page.get_product_quantity("Blue Top") == 1
assert cart_page.get_product_total("Blue Top") == (
  cart_page.get_product_price("Blue Top") * cart_page.get_product_quantity("Blue Top")
)

# NOR-003: 상품 삭제
cart_page.navigate_to_cart()
assert cart_page.is_product_in_cart("Blue Top") is True
cart_page.delete_product("Blue Top")
assert cart_page.is_product_in_cart("Blue Top") is False

# NOR-004: 동일 상품 중복 담기 시 수량 증가
products_page.navigate_to_products()
products_page.add_product_to_cart_by_name("Blue Top")
products_page.add_product_to_cart_by_name("Blue Top")
cart_page.navigate_to_cart()
assert cart_page.get_cart_row_count_for_product("Blue Top") == 1
assert cart_page.get_product_quantity("Blue Top") == 2

# NOR-005 / ABN-001: 비로그인 상태에서 결제 진입 시 로그인 모달
cart_page.navigate_to_cart()
cart_page.click_proceed_to_checkout()
assert cart_page.is_login_modal_displayed() is True

# ABN-002: 빈 장바구니 상태 확인
# (별도 세션/신규 driver로 아무 상품도 담지 않은 상태에서 수행하는 것을 권장)
empty_cart_page = CartPage(driver)
empty_cart_page.navigate_to_cart()
assert empty_cart_page.is_empty_cart_message_displayed() is True
assert empty_cart_page.is_proceed_to_checkout_button_displayed() is False
```

---

## 17. 필요한 테스트 데이터

### 테스트 상품 정보 (확정, v1.3)

| 용도 | 상품명 | 가격 | 비고 |
|------|--------|------|------|
| **정상 담기 테스트 1 (목록/상세, 삭제, 중복 담기 등 공통)** | Men Tshirt | Rs. 400 | NOR-001, NOR-002, NOR-003, NOR-004의 기본 테스트 상품 |
| **정상 담기 테스트 2 (두 번째 상품 확인용)** | Printed Off Shoulder Top - White | Rs. 315 | 여러 상품이 담긴 상태에서의 목록 표시, 삭제 후 나머지 상품 유지 확인 등에 사용 |
| **결제 진입 테스트** | Men Tshirt | Rs. 400 | 비로그인 상태, 최소 1개 이상 담긴 상태에서 Proceed To Checkout 클릭 (NOR-005 / ABN-001) |

### 테스트 데이터 관리 방식

**방식 1: 환경변수 (.env 파일)**
```
TEST_PRODUCT_1_NAME=Men Tshirt
TEST_PRODUCT_1_PRICE=400
TEST_PRODUCT_2_NAME=Printed Off Shoulder Top - White
TEST_PRODUCT_2_PRICE=315
```

**방식 2: JSON 파일 (test_data/products.json)**
```json
{
  "cart_test_product_1": {
    "name": "Men Tshirt",
    "expected_price": 400
  },
  "cart_test_product_2": {
    "name": "Printed Off Shoulder Top - White",
    "expected_price": 315
  }
}
```

**방식 3: pytest Fixture (conftest.py)**
```python
@pytest.fixture
def cart_test_product():
  return {
    "name": "Men Tshirt",
    "expected_price": 400,
  }


@pytest.fixture
def cart_test_product_secondary():
  return {
    "name": "Printed Off Shoulder Top - White",
    "expected_price": 315,
  }
```

### 데이터 보호 규칙
- ❌ 민감정보(계정 정보 등)를 코드에 하드코딩하지 않음 (로그인 필요 시 login.md 테스트 계정 재사용 검토)
- ✅ 상품 정보는 민감정보가 아니므로 별도 마스킹 불필요
- ✅ 테스트 상품 정보는 외부 데이터 파일 또는 fixture로 관리

### 확인 필요
- 테스트 종료 후 장바구니에 담긴 상품을 정리(비우기)해야 하는지, 혹은 세션 종료로 자동 초기화되는지 여부

---

## 18. 다른 기능과의 의존성

### 이 기능이 의존하는 다른 기능

| 기능 | 의존 관계 | 설명 |
|------|---------|------|
| **상품 검색 / 상품 목록 조회 (Product Search)** | 선행 필수 | 장바구니에 담을 상품을 먼저 찾아야 함 (project-prd.md 8.1, 226-230행 근거). `docs/prd/features/product_search.md`는 아직 작성되지 않았으며, 작성 시 상품 목록/상세 페이지의 Page Object 책임 분리를 이 문서와 조율할 필요가 있음 (섹션 19 참고) |
| **로그인 (Login)** | 결제 진입 시점에만 필요 (확정) | 장바구니 담기/조회/삭제 자체는 로그인이 필요 없으며, "Proceed to Checkout" 클릭 시에만 로그인 안내 모달이 노출됨. login.md 섹션 18의 "로그인 후 기능 활용(일부 기능)" 서술은 이 결제 진입 제약을 가리키는 것으로 해석 가능함 |

### 이 기능을 필요로 하는 다른 기능

| 기능 | 의존 관계 | 설명 |
|------|---------|------|
| **결제 (Checkout)** | 후행 필수(프로세스 자체는 범위 밖) | 결제를 진행하려면 먼저 장바구니에 담긴 상품이 있어야 함. 결제 프로세스 자체는 project-prd.md 6.1(158행)에 따라 이번 PRD 및 MVP 범위에서 제외되나, 결제 진입 시도(로그인 모달 노출)까지는 이 문서 범위에 포함됨 |

### 의존성 흐름도

```
상품 검색 / 상품 목록 조회 (Product Search)
    ↓
장바구니 (Shopping Cart) ← [이 기능]
    ├─→ 장바구니 추가 (상품 목록/상세 페이지, 담기 성공 모달 경유)
    ├─→ 장바구니 조회 (담긴 상품 확인)
    ├─→ 장바구니 상품 삭제
    └─→ 동일 상품 중복 담기 시 수량 증가
    ↓
Proceed To Checkout 클릭
    ├─→ (비로그인) 로그인 안내 모달 노출 — 이 문서 범위
    └─→ (로그인) 결제 페이지 진행 — 범위 밖, 확인 필요, 향후 checkout PRD
```

---

## 19. 자동화 구현 시 고려사항

**안내**: 아래 코드는 구조 설명을 위한 예시(스텁)이며 실제 동작 코드는 아닙니다. **Locator 값은 예시이며, 실제 id/name/data-* 속성은 Page Object 구현 착수 시 사용자가 실시간으로 공유할 예정입니다.**

### Page Object 설계 방향

#### 페이지 책임 분리

| 화면 | 담당 Page 클래스 | 책임 |
|------|-----------------|------|
| 상품 목록/상세 페이지 | `ProductsPage` | 상품 목록 조회, "Add to cart" 버튼 클릭(목록/상세 양쪽), 담기 성공 모달의 "View Cart" 클릭 |
| 장바구니 페이지 | `CartPage` | 담긴 상품 목록(Item/Description/Price/Quantity/Total) 조회, 상품 삭제, 빈 장바구니 상태 확인, 결제 진입(로그인 모달 노출) 확인 |

**참고**: `ProductsPage`는 향후 작성될 상품 검색 기능 PRD(`docs/prd/features/product_search.md`)의 Page Object와 책임이 겹칠 수 있습니다. 이 문서의 `ProductsPage`는 "장바구니 담기 진입" 관점의 최소 책임만 다룹니다.

#### ProductsPage 클래스 구조 (예시 - 구현은 별도 작성)

```python
# pages/products_page.py 구조 (실제 코드 아님)
# 아래 Locator 값은 예시이며, 실제 값은 Page Object 구현 착수 시 사용자가 공유할 예정입니다.

class ProductsPage(BasePage):
  # Locator 정의 (상수) - 장바구니 담기 진입 관점의 최소 요소만 포함
  ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "a.add-to-cart")  # 예시, 실제 속성 확인 필요. 상품 목록 카드/상품 상세 페이지 양쪽에 동일하게 존재(확정 v1.4)
  VIEW_PRODUCT_LINK = (By.CSS_SELECTOR, "a.view-product")  # 예시, 실제 속성 확인 필요. "Add to cart"와 별개 버튼(확정 v1.3), 클릭 시 /product_details/{id}로 이동
  QUANTITY_INPUT = (By.ID, "quantity")  # 예시, 실제 속성 확인 필요. 상품 상세 페이지 전용 요소(확정 v1.4) - 상품 목록 페이지에는 수량 입력 UI가 존재하지 않음
  ADD_TO_CART_SUCCESS_MODAL = (By.CSS_SELECTOR, "div.modal-content")  # 모달 형태는 확정, 정확한 selector는 확인 필요
  VIEW_CART_LINK_IN_MODAL = (By.LINK_TEXT, "View Cart")  # 예시, 실제 속성 확인 필요
  CONTINUE_SHOPPING_BUTTON_IN_MODAL = (By.CSS_SELECTOR, "button.close-modal")  # 예시, 실제 속성 확인 필요. 클릭 시 모달만 닫히고 현재 페이지 유지(확정 v1.4)

  def navigate_to_products(self) -> None:
    """상품 목록 페이지로 이동"""
    pass

  def add_product_to_cart_by_name(self, product_name: str) -> None:
    """상품 목록에서 특정 상품명을 찾아 Add to cart 버튼 클릭
    (상품 목록 페이지에는 수량 입력 UI가 없으므로 항상 1개만 담김, 확정 v1.4)"""
    pass

  def open_product_detail(self, product_name: str) -> None:
    """특정 상품 카드의 "View Product" 버튼을 클릭하여 상품 상세 페이지
    (`/product_details/{id}`)로 이동 (Add to cart 버튼과는 별개의 버튼, 확정 v1.3)"""
    pass

  def enter_quantity(self, quantity: int) -> None:
    """담을 수량 입력. 수량 지정은 상품 상세 페이지에서만 가능하며(확정 v1.4),
    상품 목록 페이지에는 이 메서드가 사용할 입력 UI 자체가 존재하지 않음"""
    pass

  def click_add_to_cart_button(self) -> None:
    """Add to cart 버튼 클릭 (상품 목록 카드/상품 상세 페이지 양쪽 공통, 확정 v1.4)"""
    pass

  def is_add_to_cart_success_modal_displayed(self) -> bool:
    """담기 성공 모달 표시 여부 반환"""
    pass

  def click_view_cart_in_success_modal(self) -> None:
    """담기 성공 모달의 View Cart 버튼 클릭 → 장바구니 페이지로 이동"""
    pass

  def click_continue_shopping_in_success_modal(self) -> None:
    """담기 성공 모달의 Continue Shopping 버튼 클릭.
    클릭 시 모달이 닫히고, 현재 페이지(모달을 띄웠던 상품 목록 또는 상품 상세 페이지)가
    그대로 유지됨 (페이지 이동/새로고침 없음, 확정 v1.4)"""
    pass
```

#### CartPage 클래스 구조 (예시 - 구현은 별도 작성)

```python
# pages/cart_page.py 구조 (실제 코드 아님)
# 아래 Locator 값은 예시이며, 실제 값은 Page Object 구현 착수 시 사용자가 공유할 예정입니다.

class CartPage(BasePage):
  # Locator 정의 (상수)
  CART_ROW = (By.CSS_SELECTOR, "tr.cart-item")  # 예시, 실제 구조 확인 필요
  PRODUCT_DESCRIPTION_CELL = (By.CSS_SELECTOR, "td.product-description")
  PRODUCT_PRICE_CELL = (By.CSS_SELECTOR, "td.product-price")
  PRODUCT_QUANTITY_CELL = (By.CSS_SELECTOR, "td.product-quantity")  # 표시 전용 (변경 불가)
  PRODUCT_TOTAL_CELL = (By.CSS_SELECTOR, "td.product-total")
  DELETE_ICON = (By.CSS_SELECTOR, "a.cart-delete")  # 예시, 실제 속성 확인 필요
  EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, "p.empty-cart-message")  # 문구 확정, 정확한 요소는 확인 필요
  PROCEED_TO_CHECKOUT_BUTTON = (By.CSS_SELECTOR, "a.proceed-to-checkout")  # 예시
  LOGIN_MODAL = (By.CSS_SELECTOR, "div.login-modal")  # 예시, 실제 속성 확인 필요

  def navigate_to_cart(self) -> None:
    """장바구니 페이지(/view_cart)로 이동"""
    pass

  def is_product_in_cart(self, product_name: str) -> bool:
    """특정 상품이 장바구니 목록에 존재하는지 여부 반환"""
    pass

  def get_cart_row_count_for_product(self, product_name: str) -> int:
    """특정 상품명에 해당하는 행이 몇 개 존재하는지 반환 (중복 담기 시 행 미증가 검증용)"""
    pass

  def get_product_price(self, product_name: str) -> float:
    """특정 상품의 가격 조회"""
    pass

  def get_product_quantity(self, product_name: str) -> int:
    """특정 상품의 현재 수량 조회 (표시 전용 값)"""
    pass

  def get_product_total(self, product_name: str) -> float:
    """특정 상품 행의 Total(Price x Quantity) 조회"""
    pass

  def delete_product(self, product_name: str) -> None:
    """특정 상품 행의 삭제(X) 아이콘 클릭"""
    pass

  def is_empty_cart_message_displayed(self) -> bool:
    """빈 장바구니 안내 메시지("Cart is empty! Click here to buy products.") 표시 여부 반환"""
    pass

  def is_proceed_to_checkout_button_displayed(self) -> bool:
    """Proceed To Checkout 버튼 노출 여부 반환"""
    pass

  def click_proceed_to_checkout(self) -> None:
    """Proceed To Checkout 버튼 클릭"""
    pass

  def is_login_modal_displayed(self) -> bool:
    """비로그인 상태에서 결제 진입 시도 시 노출되는 로그인 안내 모달 표시 여부 반환"""
    pass
```

**참고 (v1.1 변경)**: v1.0의 `increase_quantity`, `decrease_quantity`, `set_quantity` 메서드는 장바구니 내 수량 변경 UI가 존재하지 않는 것으로 확인되어 제거되었습니다. 대신 `delete_product`, `get_cart_row_count_for_product`, `click_proceed_to_checkout`, `is_login_modal_displayed` 메서드가 신설되었습니다.

### Locator 선택 원칙

**우선순위** (CLAUDE.md 기준):
1. **id 속성** (가장 안정적)
2. **data-* 속성** (테스트용)
   ```python
   ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "a[data-qa='add-to-cart']")
   ```
3. **name 속성**
4. **안정적인 CSS Selector**
   ```python
   CART_ROW = (By.CSS_SELECTOR, "table.cart-table tbody tr")
   ```
5. **상대 XPath** (마지막 수단)
   ```python
   DELETE_ICON = (By.XPATH, "//tr[@data-product-id='1']//a[contains(@class, 'delete')]")
   ```

**금지**: Full XPath 절대 금지
```python
# 금지
DELETE_ICON = (By.XPATH, "/html/body/div[1]/div[3]/div/table/tbody/tr[5]/td[6]/a")
```

**안내**: 위 Locator는 모두 예시 값입니다. 실제 id/name/data-* 속성은 Page Object 구현 착수 시 사용자가 실시간으로 공유할 예정이며, 별도의 사전 개발자 도구 조사는 필요하지 않습니다.

### Wait 처리 전략

**명시적 Wait 사용** (time.sleep() 절대 금지):

```python
# 예시 - 실제 코드 아님
def click_add_to_cart_button(self):
  wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BUTTON))
  self.click(self.ADD_TO_CART_BUTTON)
  wait.until(EC.visibility_of_element_located(self.ADD_TO_CART_SUCCESS_MODAL))

def delete_product(self, product_name: str):
  row_locator = self._get_row_locator_by_product_name(product_name)
  delete_icon = self._get_delete_icon_locator(row_locator)
  wait.until(EC.element_to_be_clickable(delete_icon))
  self.click(delete_icon)
  # 삭제 클릭 시 페이지 리로드 없이 즉시 삭제됨 (확정, v1.3) - 해당 행이 DOM에서 사라질 때까지 대기
  wait.until(EC.invisibility_of_element_located(row_locator))

def click_proceed_to_checkout(self):
  wait.until(EC.element_to_be_clickable(self.PROCEED_TO_CHECKOUT_BUTTON))
  self.click(self.PROCEED_TO_CHECKOUT_BUTTON)
  wait.until(EC.visibility_of_element_located(self.LOGIN_MODAL))
```

### 동적 요소 처리

- **담기 성공 모달**: 모달이 나타날 때까지 대기(`visibility_of_element_located`) 후 "View Cart" 클릭
- **상품 삭제**: 삭제(X) 아이콘 클릭 후 별도 페이지 리로드 없이 해당 상품 행이 즉시 DOM에서 사라짐 (확정, v1.3). `invisibility_of_element_located`로 해당 행이 사라질 때까지 대기하는 방식을 사용
- **빈 장바구니 상태**: 상품 목록 테이블 자체가 DOM에 없을 수 있으므로, 존재 여부(presence)가 아니라 부재(absence) 확인 로직도 함께 고려 필요
- **로그인 모달**: "Proceed To Checkout" 클릭 후 모달이 나타날 때까지 대기

### 재사용 가능한 메서드

**BasePage에 추가할 공통 메서드**:

```python
# base_page.py (예시)

class BasePage:
  def wait_for_element_clickable(self, locator, timeout=10) -> WebElement:
    """요소가 클릭 가능해질 때까지 대기"""
    pass

  def wait_for_element_invisible(self, locator, timeout=10) -> bool:
    """요소가 DOM/화면에서 사라질 때까지 대기 (삭제 검증에 활용)"""
    pass

  def is_element_present(self, locator) -> bool:
    """요소가 DOM에 존재하는지 여부 (부재 확인에도 활용 가능)"""
    pass

  def get_element_text(self, locator) -> str:
    """요소 텍스트 조회"""
    pass

  def parse_price_text_to_number(self, price_text: str) -> float:
    """가격 텍스트(예: 'Rs. 500')에서 숫자만 추출하여 반환 (utils 배치 검토)"""
    pass
```

### 네트워크 지연 고려

- **타임아웃 설정**: 기본 10초, 페이지 로드는 20초 (프로젝트 PRD 기준)
- **재시도 로직**: 네트워크 오류 시 1회 재시도 (선택사항)

### 예시: 장바구니 테스트 구현 방향

```python
# tests/test_shopping_cart.py 구조 (실제 코드 아님)

def test_add_product_to_cart_from_products_page(driver, cart_test_product):
  products_page = ProductsPage(driver)
  products_page.navigate_to_products()
  products_page.add_product_to_cart_by_name(cart_test_product["name"])
  products_page.click_view_cart_in_success_modal()

  cart_page = CartPage(driver)
  assert cart_page.is_product_in_cart(cart_test_product["name"])
  assert cart_page.get_product_quantity(cart_test_product["name"]) == 1


def test_delete_product_from_cart(driver, cart_test_product):
  products_page = ProductsPage(driver)
  products_page.navigate_to_products()
  products_page.add_product_to_cart_by_name(cart_test_product["name"])
  products_page.click_view_cart_in_success_modal()

  cart_page = CartPage(driver)
  assert cart_page.is_product_in_cart(cart_test_product["name"])
  cart_page.delete_product(cart_test_product["name"])
  assert not cart_page.is_product_in_cart(cart_test_product["name"])


def test_duplicate_add_increases_quantity(driver, cart_test_product):
  products_page = ProductsPage(driver)
  products_page.navigate_to_products()
  products_page.add_product_to_cart_by_name(cart_test_product["name"])
  products_page.add_product_to_cart_by_name(cart_test_product["name"])

  cart_page = CartPage(driver)
  cart_page.navigate_to_cart()
  assert cart_page.get_cart_row_count_for_product(cart_test_product["name"]) == 1
  assert cart_page.get_product_quantity(cart_test_product["name"]) == 2


def test_guest_checkout_shows_login_modal(driver, cart_test_product):
  products_page = ProductsPage(driver)
  products_page.navigate_to_products()
  products_page.add_product_to_cart_by_name(cart_test_product["name"])
  products_page.click_view_cart_in_success_modal()

  cart_page = CartPage(driver)
  cart_page.click_proceed_to_checkout()
  assert cart_page.is_login_modal_displayed()


def test_empty_cart_shows_message(driver):
  # 새 세션/드라이버에서 아무 상품도 담지 않은 상태로 접근하는 것을 권장
  cart_page = CartPage(driver)
  cart_page.navigate_to_cart()
  assert cart_page.is_empty_cart_message_displayed()
  assert not cart_page.is_proceed_to_checkout_button_displayed()
```

---

## 20. 확인이 필요한 미확정 사항

### 여전히 확인이 필요한 항목 (v1.4 기준)

#### 화면/UI 관련
- "Add to cart" 버튼, "View Product" 버튼의 정확한 id, CSS 클래스, data-* 속성 (문구/기능/노출 위치 자체는 확정)

#### 기능/정책 관련
- 로그인 상태에서 "Proceed to Checkout" 클릭 시 이동하는 결제 페이지의 상세 동작 (향후 checkout PRD 영역)

#### 자동화 범위에서 제외하기로 결정된 항목 (참고, 섹션 12)
- 장바구니에 최대로 담을 수 있는 상품 개수 제한 여부: 사용자 판단에 따라 자동화 테스트 대상에서 제외 (실제 동작 미확인, v1.3)
- 장바구니 데이터의 저장 방식(세션/쿠키/DB): 사용자 판단에 따라 자동화 테스트 대상에서 제외 (실제 동작 미확인, v1.3)

#### UI 요소 Locator (개발 착수 시 공유 예정)
- "Add to cart" 버튼, "View Product" 버튼, 담기 성공 모달, 장바구니 상품 행, 삭제 아이콘, Proceed To Checkout 버튼, 로그인 모달 등의 실제 HTML id, name, CSS 클래스, data-* 속성은 Page Object 구현 착수 시 사용자가 실시간으로 공유할 예정입니다. 별도의 사전 개발자 도구 조사는 필요하지 않습니다.

### v1.4에서 해소/삭제된 항목 (참고)
- ~~"Add to cart" 버튼 노출 위치~~ → 상품 목록 페이지의 상품 카드, 상품 상세 페이지 양쪽 모두에 노출됨(기존 추정을 확정으로 전환)
- ~~담기 성공 모달 내 "Continue Shopping" 버튼 클릭 시 동작~~ → 모달이 닫히고 현재 페이지(모달을 띄웠던 페이지)가 그대로 유지됨(페이지 이동/새로고침 없음)으로 확정
- ~~"Product review platform" 버튼의 정확한 성격~~ → 사용자 판단에 따라 문서에서 다룰 필요가 없는 내용으로 결정되어, 확인 완료가 아닌 **문서 범위에서 전체 삭제** 처리(섹션 7, 9, 12, 14 등 관련 서술 모두 제거)
- ~~상품 목록 페이지에서의 수량 지정 가능 여부~~ → 상품 목록 페이지에는 수량 입력 UI가 없어 항상 1개만 담기며, 수량 지정은 상품 상세 페이지에서만 가능함으로 확정

### v1.3에서 해소된 항목 (참고)
- ~~테스트 상품 데이터~~ → Men Tshirt(Rs. 400), Printed Off Shoulder Top - White(Rs. 315)로 확정
- ~~상품 상세 페이지 URL~~ → `https://automationexercise.com/product_details/{id}` (id 1~8)로 확정
- ~~상품 상세 페이지 진입 경로~~ → 상품 카드의 "View Product" 버튼 클릭으로 확정
- ~~삭제(X) 아이콘 클릭 후 UI 반응~~ → 페이지 리로드 없이 즉시 삭제로 확정
- ~~로그인 모달 노출 시 URL 변경 여부~~ → 변경 없이 `/view_cart` 유지로 확정
- ~~페이지 전체 합계(총액) 표시 요소 존재 여부~~ → 존재하지 않음으로 확정
- ~~담기 성공 모달의 전체 문구 및 레이아웃~~ → 체크마크 아이콘/"Added!"/본문 문구/"View Cart" 링크/"Continue Shopping" 버튼으로 확정("Continue Shopping" 클릭 시 동작만 확인 필요로 잔존)
- ~~빈 장바구니 "here" 링크의 이동 대상~~ → 상품 목록 페이지(`/products`)로 확정
- ~~장바구니 데이터가 새로고침 후에도 유지되는지 여부~~ → 유지됨으로 확정

### v1.2에서 해소된 항목 (참고)
- ~~상품 목록 페이지 URL~~ → `product_search.md` 섹션 4의 확정 사실을 동기화하여 `https://automationexercise.com/products`로 확정

### v1.1에서 해소된 항목 (참고)
- ~~장바구니 페이지 URL~~ → `https://automationexercise.com/view_cart` (확정)
- ~~담기 성공 안내가 모달인지 토스트인지~~ → 모달로 확정
- ~~로그인 필요 여부~~ → 담기/조회/삭제는 불필요, 결제 진입 시에만 필요로 확정
- ~~장바구니 페이지 레이아웃/컬럼 구성~~ → Item/Description/Price/Quantity/Total로 확정
- ~~수량 변경 UI 형태~~ → 변경 불가(표시 전용)로 확정
- ~~헤더 장바구니 아이콘의 개수 표시 여부~~ → 미표시로 확정
- ~~빈 장바구니 안내 문구~~ → "Cart is empty! Click here to buy products." 로 확정
- ~~동일 상품 중복 담기 시 동작~~ → 기존 행 수량 증가로 확정
- ~~가격 표시 통화 단위~~ → "Rs."로 확정

---

## 21. 완료 조건

### 장바구니 기능 자동화 완료 기준

**정상 시나리오 완료**:
- ✅ NOR-001 (상품 목록에서 장바구니 추가): 테스트 PASS
- ✅ NOR-002 (상품 상세 페이지에서 장바구니 추가): 테스트 PASS
- ✅ NOR-003 (장바구니에서 상품 삭제): 테스트 PASS
- ✅ NOR-004 (동일 상품 중복 담기 시 수량 증가): 테스트 PASS
- ✅ NOR-005 (비로그인 상태에서 결제 진입 시 로그인 모달, 또는 ABN-001로 대체 구현): 테스트 PASS

**비정상 시나리오 완료**:
- ✅ ABN-001 (비로그인 결제 진입 제약 확인, NOR-005와 중복 구현 지양): 테스트 PASS
- ✅ ABN-002 (빈 장바구니 상태 확인): 테스트 PASS

**코드 품질 기준** (CLAUDE.md 준수):
- ✅ Page Object 설계: `ProductsPage`, `CartPage` 클래스 구현 완료
  - 모든 Locator가 상수/클래스 변수로 정의됨
  - 화면 조작 메서드와 값 조회 메서드만 포함
  - Assertion 없음 (Test 계층에서만 수행)
  - 수량 변경 관련 메서드(increase_quantity 등)는 포함하지 않음

- ✅ Locator 안정성:
  - id/data-*/name 속성 우선 사용
  - Full XPath 사용 안 함

- ✅ Wait 처리:
  - time.sleep() 사용 안 함
  - Explicit Wait (WebDriverWait) 사용

- ✅ 테스트 독립성:
  - 각 테스트가 단독 실행 가능 (각 테스트에서 필요한 상품 담기부터 수행)
  - 테스트 간 순서 의존성 없음

- ✅ 코딩 컨벤션:
  - 파일명: snake_case (products_page.py, cart_page.py, test_shopping_cart.py)
  - 클래스명: PascalCase + Page 접미사 (ProductsPage, CartPage)
  - 메서드명: snake_case, 동사로 시작 (add_product_to_cart_by_name, delete_product)
  - 테스트 함수명: test_ 접두사
  - 2칸 들여쓰기

**테스트 실행 기준**:
- ✅ 모든 테스트 PASS (성공률 100%)
- ✅ 실패 시 스크린샷 저장 확인
- ✅ pytest-html 리포트 생성 확인
- ✅ 로그 파일 생성 확인

**문서 기준**:
- ✅ 이 PRD(v1.1)가 완성되고 검토됨
- ✅ Page Object 구현 착수 시 Locator 공유 프로세스가 합의됨
- ✅ 섹션 20의 "확인이 필요한 항목"들이 실제 사이트 방문으로 추가 검증되고, 검증 결과에 따라 이 PRD가 추가 갱신됨

**배포 기준**:
- ✅ 모든 테스트 코드 완성
- ✅ 코드 리뷰 완료
- ✅ GitHub Actions CI/CD 테스트 통과
- ✅ 상품 검색 기능 PRD(`docs/prd/features/product_search.md`, 작성 예정)와의 Page Object 책임 분리 조율 완료

---

## 22. 다음 단계

### 즉시 작업 (이 PRD 이후)
1. **잔여 미확정 사항 확인**: 섹션 20에 남은 항목(로그인 상태에서 결제 페이지의 상세 동작 등)을 실제 사이트 방문으로 추가 확인. "Continue Shopping" 버튼 동작, 상품 목록 페이지 수량 지정 가능 여부는 v1.4에서 확정 완료되었으며, "Product review platform" 버튼 관련 내용은 문서 범위에서 삭제됨
2. **테스트 상품 데이터 확정 완료**: Men Tshirt(Rs. 400), Printed Off Shoulder Top - White(Rs. 315)로 확정되어 별도 준비 불필요 (섹션 17 참고)
3. **Locator 공유 대기**: Page Object 구현 착수 시 사용자로부터 각 UI 요소의 id, name, CSS 클래스, data-* 속성을 실시간으로 공유받기
4. **Page Object 구현**: ProductsPage, CartPage 클래스 작성 (pages/products_page.py, pages/cart_page.py)
5. **테스트 코드 작성**: 장바구니 기능 테스트 케이스 작성 (tests/test_shopping_cart.py)
6. **테스트 실행**: pytest를 사용하여 정상/비정상 시나리오(NOR-001~005, ABN-001~002) 테스트 실행
7. **오류 수정**: 실패한 테스트 분석 및 수정, 확인된 실제 동작에 맞춰 이 PRD 갱신

### 추후 작업 (이 기능 완료 후)
1. **상품 검색(Product Search) 기능 PRD 작성**: `docs/prd/features/product_search.md` 작성 및 이 문서의 ProductsPage와 책임 분리 조율
2. **결제(Checkout) 기능 PRD 작성 검토**: 로그인 이후 결제 프로세스 자동화 검토 시 별도 PRD 작성 (project-prd.md 18.1 근거)
3. **project-prd.md 정합성 검토(사용자 승인 필요)**: project-prd.md 5.1/8.2의 "장바구니 수량 변경" 서술과 이번 확인 결과("수량 변경 불가", "삭제 가능") 간 불일치를 사용자에게 보고하고, 승인 시 project-prd.md 갱신 진행
4. **통합 테스트**: 상품 검색 → 장바구니 담기 → 조회/삭제 → 결제 진입 시도의 전체 흐름 테스트 구성

---

## 23. 참고 자료

### 관련 문서
- **프로젝트 전체 PRD**: `docs/prd/project-prd.md`
- **로그인 기능 PRD**: `docs/prd/features/login.md`
- **회원가입 기능 PRD**: `docs/prd/features/signup.md`
- **로그아웃 기능 PRD**: `docs/prd/features/logout.md`
- **프로젝트 개발 규칙**: `CLAUDE.md`
- **기능별 PRD 작성 가이드**: `docs/PRD_PROMPT.md` (있는 경우, 현재 미존재 확인)

### 외부 참고
- **Automation Exercise 공식**: https://automationexercise.com/
- **Selenium 문서**: https://selenium.dev/documentation/
- **pytest 문서**: https://docs.pytest.org/

### 버전 관리
- **이 PRD 버전**: 1.4
- **작성일**: 2026-07-22
- **최종 수정일**: 2026-07-23
- **최종 검토일**: (예정)
- **최종 승인일**: (예정)

**변경 이력**:

- **v1.4 (2026-07-23)**: 사용자가 실제 사이트를 확인하여 제공한 4가지 확정/결정 사항을 반영. **[확정된 사실 반영]** (1) "Add to cart" 버튼이 상품 목록 페이지의 상품 카드와 상품 상세 페이지 양쪽 모두에 노출된다는 사실을 기존 추정에서 확정으로 전환(섹션 4, 7, 19). (2) 담기 성공 안내 모달의 "Continue Shopping" 버튼 클릭 시 모달이 닫히고 현재 페이지(모달을 띄웠던 상품 목록 또는 상품 상세 페이지)가 그대로 유지됨(페이지 이동/새로고침 없음)을 확정(섹션 4, 7, 19, 20). (3) 상품 목록 페이지에는 수량 입력 UI가 없어 "Add to cart" 클릭 시 항상 1개만 담기고, 수량 지정은 상품 상세 페이지에서만 가능함을 확정(섹션 4, 7, 8 흐름1/흐름2, 10 CART-REQ-002 관련, 13 NOR-001/NOR-002, 19). **[범위 삭제]** "Product review platform" 버튼 관련 서술을 사용자 판단에 따라 문서 전체에서 삭제(섹션 7의 빈 장바구니 UI 요소 표, 섹션 9 예외 흐름, 섹션 12 자동화 제외 범위, 섹션 14 ABN-002, 섹션 15 비정상 케이스 기대 결과, 섹션 20). 이 항목은 "확인 완료"가 아니라 "문서 범위에서 제외"로 처리함. 빈 장바구니 안내 문구 및 "here" 링크 관련 내용은 그대로 유지함. 이번에 다루지 않은 다른 "확인 필요" 항목(예: "Add to cart" 버튼 등의 정확한 Locator 값)은 변경하지 않음. 전부 문서(PRD) 수정이며 Selenium/pytest 실제 동작 코드는 추가하지 않음.
- **v1.3 (2026-07-23)**: 사용자가 실제 사이트를 확인하여 제공한 확정 사실을 반영. **[확정된 사실 반영]** 테스트 상품 데이터(Men Tshirt Rs.400, Printed Off Shoulder Top - White Rs.315, 섹션 17), 상품 상세 페이지 URL 패턴(`https://automationexercise.com/product_details/{id}`, id 1~8, 섹션 4) 및 "View Product" 버튼을 통한 진입 경로(섹션 4, 19), 삭제(X) 아이콘 클릭 시 페이지 리로드 없이 즉시 해당 행이 사라지는 동작(섹션 7, 8, 10, 19), 비로그인 상태에서 로그인 모달 노출 시 URL이 `/view_cart`로 유지되는 동작(섹션 8, 9, 10, 13, 14), 장바구니 페이지에 행별 Total 외 페이지 전체 합계 표시 요소가 존재하지 않는다는 사실(섹션 7, 10), 담기 성공 모달의 정확한 레이아웃(체크마크 아이콘/"Added!"/본문 문구/파란색 "View Cart" 링크/초록색 "Continue Shopping" 버튼, 섹션 7), 빈 장바구니 "here" 링크가 상품 목록 페이지(`/products`)로 이동한다는 사실(섹션 7, 9), 장바구니 데이터가 새로고침 후에도 유지된다는 사실(CART-REQ-010 확정, 섹션 10)을 모두 반영함. **[스코프 결정]** 장바구니 최대 담기 개수 제한과 데이터 저장 방식(세션/쿠키/DB)은 실제 동작이 확인되지 않았으나 사용자 판단에 따라 자동화 테스트 대상에서 제외하기로 결정되어, 섹션 12(자동화 제외 범위)로 이동함(섹션 20 참고). 전부 문서(PRD) 수정이며 Selenium/pytest 실제 동작 코드는 추가하지 않음(기존 스텁 수준 예시만 구체화).
- **v1.2 (2026-07-23)**: 문서 간 정합성 동기화. `product_search.md` 섹션 4에 이미 확정되어 있던 상품 목록 페이지 URL(`https://automationexercise.com/products`)을 이 문서(섹션 4, 7, 20, 22)에 반영. 새로운 사실 확인은 없으며, 기존 문서 간 불일치를 해소한 순수 동기화 변경임. 상품 상세 페이지 URL은 여전히 확인 필요 상태로 유지됨.
- **v1.1 (2026-07-23)**: 사용자가 실제 사이트(스크린샷)를 확인하여 제공한 사실 정보를 반영한 개정.
  - **확정된 사실 반영**: 장바구니 페이지 URL(`/view_cart`), 진입 경로(헤더 "Cart" 및 담기 성공 모달의 "View Cart"), 담기 성공 안내가 모달 형태이고 "View Cart" 버튼을 포함함, 페이지 레이아웃(breadcrumb, Proceed To Checkout 버튼 위치, Item/Description/Price/Quantity/Total 컬럼 구성), 통화 단위("Rs."), 헤더 장바구니 아이콘에 개수 미표시, 빈 장바구니 안내 문구("Cart is empty! Click here to buy products." + "Product review platform" 버튼) 및 이 상태에서 Proceed To Checkout 미노출, 동일 상품 중복 담기 시 기존 행 수량 증가, 비로그인 상태에서 Proceed to Checkout 클릭 시 로그인 안내 모달 노출
  - **[핵심 변경] 수량 변경 기능 제거**: 실제 사이트에는 장바구니 내 수량을 직접 변경하는 UI가 존재하지 않음이 확인되어(Quantity는 표시 전용), v1.0의 CART-REQ-005(수량 변경), NOR-003(수량 변경 후 총액 재계산), ABN-001(수량을 0 이하로 변경 시도), Page Object의 `increase_quantity`/`decrease_quantity`/`set_quantity` 메서드를 모두 제거하거나 대체함
  - **[핵심 변경] 상품 삭제 기능을 자동화 범위에 신규 포함**: v1.0에서는 project-prd.md 8.2 Phase 2 목표에 명시되지 않았다는 이유로 자동화 제외 범위에 있었으나, 실제 사이트 확인 결과 삭제가 장바구니의 핵심 동작임이 확인되어 이번 개정에서 포함으로 전환(NOR-003, CART-REQ-006 신설). project-prd.md와의 범위 불일치는 이 변경 이력에 근거로 남기며, project-prd.md 자체의 수정은 사용자 승인 후 별도 진행 예정
  - **[핵심 변경] 결제 진입 시 로그인 요구를 정상/비정상 시나리오로 신규 추가**: 비로그인 상태에서 "Proceed to Checkout" 클릭 시 로그인 안내 모달이 노출되는 것을 확인하여 NOR-005 및 ABN-001로 반영. 결제 프로세스 자체(로그인 이후 흐름)는 여전히 범위 밖
  - **동일 상품 중복 담기 동작 확정**: project-prd.md 19.1에서 미확정이었던 사항으로, 별도 행이 아닌 기존 행의 수량 증가로 확정하여 NOR-004 신설
  - **여전히 확인 필요로 남긴 항목**: 빈 장바구니 "here" 링크의 정확한 이동 대상, "Product review platform" 버튼의 성격, 상품 목록/상세 페이지의 정확한 URL과 Add to cart 버튼 locator, 페이지 전체 합계(총액) 표시 요소의 존재 여부, 로그인 이후 결제 페이지의 상세 동작, 장바구니 최대 담기 개수 제한, 저장 방식(세션/쿠키/DB) 등(섹션 20 참고)

- **v1.0 (2026-07-22)**: 최초 작성. project-prd.md 7.1/8.2/9.1/5.2를 근거로 장바구니 추가(상품 목록/상세 페이지), 장바구니 조회(상품 목록/총액), 수량 변경(재계산) 중심으로 범위 확정. 결제(Checkout) 및 장바구니 삭제 기능은 이번 범위에서 제외. 실제 사이트 스크린샷 확인이 이루어지지 않아 URL, UI 요소 문구/형태, 로그인 필요 여부 등 다수 항목을 "확인 필요"로 명시하고 project-prd.md 근거 서술만 사실로 반영.

---

**작성자**: Automation Testing Framework Lead
**최종 검토자**: (예정)
**승인 상태**: 개정판 (검토 대기 중)

이 문서는 장바구니 기능의 자동화 테스트 작성 시 기준이 되는 요구사항 명세입니다.
실제 구현 과정에서 새로운 정보(특히 실제 사이트 방문을 통한 확인)가 발견되면 이 문서를 업데이트합니다.
