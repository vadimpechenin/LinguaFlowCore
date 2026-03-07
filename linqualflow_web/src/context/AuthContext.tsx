import { createContext, useState, useEffect } from "react";
import { getProfile } from "../api/auth";

export const AuthContext = createContext<any>(null);

export const AuthProvider = ({ children }: any) => {

    const [user, setUser] = useState(null);

    useEffect(() => {

        const token = localStorage.getItem("token");

        if (token) {
            getProfile().then(res => setUser(res.data));
        }

    }, []);

    const loginUser = (token: string) => {

        localStorage.setItem("token", token);

    };

    const logout = () => {

        localStorage.removeItem("token");
        setUser(null);

    };

    return (
        <AuthContext.Provider value={{user, loginUser, logout}}>
            {children}
        </AuthContext.Provider>
    );

};
