import type {LoginRequest, LoginResponse} from "./types.ts";
import {baseApi} from "../baseApi.ts";



export const authApi = baseApi.injectEndpoints({
    endpoints: (builder) => ({
        login: builder.query<LoginResponse, LoginRequest>({
            query: (credentials) => ({
                url: '/auth/login',
                method: 'GET',
                params: {
                    code: credentials.code,
                    scope: credentials.scope,
                    authuser: credentials.authUser,
                    prompt: credentials.prompt,
                },
            }),
        }),
        logout: builder.mutation<void, void>({
            query: () => ({
                url: '/auth/logout',
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('refreshToken')}`,
                },
            }),
        }),
    }),
});

export const { useLazyLoginQuery, useLogoutMutation } = authApi;