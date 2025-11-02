/**
 * AuthContext - Contexto de Autenticación
 * 
 * Este contexto maneja el estado de autenticación del usuario en toda la aplicación.
 * Proporciona información sobre:
 * - Usuario actual (email, nombre, rol)
 * - Estado de autenticación (isAuthenticated)
 * - Funciones para login y logout
 * 
 * Roles disponibles:
 * - 'Inversionista': Inversionista (ve KPIs de alto nivel)
 * - 'Admin': Administrador (ve todos los detalles operativos)
 */

import React, { createContext, useContext, useState, ReactNode } from 'react';
import { apiService, Usuario, LoginRequest, RegisterRequest, ApiError } from '@/lib/api';

// Definición del tipo de usuario compatible con el backend
export interface User {
  id: number;
  email: string;
  nombre: string;
  apellido: string;
  tipo_usuario: 'Inversionista' | 'Admin';
  estado: boolean;
  creado: string;
  modificado: string;
  role: 'Inversionista' | 'Admin'; // Agregado para frontend
  name: string; // Agregado para frontend
}

// Definición de la interfaz del contexto
interface AuthContextType {
  user: User | null; // Usuario actual o null si no está autenticado
  isAuthenticated: boolean; // Estado de autenticación
  login: (email: string, password: string) => Promise<boolean>; // Función de login
  register: (data: RegisterRequest) => Promise<boolean>; // Función de registro
  logout: () => void; // Función de logout
  loading: boolean; // Estado de carga
  error: string | null; // Error de autenticación
}

// Creación del contexto con valor inicial undefined
const AuthContext = createContext<AuthContextType | undefined>(undefined);

/**
 * AuthProvider - Proveedor del contexto de autenticación
 * Envuelve la aplicación para proporcionar funcionalidad de autenticación
 */
export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  // Estado del usuario actual
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Función de login con API real
   * @param email - Email del usuario
   * @param password - Contraseña del usuario
   * @returns Promise<boolean> - true si login exitoso, false si falla
   */
  const login = async (email: string, password: string): Promise<boolean> => {
    setLoading(true);
    setError(null);

    try {
      const response = await apiService.login({ email, password });
      // Validar que response.user existe antes de mapear
      if (response.user) {
        const mappedUser = {
          ...response.user,
          role: response.user.tipo_usuario,
          name: response.user.nombre,
        };
        setUser(mappedUser);
        localStorage.setItem('user', JSON.stringify(mappedUser));
        return true;
      } else {
        setError('No se recibió usuario del backend');
        return false;
      }
    } catch (error) {
      const apiError = error as ApiError;
      setError(apiError.message);
      return false;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Función de registro
   * @param data - Datos del usuario a registrar
   * @returns Promise<boolean> - true si registro exitoso, false si falla
   */
  const register = async (data: RegisterRequest): Promise<boolean> => {
    setLoading(true);
    setError(null);

    try {
      const newUser = await apiService.register(data);
      // Después del registro, hacer login automático
      const loginSuccess = await login(data.email, data.password);
      return loginSuccess;
    } catch (error) {
      const apiError = error as ApiError;
      setError(apiError.message);
      return false;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Función de logout
   * Limpia el estado del usuario y los tokens
   */
  const logout = () => {
    apiService.logout();
    setUser(null);
    setError(null);
  };

  // Cargar usuario desde localStorage al iniciar (persistencia de sesión)
  React.useEffect(() => {
    const savedUser = apiService.getCurrentUser();
    if (savedUser && apiService.isAuthenticated() && savedUser.tipo_usuario && savedUser.nombre) {
      // Mapear campos si existen
      const mappedUser = {
        ...savedUser,
        role: savedUser.tipo_usuario,
        name: savedUser.nombre,
      };
      setUser(mappedUser);
    } else {
      setUser(null);
    }
  }, []);

  // Valor del contexto que se proporciona a los componentes hijos
  const value: AuthContextType = {
    user,
    isAuthenticated: !!user && apiService.isAuthenticated(),
    login,
    register,
    logout,
    loading,
    error,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

/**
 * Hook personalizado para usar el contexto de autenticación
 * @returns AuthContextType
 * @throws Error si se usa fuera de AuthProvider
 */
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth debe ser usado dentro de un AuthProvider');
  }
  return context;
};
