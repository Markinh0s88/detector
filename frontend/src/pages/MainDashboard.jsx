import React, { useState, useEffect } from 'react';
import { Camera, Settings, Plus, Bell, Check, X } from 'lucide-react';

const MainDashboard = () => {
  const [latestPlate, setLatestPlate] = useState(null);
  const [isRegistered, setIsRegistered] = useState(false);
  const [showRegisterModal, setShowRegisterModal] = useState(false);

  // Simula a detecção de uma placa
  useEffect(() => {
    const interval = setInterval(() => {
      // TODO: Implementar detecção real de placas
      const mockPlate = "ABC1234";
      setLatestPlate(mockPlate);
      setIsRegistered(Math.random() > 0.5);
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const handleRegisterPlate = () => {
    // TODO: Implementar registro de placa
    setShowRegisterModal(false);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Feed da câmera */}
          <div className="bg-white rounded-lg shadow-md p-4">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold">Câmera ao Vivo</h2>
              <button className="p-2 rounded-full hover:bg-gray-100">
                <Settings className="h-5 w-5 text-gray-600" />
              </button>
            </div>
            <div className="bg-gray-800 h-96 rounded-lg flex items-center justify-center">
              <Camera className="h-16 w-16 text-gray-400" />
            </div>
          </div>

          {/* Painel de detecção */}
          <div className="bg-white rounded-lg shadow-md p-4">
            <h2 className="text-xl font-semibold mb-4">Última Detecção</h2>
            {latestPlate && (
              <div className="space-y-4">
                <div className="p-4 border rounded-lg">
                  <p className="text-2xl font-bold text-center">{latestPlate}</p>
                  <div className="mt-4 flex justify-center">
                    {isRegistered ? (
                      <div className="flex items-center text-green-600">
                        <Check className="h-6 w-6 mr-2" />
                        <span>Placa Registrada</span>
                      </div>
                    ) : (
                      <div className="flex items-center text-red-600">
                        <X className="h-6 w-6 mr-2" />
                        <span>Placa Não Registrada</span>
                      </div>
                    )}
                  </div>
                </div>

                {!isRegistered && (
                  <button
                    onClick={() => setShowRegisterModal(true)}
                    className="w-full py-2 px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center justify-center"
                  >
                    <Plus className="h-5 w-5 mr-2" />
                    Registrar Nova Placa
                  </button>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Modal de Registro */}
      {showRegisterModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white rounded-lg p-6 w-96">
            <h3 className="text-lg font-semibold mb-4">Registrar Nova Placa</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Placa
                </label>
                <input
                  type="text"
                  value={latestPlate}
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
                  readOnly
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Proprietário
                </label>
                <input
                  type="text"
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Apartamento
                </label>
                <input
                  type="text"
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
                />
              </div>
              <div className="flex space-x-4">
                <button
                  onClick={() => setShowRegisterModal(false)}
                  className="flex-1 py-2 px-4 border border-gray-300 rounded-md hover:bg-gray-50"
                >
                  Cancelar
                </button>
                <button
                  onClick={handleRegisterPlate}
                  className="flex-1 py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Registrar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MainDashboard;
