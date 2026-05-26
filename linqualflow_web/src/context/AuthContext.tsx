import React, { createContext, useState, useEffect } from "react";
import axios from "axios";
import { API } from "../api/api";


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
        //alert("Token в loadUser: " + token)
        try {

            const res = await API.get<User>(
                "/users/me2", // URL склеится с VITE_API_URL автоматически
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );
            //alert("Result после me2: " + res.data)
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