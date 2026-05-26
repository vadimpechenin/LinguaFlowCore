import axios, { type AxiosInstance } from "axios";
const pl_API = 'server'
//const pl_API = 'noserver'
export let API: AxiosInstance;


if (pl_API=='server'){
    API = axios.create({
        baseURL:  import.meta.env.VITE_API_URL,
    });

}else{
    API = axios.create({
        baseURL: "http://localhost:8000",
    });
}
// Выводим в консоль адрес из уже созданного объекта конфигурации
console.log("Итоговый baseURL в Axios:", API.defaults.baseURL);
API.interceptors.request.use((config) => {

    const token = localStorage.getItem("token");

    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
});

export default API;
