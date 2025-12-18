import { Navigate, Outlet } from 'react-router';
import {useSelector} from "react-redux";
import type {RootState} from "@/store/store.ts";

export default function ProtectedRoute({ adminOnly = false }: { adminOnly?: boolean }) {
    const { isAuthenticated } = useSelector((state: RootState) => state.auth);


    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }

    if(adminOnly) <Navigate to={'/login'} replace />

    return <Outlet />;
}
