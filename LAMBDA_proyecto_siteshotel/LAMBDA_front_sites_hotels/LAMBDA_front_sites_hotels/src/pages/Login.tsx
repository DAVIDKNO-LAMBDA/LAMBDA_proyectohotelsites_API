/**
 * Login - Página de Inicio de Sesión
 * 
 * Esta página permite a los usuarios autenticarse en la aplicación.
 * Características:
 * - Login con email y contraseña
 * - Validación de formulario
 * - Redirección automática al dashboard después del login
 * - Integración con backend Django usando JWT
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { BarChart3, Lock, Mail } from 'lucide-react';
import { toast } from 'sonner';

/**
 * Componente de la página de Login
 */
export const Login: React.FC = () => {
  // Estado del formulario
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // Hooks
  const navigate = useNavigate();
  const { login, isAuthenticated, loading, error } = useAuth();

  /**
   * Redireccionar si ya está autenticado
   */
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/');
    }
  }, [isAuthenticated, navigate]);

  /**
   * Mostrar errores de autenticación
   */
  useEffect(() => {
    if (error) {
      toast.error(error);
    }
  }, [error]);

  /**
   * Manejar submit del formulario
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validación básica
    if (!email || !password) {
      toast.error('Por favor completa todos los campos');
      return;
    }

    if (password.length < 4) {
      toast.error('La contraseña debe tener al menos 4 caracteres');
      return;
    }

    try {
      // Intentar login con API real
      const success = await login(email, password);

      if (success) {
        toast.success('¡Inicio de sesión exitoso!');
        navigate('/');
      }
      // Los errores se manejan automáticamente en el contexto
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-primary p-4">
      <Card className="w-full max-w-md">
        {/* Header con logo y título */}
        <CardHeader className="space-y-1 text-center">
          <div className="flex justify-center mb-4">
            <div className="bg-primary rounded-full p-3">
              <BarChart3 className="w-8 h-8 text-primary-foreground" />
            </div>
          </div>
          <CardTitle className="text-2xl font-bold">
            Hotel Sites Dashboard
          </CardTitle>
          <CardDescription>
            Plataforma de Business Intelligence Hotelero
          </CardDescription>
        </CardHeader>

        {/* Formulario de login */}
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Campo de email */}
            <div className="space-y-2">
              <Label htmlFor="email">
                <div className="flex items-center gap-2">
                  <Mail className="w-4 h-4" />
                  Email
                </div>
              </Label>
              <Input
                id="email"
                type="email"
                placeholder="usuario@ejemplo.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={loading}
                required
              />
            </div>

            {/* Campo de contraseña */}
            <div className="space-y-2">
              <Label htmlFor="password">
                <div className="flex items-center gap-2">
                  <Lock className="w-4 h-4" />
                  Contraseña
                </div>
              </Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={loading}
                required
              />
            </div>

            {/* Botón de login */}
            <Button
              type="submit"
              className="w-full"
              disabled={loading}
            >
              {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
            </Button>

            {/* Nota sobre backend real */}
            <div className="mt-4 p-3 bg-muted rounded-lg">
              <p className="text-xs text-muted-foreground text-center">
                <strong>Conectado al backend:</strong> Usa las credenciales de usuarios registrados en el sistema.
                Los roles se asignan automáticamente según el tipo_usuario.
              </p>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default Login;
