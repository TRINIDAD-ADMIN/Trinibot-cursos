from db.connection import get_connection
from datetime import datetime

def obtener_categorias():
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre FROM categorias ORDER BY nombre")
    categorias = cursor.fetchall()
    cursor.close()
    conn.close()
    return categorias

def obtener_recursos_por_categoria(categoria_id):
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    query = """SELECT titulo, descripcion, url, fecha_publicacion FROM recursos 
               WHERE categoria_id = %s AND disponible = 1 ORDER BY fecha_publicacion DESC LIMIT 5"""
    cursor.execute(query, (categoria_id,))
    recursos = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convertir fecha_publicacion a datetime para formatear en el handler
    for r in recursos:
        if isinstance(r['fecha_publicacion'], str):
            r['fecha_publicacion'] = datetime.strptime(r['fecha_publicacion'], "%Y-%m-%d %H:%M:%S")
    return recursos

def guardar_usuario(telegram_id, nombre, username):
    conn = get_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE telegram_id = %s", (telegram_id,))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO usuarios (telegram_id, nombre, username) VALUES (%s, %s, %s)",
            (telegram_id, nombre, username)
        )
        conn.commit()
    cursor.close()
    conn.close()
    return True


def obtener_recursos_por_tipo(tipo):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if tipo == "gratis":
        cursor.execute("SELECT * FROM recursos WHERE url LIKE %s ORDER BY fecha_publicacion DESC LIMIT 10", ("%free%udemy.com%",))
    elif tipo == "descuento":
        cursor.execute("SELECT * FROM recursos WHERE url LIKE %s AND url NOT LIKE %s ORDER BY fecha_publicacion DESC LIMIT 10", ("%udemy.com%", "%free%"))
    else:
        return []

    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados