# 작업 메모 (Live Polling Display)

이 문서는 `display.html`(Keyword Canvas)과 `display-mindmap.html`(Mindmap Canvas)의 레이아웃, 인터랙션, 튜닝 포인트를 한눈에 정리합니다. 변경 전 참고용으로 항상 최신 상태를 유지하세요.

## 1. Keyword Canvas (`display.html`)

### 1.1 레이아웃 구성
- **헤더**: 좌·우 화살표(`prevQuestionBtn`, `nextQuestionBtn`)로 질문을 탐색하며, 중앙에는 질문 텍스트(`conceptQuestion`)와 진행 카운터(`questionCounter`)가 표시됩니다.
- **메인 클라우드**: `.concept-words` 레이어가 전체 뷰포트를 차지하고, 모든 단어 스팬이 absolute 좌표(좌/상 + `translate(-50%, -50%)`)로 배치됩니다.
- **푸터**: 좌측에는 참여 링크 및 QR 코드(`conceptLink`, `conceptQrCode`), 우측에는 누적 답변/업데이트 시각(`conceptTotal`, `conceptUpdated`)과 `모의` 버튼이 있습니다.

### 1.2 인터랙션 & 데이터 흐름
- `navigateToQuestion(index, { force })`가 전체 화면을 리셋하고 질문 별 메타(QR, 컬러 테마)를 업데이트합니다.
- `모의` 버튼 또는 `?mock=1` 파라미터가 `isMockMode`를 토글하며, mock 모드일 때 `startRealtimeSimulation()`이 0.5초 간격으로 답변을 하나씩 추가합니다.
- 실제 데이터 모드는 현재 Supabase 요청 부분이 비활성화되어 있으며, `startRealDataPolling()` 자리에 연동 로직을 추가하면 됩니다.

### 1.3 애니메이션/시뮬레이션 파라미터
- 생성 직후 단어는 화면 중앙에서 스폰되고 `phase: 'intro'` 상태로 유지됩니다.
- 주요 상수: `INTRO_GROWTH_RATE`, `INTRO_HOLD_PROGRESS`, `INTRO_HOLD_TRAVEL_RATIO`, `INTRO_BLOOM_JITTER`, `INTRO_CHASE_BASE`, `INTRO_CHASE_SCALE`, `OUTWARD_DRIFT_FORCE`, `TARGET_ATTRACTION_FORCE`, `RADIAL_FORCE`, `MAX_PARTICLE_SPEED`, `MIN_SEPARATION`.
- `INTRO_HOLD_PROGRESS` 만큼은 반경을 0으로 고정하여 “중앙에서 머문 뒤” 퍼지는 연출을 만듭니다.
- `INTRO_HOLD_TRAVEL_RATIO`는 홀드 구간 동안 이동할 최대 반경 비율(기본 20%)을 정해, 갑작스럽지 않게 천천히 외곽으로 확장됩니다.
- `INTRO_CHASE_BASE`와 `INTRO_CHASE_SCALE`은 인트로 동안 목표 스파이럴 좌표를 추적하는 속도를 조절해 “움직이며 확대되는” 느낌을 만듭니다.
- 인트로 종료 후(`phase: 'idle'`)에는 충돌 보정과 감쇠가 적용되어 단어 간 간격과 링 반경(`ringRadius`)이 유지됩니다.

### 1.4 튜닝 체크리스트
1. `display.html?mock=1`을 띄워 `모의` 버튼을 여러 번 눌러도 항상 중앙 → 스파이럴 순으로 퍼지는지 확인합니다.
2. Prev/Next 버튼을 반복해서 눌렀을 때 이전 입자가 잔존하지 않는지, 질문 카운터가 정상인지 검증합니다.
3. 풀 HD / 4K 해상도에서 `.concept-words`가 뷰포트 전체를 활용하는지, edge padding(10%) 범위가 과하지 않은지 확인합니다.

## 2. Mindmap Canvas (`display-mindmap.html`)

### 2.1 레이아웃 구성
- **헤더**: 상단의 셀렉트(`questionSelect`)로 질문을 고르고, 상태 배지(`conceptStatus`)와 인라인 설명(“답변에서 추출된 단어만을 미니멀하게 배치”)가 함께 노출됩니다.
- **메인 레이어**: Keyword Canvas와 동일하게 `.concept-words`에 모든 단어가 absolute 포지셔닝으로 배치됩니다.
- **푸터**: 참여 링크, 누적/업데이트 카운터, `모의`/`재배치` 버튼이 있고 QR 대신 간략 링크만 제공됩니다.

### 2.2 배치 알고리즘
- `wordPositions` 맵이 각 단어의 좌표/폭/높이를 기억해 다음 렌더 사이클에서도 겹침을 최소화합니다.
- `findWordPosition()`은 골든 앵글 스파이럴을 따라 후보 좌표를 생성하고, `WORD_PADDING`(16px) 여백을 준 뒤 충돌 검사를 통과하면 확정합니다.
- 새 단어는 visibility를 숨긴 뒤 실제 크기를 측정하여 위치를 잡고, 이후 `translate(-50%, -50%) scale(...)`로 살짝 크기 변화를 줍니다.
- `재배치` 버튼은 `wordPositions.clear()` 후 기존 단어를 다시 배치해 빠르게 다른 구성을 확인하도록 돕습니다.

### 2.3 Mock/실데이터 흐름
- `?mock=1` 또는 `모의` 버튼으로 300개의 샘플 답변을 만들며, 각 답변은 prefix/keyword/suffix 조합으로 랜덤 생성됩니다.
- `getAnswers(question.id, 300)` 호출부에 Supabase 쿼리가 연결되어 있으므로, 실제 연동 시 인증 키와 RLS 정책을 체크해야 합니다.
- 질문을 바꾸면 `wordPositions.clear()`와 `wordsLayer.innerHTML = ''`가 즉시 실행되어 이전 배치를 제거합니다.

## 3. 공통 옵션 & 참고사항
- `?question=N`: 두 화면 모두 동일하게 1-based 질문 ID를 지정할 수 있습니다.
- `?mock=1`: 초기 진입부터 mock 모드를 활성화합니다. UI 버튼과 URL 파라미터가 항상 동기화되도록 class 토글을 함께 처리합니다.
- 스타일은 `style.css`의 `.concept-*` 네이밍을 공유하므로, 한 화면에 추가한 스타일이 다른 화면에도 영향을 줄 수 있습니다.

## 4. 다음 액션 아이디어
1. Mindmap에도 인트로 페이드/확산 모션을 추가해 두 화면의 무드가 통일되도록 하기.
2. 실데이터 노출 시 금칙어 필터 또는 길이 제한을 둘지 정책 확정.
3. Supabase 실시간 채널을 붙여 폴링(2초)을 대체하고, 네트워크 에러 시 폴백 전략 마련.
4. 운영 중 프리셋(색상/폰트/모션) 세트를 만들어 행사별 테마 변경을 쉽게 할 수 있는 토글 추가.
