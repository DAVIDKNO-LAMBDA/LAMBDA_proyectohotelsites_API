import React, { useState } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

const Usuarios: React.FC = () => {
  const { user } = useAuth();
  const [email, setEmail] = useState(''); 
  const [username, setUsername] = useState('');
  const [grupo, setGrupo] = useState('Inversionista');
  const [mensaje, setMensaje] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/api/usuarios/crear/', {
        email,
        username,
        grupo,
      }, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
      });
      setMensaje('Usuario creado y email enviado.');
      setEmail('');
      setUsername('');
      setGrupo('Inversionista');
    } catch (error: any) {
      setMensaje(error.response?.data?.error || 'Error al crear usuario');
    }
  };

  if (user?.role !== 'Admin') {
    return <p>No tienes permisos para ver esta página.</p>;
  }

  return (
    <div>
      <h2>Crear usuario</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Nombre de usuario"
          value={username}
          onChange={e => setUsername(e.target.value)}
          required
        />
        <select value={grupo} onChange={e => setGrupo(e.target.value)}>
          <option value="Admin">Admin</option>
          <option value="Inversionista">Inversionista</option>
        </select>
        <button type="submit">Crear usuario</button>
      </form>
      {mensaje && <p>{mensaje}</p>}
    </div>
  );
};

export default Usuarios;
