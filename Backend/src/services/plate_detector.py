# backend/src/services/plate_detector.py
import cv2
import numpy as np
from easyocr import Reader
import torch

class PlateDetector:
    def __init__(self):
        # Inicializar o EasyOCR para reconhecimento de texto
        self.reader = Reader(['en'])
        
        # Carregar o modelo YOLOv5 para detecção de placas
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', 
                                  path='models/best.pt')  # Substitua pelo caminho do seu modelo treinado
        
        # Configurações
        self.min_confidence = 0.8
        self.min_plate_size = 100
        self.max_plate_size = 1000

    def preprocess_image(self, image):
        """Pré-processa a imagem para melhorar a detecção"""
        # Converter para escala de cinza
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Aplicar blur para reduzir ruído
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        
        # Equalização do histograma para melhorar o contraste
        equalized = cv2.equalizeHist(blur)
        
        return equalized

    async def detect_plates(self, image):
        """Detecta placas de carro na imagem"""
        results = []
        
        # Pré-processar a imagem
        processed_image = self.preprocess_image(image)
        
        # Detectar objetos usando YOLOv5
        detections = self.model(processed_image)
        
        # Processar cada detecção
        for det in detections.xyxy[0]:
            if det[4] >= self.min_confidence:  # Verificar confiança
                x1, y1, x2, y2 = map(int, det[:4])
                
                # Verificar tamanho da placa
                width = x2 - x1
                height = y2 - y1
                if (width < self.min_plate_size or 
                    height < self.min_plate_size or
                    width > self.max_plate_size or
                    height > self.max_plate_size):
                    continue
                
                # Extrair região da placa
                plate_region = processed_image[y1:y2, x1:x2]
                
                # Reconhecer texto usando EasyOCR
                ocr_result = self.reader.readtext(plate_region)
                
                # Processar resultados do OCR
                for bbox, text, conf in ocr_result:
                    # Filtrar apenas texto que parece uma placa válida
                    if self.is_valid_plate(text):
                        results.append({
                            'plate_number': text,
                            'confidence': float(conf),
                            'bbox': [x1, y1, x2, y2]
                        })
        
        return results

    def is_valid_plate(self, text):
        """Verifica se o texto detectado parece uma placa válida"""
        # Remover espaços e caracteres especiais
        text = ''.join(e for e in text if e.isalnum())
        
        # Verificar comprimento típico de uma placa brasileira
        if len(text) != 7:
            return False
        
        # Verificar padrão básico (3 letras + 4 números para placas antigas)
        # ou (4 letras + 3 números para placas Mercosul)
        old_pattern = (text[:3].isalpha() and text[3:].isdigit())
        mercosul_pattern = (text[:4].isalpha() and text[4:].isdigit())
        
        return old_pattern or mercosul_pattern

    def draw_detection(self, image, detection):
        """Desenha a detecção na imagem"""
        x1, y1, x2, y2 = detection['bbox']
        plate_number = detection['plate_number']
        confidence = detection['confidence']
        
        # Desenhar retângulo
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Adicionar texto
        text = f"{plate_number} ({confidence:.2f})"
        cv2.putText(image, text, (x1, y1-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        return image

    def update_settings(self, settings):
        """Atualiza as configurações do detector"""
        self.min_confidence = settings.get('detection_confidence', self.min_confidence)
        self.min_plate_size = settings.get('min_plate_size', self.min_plate_size)
        self.max_plate_size = settings.get('max_plate_size', self.max_plate_size)
