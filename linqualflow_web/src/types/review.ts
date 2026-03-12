export interface RecommendWord {

    id: string

    texten: string

    transcription?: string

    textl: string

    partofspeech: string

    examplesentence?: string

    difficultylevel: string

    audiourl?: string

    createdat: string

}

export interface AnswerProgress {
    wordid: string
    iscorrect: boolean
    response_time_ms: number
}

export interface RefreshWords {
    refresh: boolean
}

export interface ProgressWordAnswer {
    id: string
    userid: string
    wordid: string
    lastreviewed?: string
    nextreviewed?: string
    successrate: number
    reviewcount: number
    isknown: boolean
    createdat: string
}