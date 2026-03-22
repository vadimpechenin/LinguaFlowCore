import { useLocation, useNavigate } from "react-router-dom"
import React, { useState, useMemo } from "react"
import {styles} from "../components/Styles"
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

    const [usedIndices, setUsedIndices] = useState<number[]>([]);

    const cleanWord = useMemo(() => {
        if (question.type === "scramble") {
            // Убираем "Unscramble:", двоеточия и пробелы в начале
            return question.question.replace(/^unscramble:\s*/i, "").trim();
        }
        return "";
    }, [index, question.question, question.type]);

    // Перемешиваем буквы только при смене вопроса
    const scrambledLetters = useMemo(() => {
        if (question.type === "scramble" && cleanWord) {
            setUsedIndices([]); // Сброс при смене вопроса
            return shuffleArray(cleanWord.split(""));
        }
        return [];
    }, [cleanWord]);

    const handleLetterClick = (letter: string, charIndex: number) => {
        if (usedIndices.includes(charIndex)) return; // Нельзя нажать дважды
        setInputValue(prev => prev + letter);
        setUsedIndices(prev => [...prev, charIndex]);
    };

    const resetScramble = () => {
        setInputValue("");
        setUsedIndices([]);
    };
    const handleBackspace = () => {
        if (usedIndices.length === 0) return;

        // 1. Убираем последний добавленный индекс из списка использованных
        const newUsedIndices = [...usedIndices];
        newUsedIndices.pop(); // удаляем последний элемент
        setUsedIndices(newUsedIndices);

        // 2. Убираем последний символ из инпута
        setInputValue(prev => prev.slice(0, -1));
    };

    // Перемешиваем опции только когда меняется индекс вопроса
    const shuffledOptions = useMemo(() => {
        return question.options ? shuffleArray(question.options) : [];
    }, [index, question.options]);

    const handleAnswer = async (userAnswer: string) => {
        // Логика проверки: предполагаем, что в исходном массиве правильный ответ всегда под индексом 0
        //if (question.type === "scramble"){
        //    console.log(userAnswer.trim().toLowerCase())
        //    console.log(question.options?.[0].toLowerCase())
        //}
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
                {question.type === "scramble"
                    ? "Unscramble:"
                    : question.question}
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
                    <div style={styles.scrambleWrapper}>
                        <div style={styles.lettersGrid}>
                            {scrambledLetters.map((char, charIndex) => {
                                const isUsed = usedIndices.includes(charIndex);
                                return (
                                    <button
                                        key={charIndex}
                                        disabled={isUsed}
                                        style={{
                                            ...styles.letterTile,
                                            opacity: isUsed ? 0.3 : 1,
                                            cursor: isUsed ? "default" : "pointer",
                                            transform: isUsed ? "scale(0.9)" : "scale(1)"
                                        }}
                                        onClick={() => handleLetterClick(char, charIndex)}
                                    >
                                        {char}
                                    </button>
                                );
                            })}
                        </div>

                        {/* Поле ввода (сделаем только для чтения или оставим ввод) */}
                        <div style={{ display: 'flex', gap: '10px', alignItems: 'center', marginTop: '20px' }}>
                            <input
                                style={{ ...styles.input, flex: 1 }}
                                value={inputValue}
                                placeholder="Собираем слово..."
                                readOnly
                            />
                            {/* Кнопка стирания последней буквы */}
                            <button
                                onClick={handleBackspace}
                                disabled={inputValue.length === 0}
                                style={styles.backspaceButton}
                            >
                                ⌫
                            </button>
                        </div>
                        <div style={{ marginTop: '20px', display: 'flex', gap: '10px', justifyContent: 'center' }}>
                                <button
                                    style={styles.secondaryButton}
                                    onClick={resetScramble}
                                >
                                    ✕
                                </button>
                            <button
                                style={styles.primaryButton}
                                onClick={() => handleAnswer(inputValue)}
                            >
                                Submit
                            </button>
                        </div>
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
                    <h3>Exam results:</h3>
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
                <button style={{ marginTop: '20px' }} onClick={() => navigate("/")}>Back to menu</button>
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
