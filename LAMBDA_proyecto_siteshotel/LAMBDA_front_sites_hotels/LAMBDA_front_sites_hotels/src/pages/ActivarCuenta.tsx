import React, { useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

const ActivarCuenta: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const uid = searchParams.get('uid');
  const token = searchParams.get('token');
  const [password, setPassword] = useState('');
  const [mensaje, setMensaje] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/api/usuarios/activar/', {
        uid,
        token,
        password,
      });
      setMensaje('¡Cuenta activada! Ahora puedes iniciar sesión.');
      setTimeout(() => navigate('/login'), 2000);
    } catch (error: any) {
      setMensaje(error.response?.data?.mensaje || 'Error al activar la cuenta');
    }
  };

  return (
    <div>
      <h2>Activar cuenta</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="password"
          placeholder="Nueva contraseña"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
        />
        <button type="submit">Activar</button>
      </form>
      {mensaje && <p>{mensaje}</p>}
    </div>
  );
};

export default ActivarCuenta;