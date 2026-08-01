"""SLACK_WEBHOOK_URL 시크릿 등록 후 GitHub Actions Slack 실패 알림 동작을 검증하기 위한 임시 테스트.

검증 완료 후 이 파일은 삭제됩니다.
"""


def test_deliberately_fail_for_slack_notification_check() -> None:
  assert False, "Slack 실패 알림 동작 검증을 위해 의도적으로 실패시킨 테스트입니다."
