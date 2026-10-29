import io
import json
import logging
from fastapi import File, UploadFile, HTTPException, Depends
from google import genai
from google.genai import types
from PIL import Image
from config import get_settings
from models import model_request_data


API_KEY = get_settings().API_KEY
PROMT = get_settings().PROMT


cliente = genai.Client(api_key= API_KEY)

logger = logging.getLogger(__name__)

def get_request_data( imagen: UploadFile = File(...)) -> UploadFile:
    
    if not imagen.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo subido no es una imagen válida")

    try:

        content = imagen.file.read()
        imagen.file.seek(0)
        image = Image.open(io.BytesIO(content))

        response_model = cliente.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents = [
                image,
                PROMT
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=model_request_data.RespuestaModelo
            )

        )

        logger.info("El modelo ha respondido")
        respuesta = json.loads(response_model.text)
        if(respuesta['es_resonancia_cerebro'] == False):
           raise HTTPException(status_code=400, detail=f"La imágen no es válida")
        return imagen

    except HTTPException:
        raise
    except Exception as e:
        logger.warning("El modelo de gemini no proceso la imagen ")
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")
    



