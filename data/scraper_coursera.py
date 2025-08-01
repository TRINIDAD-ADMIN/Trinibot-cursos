# Scraper for Coursera
import requests
from bs4 import BeautifulSoup
from db.connection import get_connection
from datetime import datetime
import time

BASE_URL = "https://www.coursera.org"
LISTING_URL = "https://www.coursera.org/courses?query=free"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def obtener_cursos_coursera(paginas=1):
    cursos = []

    for pagina in range(paginas):
        print(f"📦 Procesando página {pagina + 1} de Coursera...")

        url = f"{LISTING_URL}&page={pagina + 1}"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        tarjetas = soup.select("li.ais-InfiniteHits-item")

        for card in tarjetas:
            try:
                a_tag = card.select_one("a")
                if not a_tag:
                    continue

                url_curso = BASE_URL + a_tag["href"]
                titulo = card.select_one("h2") or card.select_one("h3")
                descripcion = card.select_one("p")

                cursos.append({
                    "titulo": titulo.get_text(strip=True) if titulo else "Curso sin título",
                    "descripcion": descripcion.get_text(strip=True) if descripcion else "Sin descripción",
                    "url": url_curso
                })

                time.sleep(0.5)  # para evitar bloqueo
            except Exception as e:
                print(f"⚠️ Error procesando un curso: {e}")
                continue

    return cursos

def guardar_en_bd(cursos, categoria_id=16):  # Usa la categoría 16 o la que tengas para Coursera
    conn = get_connection()
    cursor = conn.cursor()
    nuevos = 0

    for curso in cursos:
        cursor.execute("SELECT COUNT(*) FROM recursos WHERE url = %s", (curso["url"],))
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO recursos (titulo, descripcion, url, categoria_id, fecha_publicacion, disponible)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                curso["titulo"],
                curso["descripcion"],
                curso["url"],
                categoria_id,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                1
            ))
            nuevos += 1

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Guardados {nuevos} nuevos cursos en la BD.")

if __name__ == "__main__":
    cursos = obtener_cursos_coursera(paginas=2)
    guardar_en_bd(cursos, categoria_id=16)  # Asegúrate que exista esta categoría
