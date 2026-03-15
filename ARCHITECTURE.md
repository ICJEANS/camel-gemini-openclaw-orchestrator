# ARCHITECTURE.md

Date: 2026-03-10
Project: camel-gemini-openclaw-orchestrator
Architecture Version: v1.0

## 1) System Architecture (text)

```text
User Goal
  -> Gemini Chief (Planner/Supervisor)
      -> Team Lead A (architecture)
          -> Worker A1/A2/A3 -> GPT CLI Bridge
      -> Team Lead B (implementation)
          -> Worker B1/B2/B3 -> GPT CLI Bridge
      -> Team Lead C (verification)
          -> Worker C1/C2/C3 -> GPT CLI Bridge

GPT CLI Bridge
  -> openai api chat.completions.create
  -> result collection

Critic/Validator
  -> acceptance criteria check
  -> retry or escalate

Reporter
  -> final merged report + artifacts
```

## 2) Runtime Stability Flow

```text
[Task Intake]
  -> [Task Contract Validate]
  -> [Queue Dispatch (default: sequential)]
  -> [Worker Execute]
  -> [Timeout/Retry/Backoff]
  -> [Result Validate]
  -> [Checkpoint Save]
  -> [Final Merge]
```

## 3) Module Responsibilities
- planner.py: 상위 계획/요약
- orchestrator.py: 팀/워커 실행 순서, 흐름 제어
- openclaw_bridge.py: OpenClaw 위임 호출
- validator (planned): 결과 품질/완료 조건 검증
- telemetry (planned): JSONL 로그/메트릭

## 4) Failure Handling
1. 첫 실패: 축소 범위로 1회 재시도
2. 연속 실패: 단계/에러스니펫/대안 A-B 보고
3. 락/경합 감지: 즉시 순차 모드 고정

## 5) Stability Test Matrix
- S1: 단건 실행 성공
- S2: 3팀 순차 실행 성공
- S3: timeout 유도 후 복구 검증
- S4: 세션 경합 상황에서 graceful fail 검증
- S5: 10회 반복 회귀 테스트

## 6) Artifacts
- PROGRESS.md: 체크포인트
- logs/run-*.jsonl: 구조화 로그
- reports/summary-*.md: 최종 요약
