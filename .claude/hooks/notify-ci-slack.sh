#!/usr/bin/env bash
# git push 이후 GitHub Actions(test.yml) 실행 결과를 대기하여 Slack으로 성공/실패 알림 전송
# PostToolUse(Bash) Hook에서 async로 호출됨: stdin으로 tool 실행 정보를 JSON으로 받음
set -u

INPUT=$(cat)
COMMAND=$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty')

# git push 명령이 아니면 아무 것도 하지 않음
printf '%s' "$COMMAND" | grep -Eq '(^|[;&|]) *git push' || exit 0

# Slack Webhook URL이 없으면 알림을 보낼 수 없으므로 종료
if [ -z "${SLACK_WEBHOOK_URL:-}" ]; then
  exit 0
fi

command -v gh >/dev/null 2>&1 || exit 0
command -v jq >/dev/null 2>&1 || exit 0

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
cd "$REPO_ROOT" || exit 0

BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
SHA=$(git rev-parse HEAD 2>/dev/null)
[ -n "$BRANCH" ] && [ -n "$SHA" ] || exit 0

# 워크플로우 실행이 큐에 등록될 때까지 대기 (최대 2분30초)
RUN_ID=""
for _ in $(seq 1 30); do
  RUN_ID=$(gh run list --workflow=test.yml --branch="$BRANCH" --limit=5 \
    --json databaseId,headSha -q ".[] | select(.headSha==\"$SHA\") | .databaseId" 2>/dev/null | head -n1)
  [ -n "$RUN_ID" ] && break
  sleep 5
done

[ -n "$RUN_ID" ] || exit 0

# 워크플로우가 끝날 때까지 대기 (gh 기본 폴링)
gh run watch "$RUN_ID" --exit-status >/dev/null 2>&1
EXIT_CODE=$?

CONCLUSION=$(gh run view "$RUN_ID" --json conclusion -q '.conclusion' 2>/dev/null)
RUN_URL=$(gh run view "$RUN_ID" --json url -q '.url' 2>/dev/null)

if [ "$EXIT_CODE" -eq 0 ]; then
  STATUS_TEXT="성공 :white_check_mark:"
else
  STATUS_TEXT="실패 :x:"
fi

MESSAGE=$(printf '*CI/CD %s*\n브랜치: `%s`\n커밋: `%s`\n결과: %s\n<%s|워크플로우 결과 보기>' \
  "$STATUS_TEXT" "$BRANCH" "${SHA:0:7}" "${CONCLUSION:-unknown}" "$RUN_URL")

PAYLOAD=$(jq -n --arg text "$MESSAGE" '{text: $text}')

curl -s -X POST -H 'Content-type: application/json' --data "$PAYLOAD" "$SLACK_WEBHOOK_URL" >/dev/null
