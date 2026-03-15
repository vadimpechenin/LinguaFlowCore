import API from "./api"

import type {
    ExamResponseAllFields,
    ExamStart,
    ExamResponse,
    ExamSubmit,
    ExamResult
} from "../types/exams"

export const getUserExams = async (): Promise<ExamResponseAllFields[]> => {

    const res = await API.get("/exams")

    return res.data

}

export const startExam = async (
    data: ExamStart
): Promise<ExamResponse> => {

    const res = await API.post("/exams/start", data)

    return res.data

}

export const submitExam = async (
    examId: string,
    data: ExamSubmit
): Promise<ExamResult> => {

    const res = await API.post(`/exams/${examId}/submit`, data)

    return res.data

}
