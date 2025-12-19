import type {FC} from 'react';
// import {useEffect} from 'react';
// import {useNavigate} from 'react-router';
// import {useSelector} from 'react-redux';
// import type {RootState} from '../store/store';

const RESPONSE_TYPE = 'code';
const CLIENT_ID = '211043075627-go3joan2ll0scbt3e43qm2tlcpk3jpdd.apps.googleusercontent.com';
const SCOPE = 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid';
const ACCESS_TYPE = 'offline';
// const REDIRECT_URI = 'http://localhost:5173/login-callback';
// const REDIRECT_URI = 'http://localhost/login-callback';
const REDIRECT_URI = 'http://chat.sdu.edu.kz/login-callback';
// const REDIRECT_URI = 'https://dev.dsfyww8pm8b26.amplifyapp.com/login-callback';

const LoginPage: FC = () => {
    // const navigate = useNavigate();
    // const isAuthenticated = useSelector((state: RootState) => state.auth.isAuthenticated);
    //
    // useEffect(() => {
    //     if (isAuthenticated) {
    //         navigate('/main-page');
    //     }
    // }, [isAuthenticated, navigate]);

    return (
        <div className="h-[100dvh] flex items-center justify-center bg-gray-50">
            <div className="max-w-md w-full space-y-8 p-8 bg-white rounded-lg shadow-lg">
                <div>
                    <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
                        Welcome back
                    </h2>
                </div>
                <a
                    href={`https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=${REDIRECT_URI}&response_type=${RESPONSE_TYPE}&client_id=${CLIENT_ID}&scope=${SCOPE}&access_type=${ACCESS_TYPE}`}
                    className="w-full flex items-center justify-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200"
                >
                    <img
                        src="https://www.google.com/favicon.ico"
                        alt="Google"
                        className="w-5 h-5 mr-2"
                    />
                    Sign in with Google
                </a>
            </div>
        </div>
    );
};

export default LoginPage;