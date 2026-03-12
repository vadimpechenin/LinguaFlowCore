import API from "./api"
import type { WordCreate, WordResponse, WordRead } from "../types/words"

export const createWord = async (
    answer: WordCreate
): Promise<WordResponse> => {

    const res = await API.post("/words",
        answer)
    return res.data
}

export const createWordsFromTable = async (
    words: WordCreate[]
): Promise<WordRead[]> => {
    const res = await API.post("/words/from_table", words);
    return res.data;
};