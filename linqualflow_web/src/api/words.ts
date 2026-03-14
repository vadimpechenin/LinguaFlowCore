import API from "./api"
import type { WordCreate, WordResponse, WordRead, WordID } from "../types/words"


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

export const getAvailableWords = async (): Promise<WordResponse[]> => {

    const res = await API.get("/words/available")

    return res.data

}


export const addWordsToProgress= async (
    words: WordID[]) => {

    const res = await API.post("/words/add-to-progress", words);

    return res.data

}
