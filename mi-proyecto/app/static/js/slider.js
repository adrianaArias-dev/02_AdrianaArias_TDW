const track = document.getElementById('slider-track');
const dotsContainer = document.getElementById('slider-dots');
const totalSlides = track.children.length;
let actual = 0;

function crearDots() {
    for (let i = 0; i < totalSlides; i++) {
        const dot = document.createElement('span');
        dot.className = 'dot' + (i === 0 ? ' active' : '');
        dot.onclick = () => irASlide(i);
        dotsContainer.appendChild(dot);
    }
}

function actualizar() {
    track.style.transform = `translateX(-${actual * 100}%)`;
    document.querySelectorAll('.dot').forEach((dot, i) => {
        dot.classList.toggle('active', i === actual);
    });
}

function cambiarSlide(direccion) {
    actual = (actual + direccion + totalSlides) % totalSlides;
    actualizar();
}

function irASlide(indice) {
    actual = indice;
    actualizar();
}

crearDots();
setInterval(() => cambiarSlide(1), 4000); // auto-avance cada 4 seg