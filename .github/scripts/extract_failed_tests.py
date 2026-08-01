"""pytest 출력 로그에서 실패한 테스트별 위치(파일:줄)와 예외 클래스명을 추출해
Slack 알림용 텍스트로 출력한다. CI(.github/workflows/test.yml)의
"Extract failed test summary" 스텝에서만 사용된다.
"""

import re
import sys

LOG_PATH = "reports/pytest_output.log"

HEADER_RE = re.compile(r"^_{5,} (.+?) _{5,}$", re.MULTILINE)
LOCATION_RE = re.compile(r"^(tests/\S+\.py):(\d+):", re.MULTILINE)
EXCEPTION_RE = re.compile(r"^E\s+(\S+):", re.MULTILINE)


def build_entries(content: str) -> list[str]:
  headers = list(HEADER_RE.finditer(content))
  summary_idx = content.find("short test summary info")
  if summary_idx == -1:
    summary_idx = len(content)

  entries = []
  for i, header in enumerate(headers):
    start = header.end()
    end = headers[i + 1].start() if i + 1 < len(headers) else summary_idx
    block = content[start:end]

    location_match = LOCATION_RE.search(block)
    if location_match:
      location = f'{location_match.group(1)} ( "{location_match.group(2)}줄" )'
    else:
      location = "위치 확인 불가"

    exception_match = EXCEPTION_RE.search(block)
    exception_name = (
      exception_match.group(1).rsplit(".", 1)[-1] if exception_match else "알 수 없음"
    )

    entries.append(f"FAILED\n실패위치 : {location}\n실패원인 : {exception_name}")

  return entries


def main() -> None:
  try:
    with open(LOG_PATH, encoding="utf-8", errors="replace") as f:
      content = f.read()
    entries = build_entries(content)
    output = "\n\n".join(entries) if entries else "(실패한 테스트를 로그에서 특정하지 못함 - Actions 로그 확인 필요)"
  except OSError:
    output = "(pytest 출력 로그를 찾지 못함 - Actions 로그 확인 필요)"

  print(output)


if __name__ == "__main__":
  sys.exit(main())
