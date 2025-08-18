# check_imports.py
import importlib

# Lista de dependencias que tu proyecto usa
modules = [
    "flask",
    "gunicorn",
    "python_dotenv",
    "mysql.connector",
    "requests",
    "bs4",
    "telegram"
]

print("===== VERIFICANDO DEPENDENCIAS =====")
for module in modules:
    try:
        importlib.import_module(module)
        print(f"[OK] {module}")
    except ImportError as e:
        print(f"[ERROR] {module} -> {e}")

print("===== FIN DE VERIFICACIÓN =====")
