from __future__ import annotations
from pathlib import Path
import sys

HTML_PATH = Path(__file__).parent / "index.html"

def read_html() -> str:
    try:
        return HTML_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        sys.exit("index.html no encontrado; ejecuta desde la raíz del proyecto.")

def slice_section(html: str, section_id: str) -> str:
    marker = f'id="{section_id}"'
    try:
        start = html.index(marker)
    except ValueError:
        raise AssertionError(f"No se encontró la sección #{section_id} en el HTML.")
    end = html.find("</section>", start)
    if end == -1:
        raise AssertionError(f"La sección #{section_id} no tiene cierre </section>.")
    return html[start:end]

def assert_in_html(html: str, needle: str) -> None:
    if needle not in html:
        raise AssertionError(f"Falta el fragmento obligatorio: {needle!r}")

def run_checks() -> None:
    html = read_html()

    # Navegación principal
    for label in ["Inicio", "Servicios", "Estilistas", "Galería", "Reseñas", "Promos", "Contacto"]:
        assert_in_html(html, f">{label}<")

    # Hero CTAs
    for cta in ["Reservar cita", "Ver servicios"]:
        assert_in_html(html, cta)

    # Servicios: al menos 6 tarjetas dentro de la sección correspondiente.
    servicios = slice_section(html, "servicios")
    service_cards = servicios.count('class="card"')
    if service_cards < 6:
        raise AssertionError(f"Se esperaban al menos 6 servicios y se encontraron {service_cards}.")

    # Estilistas: mínimo 3 perfiles
    estilistas = slice_section(html, "estilistas")
    stylist_cards = estilistas.count('class="card"')
    if stylist_cards < 3:
        raise AssertionError(f"Se esperaban 3 estilistas y se encontraron {stylist_cards}.")

    # Galería: 8 tarjetas con toggle
    galeria = slice_section(html, "galeria")
    gallery_cards = galeria.count('gallery-card')
    if gallery_cards < 8:
        raise AssertionError(f"Se esperaban 8 elementos en galería y se encontraron {gallery_cards}.")
    toggles = galeria.count('data-gallery-toggle')
    if toggles < 8:
        raise AssertionError(f"Cada tarjeta debe tener toggle; se encontraron {toggles} de 8.")

    # Reseñas: 5 entradas
    resenas = slice_section(html, "reseñas")
    review_cards = resenas.count('class="review')
    if review_cards < 5:
        raise AssertionError(f"Se esperaban 5 reseñas y se encontraron {review_cards}.")

    # Promos: botones y dos promociones
    promos = slice_section(html, "promos")
    assert_in_html(promos, "Quiero la promo")
    promo_items = promos.count('class="promo-item"')
    if promo_items < 2:
        raise AssertionError(f"Se esperaban 2 promos y se encontraron {promo_items}.")

    # Formulario de contacto: campos requeridos
    contacto = slice_section(html, "contacto")
    for field_id in ["nombre", "telefono", "servicio", "fecha", "hora", "mensaje"]:
        assert_in_html(contacto, f'id="{field_id}"')

    print("✅ Estructura mínima verificada: navegación, hero, servicios, estilistas, galería, reseñas, promos y contacto.")

if __name__ == "__main__":
    run_checks()
