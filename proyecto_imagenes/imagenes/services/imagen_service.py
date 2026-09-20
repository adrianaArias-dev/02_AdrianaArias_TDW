import os
import uuid

from flask import current_app
from PIL import Image
from werkzeug.utils import secure_filename


def extension_permitida(nombre_archivo: str, extensiones_permitidas: set) -> bool:
    return (
        "." in nombre_archivo
        and nombre_archivo.rsplit(".", 1)[1].lower() in extensiones_permitidas
    )


def _optimizar_imagen(ruta_entrada: str, ruta_salida: str, ancho_max: int = 900, calidad: int = 80):
    with Image.open(ruta_entrada) as img:
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        if img.width > ancho_max:
            proporcion = ancho_max / float(img.width)
            nuevo_alto = int(img.height * proporcion)
            img = img.resize((ancho_max, nuevo_alto), Image.LANCZOS)

        img.save(ruta_salida, "JPEG", optimize=True, quality=calidad)


def guardar_y_optimizar_imagen(archivo) -> dict:
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    processed_folder = current_app.config["PROCESSED_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(processed_folder, exist_ok=True)

    nombre_seguro = secure_filename(archivo.filename)
    identificador = uuid.uuid4().hex[:8]

    nombre_original = f"{identificador}_{nombre_seguro}"
    ruta_original = os.path.join(upload_folder, nombre_original)
    archivo.save(ruta_original)

    nombre_procesado = f"{identificador}_optimizada.jpg"
    ruta_procesada = os.path.join(processed_folder, nombre_procesado)
    try:
        _optimizar_imagen(ruta_original, ruta_procesada)
    except Exception:
        if os.path.exists(ruta_original):
            os.remove(ruta_original)
        if os.path.exists(ruta_procesada):
            os.remove(ruta_procesada)
        raise

    return {
        "archivo_original": nombre_original,
        "archivo_procesado": nombre_procesado,
        "peso_original": os.path.getsize(ruta_original),
        "peso_procesado": os.path.getsize(ruta_procesada),
    }
