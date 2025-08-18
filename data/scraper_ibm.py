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

BASE_URL = "https://skillsbuild.org"
CATALOGO_URL = "https://skillsbuild.org/es/college-students/course-catalog"
DELAY_RANGE = tuple(map(int, os.getenv("DELAY_RANGE", "5,10").split(",")))

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

def buscar_cursos_skillsbuild(categoria_id, nombre_categoria):
    opciones = Options()
    opciones.add_argument("--headless")
    opciones.add_argument("--disable-gpu")
    opciones.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=opciones)

    driver.get(CATALOGO_URL)
    time.sleep(8)  # Esperar carga completa

    cursos = []

    # Traer todos los cursos que aparezcan (ojo que no hay paginación visible)
    try:
        contenedores = driver.find_elements(By.CSS_SELECTOR, "div.mb-16.px-0.cds--subgrid.cds--subgrid--wide")
        print(f"🔍 Se encontraron {len(contenedores)} cursos en SkillsBuild para '{nombre_categoria}'")
        for cont in contenedores:
            try:
                titulo = cont.find_element(By.CSS_SELECTOR, "h3.cds--expressive-heading-03").text.strip()
                descripcion = cont.find_element(By.CSS_SELECTOR, "div.wysiwyg-content.cds--body-long-02").text.strip()
                url = cont.find_element(By.CSS_SELECTOR, "a.cds--btn.cds--btn--primary").get_attribute("href")

                certificado = 0  # Asumimos 0, no está claro si dan certificado

                # Tipo: Asumimos 'gratis' porque IBM SkillsBuild es gratuito
                tipo = 'gratis'

                cursos.append({
                    "titulo": titulo,
                    "descripcion": descripcion,
                    "url": url,
                    "certificado": certificado,
                    "tipo": tipo
                })
            except Exception as e:
                print(f"⚠️ Error extrayendo un curso: {e}")

    except Exception as e:
        print(f"⚠️ Error obteniendo cursos: {e}")

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
                (titulo, descripcion, url, categoria_id, fecha_publicacion, disponible, tipo, certificado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                curso["titulo"],
                curso["descripcion"],
                curso["url"],
                categoria_id,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                1,
                curso["tipo"],
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

    # Si la categoría 'programacion' (o similar) está en tu tabla, usa esa id para todos los cursos encontrados
    # Ejemplo: asignamos todos a la categoría con nombre que contenga "programacion"
    cat_prog_id = 62
    for cat_id, cat_nombre in categorias.items():
        if "programacion" in cat_nombre.lower() or "tecnologia" in cat_nombre.lower():
            cat_prog_id = cat_id
            break

    if not cat_prog_id:
        print("⚠️ No se encontró categoría 'programacion' o 'tecnologia' en BD para asignar cursos.")
        return

    print(f"Buscando cursos IBM SkillsBuild para categoría ID {cat_prog_id} (programacion/tecnologia)")

    cursos = buscar_cursos_skillsbuild(cat_prog_id, "programacion/tecnologia")
    if cursos:
        insertados = guardar_cursos(cursos, cat_prog_id)
        print(f"✅ Insertados {insertados} cursos nuevos en categoría ID {cat_prog_id}")
    else:
        print("⚠️ No se encontraron cursos reales en SkillsBuild.")

if __name__ == "__main__":
    main()
