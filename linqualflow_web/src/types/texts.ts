export interface TextRequest {
    title: string
    content: string
    language: string
}

export interface TextResponse {
    id: string
    title: string
    content: string
}

export interface TextAnalyzeRequest {
    title: string
}

export interface TextAnalyzeResponse {
    title: string
    level: string
    unknown_words: number
    coveragepercent: number
    recommended_words: string[]
}