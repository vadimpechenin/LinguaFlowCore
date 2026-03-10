import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { UserCircle, LogOut, Settings } from 'lucide-react';
import { AuthContext } from "../context/AuthContext";


export default function Dashboard() {
    const navigate = useNavigate();

    // Берем данные об авторизации из контекста
    // (Названия переменных user или isAuthenticated зависят от того, как они описаны в вашем AuthContext)
    const { user, logoutUser } = useContext(AuthContext);
    const isLoggedIn = !!user; // Если объект user есть — значит залогинен

    return (
        <div style={{ padding: '20px', position: 'relative' }}>
            <div style={{ position: 'absolute', top: '20px', right: '20px', display: 'flex', gap: '10px' }}>
                {isLoggedIn ? (
                    <>
                        <button onClick={() => navigate('/settings')} style={buttonStyle}>
                            <Settings size={20} />
                            <span>настройки</span>
                        </button>

                        {/* Используем функцию logout из контекста */}
                        <button onClick={logoutUser} style={logoutButtonStyle}>
                            <LogOut size={20} />
                            <span>выйти</span>
                        </button>
                    </>
                ) : (
                    <button onClick={() => navigate('/login')} style={buttonStyle}>
                        <UserCircle size={20} />
                        <span>войти</span>
                    </button>
                )}
            </div>

            <div>
                <h1>LinqualFlow</h1>
                <ul style={{ marginTop: '40px' }}>
                    <li>📚 Review words (coming soon)</li>
                    <li>📖 Text analysis (coming soon)</li>
                    <li>📊 Statistics (coming soon)</li>
                    <li>📝 Exams (coming soon)</li>
                </ul>
            </div>
        </div>
    );
}

// Общие стили
const buttonStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    padding: '8px 16px',
    borderRadius: '20px',
    border: '1px solid #ddd',
    backgroundColor: '#fff',
    cursor: 'pointer',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    fontWeight: 500,
    color: '#333'
};

// Стили для кнопки выхода
const logoutButtonStyle: React.CSSProperties = {
    ...buttonStyle,
    color: '#d32f2f',
    borderColor: '#ffcdd2'
};