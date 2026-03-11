export interface SettingResponse {

    userid: string

    interfacelanguage: string

    learninglanguage: string

    preferredvoice: string

    dailywordlimit: number

    enableaudio: boolean

    enablenotifications: boolean

    timezone: string

}

export interface SettingUpdate {
    interfacelanguage?: string

    learninglanguage?: string

    preferredvoice?: string

    dailywordlimit?: number

    enableaudio?: boolean

    enablenotifications?: boolean

    timezone?: string
}