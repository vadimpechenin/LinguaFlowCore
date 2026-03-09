import { createContext, useState, useEffect } from "react"

interface AuthContextType {
    token: string | null
    loginUser: (token: string) => void
    logout: () => void
}

export const AuthContext = createContext<AuthContextType | null>(null)

export const AuthProvider = ({ children }: any) => {

    const [token, setToken] = useState<string | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {

        const storedToken = localStorage.getItem("token")

        if (storedToken) {
            setToken(storedToken)
        }

        setLoading(false)

    }, [])

    const loginUser = (newToken: string) => {

        localStorage.setItem("token", newToken)

        setToken(newToken)

    }

    const logout = () => {

        localStorage.removeItem("token")

        setToken(null)

    }

    if (loading) {
        return <div>Loading...</div>
    }

    return (

        <AuthContext.Provider
            value={{
                token,
                loginUser,
                logout
            }}
        >

            {children}

        </AuthContext.Provider>

    )

}
