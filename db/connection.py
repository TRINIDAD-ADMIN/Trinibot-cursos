import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    # Obtener variables de entorno
    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    database = os.getenv("DB_NAME")
    port = int(os.getenv("DB_PORT", 3306))
    
    # Debug - Mostrar lo que estamos usando (sin contraseña completa)
    print(f"🔗 Conectando a: {host}:{port}")
    print(f"👤 Usuario: {user}")
    print(f"🗄️ Base de datos: {database}")
    
    # Verificar que tenemos todas las variables necesarias
    if not host:
        print("❌ Error: DB_HOST no está configurado")
        return None
    if not user:
        print("❌ Error: DB_USER no está configurado")
        return None
    if not password:
        print("❌ Error: DB_PASS no está configurado")
        return None
    if not database:
        print("❌ Error: DB_NAME no está configurado")
        return None
    
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',
            autocommit=True,
            connect_timeout=10  # Timeout de 10 segundos
        )
        
        if connection.is_connected():
            print(f"✅ Conectado exitosamente a {host}")
            return connection
            
    except Error as e:
        print(f"❌ Error de conexión a la base de datos: {e}")
        print(f"🔍 Intentaba conectar a: {host}:{port}")
        return None