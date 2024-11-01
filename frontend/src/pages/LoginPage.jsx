import React, { useState } from 'react';
import { Lock, Building2 } from 'lucide-react';

const LoginPage = () => {
  const [credentials, setCredentials] = useState({
    condominiumId: '',
    password: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    // TODO: Implementar autenticação
    console.log('Login attempt:', credentials);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md w-96">
        <div className="text-center mb-8">
          <Building2 className="mx-auto h-12 w-12 text-blue-600" />
          <h2 className="mt-4 text-2xl font-bold text-gray-900">Sistema de Controle de Acesso</h2>
          <p className="mt-2 text-gray-600">Faça login para continuar</p>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              ID do Condomínio
            </label>
            <input
              type="text"
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none"
              value={credentials.condominiumId}
              onChange={(e) => setCredentials({
                ...credentials,
                condominiumId: e.target.value
              })}
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Senha
            </label>
            <input
              type="password"
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none"
              value={credentials.password}
              onChange={(e) => setCredentials({
                ...credentials,
                password: e.target.value
              })}
              required
            />
          </div>

          <button
            type="submit"
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <Lock className="h-5 w-5 mr-2" />
            Entrar
          </button>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
