import React, { createContext, useState, useEffect } from "react";
import axios from "axios";

interface User {
    id: string;
    username: string;
}

interface AuthContextType {
    user: User | null;
    loginUser: (token: string) => Promise<void>;
    logoutUser: () => void;
}

export const AuthContext = createContext<AuthContextType>({
    user: null,
    loginUser: async () => {},
    logoutUser: () => {}
});

export const AuthProvider = ({ children }: any) => {

    const [user, setUser] = useState<User | null>(null);

    // Проверка токена при старте
    useEffect(() => {

        const token = localStorage.getItem("token");

        if (token) {
            loadUser(token);
        }

    }, []);

    const loadUser = async (token: string) => {

        try {

            const res = await axios.get(
                "http://localhost:8000/users/me2",
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            setUser(res.data);

        } catch {

            localStorage.removeItem("token");
            setUser(null);

        }

    };

    const loginUser = async (token: string) => {

        localStorage.setItem("token", token);

        await loadUser(token);

    };

    const logoutUser = () => {

        localStorage.removeItem("token");

        setUser(null);

    };

    return (
        <AuthContext.Provider
            value={{
                user,
                loginUser,
                logoutUser
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};