from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/carrusel')
def carrusel():
    return render_template('carrusel_slider/carrusel.html')

@main.route('/slider')
def slider():
    return render_template('carrusel_slider/slider.html')