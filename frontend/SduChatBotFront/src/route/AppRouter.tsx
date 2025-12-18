import {BrowserRouter, Navigate, Route, Routes} from "react-router";
import LoginPage from "../pages/LoginPage.tsx";
import LoginCallBackPage from "../pages/LoginCallBackPage.tsx";
import ErrorPage from "../pages/ErrorPage.tsx";
import MainPage from "../pages/MainPage.tsx";
import ProtectedRoute from "@/route/ProtectedRoute.tsx";

function AppRouter() {

    return (
        <>
            <BrowserRouter>
                <Routes>
                    <Route path="/error" element={<ErrorPage/>}/>
                    <Route path="/login" element={<LoginPage/>}/>
                    <Route path="/login-callback" element={<LoginCallBackPage/>}/>
                    <Route element={<ProtectedRoute/>}>
                        <Route path="/" element={<MainPage/>}/>
                        <Route path="/:id" element={<MainPage/>}/>
                    </Route>
                    <Route path="/" element={<Navigate to="/" replace/>}/>
                    <Route path="*" element={<Navigate to="/error" replace/>}/>
                </Routes>
            </BrowserRouter>
        </>
    )
}

export default AppRouter
