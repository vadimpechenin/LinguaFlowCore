import React from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchReviewWords } from '../api/review';
import type { RefreshWords} from "../types/review";

export default function PreReviewPage() {
    const navigate = useNavigate();

    const handleStart = async (refresh: boolean) => {
        const request: RefreshWords = {
            refresh: refresh
        }
        try {
            // Выполняем запрос к API
            const { words, was_refreshed } = await fetchReviewWords(request);
            // Если refresh=true (новый набор) -> показываем список (showList: true)
            // Если refresh=false (продолжить) -> сразу к карточкам (showList: false)
            // После успешного ответа переходим на страницу обучения
            navigate('/review', { state: { words: words,
                    showList: was_refreshed } });
        } catch (error) {
            console.error("Ошибка при подготовке слов:", error);
            alert("Не удалось загрузить слова");
        }
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '20px', marginTop: '50px' }}>
            <h1>Подготовка к повторению</h1>
            <div style={{ display: 'flex', gap: '20px' }}>
                <button onClick={() => handleStart(true)} style={actionButtonStyle}>
                    Создать новый набор
                </button>
                <button onClick={() => handleStart(false)} style={actionButtonStyle}>
                    Продолжить учиться
                </button>
            </div>
            <button onClick={() => navigate('/')} style={{ background: 'none', border: 'none', color: 'gray', cursor: 'pointer' }}>
                Назад
            </button>
        </div>
    );
}

const actionButtonStyle: React.CSSProperties = {
    padding: '15px 30px',
    fontSize: '16px',
    borderRadius: '10px',
    border: '1px solid #ddd',
    backgroundColor: '#fff',
    cursor: 'pointer',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
};