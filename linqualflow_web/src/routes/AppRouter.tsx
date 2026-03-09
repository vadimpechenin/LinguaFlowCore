import { BrowserRouter, Routes, Route } from "react-router-dom";

import LoginPage from "../pages/LoginPage";
import RegisterPage from "../pages/RegisterPage";
import Dashboard from "../pages/Dashboard";
import ReviewPage from "../pages/ReviewPage";

export default function AppRouter(){

    return (

        <BrowserRouter>

            <Routes>

                <Route path="/" element={<Dashboard/>} />

                <Route path="/login" element={<LoginPage/>} />

                <Route path="/register" element={<RegisterPage/>} />

                <Route path="/review" element={<ReviewPage />} />

            </Routes>

        </BrowserRouter>

    )

}
