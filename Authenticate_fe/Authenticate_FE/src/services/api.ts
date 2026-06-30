import type { ConfigData, UserData } from "@/types/users";
import axios, { AxiosError, type AxiosInstance } from "axios";

export class ApiService {
    #axiosInstance: AxiosInstance
    #user: UserData | undefined

    constructor(user?: UserData) {
        this.#axiosInstance = axios.create({
            baseURL: import.meta.env.VITE_BACKEND_URL,
            headers: { "Content-Type": "application/json" },
            timeout: import.meta.env.VITE_BACKEND_TIMEOUT,
        });
        this.#user = user;

        this.#axiosInstance.interceptors.request.use(
            (config) => {
                const url = config.url ?? "";

                const isAuthEndpoint =
                    url.startsWith("/auth/jwt/refresh/") ||
                    url.startsWith("/auth/jwt/create/") ||
                    url.startsWith("/users/auth/jwt/create");

                if (!isAuthEndpoint && this.#user?.access_token) {
                    config.headers = config.headers ?? {};
                    if (!("Authorization" in config.headers)) {
                        config.headers.Authorization = `JWT ${this.#user.access_token}`;
                    }
                }

                return config;
            },
            (error) => Promise.reject(error)
        );

    }


    get axios() {
        return this.#axiosInstance;
    }
    get user() {
        return this.#user;
    }
    setUser(user?: UserData) {
        this.#user = user;
    }
    async login(email: string, password: string): Promise<UserData> {
        const response = await this.#axiosInstance.post<UserData>("/users/auth/jwt/create/", {
            "email": email,
            "password": password
        });
        const user = response.data;
        this.#user = user;
        return this.#user;
    }
    logout() {
        this.#user = undefined;
        return this.#user;
    }
    async refreshToken(): Promise<string> {
        if (!this.#user?.refresh_token) { throw new Error("Missing refresh token"); }
        try {
            const response = await this.#axiosInstance.post("/users/auth/jwt/refresh/",
                { "refresh": this.#user!.refresh_token },
                { headers: { Authorization: "" as any } }
            );
            const access = response.data.access;
            if (this.#user) {
                this.#user = { ...this.#user, access_token: access };
            }
            return access;
        } catch (error) {
            if (error instanceof AxiosError && error.response?.status === 401) { this.logout(); }
            // Le refresh token est invalide / expiré → session terminée
            throw error;
        }
    }
    async getConfig(): Promise<ConfigData> {
        const response = await this.#axiosInstance.get("/core/theme/me/");
        return response.data;
    }
    async postActivation(uid: string, token: string) {
        const response = await this.#axiosInstance.post("/users/auth/activation/", { "uid": uid, "token": token });
        return response.data;
    }
    async postResendActivation(email: string) {
        const response = await this.#axiosInstance.post("/users/auth/resend_activation/", { "email": email });
        return response.data;
    }
    async postResetPassword(uid: string, token: string, new_password: string) {
        const response = await this.#axiosInstance.post("/users/auth/users/reset_password_confirm/", { "uid": uid, "token": token, "new_password": new_password });
        return response.data;
    }
    async postPasswordForgotten(email: string) {
        const response = await this.#axiosInstance.post("/users/auth/users/reset_password/", { "email": email });
        return response.data;
    }
}
