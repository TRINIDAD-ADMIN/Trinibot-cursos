import requests
from bs4 import BeautifulSoup
from logs.logger import logger

def scrapear_cursos_udemy():
    logger.info("Iniciando scraping de Udemy...")

    url = "https://www.discudemy.com/"  # Ejemplo
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        cursos = soup.find_all(class_="course-article")

        for curso in cursos:
            titulo = curso.find("h3").text.strip() if curso.find("h3") else "Sin título"
            url_curso = curso.find("a")["href"] if curso.find("a") else "#"
            logger.info(f"Curso encontrado: {titulo} - {url_curso}")

            # Aquí insertar o actualizar en BD

    except Exception as e:
        logger.error(f"Error en scraping Udemy: {e}")
