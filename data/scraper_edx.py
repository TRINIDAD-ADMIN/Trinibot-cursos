import requests
from db.connection import get_connection
from datetime import datetime

API_URL = "https://api.edx.org/catalog/v1/courses"
HEADERS = {
    "Accept": "application/json"
}

def obtener_cursos_edx(paginas=2):
    cursos = []
    page = 1
    while page <= paginas:
        print(f"📦 Procesando página {page} de edX...")
        params = {
            "price": "free",     # Filtrar solo cursos gratuitos
            "page": page,
            "page_size": 20      # Puedes ajustar para traer más o menos
        }
        response = requests.get(API_URL, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f"❌ Error en la API de edX, código {response.status_code}")
            break
        
        data = response.json()
        results = data.get("results", [])
        if not results:
            print("⚠️ No se encontraron cursos en esta página.")
            break
        
        for curso in results:
            titulo = curso.get("title", "Curso sin título")
            descripcion = curso.get("short_description", "Sin descripción")
            url = curso.get("marketing_url") or curso.get("url")
            if not url:
                continue
            
            cursos.append({
                "titulo": titulo,
                "descripcion": descripcion,
                "url": url
            })
        
        page += 1
    
    return cursos

def guardar_en_bd(cursos, categoria_id=18):  # Categoría 18 por ejemplo para edX
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
    cursos = obtener_cursos_edx(paginas=3)
    guardar_en_bd(cursos, categoria_id=18)
