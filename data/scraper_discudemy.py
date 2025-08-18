import requests
from bs4 import BeautifulSoup
from db.connection import get_connection
from datetime import datetime
import time
import random
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://www.discudemy.com"
DELAY_RANGE = tuple(map(int, os.getenv("DELAY_RANGE", "1,3").split(",")))  # segundos

def obtener_categorias():
    """Obtiene categorías desde la BD en formato {id: nombre}"""
    conn = get_connection()
    categorias = {}
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre FROM categorias")
            for id_, nombre in cursor.fetchall():
                categorias[id_] = nombre.lower()
            cursor.close()
        finally:
            conn.close()
    return categorias

def asignar_categoria(categorias, titulo, descripcion):
    """Intenta asignar la categoría según palabras clave en título o descripción."""
    texto = f"{titulo} {descripcion}".lower()
    for cat_id, cat_nombre in categorias.items():
        if cat_nombre in texto:
            return cat_id
    return None

def tiene_certificado(titulo, descripcion, descripcion_intermedia=""):
    """
    Detecta si un curso tiene certificado buscando palabras clave 
    en título, descripción o descripción intermedia (pagina curso).
    """
    texto = f"{titulo} {descripcion} {descripcion_intermedia}".lower()
    keywords = ["certificado", "certificación", "certificate", "diploma", "acreditado"]
    return 1 if any(k in texto for k in keywords) else 0

def obtener_cursos_discudemy(paginas=2):
    cursos = []
    categorias = obtener_categorias()
    if not categorias:
        print("⚠️ No se pudieron cargar categorías desde la BD.")
        return cursos

    for pagina in range(1, paginas + 1):
        print(f"📦 Procesando página {pagina} de DiscUdemy...")
        url = f"{BASE_URL}/all/{pagina}"
        try:
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
                    if not url_intermedio.startswith("http"):
                        url_intermedio = BASE_URL + url_intermedio
                    descripcion = descripcion_tag.get_text(strip=True) if descripcion_tag else "Sin descripción"

                    # Acceder a la URL intermedia para obtener enlace final de Udemy y descripción extra
                    curso_resp = requests.get(url_intermedio, headers={"User-Agent": "Mozilla/5.0"})
                    sub_soup = BeautifulSoup(curso_resp.text, "html.parser")
                    final_link_tag = sub_soup.select_one(".ui.center.aligned.basic.segment a")

                    if not final_link_tag or not final_link_tag.get("href"):
                        print("⚠️ Enlace Udemy no encontrado.")
                        continue

                    url_udemy = final_link_tag["href"]

                    # Extraer descripción adicional de la página intermedia para mejor detección de certificado
                    descripcion_intermedia = ""
                    descripcion_extra_tag = sub_soup.select_one("div.description, div.content, div.course-description")
                    if descripcion_extra_tag:
                        descripcion_intermedia = descripcion_extra_tag.get_text(strip=True)

                    # Asignar categoría
                    categoria_id = asignar_categoria(categorias, titulo, descripcion)
                    if categoria_id is None:
                        categoria_id = 62  # Programación por defecto

                    # Detectar certificado
                    certificado = tiene_certificado(titulo, descripcion, descripcion_intermedia)

                    cursos.append({
                        "titulo": titulo,
                        "descripcion": descripcion,
                        "url": url_udemy,
                        "categoria_id": categoria_id,
                        "certificado": certificado
                    })

                    time.sleep(random.uniform(*DELAY_RANGE))  # Delay aleatorio
                except Exception as e:
                    print(f"⚠️ Error procesando un curso: {e}")
                    continue
        except Exception as e:
            print(f"⚠️ Error accediendo a la página {pagina}: {e}")
            continue

    return cursos

def guardar_en_bd(cursos):
    conn = get_connection()
    if not conn:
        print("⚠️ No se pudo conectar a la base de datos para guardar cursos.")
        return

    cursor = conn.cursor()
    nuevos = 0

    for curso in cursos:
        cursor.execute("SELECT COUNT(*) FROM recursos WHERE url = %s", (curso["url"],))
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO recursos (titulo, descripcion, url, categoria_id, fecha_publicacion, disponible, certificado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                curso["titulo"],
                curso["descripcion"],
                curso["url"],
                curso["categoria_id"],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                1,
                curso["certificado"]
            ))
            nuevos += 1

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Guardados {nuevos} nuevos cursos en la BD.")

if __name__ == "__main__":
    paginas_a_scrapear = 2
    cursos = obtener_cursos_discudemy(paginas=paginas_a_scrapear)
    if cursos:
        guardar_en_bd(cursos)
    else:
        print("No se encontraron cursos para guardar.")
