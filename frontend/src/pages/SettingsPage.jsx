import React, { useState } from 'react';
import { Save, Camera, Volume2, Database, ArrowLeft } from 'lucide-react';

const SettingsPage = () => {
  const [settings, setSettings] = useState({
    camera: {
      ip: '192.168.1.100',
      port: '8080',
      username: 'admin',
      password: '',
      streamPath: '/video'
    },
    sound: {
      enableSound: true,
      successVolume: 80,
      errorVolume: 70
    },
    detection: {
      confidence: 0.8,
      minPlateSize: 100,
      maxPlateSize: 1000
    }
  });

  const handleSave = async () => {
    // TODO: Implementar salvamento das configurações
    console.log('Saving settings:', settings);
  };

  const handleTestConnection = async () => {
    // TODO: Implementar teste de conexão com a câmera
    console.log('Testing camera connection...');
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-4xl mx-auto p-6">
        <div className="flex items-center mb-6">
          <button className="p-2 hover:bg-gray-200 rounded-full">
            <ArrowLeft className="h-6 w-6" />
          </button>
          <h1 className="text-2xl font-bold ml-2">Configurações do Sistema</h1>
        </div>

        <div className="space-y-6">
          {/* Configurações da Câmera */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center mb-4">
              <Camera className="h-6 w-6 text-gray-600 mr-2" />
              <h2 className="text-xl font-semibold">Configurações da Câmera IP</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Endereço IP
                </label>
                <input
                  type="text"
                  value={settings.camera.ip}
                  onChange={(e) => setSettings({
                    ...settings,
                    camera: { ...settings.camera, ip: e.target.value }
                  })}
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Porta
                </label>
                <input
                  type="text"
                  value={settings.camera.port}
                  onChange={(e) => setSettings({
                    ...settings,
                    camera: { ...settings.camera, port: e.target.value }
                  })}
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Usuário
                </label>
                <input
                  type="text"
                  value={settings.camera.username}
                  onChange={(e) => setSettings({
                    ...settings,
                    camera: { ...settings.camera, username: e.target.value }
                  })}
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Senha
                </label>
                <input
                  type="password"
                  value={settings.camera.password}
                  onChange={(e) => setSettings({
                    ...settings,
                    camera: { ...settings.camera, password: e.target.value }
                  })}
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
                />
              </div>
            </div>
            <button
              onClick={handleTestConnection}
              className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Testar Conexão
            </button>
          </div>

          {/* Configurações de Som */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center mb-4">
              <Volume2 className="h-6 w-6 text-gray-600 mr-2" />
              <h2 className="text-xl font-semibold">Configurações de Som</h2>
            </div>
            <div className="space-y-4">
              <div className="flex items-center">
                <input
                  type="checkbox"
                  checked={settings.sound.enableSound}
                  onChange={(e) => setSettings({
                    ...settings,
                    sound: { ...settings.sound, enableSound: e.target.checked }
                  })}
                  className="h-4 w-4 text-blue-600 rounded"
                />
                <label className="ml-2 text-sm font-medium text-gray-700">
                  Ativar sons do sistema
                </label>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Volume do som de sucesso
                </label>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={settings.sound.successVolume}
                  onChange={(e) => setSettings({
                    ...settings,
                    sound: { ...settings.sound, successVolume: e.target.value }
                  })}
                  className="mt-1 block w-full"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Volume do som de erro
                </label>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={settings.sound.errorVolume}
                  onChange={(e) => setSettings({
                    ...settings,
                    sound: { ...settings.sound, errorVolume: e.target.value }
                  })}
                  className="mt-1 block w-full"
                />
              </div>
            </div>
          </div>

          {/* Configurações de Detecção */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center mb-4">
              <Database className="h-6 w-6 text-gray-600 mr-2" />
              <h2 className="text-xl font-semibold">Configurações de Detecção</h2>
            </div>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Confiança mínima (0-1)
                </label>
                <input
                  type="number"
                  min="0"
                  max="1"
                  step="0.1"
                  value={settings.detection.confidence}
                  onChange={(e) => setSettings({
                    ...settings,
                    detection: { ...settings.detection, confidence: parseFloat(e.target.value) }
                  })}
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Tamanho mínimo da placa (pixels)
                </label>
                <input
                  type="number"
                  value={settings.detection.minPlateSize}
                  onChange={(e) => setSettings({
                    ...settings,
                    detection: { ...settings.detection, minPlateSize: parseInt(e.target.value) }
                  })}
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Tamanho máximo da placa (pixels)
                </label>
                <input
                  type="number"
                  value={settings.detection.maxPlateSize}
                  onChange={(e) => setSettings({
                    ...settings,
                    detection: { ...settings.detection, maxPlateSize: parseInt(e.target.value) }
                  })}
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
                />
              </div>
            </div>
          </div>

          {/* Botão Salvar */}
          <div className="flex justify-end">
            <button
              onClick={handleSave}
              className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 flex items-center"
            >
              <Save className="h-5 w-5 mr-2" />
              Salvar Configurações
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
