import { useLocation, useNavigate } from "react-router-dom"
import React, { useState, useMemo } from "react"

import { submitExam } from "../api/exams"

import type {
    ExamResponse,
    ExamSubmitAnswer, ExamResult, ExamQuestion
} from "../types/exams"

// Хелпер для перемешивания массива
const shuffleArray = <T,>(array: T[]): T[] => [...array].sort(() => Math.random() - 0.5);

export default function ExamRunner() {

    const location = useLocation()
    const navigate = useNavigate()
    const exam = location.state as ExamResponse;

    const [index, setIndex] = useState(0);
    const [inputValue, setInputValue] = useState("");
    const [answers, setAnswers] = useState<ExamSubmitAnswer[]>([]);
    const [finished, setFinished] = useState(false);
    const [result, setResult] = useState<ExamResult | null>(null);

    const [showAnswer, setShowAnswer] = useState(false);

    if (!exam || !exam.questions) return <div>No exam data</div>;

    const question: ExamQuestion = exam.questions[index];

    // Перемешиваем опции только когда меняется индекс вопроса
    const shuffledOptions = useMemo(() => {
        return question.options ? shuffleArray(question.options) : [];
    }, [index, question.options]);

    const handleAnswer = async (userAnswer: string) => {
        // Логика проверки: предполагаем, что в исходном массиве правильный ответ всегда под индексом 0
        const isCorrect =
            question.type === "multiple_choice"
            ? userAnswer === question.options?.[0]
            : (question.type === "flashcard_forward" || question.type === "flashcard_reverse")
                ? userAnswer === "true"
                : question.type === "scramble"
                    ? userAnswer.trim().toLowerCase() === question.options?.[0].toLowerCase()
                    : true;

        const newAnswer: ExamSubmitAnswer = {
            word_id: question.word_id,
            is_correct: isCorrect
        };

        const updatedAnswers = [...answers, newAnswer];
        setAnswers(updatedAnswers);
        setInputValue("");
        setShowAnswer(false);

        if (index < exam.questions.length - 1) {
            setIndex(prev => prev + 1);
        } else {
            await finishExam(updatedAnswers);
        }
    };

    const finishExam = async (finalAnswers: ExamSubmitAnswer[]) => {
        try {
            const res = await submitExam(exam.examid, { answers: finalAnswers });
            setResult(res);
            setFinished(true);
        } catch (error) {
            alert("Error submitting exam");
        }
    };

    function renderQuestionContent() {
        const questionText = (
            <div style={{ margin: '20px 0', fontSize: '1.4rem', fontWeight: 'bold' }}>
                {question.question}
            </div>
        );

        const content = (() => {
        switch (question.type) {
            case "multiple_choice":
                return (
                    <div style={styles.optionsContainer}>
                        {shuffledOptions.map(opt => (
                            <button
                                key={opt}
                                style={styles.optionButton}
                                onClick={() => handleAnswer(opt)}
                            >
                                {opt}
                            </button>
                        ))}
                    </div>
                );
            case "scramble":
                return (
                    <div style={styles.scrambleContainer}>
                        <input
                            style={styles.input}
                            value={inputValue}
                            placeholder="Type answer..."
                            onChange={e => setInputValue(e.target.value)}
                            onKeyDown={e => e.key === "Enter" && handleAnswer(inputValue)}
                        />
                        <button style={styles.primaryButton} onClick={() => handleAnswer(inputValue)}>
                            Submit
                        </button>
                    </div>
                );
            case "flashcard_forward":
            case "flashcard_reverse":
                return (
                    <div style={styles.flashcardContainer}>
                        {!showAnswer ? (
                            <button
                                style={styles.primaryButton}
                                onClick={() => setShowAnswer(true)}
                            >
                                Show answer
                            </button>
                        ) : (
                            <>
                                <div style={styles.answerText}>{question.options?.[0]}</div>
                                <div style={styles.buttonGroup}>
                                    <button
                                        style={styles.correctButton}
                                        onClick={() => handleAnswer("true")}
                                    >
                                        Correct
                                    </button>
                                    <button
                                        style={styles.wrongButton}
                                        onClick={() => handleAnswer("false")}
                                    >
                                        No correct
                                    </button>
                                </div>
                            </>
                        )}
                    </div>
                );
            default:
                return null;
        }
    })();

        return (
            <>
                {questionText}
                {content}
            </>
        );
    }

    if (finished && result) {
        return (
            <div style={styles.container}>
                <h2>Exam Results</h2>
                <div style={{ fontSize: '1.2rem', marginBottom: '20px' }}>
                    <strong>Score: {result.score}%</strong> | Level: {result.estimatedlevel}
                </div>

                <div style={styles.resultsList}>
                    <h3>Детализация по вопросам:</h3>
                    {exam.questions.map((q, i) => {
                        const answer = answers.find(a => a.word_id === q.word_id);
                        return (
                            <div key={i} style={{
                                padding: '10px',
                                borderBottom: '1px solid #eee',
                                color: answer?.is_correct ? '#28a745' : '#dc3545'
                            }}>
                                <strong>{q.question}</strong> — {q.options?.[0]}
                                {answer?.is_correct ? ' (✅)' : ' (❌)'}
                            </div>
                        );
                    })}
                </div>
                <button style={{ marginTop: '20px' }} onClick={() => navigate("/")}>Go Home</button>
            </div>
        );
    }

    return (
        <div style={styles.container}>
            <div style={styles.progress}>
                Question {index + 1} / {exam.questions.length}
            </div>
            <div style={styles.questionText}>
                {question.question}
            </div>
            {renderQuestionContent()}
        </div>
    );
}

const styles: Record<string, React.CSSProperties> = {

    container:{
        maxWidth:600,
        margin:"0 auto",
        padding:20,
        textAlign:"center"
    },

    question:{
        fontSize:24,
        marginBottom:30
    },

    optionsContainer:{
        display:"flex",
        flexDirection:"column",
        gap:12
    },

    optionButton:{
        padding:"12px 20px",
        fontSize:16,
        borderRadius:8,
        border:"1px solid #ccc",
        cursor:"pointer"
    },

    flashcardContainer:{
        marginTop:20
    },

    scrambleContainer:{
        display:"flex",
        flexDirection:"column",
        gap:12,
        alignItems:"center"
    },

    input:{
        padding:10,
        fontSize:16,
        width:200
    },
    correctButton: {
        padding: '10px 20px',
        backgroundColor: '#28a745',
        color: 'white',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        fontWeight: 'bold' as const
    },
    wrongButton: {
        padding: '10px 20px',
        backgroundColor: '#dc3545',
        color: 'white',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        fontWeight: 'bold' as const
    },
    primaryButton:{
        padding:"12px 20px",
        borderRadius:8,
        border:"none",
        background:"#007bff",
        color:"#fff",
        cursor:"pointer"
    }

}

