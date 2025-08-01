import requests
from bs4 import BeautifulSoup
from db.connection import get_connection
from datetime import datetime
import time

BASE_URL = "https://www.discudemy.com"

def obtener_cursos_discudemy(paginas=2):
    cursos = []

    for pagina in range(1, paginas + 1):
        print(f"📦 Procesando página {pagina} de DiscUdemy...")
        url = f"{BASE_URL}/all/{pagina}"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        tarjetas = soup.select("section.card")

        for card in tarjetas:
            try:
                titulo_tag = card.select_one("a.card-header")
                descripcion_tag = card.select_one("div.description")

                if not titulo_tag:
                    print("⚠️ Título no encontrado.")
                    continue

                titulo = titulo_tag.get_text(strip=True)
                url_intermedio = titulo_tag['href']
                descripcion = descripcion_tag.get_text(strip=True) if descripcion_tag else "Sin descripción"

                # Acceder a la URL intermedia para obtener enlace final de Udemy
                curso_resp = requests.get(url_intermedio, headers={"User-Agent": "Mozilla/5.0"})
                sub_soup = BeautifulSoup(curso_resp.text, "html.parser")
                final_link_tag = sub_soup.select_one(".ui.center.aligned.basic.segment a")

                if not final_link_tag or not final_link_tag.get("href"):
                    print("⚠️ Enlace Udemy no encontrado.")
                    continue

                url_udemy = final_link_tag["href"]

                cursos.append({
                    "titulo": titulo,
                    "descripcion": descripcion,
                    "url": url_udemy
                })

                time.sleep(1)  # Delay entre peticiones
            except Exception as e:
                print(f"⚠️ Error procesando un curso: {e}")
                continue

    return cursos

def guardar_en_bd(cursos, categoria_id=15):  # Asegúrate que la categoría 15 (Udemy) exista
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
    cursos = obtener_cursos_discudemy(paginas=2)
    guardar_en_bd(cursos, categoria_id=15)
