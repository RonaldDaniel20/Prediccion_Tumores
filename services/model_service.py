import numpy as np
import onnxruntime as ort
import cv2
import io
import logging
from PIL import Image
from fastapi import UploadFile, File

session_ort = ort.InferenceSession('modelo.onnx', providers=['CPUExecutionProvider'])

tipos_de_tumores = {0: 'glioma', 1: 'meningioma', 2: 'notumor', 3: 'pituitary'}

logger = logging.getLogger(__name__)

def ApplyCLAHE(imagen, clip_limit = 2.0, tile_grid_size = (8,8)):
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    img_np = np.array(imagen)
    lab = cv2.cvtColor(img_np, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)

    l_clahe = clahe.apply(l)
    lab_clahe = cv2.merge((l_clahe, a, b))
    img_clahe = cv2.cvtColor(lab_clahe, cv2.COLOR_Lab2RGB)
    return Image.fromarray(img_clahe)

def DeleteNoise(imagen, k = 3):
    img_np = np.array(imagen)
    img_np = cv2.medianBlur(img_np, k)
    return Image.fromarray(img_np)


def preprocesar_imagen(imagen):
    imagen_clahe = ApplyCLAHE(imagen= imagen)
    imagen_delete_noise = DeleteNoise(imagen=imagen_clahe)

    img_np = np.array(imagen_delete_noise.resize((300, 300))).astype(np.float32) / 255

    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])

    img_np = (img_np - mean) / std

    img_np = np.transpose(img_np, (2,0,1))
    return np.expand_dims(img_np, axis=0).astype(np.float32)


def realizar_prediccion(imagen: UploadFile):

    contenido = imagen.file.read()
    imagen = Image.open(io.BytesIO(contenido)).convert("RGB")
    imagen_procesada = preprocesar_imagen(imagen)
    logger.debug("Se ha aplicado la eliminación de ruido y se aplicado clahe")

    inputs = {session_ort.get_inputs()[0].name: imagen_procesada }
    response_model = session_ort.run(None, inputs)[0]
    
    exp_salida = np.exp(response_model[0] - np.max(response_model[0]))
    probabilidades = exp_salida / exp_salida.sum()

    tipo_de_tumor = np.argmax(probabilidades)
    confianza = probabilidades[tipo_de_tumor] * 100
    tumor = tipos_de_tumores[tipo_de_tumor]
    logger.info("La inferencia de la red neuronal ha termiando con éxito")

    return tumor, confianza



 



