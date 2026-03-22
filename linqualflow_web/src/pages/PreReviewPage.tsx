import React from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchReviewWords } from '../api/review';
import type { RefreshWords} from "../types/review";
import {ArrowLeft} from 'lucide-react';
import {actionButtonStyle, backButtonStyle} from "../components/Styles"

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
            console.error("Error preparing words:", error);
            alert("Failed to load words");
        }
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '20px', marginTop: '50px' }}>
            <button
                onClick={() => navigate('/')}
                style={backButtonStyle}
            >
                <ArrowLeft size={20} />
                {"Back to Dashboard"}
            </button>
            <h1>Preparing for a Review</h1>
            <div style={{ display: 'flex', gap: '20px' }}>
                <button onClick={() => handleStart(true)} style={actionButtonStyle}>
                    Create a New Set
                </button>
                <button onClick={() => handleStart(false)} style={actionButtonStyle}>
                    Continue Studying
                </button>
            </div>
        </div>
    );
}