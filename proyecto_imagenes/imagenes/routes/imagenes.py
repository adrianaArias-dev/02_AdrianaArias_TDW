from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

from ..database import db
from ..models.imagen import Imagen
from ..services.imagen_service import (
    extension_permitida,
    guardar_y_optimizar_imagen,
)

imagenes_bp = Blueprint("imagenes", __name__)


@imagenes_bp.route("/")
def index():
    imagenes = Imagen.query.order_by(Imagen.fecha.desc()).all()
    return render_template("imagenes/index.html", imagenes=imagenes)


@imagenes_bp.route("/nueva")
def nueva():
    return render_template("imagenes/form.html")


@imagenes_bp.route("/procesar", methods=["POST"])
def procesar():
    nombre = request.form.get("nombre", "").strip()
    email = request.form.get("email", "").strip()
    comentario = request.form.get("comentario", "").strip()
    imagen = request.files.get("imagen")

    errores = []

    if not nombre or len(nombre) < 3:
        errores.append("El nombre debe tener al menos 3 caracteres.")

    if "@" not in email or "." not in email.split("@")[-1]:
        errores.append("El correo electrónico no es válido.")

    if not imagen or imagen.filename == "":
        errores.append("Debe seleccionar una imagen.")
    elif not extension_permitida(imagen.filename, current_app.config["EXTENSIONES_PERMITIDAS"]):
        errores.append("Formato de imagen no permitido (use png, jpg, jpeg, gif o webp).")

    if errores:
        for error in errores:
            flash(error, "error")
        return redirect(url_for("imagenes.nueva"))

    try:
        datos_procesado = guardar_y_optimizar_imagen(imagen)
    except Exception as exc:
        flash(f"Ocurrió un error al procesar la imagen: {exc}", "error")
        return redirect(url_for("imagenes.nueva"))

    registro = Imagen(
        nombre=nombre,
        email=email,
        comentario=comentario,
        archivo_original=datos_procesado["archivo_original"],
        archivo_procesado=datos_procesado["archivo_procesado"],
        peso_original=datos_procesado["peso_original"],
        peso_procesado=datos_procesado["peso_procesado"],
    )
    db.session.add(registro)
    db.session.commit()

    flash("Imagen procesada y optimizada correctamente.", "exito")
    return redirect(url_for("imagenes.index"))
