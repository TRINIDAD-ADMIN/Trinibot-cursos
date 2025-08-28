#!/usr/bin/env python3
from db.connection import get_connection

def test_local_connection():
    print("🧪 Probando conexión local a Hostinger...")
    
    connection = get_connection()
    
    if connection:
        try:
            cursor = connection.cursor()
            
            # Test 1: Versión MySQL
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"📊 MySQL versión: {version[0]}")
            
            # Test 2: Mostrar tablas
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"📋 Tablas en la base de datos: {len(tables)}")
            for table in tables:
                print(f"  - {table[0]}")
            
            # Test 3: Si existe tabla categorias
            cursor.execute("SELECT COUNT(*) FROM categorias")
            categorias_count = cursor.fetchone()[0]
            print(f"🏷️ Total categorías: {categorias_count}")
            
            cursor.close()
            print("✅ Conexión local exitosa!")
            return True
            
        except Exception as e:
            print(f"❌ Error durante las pruebas: {e}")
            return False
        finally:
            connection.close()
    else:
        print("❌ No se pudo conectar")
        return False

if __name__ == "__main__":
    test_local_connection()