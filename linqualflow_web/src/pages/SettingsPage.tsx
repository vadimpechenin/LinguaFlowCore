import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getSettings, updateSettings } from '../api/settings';
import type { SettingResponse, SettingUpdate } from '../types/settings';
import {ArrowLeft} from 'lucide-react';
import {backButtonStyle} from "../components/Styles";


export default function SettingsPage() {
    const navigate = useNavigate();
    const [settings, setSettings] = useState<SettingResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [message, setMessage] = useState('');

    // Загрузка настроек при входе на страницу
    useEffect(() => {
        getSettings()
            .then(data => setSettings(data))
            .catch(err => console.error("Error load:", err))
            .finally(() => setLoading(false));
    }, []);

    // Обработка изменений в полях ввода
    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        if (!settings) return;
        const { name, value, type } = e.target;

        setSettings({
            ...settings,
            [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
        });
    };

    // Сохранение настроек
    const handleSave = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!settings) return;

        const updateData: SettingUpdate = { ...settings };
        try {
            await updateSettings(updateData);
            setMessage('Настройки успешно обновлены!');
        } catch (err) {
            setMessage('Ошибка при сохранении.');
        }
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div style={{ padding: '20px', maxWidth: '500px' }}>
            <button
                onClick={() => navigate('/')}
                style={backButtonStyle}
            >
                <ArrowLeft size={20} />
                {"Back to Dashboard"}
            </button>
            <h1>User Settings</h1>
            {message && <p><strong>{message}</strong></p>}

            <form onSubmit={handleSave}>
                <div>
                    <label>Interface Language:</label>
                    <input name="interfacelanguage" value={settings?.interfacelanguage} onChange={handleChange} />
                </div>

                <div>
                    <label>Learning Language:</label>
                    <input name="learninglanguage" value={settings?.learninglanguage} onChange={handleChange} />
                </div>

                <div>
                    <label>Daily Word Limit:</label>
                    <input type="number" name="dailywordlimit" value={settings?.dailywordlimit} onChange={handleChange} />
                </div>

                <div>
                    <label>
                        <input type="checkbox" name="enableaudio" checked={settings?.enableaudio} onChange={handleChange} />
                        Enable Audio
                    </label>
                </div>

                <div>
                    <label>
                        <input type="checkbox" name="enablenotifications" checked={settings?.enablenotifications} onChange={handleChange} />
                        Notifications
                    </label>
                </div>

                <div style={{ marginTop: '20px' }}>
                    <button type="submit">Change Settings</button>
                </div>
            </form>
        </div>
    );
}
