import React, { useState, useRef, useEffect } from 'react';
import { read, utils } from 'xlsx';
import { useNavigate } from 'react-router-dom';
import {
    addWordsToProgress, createWord, createWordsFromTable,
    getAvailableWords
} from "../api/words";
import { FileUp, PlusCircle, ArrowLeft, Send, Loader2, ListPlus } from 'lucide-react';
import type {WordCreate, WordID, WordResponse} from "../types/words"

export default function WordsPage() {
    const navigate = useNavigate();
    const fileInputRef = React.useRef<HTMLInputElement>(null);
    // Состояние для переключения между меню и формой
    const [view, setView] = useState<'menu' | 'addForm'| 'selectWords'>('menu');
    const [loading, setLoading] = useState(false);

    // Состояния для полей WordCreate
    const [texten, setTexten] = useState("slew");
    const [transcription, setTranscription] = useState("sluː");
    const [textl, setTextl] = useState("убил");
    const [partofspeech, setPartofspeech] = useState("verb");
    const [examplesentence, setExamplesentence] = useState("The pirate slew his enemy.");
    const [difficultylevel, setDifficultylevel] = useState("B2");
    // -----------------------
    // SELECT WORDS STATE
    // -----------------------

    const [availableWords, setAvailableWords] = useState<WordResponse[]>([]);
    const [selected, setSelected] = useState<Set<string>>(new Set());

    // -----------------------
    // LOAD AVAILABLE WORDS
    // -----------------------

    useEffect(() => {

        if (view !== "selectWords") return;

        const loadWords = async () => {

            try {

                setLoading(true);

                const words = await getAvailableWords();

                setAvailableWords(words);

            } catch (err) {

                console.error(err);

                alert("Error loading words");

            } finally {

                setLoading(false);

            }

        };

        loadWords();

    }, [view]);
    // -----------------------
    // SELECT WORD TOGGLE
    // -----------------------

    const toggleWord = (id: string) => {

        const newSet = new Set(selected);

        if (newSet.has(id)) {

            newSet.delete(id);

        } else {

            newSet.add(id);

        }

        setSelected(newSet);

    };

    // -----------------------
    // ADD SELECTED WORDS
    // -----------------------

    const addSelectedWords = async () => {

        if (selected.size === 0) return;

        try {

            setLoading(true);

            const ids = Array.from(selected);
            const wordsToSide: WordID[] = ids.map(id => ({id}));
            const result = await addWordsToProgress(wordsToSide);

            alert(`${ids.length} words added`);

            setSelected(new Set());

            setView("menu");

        } catch (err) {

            console.error(err);

            alert("Error adding words");

        } finally {

            setLoading(false);

        }

    };

    // -----------------------
    // ADD WORD
    // -----------------------
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await createWord({
                texten,
                transcription: transcription || null,
                textl: textl || null,
                partofspeech: partofspeech || null,
                examplesentence: examplesentence || null,
                difficultylevel
            });
            alert("Word added!");
            setView('menu'); // Возвращаемся в меню после успеха
            // Очистка полей
            setTexten(""); setTranscription(""); setTextl("");
            setPartofspeech(""); setExamplesentence("");
        } catch (error) {
            console.error(error);
            alert("Error adding word");
        }
    };

    // ЛОГИКА ИМПОРТА EXCEL
    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = async (evt) => {
            try {
                setLoading(true);
                const bstr = evt.target?.result;
                const wb = read(bstr, { type: 'binary' });
                const wsname = wb.SheetNames[0];
                const ws = wb.Sheets[wsname];

                // Превращаем в массив объектов
                const data = utils.sheet_to_json(ws);

                // Маппинг колонок по вашей логике из Python
                const wordsToSide: WordCreate[] = data.map((row: any) => ({
                    texten: row["Word / Expression"],
                    transcription: row["Transcription (BrE)"] || null,
                    textl: row["Translation (RU)"] || null,
                    partofspeech: row["Part of Speech"] || null,
                    examplesentence: row["Example from the book"] || null,
                    difficultylevel: String(row["Level"] || "beginner")
                }));

                if (wordsToSide.length === 0) throw new Error("File is empty");

                alert(`Sending ${wordsToSide.length} words to server...`);

                const savedWords = await createWordsFromTable(wordsToSide);
                alert(`Success! Added ${savedWords.length} new words to database.`);

            } catch (err) {
                console.error(err);
                alert("Error processing Excel file. Check column names!");
            } finally {
                setLoading(false);
                if (fileInputRef.current) fileInputRef.current.value = ""; // Сброс инпута
            }
        };
        reader.readAsBinaryString(file);
    };


    return (

        <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>

            <button
                onClick={() =>
                    view === 'menu'
                        ? navigate('/')
                        : setView('menu')
                }
                style={backButtonStyle}
            >

                <ArrowLeft size={20} />

                {view === 'menu'
                    ? "Back to Dashboard"
                    : "Back to Selection"}

            </button>

            <h1>

                {view === 'menu'
                    ? "Manage Your Words"
                    : view === 'addForm'
                        ? "Add New Word"
                        : "Select Words"}

            </h1>

            {/* MENU */}

            {view === 'menu' && (

                <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>

                    <input
                        type="file"
                        ref={fileInputRef}
                        style={{ display: 'none' }}
                        accept=".xlsx,.xls"
                        onChange={handleFileUpload}
                    />

                    <button
                        disabled={loading}
                        onClick={() => fileInputRef.current?.click()}
                        style={menuButtonStyle}
                    >

                        {loading
                            ? <Loader2 className="animate-spin" size={20}/>
                            : <FileUp size={20}/>
                        }

                        Import from file

                    </button>

                    <button
                        onClick={() => setView('addForm')}
                        style={menuButtonStyle}
                    >

                        <PlusCircle size={20}/>

                        Add one word

                    </button>

                    <button
                        onClick={() => setView('selectWords')}
                        style={menuButtonStyle}
                    >

                        <ListPlus size={20}/>

                        Select from database

                    </button>

                </div>

            )}

            {/* ADD FORM */}

            {view === 'addForm' && (

                <form onSubmit={handleSubmit} style={formStyle}>

                    <input
                        placeholder="English word"
                        value={texten}
                        onChange={e => setTexten(e.target.value)}
                        required
                        style={inputStyle}
                    />

                    <input
                        placeholder="Transcription"
                        value={transcription}
                        onChange={e => setTranscription(e.target.value)}
                        style={inputStyle}
                    />

                    <input
                        placeholder="Translation"
                        value={textl}
                        onChange={e => setTextl(e.target.value)}
                        style={inputStyle}
                    />

                    <textarea
                        placeholder="Example sentence"
                        value={examplesentence}
                        onChange={e => setExamplesentence(e.target.value)}
                        style={inputStyle}
                    />

                    <button type="submit" style={submitButtonStyle}>

                        <Send size={18}/>

                        Save Word

                    </button>

                </form>

            )}

            {/* SELECT WORDS */}

            {view === 'selectWords' && (

                <div>

                    {loading ? (

                        <p>Loading words...</p>

                    ) : (

                        <>

                            <p>

                                Selected: {selected.size}

                            </p>

                            <div style={{maxHeight: 400, overflow: "auto"}}>

                                {availableWords.map(word => (

                                    <label
                                        key={word.id}
                                        style={{
                                            display: "flex",
                                            gap: 10,
                                            padding: 6
                                        }}
                                    >

                                        <input
                                            type="checkbox"
                                            checked={selected.has(word.id)}
                                            onChange={() => toggleWord(word.id)}
                                        />

                                        <b>{word.texten}</b>

                                        {word.transcription}

                                        — {word.textl}

                                    </label>

                                ))}

                            </div>

                            <button
                                onClick={addSelectedWords}
                                disabled={selected.size === 0}
                                style={submitButtonStyle}
                            >

                                Add {selected.size} words

                            </button>

                        </>

                    )}

                </div>

            )}

        </div>

    );

}


// Стили
const buttonStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    borderRadius: '20px',
    border: '1px solid #ddd',
    backgroundColor: '#fff',
    cursor: 'pointer',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    fontWeight: 500,
    color: '#333'
};

const menuButtonStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    borderRadius: '20px',
    border: '1px solid #ddd',
    backgroundColor: '#fff',
    cursor: 'pointer',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    fontWeight: 500,
    color: '#333'
};


const inputStyle: React.CSSProperties = {
    padding: '12px',
    borderRadius: '8px',
    border: '1px solid #ddd',
    fontSize: '16px',
    width: '100%',
    boxSizing: 'border-box'
};

const formStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px'
};

const submitButtonStyle: React.CSSProperties = {
    ...buttonStyle,
    justifyContent: 'center',
    padding: '14px',
    backgroundColor: '#007bff',
    color: '#fff',
    border: 'none',
    marginTop: '10px'
};

const backButtonStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    background: 'none',
    border: 'none',
    cursor: 'pointer',
    color: '#666',
    marginBottom: '20px',
    padding: 0
};