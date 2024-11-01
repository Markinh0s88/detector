# backend/src/services/camera_service.py
import cv2
import asyncio
import numpy as np
from typing import Optional

class CameraService:
    def __init__(self):
        self.camera = None
        self.settings = {
            'ip': '192.168.1.100',
            'port': '8080',
            'username': 'admin',
            'password': '',
            'stream_path': '/video'
        }
        self.is_running = False
        self.last_frame = None
        self.lock = asyncio.Lock()

    async def connect(self):
        """Conecta à câmera IP"""
        if self.camera is not None:
            self.release()

        # Construir URL da câmera
        auth = f"{self.settings['username']}:{self.settings['password']}@" if self.settings['username'] else ""
        url = f"rtsp://{auth}{self.settings['ip']}:{self.settings['port']}{self.settings['stream_path']}"

        try:
            self.camera = cv2.VideoCapture(url)
            if not self.camera.isOpened():
                raise Exception("Não foi possível conectar à câmera")
            
            self.is_running = True
            asyncio.create_task(self._frame_grabber())
            return True
        except Exception as e:
            print(f"Erro ao conectar à câmera: {str(e)}")
            return False

    async def _frame_grabber(self):
        """Loop assíncrono para capturar frames da câmera"""
        while self.is_running and self.camera is not None:
            ret, frame = self.camera.read()
            if ret:
                async with self.lock:
                    self.last_frame = frame
            await asyncio.sleep(0.033)  # ~30 FPS

    async def get_frame(self) -> Optional[np.ndarray]:
        """Retorna o último frame capturado"""
        async with self.lock:
            if self.last_frame is not None:
                return self.last_frame.copy()
        return None

    def release(self):
        """Libera os recursos da câmera"""
        self.is_running = False
        if self.camera is not None:
            self.camera.release()
            self.camera = None

    async def update_settings(self, new_settings: dict):
        """Atualiza as configurações da câmera e reconecta"""
        self.settings.update(new_settings)
        return await self.connect()

    async def test_connection(self) -> bool:
        """Testa a conexão com a câmera"""
        try:
            success = await self.connect()
            if success:
                # Tentar capturar um frame para confirmar que está funcionando
                frame = await self.get_frame()
                if frame is not None:
                    return True
            return False
        except Exception as e:
            print(f"Erro ao testar conexão: {str(e)}")
            return False
        finally:
            self.release()

    async def get_stream_url(self) -> str:
        """Retorna a URL do stream da câmera"""
        auth = f"{self.settings['username']}:{self.settings['password']}@" if self.settings['username'] else ""
        return f"rtsp://{auth}{self.settings['ip']}:{self.settings['port']}{self.settings['stream_path']}"

    def is_connected(self) -> bool:
        """Verifica se a câmera está conectada e funcionando"""
        return self.camera is not None and self.camera.isOpened()
