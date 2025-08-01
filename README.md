# Telegram Bot for Free Courses

# Telegram Bot Cursos Gratuitos

Bot profesional para notificar cursos gratuitos y con cupones, con scraping automático y panel admin.

## Instalación

1. Clona el repo
2. Crea y activa entorno virtual
3. Instala dependencias: `pip install -r requirements.txt`
4. Configura `.env` con tu token y datos BD
5. Ejecuta el bot: `python main.py`

## Estructura

- bot/: lógica Telegram
- data/: scrapers y IA
- db/: conexión y modelos
- jobs/: tareas programadas
- logs/: logs
- web/: panel admin
- main.py: entrada

## Uso

Inicia bot con `/start`, selecciona categoría, recibe cursos.

## Consideraciones

Respeta términos de los sitios scrappeados. Usa el bot para información legal.
