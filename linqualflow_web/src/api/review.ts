import API from "./api"
import type { RecommendWord, AnswerProgress, ProgressWordAnswer, RefreshWords } from "../types/review"
import type {ProgressSummary} from "../types/statistics";

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

export const fetchReviewWords = async (refresh: RefreshWords) => {
    // Отправляем GET запрос с параметром refresh
    console.log("Обновление: " + refresh.refresh)

    const res = await API.post("/review/words",refresh);
    return res.data;
};

export const getSummaryStatistics = async (
): Promise<ProgressSummary> => {

    const res = await API.get("/review/progress/summary")
    return res.data
}