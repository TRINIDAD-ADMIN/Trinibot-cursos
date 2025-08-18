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

## Comando para ejecutar el proyecto

- python -m data.scraper_coursera: Para coger datos en la plataforma
- python -m data.verificador_cursos: Para verificar curso disponile y no disponible (eliminar en auto desde la db los cursos no disponibles)

* python -m data.scraper_coursera_selenium

**\*\***\*\*\***\*\***PLATAFORMAS QUE ESTAN PROTEGIDOS QIE NO SE PUEDEN SCRAPER NI CON SELENIUM
Coursenavia,
LearnViral sitio no disponible
class central, acces limitados
edx no tiene api
coursera, respuetas de json, dificil de scrapear
saylor academy: selector de categoria es por id, no es por nombre
open who, api no disponible

TP_2508_9156

Nombre de la base de datos MySQL
u749682169_trinibot_cursos

Nombre de usuario MySQL
u749682169_trinibot

Contraseña\* Qd0g&KM=
