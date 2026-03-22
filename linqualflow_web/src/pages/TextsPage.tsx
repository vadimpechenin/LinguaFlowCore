import React, { useState, ChangeEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    loadText, submitText, analyzeText
} from "../api/texts";
import type {TextAnalyzeRequest, TextAnalyzeResponse, TextRequest} from "../types/texts";
import {backButtonStyle, buttonStyle} from "../components/Styles";
import {ArrowLeft} from 'lucide-react';

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
                    setStatus("The file was read successfully");
                    foundAny = true;
                    break;
                }
            }

            if (!foundAny) {
                setStatus("Error: Check availability 'Title:' and '=== END ==='");
            }
        };

        reader.readAsText(file, "UTF-8");
    };

    const handleSubmitText = async () => {
        try {
            const payload: TextRequest = { title, content, language };
            await submitText(payload);
            alert("Successfully sent!");
            setMode('MENU');
        } catch (e) {
            alert("Error sending");
        }
    };

    // 1. Метод загрузки текста
    const handleLoadText = async () => {
        try {
            setStatus('Loading...');
            const data = await loadText(title);
            setContent(data.content);
            setStatus(`"${data.title}" text found.`);
        } catch (e) {
            setContent('');
            setStatus('Error: text not found.');
        }
    };

    // 2. Метод анализа текста
    const handleAnalyzeText = async () => {
        try {
            setStatus('Analysis in progress...');
            const payload: TextAnalyzeRequest = { title};
            const data = await analyzeText(payload);
            setAnalysisResult(data);
            setStatus('The analysis was completed successfully.');
        } catch (e) {
            setAnalysisResult(null);
            setStatus('Error while parsing text.');
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
                    <button
                        onClick={() => navigate('/')}
                        style={backButtonStyle}
                    >
                        <ArrowLeft size={20} />
                        {"Back to Dashboard"}
                    </button>
                    <hr />
                    <button onClick={() => setMode('SUBMIT')} style={buttonStyle}>
                        <span>Load file (.txt)</span>
                    </button>
                    <button onClick={() => setMode('LOAD')} style={buttonStyle}>
                        <span>Read text</span>
                        </button>
                    <button onClick={() => setMode('ANALYZE')} style={buttonStyle}>
                        <span>Analyze text</span>
                        </button>
                </div>
            )}

            {mode === 'SUBMIT' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxWidth: '500px' }}>
                    <h3>Downloading and parsing a file</h3>
                    {/* Скрываем стандартный инпут через ref */}
                    <input
                        type="file"
                        id="file-upload"
                        style={{ display: 'none' }}
                        onChange={handleFileChange}
                    />

                    {/* Рисуем свою кнопку, которая кликает по скрытому инпуту */}
                    <button
                        style={buttonStyle}
                        onClick={() => document.getElementById('file-upload')?.click()}
                    >
                        Select file .txt
                    </button>

                    {/* Показываем имя файла, если он выбран (опционально) */}
                    {status && <p style={{ color: 'gray', fontSize: '0.9em' }}>{status}</p>}
                    <label>Text language:</label>
                    <input value={language} onChange={e => setLanguage(e.target.value)} placeholder="Напр: en" />

                    <label>Header (from file):</label>
                    <input value={title} readOnly style={{ background: '#f0f0f0' }} />

                    <label>Content (preview):</label>
                    <textarea value={content} readOnly rows={5} style={{ background: '#f0f0f0' }} />

                    <p style={{ color: 'gray', fontSize: '0.9em' }}>{status}</p>

                    <button disabled={!title || !content} onClick={handleSubmitText}>Send to server</button>
                    <button onClick={reset}>Back</button>
                </div>
            )}

            {/* ЭКРАН LOAD (Прочитать текст) */}
            {mode === 'LOAD' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '15px', maxWidth: '600px' }}>
                    <h3>View text</h3>
                    <div style={{ display: 'flex', gap: '10px' }}>
                        <input
                            placeholder="Enter the title of the text"
                            value={title}
                            onChange={e => setTitle(e.target.value)}
                            style={{ flex: 1, padding: '5px' }}
                        />
                        <button onClick={handleLoadText}>Send a request</button>
                    </div>

                    {content && (
                        <div style={{ marginTop: '10px' }}>
                            <label>Content:</label>
                            <textarea
                                value={content}
                                readOnly
                                rows={10}
                                style={{ width: '100%', marginTop: '5px', padding: '10px', background: '#f9f9f9' }}
                            />
                        </div>
                    )}
                    <p style={{ color: status.includes('Ошибка') ? 'red' : 'blue' }}>{status}</p>
                    <button onClick={reset} style={{ alignSelf: 'flex-start' }}>Back</button>
                </div>
            )}

            {/* ЭКРАН ANALYZE (Анализ) */}
            {mode === 'ANALYZE' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '15px', maxWidth: '600px' }}>
                    <h3>Text complexity analysis</h3>
                    <div style={{ display: 'flex', gap: '10px' }}>
                        <input
                            placeholder="Title of the text to be analyzed"
                            value={title}
                            onChange={e => setTitle(e.target.value)}
                            style={{ flex: 1, padding: '5px' }}
                        />
                        <button onClick={handleAnalyzeText}>Run analysis</button>
                    </div>

                    {analysisResult && (
                        <div style={{ background: '#f0f4f8', padding: '15px', borderRadius: '8px', marginTop: '10px' }}>
                            <h4 style={{ margin: '0 0 10px 0' }}>Results for: {analysisResult.title}</h4>
                            <p><b>Level</b> {analysisResult.level}</p>
                            <p><b>Unknown words:</b> {analysisResult.unknown_words}</p>
                            <p><b>Coverage:</b> {analysisResult.coveragepercent}%</p>

                            <p><b>Recommended words:</b></p>
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
                    <button onClick={reset} style={{ alignSelf: 'flex-start' }}>Back</button>
                </div>
            )}

            {/* Блок SUBMIT (остается как был в предыдущем шаге) */}
            {/* ... */}
        </div>
    );
}