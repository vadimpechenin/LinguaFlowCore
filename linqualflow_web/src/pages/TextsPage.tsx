import React, { useState, ChangeEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    loadText, submitText, analyzeText
} from "../api/texts";
import type {TextAnalyzeRequest, TextAnalyzeResponse, TextRequest} from "../types/texts";

type ViewMode = 'MENU' | 'SUBMIT' | 'LOAD' | 'ANALYZE';

export default function TextsPage() {
    const navigate = useNavigate();
    const [mode, setMode] = useState<ViewMode>('MENU');

    // Поля формы
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [language, setLanguage] = useState('en'); // Пользователь может менять
    const [analysisResult, setAnalysisResult] = useState<TextAnalyzeResponse | null>(null);
    const [status, setStatus] = useState('');

    // Парсинг файла (Аналог вашего Python кода)
    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (event) => {
            const fullText = event.target?.result as string;
            const blocks = fullText.split("=== TEXT ===");

            let foundAny = false; // Флаг для отслеживания успеха

            for (const block of blocks) {
                const trimmedBlock = block.trim();
                if (!trimmedBlock || !trimmedBlock.includes("=== END ===")) continue;

                const lines = trimmedBlock.split(/\r?\n/);
                let foundTitle = "";
                const bodyLines: string[] = [];

                for (const line of lines) {
                    const cleanLine = line.trim();
                    if (cleanLine.startsWith("Title:")) {
                        foundTitle = cleanLine.replace("Title:", "").trim();
                        continue;
                    }
                    if (cleanLine.startsWith("Author:") || cleanLine.includes("=== END ===")) {
                        continue;
                    }
                    if (cleanLine) {
                        bodyLines.push(cleanLine);
                    }
                }

                if (foundTitle && bodyLines.length > 0) {
                    setTitle(foundTitle);
                    setContent(bodyLines.join("\n"));
                    setStatus("Файл успешно прочитан");
                    foundAny = true;
                    break;
                }
            }

            if (!foundAny) {
                setStatus("Ошибка: проверьте наличие 'Title:' и '=== END ==='");
            }
        };

        reader.readAsText(file, "UTF-8");
    };

    const handleSubmitText = async () => {
        try {
            const payload: TextRequest = { title, content, language };
            await submitText(payload);
            alert("Успешно отправлено!");
            setMode('MENU');
        } catch (e) {
            alert("Ошибка при отправке");
        }
    };

    // 1. Метод загрузки текста
    const handleLoadText = async () => {
        try {
            setStatus('Загрузка...');
            const data = await loadText(title);
            setContent(data.content);
            setStatus(`Текст "${data.title}" найден.`);
        } catch (e) {
            setContent('');
            setStatus('Ошибка: текст не найден.');
        }
    };

    // 2. Метод анализа текста
    const handleAnalyzeText = async () => {
        try {
            setStatus('Анализируем...');
            const payload: TextAnalyzeRequest = { title};
            const data = await analyzeText(payload);
            setAnalysisResult(data);
            setStatus('Анализ завершен успешно.');
        } catch (e) {
            setAnalysisResult(null);
            setStatus('Ошибка при анализе текста.');
        }
    };

    const reset = () => {
        setMode('MENU');
        setTitle('');
        setContent('');
        setStatus('');
    };

    return (
        <div style={{ padding: '20px' }}>
            {mode === 'MENU' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', width: '250px' }}>
                    <button onClick={() => setMode('SUBMIT')}>Загрузить файл (.txt)</button>
                    <button onClick={() => setMode('LOAD')}>Прочитать текст</button>
                    <button onClick={() => setMode('ANALYZE')}>Анализировать текст</button>
                    <hr />
                    <button onClick={() => navigate('/')}>В главное меню</button>
                </div>
            )}

            {mode === 'SUBMIT' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxWidth: '500px' }}>
                    <h3>Загрузка и парсинг файла</h3>
                    <input type="file" accept=".txt" onChange={handleFileChange} />

                    <label>Язык текста:</label>
                    <input value={language} onChange={e => setLanguage(e.target.value)} placeholder="Напр: en" />

                    <label>Заголовок (из файла):</label>
                    <input value={title} readOnly style={{ background: '#f0f0f0' }} />

                    <label>Контент (превью):</label>
                    <textarea value={content} readOnly rows={5} style={{ background: '#f0f0f0' }} />

                    <p style={{ color: 'gray', fontSize: '0.9em' }}>{status}</p>

                    <button disabled={!title || !content} onClick={handleSubmitText}>Отправить на сервер</button>
                    <button onClick={reset}>Назад</button>
                </div>
            )}

            {/* ЭКРАН LOAD (Прочитать текст) */}
            {mode === 'LOAD' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '15px', maxWidth: '600px' }}>
                    <h3>Просмотр текста</h3>
                    <div style={{ display: 'flex', gap: '10px' }}>
                        <input
                            placeholder="Введите название текста"
                            value={title}
                            onChange={e => setTitle(e.target.value)}
                            style={{ flex: 1, padding: '5px' }}
                        />
                        <button onClick={handleLoadText}>Отправить запрос</button>
                    </div>

                    {content && (
                        <div style={{ marginTop: '10px' }}>
                            <label>Содержимое:</label>
                            <textarea
                                value={content}
                                readOnly
                                rows={10}
                                style={{ width: '100%', marginTop: '5px', padding: '10px', background: '#f9f9f9' }}
                            />
                        </div>
                    )}
                    <p style={{ color: status.includes('Ошибка') ? 'red' : 'blue' }}>{status}</p>
                    <button onClick={reset} style={{ alignSelf: 'flex-start' }}>Назад</button>
                </div>
            )}

            {/* ЭКРАН ANALYZE (Анализ) */}
            {mode === 'ANALYZE' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '15px', maxWidth: '600px' }}>
                    <h3>Анализ сложности текста</h3>
                    <div style={{ display: 'flex', gap: '10px' }}>
                        <input
                            placeholder="Название текста для анализа"
                            value={title}
                            onChange={e => setTitle(e.target.value)}
                            style={{ flex: 1, padding: '5px' }}
                        />
                        <button onClick={handleAnalyzeText}>Запустить анализ</button>
                    </div>

                    {analysisResult && (
                        <div style={{ background: '#f0f4f8', padding: '15px', borderRadius: '8px', marginTop: '10px' }}>
                            <h4 style={{ margin: '0 0 10px 0' }}>Результаты для: {analysisResult.title}</h4>
                            <p><b>Уровень:</b> {analysisResult.level}</p>
                            <p><b>Незнакомых слов:</b> {analysisResult.unknown_words}</p>
                            <p><b>Покрытие:</b> {analysisResult.coveragepercent}%</p>

                            <p><b>Рекомендованные слова:</b></p>
                            <ul style={{
                                display: 'grid',
                                gridTemplateColumns: '1fr 1fr',
                                gap: '5px',
                                paddingLeft: '20px'
                            }}>
                                {analysisResult.recommended_words.map((word, index) => (
                                    <li key={index} style={{ color: '#2c3e50' }}>{word}</li>
                                ))}
                            </ul>
                        </div>
                    )}
                    <p style={{ color: status.includes('Ошибка') ? 'red' : 'blue' }}>{status}</p>
                    <button onClick={reset} style={{ alignSelf: 'flex-start' }}>Назад</button>
                </div>
            )}

            {/* Блок SUBMIT (остается как был в предыдущем шаге) */}
            {/* ... */}
        </div>
    );
}