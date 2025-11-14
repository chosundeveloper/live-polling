// Supabase Configuration
// TODO: Supabase 프로젝트 생성 후 아래 값들을 업데이트하세요
//
// 설정 방법:
// 1. https://supabase.com 에서 로그인
// 2. New Project 생성
// 3. Project Settings > API 에서 아래 값들 복사
// 4. SQL Editor에서 테이블 생성 (아래 SQL 실행)

/*
-- Supabase SQL Editor에서 실행할 코드:

CREATE TABLE answers (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  question_id INTEGER NOT NULL,
  answer_text TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Realtime 활성화
ALTER PUBLICATION supabase_realtime ADD TABLE answers;

-- 인덱스 생성 (성능 향상)
CREATE INDEX idx_answers_question_id ON answers(question_id);
CREATE INDEX idx_answers_created_at ON answers(created_at DESC);
*/

const SUPABASE_URL = 'https://ykdmlgrlpwkqyyemcefz.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlrZG1sZ3JscHdrcXl5ZW1jZWZ6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEyNDI3NTMsImV4cCI6MjA3NjgxODc1M30.pRfCXTTXZHfp5Fohy4LLrHNujqds4Tir3pSMQIZLCvI';

// Supabase 클라이언트 초기화
const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// 질문 데이터
const QUESTIONS = [
    {
        id: 1,
        question: "오늘 가장 기억에 남는 순간은?",
        placeholder: "예: 친구와 나눈 대화, 배운 새로운 것...",
        color: "#667eea",
        type: "text"
    },
    {
        id: 2,
        question: "이 자리에서 배운 것 한 가지는?",
        placeholder: "예: 새로운 기술, 인사이트, 경험...",
        color: "#f093fb",
        type: "text"
    },
    {
        id: 3,
        question: "한 단어로 오늘을 표현한다면?",
        placeholder: "예: 행복, 성장, 도전...",
        color: "#4facfe",
        type: "text"
    }
];

// 답변 제출
async function submitAnswer(questionId, answerText) {
    try {
        const { data, error } = await supabase
            .from('answers')
            .insert([
                { question_id: questionId, answer_text: answerText }
            ]);

        if (error) throw error;
        return { success: true, data };
    } catch (error) {
        console.error('Error submitting answer:', error);
        return { success: false, error: error.message };
    }
}

// 답변 가져오기
async function getAnswers(questionId, limit = 50) {
    try {
        const { data, error } = await supabase
            .from('answers')
            .select('*')
            .eq('question_id', questionId)
            .order('created_at', { ascending: false })
            .limit(limit);

        if (error) throw error;
        return { success: true, data };
    } catch (error) {
        console.error('Error fetching answers:', error);
        return { success: false, error: error.message };
    }
}

// Realtime 구독 (선택사항 - polling 대신 사용 가능)
function subscribeToAnswers(questionId, callback) {
    const subscription = supabase
        .channel(`answers-${questionId}`)
        .on(
            'postgres_changes',
            {
                event: 'INSERT',
                schema: 'public',
                table: 'answers',
                filter: `question_id=eq.${questionId}`
            },
            callback
        )
        .subscribe();

    return subscription;
}
