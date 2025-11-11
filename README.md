# 📊 Live Polling - 실시간 질문 & 답변 시스템

실시간으로 질문에 대한 답변을 받고 화면에 표시하는 인터랙티브 웹 애플리케이션입니다.

## ✨ 주요 기능

- 📺 **3개의 디스플레이 화면**: 각 질문별로 독립된 디스플레이
- 📱 **QR 코드 스캔**: 모바일에서 QR 코드를 스캔하여 즉시 답변
- 🔄 **실시간 업데이트**: 2초마다 polling하여 새로운 답변 표시
- 💬 **예쁜 UI**: 그라데이션 배경과 카드 형태의 답변 표시
- ⚡ **빠른 응답**: Supabase를 사용한 효율적인 데이터 관리

## 🎯 질문 목록

1. **오늘 가장 기억에 남는 순간은?**
2. **이 자리에서 배운 것 한 가지는?**
3. **한 단어로 오늘을 표현한다면?**

## 🚀 빠른 시작

### 1. Supabase 프로젝트 설정

1. [Supabase](https://supabase.com)에 가입하고 새 프로젝트 생성
2. **SQL Editor**에서 다음 코드 실행:

```sql
-- 답변 테이블 생성
CREATE TABLE answers (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  question_id INTEGER NOT NULL,
  answer_text TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Realtime 활성화 (선택사항)
ALTER PUBLICATION supabase_realtime ADD TABLE answers;

-- 인덱스 생성 (성능 향상)
CREATE INDEX idx_answers_question_id ON answers(question_id);
CREATE INDEX idx_answers_created_at ON answers(created_at DESC);
```

3. **Project Settings > API**에서 다음 값 복사:
   - Project URL
   - anon/public key

### 2. 설정 파일 업데이트

`supabase-config.js` 파일을 열고 다음 값을 업데이트:

```javascript
const SUPABASE_URL = 'YOUR_PROJECT_URL'; // 복사한 URL
const SUPABASE_ANON_KEY = 'YOUR_ANON_KEY'; // 복사한 anon key
```

### 3. 로컬에서 실행

```bash
# 저장소 클론
git clone https://github.com/chosundeveloper/live-polling.git
cd live-polling

# 간단한 웹 서버 실행 (선택사항)
python -m http.server 8000
# 또는
npx serve

# 브라우저에서 열기
open http://localhost:8000
```

또는 그냥 `index.html`을 브라우저에서 직접 열어도 됩니다!

## 📁 프로젝트 구조

```
live-polling/
├── index.html              # 메인 페이지 (질문 선택)
├── display.html            # 디스플레이 화면 (질문 + QR + 실시간 답변)
├── answer.html             # 답변 제출 페이지 (모바일)
├── style.css               # 전체 스타일링
├── supabase-config.js      # Supabase 설정 및 API 함수
└── README.md               # 프로젝트 문서
```

## 🎮 사용 방법

### 발표자/주최자:

1. `index.html` 페이지 열기
2. 원하는 질문의 **"📺 디스플레이 보기"** 클릭
3. 화면에 질문과 QR 코드가 표시됨
4. 이 화면을 프로젝터/대형 화면에 표시

### 참가자:

1. 화면에 표시된 QR 코드를 스마트폰으로 스캔
2. 자동으로 답변 페이지로 이동
3. 답변 입력 후 제출
4. 실시간으로 디스플레이 화면에 답변이 나타남!

### 디스플레이 미리보기 모드

답변 데이터가 없어도 `display.html?mock=1` 주소로 접속하면 질문마다 100개의 샘플 답변이 자동 생성됩니다. 행사 전에 화면 배치나 가독성을 점검할 때 활용하세요.

## 🔄 실시간 업데이트 방식

이 프로젝트는 **Live Polling** 방식을 사용합니다:

- 디스플레이 화면이 2초마다 Supabase에 새로운 답변을 요청
- 새로운 답변이 있으면 자동으로 화면에 추가
- 간단하고 안정적인 방식

## 🌐 배포

### GitHub Pages로 배포 (자동)

이 저장소는 GitHub Actions를 통해 자동으로 배포됩니다:

1. `main` 브랜치에 코드 푸시
2. GitHub Actions가 자동으로 GitHub Pages에 배포
3. `https://chosundeveloper.github.io/live-polling/` 에서 접속 가능

## 🛠️ 기술 스택

- **Frontend**: Vanilla JavaScript (프레임워크 없음!)
- **Backend**: Supabase (PostgreSQL)
- **Styling**: CSS3 (Gradient, Flexbox, Grid)
- **QR Code**: qrcode.js
- **Deployment**: GitHub Pages
- **CI/CD**: GitHub Actions

## 📊 Live Polling vs 다른 방식

| 방식 | 장점 | 단점 |
|------|------|------|
| **Polling** ✅ | 간단, 안정적, 호환성 좋음 | 약간의 지연 가능 |
| WebSocket | 진짜 실시간 | 복잡함, 연결 관리 필요 |
| SSE | 서버→클라이언트 효율적 | 단방향만 가능 |
| Long Polling | 지연 적음 | 서버 부하 높음 |

## 🎨 커스터마이징

### 질문 변경하기

`supabase-config.js` 파일에서 `QUESTIONS` 배열 수정:

```javascript
const QUESTIONS = [
    {
        id: 1,
        question: "새로운 질문?",
        placeholder: "답변 힌트...",
        color: "#667eea"
    },
    // ...
];
```

### 색상 변경하기

`style.css` 파일에서 그라데이션 색상 변경:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Polling 간격 변경

`display.html`에서 `setInterval` 값 수정 (밀리초):

```javascript
this.pollingInterval = setInterval(() => {
    this.loadAnswers();
}, 2000); // 2000 = 2초
```

## 🐛 문제 해결

**Q: 답변이 제출되지 않아요**
- Supabase URL과 Key가 올바른지 확인
- 브라우저 콘솔에서 에러 메시지 확인
- Supabase 대시보드에서 테이블이 생성되었는지 확인

**Q: QR 코드가 안 보여요**
- `qrcode.js` 라이브러리가 로드되었는지 확인
- 인터넷 연결 확인 (CDN 사용)

**Q: 실시간 업데이트가 안 돼요**
- 브라우저 콘솔에서 에러 확인
- Supabase 데이터베이스 연결 상태 확인

## 📝 라이선스

MIT License

## 👨‍💻 제작

Made with ❤️ by [chosundeveloper](https://github.com/chosundeveloper)

## 🙏 기여

이슈와 PR은 언제나 환영합니다!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
