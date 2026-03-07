import API from "./api";

export const register = (data: {
    name?: string
    username?: string
    email: string
    password: string
    initiallevel?: string
}) => {

    return API.post("/auth/register", data);

};

export const login = (data: {
    username: string
    password: string
}) => {

    return API.post("/auth/login", data);

};

export const getProfile = () => {

    return API.get("/users/me");

};
