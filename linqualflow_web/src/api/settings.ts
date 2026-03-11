import API from "./api"
import type { SettingResponse, SettingUpdate } from "../types/settings"

export const getSettings = async (): Promise<SettingResponse> => {

    const res = await API.get("/user-settings")

    return res.data

}

export const updateSettings = async (
    answer: SettingUpdate
) => {

    const res = await API.put("/user-settings",
        answer)
    return res.data
}