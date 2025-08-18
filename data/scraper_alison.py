from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from db.connection import get_connection
from datetime import datetime
import time
import random
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://alison.com"
DELAY_RANGE = tuple(map(int, os.getenv("DELAY_RANGE", "5,10").split(",")))  # mayor para evitar bloqueos

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

def obtener_descripcion_curso(driver, url_curso):
    try:
        driver.get(url_curso)
        time.sleep(3)  # espera a que cargue la página

        # Ajusta el selector según la estructura actual de Alison para la descripción
        desc_elem = driver.find_element(By.CSS_SELECTOR, "div.course-description")
        descripcion = desc_elem.text.strip()
        return descripcion
    except Exception as e:
        print(f"⚠️ Error al obtener descripción para {url_curso}: {e}")
        return ""

def buscar_cursos_por_categoria(nombre_categoria, max_paginas=1):
    opciones = Options()
    opciones.add_argument("--headless")
    opciones.add_argument("--disable-gpu")
    opciones.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=opciones)

    cursos = []

    for pagina in range(1, max_paginas + 1):
        url = f"{BASE_URL}/courses?query={nombre_categoria}&page={pagina}"
        print(f"🔍 Buscando cursos para: {nombre_categoria} - página {pagina}")
        driver.get(url)
        time.sleep(5)

        cards = driver.find_elements(By.CSS_SELECTOR, "div.card.card--white")
        if not cards:
            print(f"⚠️ No se encontraron cursos en la página {pagina} para {nombre_categoria}")
            break

        for card in cards:
            try:
                titulo = card.find_element(By.TAG_NAME, "h3").text
                url_curso = card.find_element(By.CSS_SELECTOR, "a.card__more").get_attribute("href")

                certificado = 0
                try:
                    certificado_tag = card.find_element(By.CSS_SELECTOR, "span.course-type-1")
                    if "certificate" in certificado_tag.text.lower():
                        certificado = 1
                except:
                    pass

                # Obtener descripción real del curso
                descripcion = obtener_descripcion_curso(driver, url_curso)

                cursos.append({
                    "titulo": titulo,
                    "descripcion": descripcion,
                    "url": url_curso,
                    "certificado": certificado
                })
            except Exception as e:
                print(f"⚠️ Error extrayendo curso en '{nombre_categoria}': {e}")

        time.sleep(random.uniform(*DELAY_RANGE))

    driver.quit()
    return cursos

def guardar_cursos(cursos, categoria_id):
    conn = get_connection()
    if not conn:
        print("⚠️ No se pudo conectar a la base de datos para guardar cursos.")
        return 0

    cursor = conn.cursor()
    nuevos = 0
    for curso in cursos:
        cursor.execute("SELECT COUNT(*) FROM recursos WHERE url = %s", (curso["url"],))
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO recursos 
                (titulo, descripcion, url, categoria_id, fecha_publicacion, disponible, certificado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                curso["titulo"],
                curso["descripcion"],
                curso["url"],
                categoria_id,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                1,
                curso["certificado"]
            ))
            nuevos += 1
    conn.commit()
    cursor.close()
    conn.close()
    return nuevos

def main():
    categorias = obtener_categorias()
    if not categorias:
        print("⚠️ No se pudieron cargar categorías desde la BD.")
        return

    total_nuevos = 0
    for cat_id, cat_nombre in categorias.items():
        print(f"Buscando cursos para categoría: {cat_nombre}")
        cursos = buscar_cursos_por_categoria(cat_nombre)
        if cursos:
            insertados = guardar_cursos(cursos, cat_id)
            print(f"✅ Insertados {insertados} cursos nuevos en '{cat_nombre}'")
            total_nuevos += insertados
        else:
            print(f"ℹ️ No se encontraron cursos para '{cat_nombre}'")

    print(f"\n🎉 Total de cursos insertados: {total_nuevos}")

if __name__ == "__main__":
    main()
