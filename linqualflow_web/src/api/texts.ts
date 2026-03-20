import API from "./api"
import type { TextAnalyzeResponse, TextRequest, TextAnalyzeRequest, TextResponse } from "../types/texts"


export const loadText = async (
    textTitle: string
): Promise<TextResponse> => {
    const res = await API.get(`/texts/${encodeURIComponent(textTitle)}`)
    return res.data
}

export const submitText = async (
    text: TextRequest
): Promise<TextResponse> => {
    const res = await API.post("/texts", text);
    return res.data;
};

export const analyzeText = async (
    textTitle: TextAnalyzeRequest
): Promise<TextAnalyzeResponse> => {
    const res = await API.post("/texts/analyze", textTitle)
    return res.data
}
