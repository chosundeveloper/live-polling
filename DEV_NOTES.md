# 작업 메모 (Live Polling Display)

## Particle Canvas (`display.html`)
- 새 단어는 항상 화면 중앙 근처에서 생성되며 `phase: intro` 동안 황금각 스파이럴 타깃까지 서서히 이동합니다.
- `INTRO_GROWTH_RATE`, `OUTWARD_DRIFT_FORCE`, `TARGET_ATTRACTION_FORCE`, `RADIAL_FORCE` 값을 조정해 퍼지는 속도와 흔들림을 미세하게 제어할 수 있습니다.
- 인트로 종료 후(`phase: idle`)에는 저속 드리프트와 충돌 보정이 적용되어 단어 간 간격이 유지됩니다.
- 애니메이션 확인 시 `display.html?mock=1`을 사용하고, 필요하면 `QUESTIONS` 상수에서 기본 문항을 교체합니다.

## Mindmap Canvas (`display-mindmap.html`)
- `wordPositions` 맵은 각 단어의 좌표와 크기를 기억하여 새로고침 없이도 겹침을 최대한 회피합니다.
- `findWordPosition`은 골든 앵글 스파이럴로 후보 좌표를 생성하고, `WORD_PADDING`만큼 여백을 둔 뒤 배치합니다.
- `MOCK` 버튼 혹은 `?mock=1` 파라미터로 300개의 샘플 답변을 생성해 배치 품질을 빠르게 확인할 수 있습니다.
- 질문을 바꿀 때는 `wordPositions.clear()`로 상태를 초기화한 뒤 `loadAnswers()`를 호출해 새 데이터에 맞춘 레이아웃을 구성합니다.

## 다음 액션 아이디어
1. Mindmap 단어에도 간단한 페이드/이동 인트로 애니메이션을 적용해 시각적 통일감을 줄 것.
2. 실 데이터 연동 시 답변 텍스트를 그대로 노출할지, 금칙어 필터를 둘지 정책 결정.
3. 장기적으로는 Supabase 실시간 채널을 붙여 폴링 간격(2초)을 줄이고 즉시 반영을 검토.
