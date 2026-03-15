# REQUIREMENTS.md

Date: 2026-03-10
Project: camel-gemini-openclaw-orchestrator
Requirement Version: v1.0

## 1) Purpose
coopAI(CAMEL) 기반 협업 오케스트레이터를 GPT CLI 중심으로 운영해, 코딩 워크플로우를 단순화하고 재현 가능한 결과를 얻는다.

## 2) Scope
- 포함:
  - Gemini Chief + 3팀(각 3 worker + 1 lead) 구조 유지
  - OpenClaw 실행 위임 경로 안정화
  - 안정성 테스트 체계 수립/자동화
- 제외(현재):
  - GUI 대시보드 고도화
  - 대규모 분산 환경 확장

## 3) Functional Requirements
1. 작업 계약(Task Contract) 표준화
2. 실행 큐/순차 모드 기본화(락 충돌 회피)
3. 재시도 + timeout + backoff 정책
4. 팀/워커 결과 검증 게이트
5. 체크포인트(PROGRESS.md) 저장 및 재개
6. 구조화 로그(JSONL) 저장
7. E2E 안정성 진단 스크립트 제공

## 4) Non-Functional Requirements
- 안정성: 장시간 실행 중 치명적 중단 최소화
- 추적성: 실행 단계별 원인 추적 가능
- 재현성: 동일 입력에 유사한 실행 흐름 보장
- 비용효율: 불필요한 장문/반복 호출 억제

## 5) Success Criteria
- 기본 시나리오 10회 연속 완료
- 락/타임아웃 발생 시 자동 복구 또는 명확한 실패 리포트
- 최종 보고서에 팀별 결과/근거 포함

## 6) Open Decisions
- 병렬 모드 재도입 조건(임계치)
- 세션 분리 전략(팀별/워커별)
- 운영 모드 분류(dev/stable/prod)
