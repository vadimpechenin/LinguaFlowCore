import API from "./api"
import type { RecommendWord, AnswerProgress, ProgressWordAnswer } from "../types/review"

export const getReviewWords = async (): Promise<RecommendWord[]> => {

    const res = await API.get("/review/words")

    return res.data

}

export const sendReviewAnswer = async (
    answer: AnswerProgress
): Promise<ProgressWordAnswer> => {

    const res = await API.post("/review/answer",
        answer)
    return res.data
}