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
data/scraper_discudemy.py
  data/ esta el archivo verificador_cursos.py/
- db/: conexión y modelos
- jobs/: tareas programadas
- logs/: logs
- web/: panel admin
- webhook.py: entrada
requirements.txt

## Uso

Inicia bot con `/start`, selecciona categoría, recibe cursos.

## Consideraciones

Respeta términos de los sitios scrappeados. Usa el bot para información legal.

## Comando para ejecutar el proyecto

- python -m data.scraper_coursera: Para coger datos en la plataforma
- python -m data.verificador_cursos: Para verificar curso disponile y no disponible (eliminar en auto desde la db los cursos no disponibles)
