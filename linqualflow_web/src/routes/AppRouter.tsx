import { BrowserRouter, Routes, Route } from "react-router-dom";

import LoginPage from "../pages/LoginPage";
import RegisterPage from "../pages/RegisterPage";
import SettingsPage from "../pages/SettingsPage";
import Dashboard from "../pages/Dashboard";
import ReviewPage from "../pages/ReviewPage";
import PreReviewPage from "../pages/PreReviewPage";
import WordsPage from "../pages/WordsPage";

export default function AppRouter(){

    return (

        <BrowserRouter>

            <Routes>

                <Route path="/" element={<Dashboard/>} />

                <Route path="/login" element={<LoginPage/>} />

                <Route path="/register" element={<RegisterPage/>} />

                <Route path="/user-settings" element={<SettingsPage/>} />

                <Route path="/words" element={<WordsPage/>} />

                <Route path="/prereview" element={<PreReviewPage/>} />

                <Route path="/review" element={<ReviewPage />} />

            </Routes>

        </BrowserRouter>

    )

}
