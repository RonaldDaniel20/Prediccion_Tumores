from fastapi import APIRouter
from dependencias import get_request_data
from fastapi import UploadFile, HTTPException, Depends
from PIL import Image
from services import model_service


router = APIRouter(
    prefix = "/modelo",
    tags = ["modelo"],
)

@router.post("/predecir")
def predecir(imagen_validad: UploadFile = Depends(get_request_data) ): 
    try:
        tumor, confianza = model_service.realizar_prediccion(imagen_validad)
        return {
            "status": "ok",
            "message": "La imagen ha sido procesada con éxito",
            "tipo_de_tumor": f"{tumor}",
            "confianza": f"{confianza:.2f}%"
        }
    except Exception as e:
        HTTPException(status_code=500, detail="Hubo un error en el servidor")
    



