import React, { useState, useEffect } from 'react';
import {
    TrendingUp,
    BookOpen,
    CheckSquare,
    Flame,
    Loader2,
    ArrowLeft
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import type {ProgressSummary} from "../types/statistics"
import {getSummaryStatistics} from "../api/review";
import {backButtonStyle, centerStyle, cardStyle, valueStyle, gridStyle, iconWrapperStyle} from "../components/Styles";

export default function StatisticsPage() {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [summary, setSummary] = useState<ProgressSummary | null>(null);
    // Загрузка настроек при входе на страницу
    useEffect(() => {
        getSummaryStatistics()
            .then(data => {
                setSummary(data);
            })
            .catch(err => console.error("Error loading stats:", err))
            .finally(() => setLoading(false));
    }, []);
    if (loading) {
        return (
            <div style={centerStyle}>
                <Loader2 className="animate-spin" size={48} color="#007bff" />
                <p>Loading your progress...</p>
            </div>
        );
    }

    return (
        <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
            <button
                onClick={() => navigate('/')}
                style={backButtonStyle}
            >
                <ArrowLeft size={20} />
                {"Back to Dashboard"}
            </button>

            <h1 style={{ marginBottom: '30px' }}>Your Learning Progress</h1>

            <div style={gridStyle}>
                {/* Карточка: Всего слов */}
                <div style={cardStyle}>
                    <div style={iconWrapperStyle("#e3f2fd")}>
                        <BookOpen color="#1976d2" />
                    </div>
                    <h3>Total Words</h3>
                    <p style={valueStyle}>{summary?.total_words || 0}</p>
                </div>

                {/* Карточка: Изучено */}
                <div style={cardStyle}>
                    <div style={iconWrapperStyle("#e8f5e9")}>
                        <CheckSquare color="#388e3c" />
                    </div>
                    <h3>Learned Words</h3>
                    <p style={valueStyle}>{summary?.learned_words || 0}</p>
                </div>

                {/* Карточка: Ударный режим */}
                <div style={cardStyle}>
                    <div style={iconWrapperStyle("#fff3e0")}>
                        <Flame color="#f57c00" />
                    </div>
                    <h3>Daily Streak</h3>
                    <p style={valueStyle}>{summary?.daily_streak || 0} days</p>
                </div>

                {/* Карточка: Успешность */}
                <div style={cardStyle}>
                    <div style={iconWrapperStyle("#f3e5f5")}>
                        <TrendingUp color="#7b1fa2" />
                    </div>
                    <h3>Success Rate</h3>
                    <p style={valueStyle}>
                        {summary?.success_rate ? `${(summary.success_rate * 100).toFixed(1)}%` : '0%'}
                    </p>
                </div>
            </div>
        </div>
    );
}

