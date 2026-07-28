# 화면과 무관한 공통 유틸리티 함수를 이곳에 추가한다 (2회 이상 반복되는 로직만)
import re
import uuid


def generate_random_email(prefix: str = "test") -> str:
  """회원가입 테스트용 고유 이메일 생성 (실행마다 값이 달라 실사이트 중복 등록과 무관해짐)"""
  return f"{prefix}_{uuid.uuid4().hex[:10]}@example.com"


def parse_price_text(price_text: str) -> int:
  """'Rs. 500' 형식 텍스트에서 숫자만 추출"""
  digits = re.sub(r"[^0-9]", "", price_text)
  return int(digits)


def normalize_whitespace(text: str) -> str:
  """실제 사이트에서 광고 스크립트가 상품명 사이에 삽입하는 여분의 공백을 정리"""
  return " ".join(text.split())
