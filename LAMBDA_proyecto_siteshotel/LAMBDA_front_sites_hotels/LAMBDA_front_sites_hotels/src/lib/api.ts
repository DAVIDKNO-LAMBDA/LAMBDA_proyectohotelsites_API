/**
 * API Service - Cliente para conectar con el backend Django
 *
 * Maneja todas las solicitudes HTTP hacia la API:
 * - Login y registro de usuarios
 * - Inyección automática de tokens JWT
 * - Renovación automática del token si expira
 * - Manejo centralizado de errores
 */

import axios, {
  AxiosInstance,
  AxiosResponse,
  AxiosError,
  InternalAxiosRequestConfig,
} from "axios";

// ===============================
// 🌐 Configuración base
// ===============================
const API_BASE_URL = "http://localhost:8000/api";

// ===============================
// 🧩 Tipos
// ===============================
export interface Usuario {
  id: number;
  email: string;
  nombre: string;
  apellido: string;
  tipo_usuario: "Inversionista" | "Admin";
  estado: boolean;
  creado: string;
  modificado: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
  user: Usuario;
}

export interface RegisterRequest {
  email: string;
  password: string;
  nombre: string;
  apellido: string;
  tipo_usuario: "Inversionista" | "Admin";
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface ApiError {
  message: string;
  errors?: Record<string, string[]>;
}

// ===============================
// ⚙️ Clase principal del servicio
// ===============================
class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
      headers: { "Content-Type": "application/json" },
    });

    // ===============================
    // 🧩 Interceptor de solicitud
    // ===============================
    this.client.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        const token = this.getAccessToken();

        if (token) {
          // ✅ Inicializar headers de forma segura
          if (!config.headers) {
            config.headers = {} as any;
          }

          // ✅ Compatibilidad Axios v1.6+ (usa .set si está disponible)
          if (typeof (config.headers as any).set === "function") {
            (config.headers as any).set("Authorization", `Bearer ${token}`);
          } else {
            if (config.headers) {
              (config.headers as any).Authorization = `Bearer ${token}`;
            }
          }

          console.log("✅ Token agregado al header:", token.substring(0, 20) + "...");
        } else {
          console.warn("⚠️ No se encontró token de acceso en localStorage");
        }

        return config;
      },
      (error) => Promise.reject(error)
    );

    // ===============================
    // 🧩 Interceptor de respuesta
    // ===============================
    this.client.interceptors.response.use(
      (response: AxiosResponse) => response,
      async (error: AxiosError) => {
        if (error.response?.status === 401 && this.getRefreshToken()) {
          try {
            console.warn("⚠️ Token expirado, intentando renovarlo...");
            await this.refreshToken();

            const originalRequest = error.config;
            if (originalRequest) {
              const token = this.getAccessToken();
              if (token) {
                if (!originalRequest.headers) {
                  originalRequest.headers = {} as any;
                }

                if (typeof (originalRequest.headers as any).set === "function") {
                  (originalRequest.headers as any).set(
                    "Authorization",
                    `Bearer ${token}`
                  );
                } else {
                  (originalRequest.headers as any).Authorization = `Bearer ${token}`;
                }

                console.log("🔄 Retrying request con nuevo token...");
                return this.client.request(originalRequest);
              }
            }
          } catch (refreshError) {
            console.error("❌ Error al renovar el token:", refreshError);
            this.clearTokens();
            window.location.href = "/login";
          }
        }
        return Promise.reject(this.handleApiError(error));
      }
    );
  }

  // ===============================
  // 🔐 Autenticación
  // ===============================
  private getAccessToken(): string | null {
    return localStorage.getItem("access_token");
  }

  private getRefreshToken(): string | null {
    return localStorage.getItem("refresh_token");
  }

  private setTokens(access: string, refresh: string): void {
    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
  }

  private clearTokens(): void {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
  }

  private async refreshToken(): Promise<void> {
    const refresh = this.getRefreshToken();
    if (!refresh) throw new Error("No hay refresh token disponible");

    const response = await axios.post(`${API_BASE_URL}/token/refresh/`, { refresh });
    this.setTokens(response.data.access, refresh);
    console.log("🔄 Token de acceso renovado correctamente");
  }

  // ===============================
  // 👤 Usuarios
  // ===============================
  async register(data: RegisterRequest): Promise<Usuario> {
    try {
      const response = await this.client.post<Usuario>("/usuarios/registrar/", data);
      return response.data;
    } catch (error) {
      throw this.handleApiError(error as AxiosError);
    }
  }

  async login(data: LoginRequest): Promise<LoginResponse> {
    try {
      const response = await this.client.post<LoginResponse>("/usuarios/login/", data);

      const access = (response.data as any).access;
      const refresh = (response.data as any).refresh;
      const user = (response.data as any).user;

      if (!access || !refresh) {
        throw new Error("⚠️ No se recibieron tokens válidos desde el servidor");
      }

      this.setTokens(access, refresh);
      localStorage.setItem("user", JSON.stringify(user));

      console.log("✅ Tokens guardados correctamente");
      return response.data;
    } catch (error) {
      throw this.handleApiError(error as AxiosError);
    }
  }

  async getProfile(): Promise<Usuario> {
    try {
      const response = await this.client.get<Usuario>("/usuarios/perfil/");
      return response.data;
    } catch (error) {
      throw this.handleApiError(error as AxiosError);
    }
  }

  logout(): void {
    this.clearTokens();
    console.info("👋 Sesión cerrada correctamente");
  }

  isAuthenticated(): boolean {
    return !!this.getAccessToken();
  }

  getCurrentUser(): Usuario | null {
    const userStr = localStorage.getItem("user");
    if (!userStr) return null;
    try {
      return JSON.parse(userStr);
    } catch {
      console.error("❌ Error al parsear usuario del localStorage");
      return null;
    }
  }

  // ===============================
  // 📊 Dashboard / KPIs
  // ===============================
  async getDashboardMetrics(property: string, area: string, period: string) {
    try {
      const response = await this.client.get("/dashboard/metrics/", {
        params: { property, area, period },
      });
      return response.data;
    } catch (error) {
      throw this.handleApiError(error as AxiosError);
    }
  }

  // ===============================
  // ⚠️ Manejo de errores global
  // ===============================
  private handleApiError(error: AxiosError): ApiError {
    console.error("❌ Error en solicitud API:", error);

    if (error.response?.data) {
      const errorData = error.response.data as any;

      if (errorData.detail) {
        return {
          message: errorData.detail,
          errors: errorData.errors || {},
        };
      }

      if (typeof errorData === "object") {
        const firstError = Object.values(errorData)[0];
        return {
          message: Array.isArray(firstError)
            ? firstError[0]
            : "Error en la solicitud",
          errors: errorData,
        };
      }
    }

    return { message: error.message || "Error de conexión con el servidor" };
  }
}

// ===============================
// 🧩 Exportación
// ===============================
export const apiService = new ApiService();
export default apiService;
