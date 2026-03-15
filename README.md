# camel-gemini-openclaw-orchestrator

3-3-3 하이브리드 멀티에이전트 오케스트레이터.

- 총괄: **Gemini Chief 1명**
- 도메인 팀: **3팀**
- 팀 구성: 각 팀당 **Team Lead 1명 + Worker 3명**
- 실행 계층: Worker는 실제 작업을 **OpenClaw**로 위임

## 구조

- Team A (architecture): 3 workers + 1 lead
- Team B (implementation): 3 workers + 1 lead
- Team C (verification): 3 workers + 1 lead
- Gemini Chief: 팀별 결과 통합/최종 결정

## 설치

```bash
cd projects/camel-gemini-openclaw-orchestrator
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
# Gemini 연동 시
pip install -e .[gemini]
```

## 실행

### 1) 드라이런(기본)

```bash
python3 -m src.main "새 기능 설계하고 검증 계획 수립"
```

### 2) OpenClaw 실 실행

```bash
python3 -m src.main "테스트 자동화 파이프라인 구축" --live --session-key "agent:main:telegram:direct:8709111146"
```

### 3) GPT-mini Router + Skill/MCP 선택 + OpenClaw 실행 + CAMEL 리뷰 (v2.0)

```bash
# dry-run
python3 -m src.coop_pipeline "quick-web-demo를 검수하고 개선안 보고"

# live
python3 -m src.coop_pipeline "quick-web-demo를 검수하고 개선안 보고" --live

# config override
python3 -m src.coop_pipeline "목표" --config configs/pipeline_config.json --model gpt-4.1-mini --retries 1
```

## 환경변수

`.env.example` 참고.

- `GEMINI_API_KEY`: CAMEL 총괄(Planner/Summarizer) 모델 호출용
- `OPENCLAW_SESSION_KEY`: OpenClaw 위임 대상 세션키(선택)

## 주의

- 총괄/계획은 CAMEL(Gemini), 실제 부작용 작업은 OpenClaw로 분리.
- 파괴적 작업은 승인 정책을 별도로 두는 것을 권장.
