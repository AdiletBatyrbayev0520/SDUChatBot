import {useEffect} from 'react';
import {useNavigate, useSearchParams} from 'react-router';
import {useLazyLoginQuery} from '../services/auth/authApi.ts';
import {useDispatch} from 'react-redux';
import {setTokens} from '../store/authSlice';

const LoginCallBackPage = () => {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const [login] = useLazyLoginQuery();

    useEffect(() => {
        const handleCallback = async () => {
            try {
                const code = searchParams.get('code');
                const scope = searchParams.get('scope');
                const authUser = searchParams.get('authuser');
                const prompt = searchParams.get('prompt');

                if (!code || !scope || !authUser || !prompt) {
                    console.error('Missing required parameters');
                    navigate('/login');
                    return;
                }

                const response = await login({
                    code,
                    scope,
                    authUser,
                    prompt
                }).unwrap();

                if (response) {
                    // Store tokens in Redux store
                    dispatch(setTokens({
                        accessToken: response.accessToken,
                        refreshToken: response.refreshToken
                    }));

                    // Redirect to main page
                    navigate('/main-page');
                }
            } catch (error) {
                console.error('Authentication error:', error);
                navigate('/login');
            }
        };

        handleCallback();
    }, [searchParams, navigate, login, dispatch]);

    return (
        <div className="flex items-center justify-center min-h-screen">
            <div className="text-center">
                <h1 className="text-2xl font-semibold mb-4">Processing login...</h1>
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
            </div>
        </div>
    );
};

export default LoginCallBackPage;
