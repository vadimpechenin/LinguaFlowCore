// Базовый интерфейс (аналог WordCreate)
export interface WordCreate {
    texten: string;
    transcription?: string | null;
    textl?: string | null;
    partofspeech?: string | null;
    examplesentence?: string | null;
    difficultylevel: string;
}

// Интерфейс для чтения (аналог WordRead)
export interface WordRead extends WordCreate {
    id: string;
}

// Интерфейс для отправки ID
export interface WordID{
    id: string;
}

// Полный ответ сервера (аналог WordResponse)
export interface WordResponse {
    id: string;
    texten: string;
    transcription: string | null;
    textl: string;
    partofspeech: string | null;
    examplesentence: string | null;
    difficultylevel: string;
    audiourl: string | null;
    createdat: string;
}