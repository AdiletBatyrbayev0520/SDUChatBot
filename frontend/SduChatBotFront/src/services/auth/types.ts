export interface LoginRequest {
    code: string;
    scope: string;
    authUser: string;
    prompt: string;
}

export interface LoginResponse {
    accessToken: string;
    refreshToken: string;
}