export interface ExamResponseAllFields {

    id: string
    userid: string
    difficultylevel: string
    size: number
    takenat: string

}

export interface ExamStart {

    difficultylevel: string
    size: number

}

type QuestionType =
    | "flashcard_forward"
    | "flashcard_reverse"
    | "multiple_choice"
    | "scramble"

export interface ExamQuestion {

    word_id: string
    type:QuestionType
    question: string
    options?: string[]

}

export interface ExamResponse {

    examid: string
    questions: ExamQuestion[]

}

export interface ExamSubmitAnswer {

    word_id: string
    is_correct: boolean

}

export interface ExamSubmit {

    answers: ExamSubmitAnswer[]

}

export interface ExamResult {

    score: number
    estimatedlevel: string

}
