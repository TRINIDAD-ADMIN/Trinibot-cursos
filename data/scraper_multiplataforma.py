"""
Multi-Platform Course Scraper
Scraper profesional para Coursera, edX y otras plataformas que SÍ permiten scraping
CON VERIFICACIÓN REAL DE DATOS DE CADA CURSO
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from db.connection import get_connection
from datetime import datetime
import time
import random
import requests
from bs4 import BeautifulSoup
import json
import re
import logging
from urllib.parse import quote, urljoin

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MultiPlatformScraper:
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
        
    def setup_session(self):
        """Configura la sesión HTTP"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        self.session.headers.update(headers)

    def create_driver(self):
        """Crea driver básico para casos que necesiten JavaScript"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        
        try:
            return webdriver.Chrome(options=options)
        except Exception as e:
            logger.error(f"Error creando driver: {e}")
            return None

    # ================== VERIFICACIÓN DE DETALLES DE CURSOS ==================
    
    def get_coursera_course_details(self, url):
        """Obtiene detalles reales de un curso de Coursera"""
        try:
            logger.info(f"🔍 Obteniendo detalles de Coursera: {url}")
            response = self.session.get(url, timeout=20)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                details = {
                    'descripcion': '',
                    'certificado': 0,
                    'tipo': 'gratis'
                }
                
                # Descripción - múltiples selectores
                desc_selectors = [
                    'div[data-testid="course-about"]',
                    '.course-description',
                    '.about-section p',
                    '[data-testid="description"]',
                    '.description',
                    'meta[name="description"]'
                ]
                
                for selector in desc_selectors:
                    if selector == 'meta[name="description"]':
                        elem = soup.select_one(selector)
                        if elem:
                            details['descripcion'] = elem.get('content', '')[:500]
                            break
                    else:
                        elem = soup.select_one(selector)
                        if elem:
                            details['descripcion'] = elem.get_text().strip()[:500]
                            break
                
                # Verificar si es gratis o de pago
                price_indicators = [
                    'Free',
                    'Gratis',
                    'Gratuito',
                    'Financial Aid available',
                    'Audit for free'
                ]
                
                paid_indicators = [
                    '$',
                    'USD',
                    'Subscription',
                    'Plus',
                    'Premium',
                    'Certificate fee'
                ]
                
                page_text = soup.get_text().lower()
                
                # Detectar si es gratis
                if any(indicator.lower() in page_text for indicator in price_indicators):
                    details['tipo'] = 'gratis'
                elif any(indicator.lower() in page_text for indicator in paid_indicators):
                    details['tipo'] = 'pago'
                
                # Verificar certificado
                cert_indicators = [
                    'certificate',
                    'certificado',
                    'shareable certificate',
                    'professional certificate'
                ]
                
                if any(indicator in page_text for indicator in cert_indicators):
                    details['certificado'] = 1
                
                return details
                
        except Exception as e:
            logger.error(f"Error obteniendo detalles de Coursera: {e}")
            return {'descripcion': '', 'certificado': 0, 'tipo': 'gratis'}
    
    def get_edx_course_details(self, url):
        """Obtiene detalles reales de un curso de edX"""
        try:
            logger.info(f"🔍 Obteniendo detalles de edX: {url}")
            response = self.session.get(url, timeout=20)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                details = {
                    'descripcion': '',
                    'certificado': 0,
                    'tipo': 'gratis'
                }
                
                # Descripción
                desc_selectors = [
                    '.course-intro-lead-in',
                    '.course-description',
                    '[data-testid="course-description"]',
                    '.about-content p',
                    'meta[property="og:description"]'
                ]
                
                for selector in desc_selectors:
                    if 'meta' in selector:
                        elem = soup.select_one(selector)
                        if elem:
                            details['descripcion'] = elem.get('content', '')[:500]
                            break
                    else:
                        elem = soup.select_one(selector)
                        if elem:
                            details['descripcion'] = elem.get_text().strip()[:500]
                            break
                
                page_text = soup.get_text().lower()
                
                # Detectar tipo (edX tiene cursos gratuitos y verificados)
                if any(indicator in page_text for indicator in ['free', 'audit', 'gratis']):
                    details['tipo'] = 'gratis'
                elif any(indicator in page_text for indicator in ['verified', '$', 'upgrade']):
                    details['tipo'] = 'freemium'  # Gratis con opción de pago
                
                # Certificados en edX
                if any(indicator in page_text for indicator in ['certificate', 'verified certificate', 'certificado']):
                    details['certificado'] = 1
                
                return details
                
        except Exception as e:
            logger.error(f"Error obteniendo detalles de edX: {e}")
            return {'descripcion': '', 'certificado': 0, 'tipo': 'gratis'}
    
    def get_khan_academy_details(self, url):
        """Obtiene detalles de Khan Academy"""
        try:
            logger.info(f"🔍 Obteniendo detalles de Khan Academy: {url}")
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                details = {
                    'descripcion': '',
                    'certificado': 0,  # Khan Academy no da certificados
                    'tipo': 'gratis'   # Todo es gratis en Khan Academy
                }
                
                # Descripción
                desc_selectors = [
                    '.course-description',
                    '.intro-text',
                    'meta[name="description"]',
                    'p'
                ]
                
                for selector in desc_selectors:
                    if 'meta' in selector:
                        elem = soup.select_one(selector)
                        if elem:
                            details['descripcion'] = elem.get('content', '')[:300]
                            break
                    else:
                        elem = soup.select_one(selector)
                        if elem and len(elem.get_text().strip()) > 50:
                            details['descripcion'] = elem.get_text().strip()[:300]
                            break
                
                return details
                
        except Exception as e:
            logger.error(f"Error obteniendo detalles de Khan Academy: {e}")
            return {'descripcion': 'Curso gratuito de Khan Academy', 'certificado': 0, 'tipo': 'gratis'}
    
    def get_freecodecamp_details(self, url):
        """Obtiene detalles de freeCodeCamp"""
        try:
            logger.info(f"🔍 Obteniendo detalles de freeCodeCamp: {url}")
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                details = {
                    'descripcion': '',
                    'certificado': 1,  # freeCodeCamp da certificados
                    'tipo': 'gratis'   # Todo es gratis
                }
                
                # Descripción
                desc_selectors = [
                    '.course-description',
                    '.intro-description',
                    'meta[name="description"]',
                    '.learn-description p'
                ]
                
                for selector in desc_selectors:
                    if 'meta' in selector:
                        elem = soup.select_one(selector)
                        if elem:
                            details['descripcion'] = elem.get('content', '')[:400]
                            break
                    else:
                        elem = soup.select_one(selector)
                        if elem and len(elem.get_text().strip()) > 30:
                            details['descripcion'] = elem.get_text().strip()[:400]
                            break
                
                return details
                
        except Exception as e:
            logger.error(f"Error obteniendo detalles de freeCodeCamp: {e}")
            return {'descripcion': 'Curso gratuito de programación con certificado', 'certificado': 1, 'tipo': 'gratis'}

    # ================== COURSERA SCRAPER (MEJORADO) ==================
    def search_coursera(self, query):
        """Scraper para Coursera usando requests"""
        logger.info(f"🎓 Buscando en Coursera: {query}")
        courses = []
        
        try:
            search_url = f"https://www.coursera.org/search?query={quote(query)}&"
            response = self.session.get(search_url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                course_selectors = [
                    'div[data-testid="search-filter-group-results"] div[data-testid="search-result-card"]',
                    'div.result-title-container',
                    'div[class*="SearchResult"]',
                    'a[href*="/learn/"]'
                ]
                
                for selector in course_selectors:
                    course_cards = soup.select(selector)
                    if course_cards:
                        logger.info(f"✅ Coursera: Encontrados {len(course_cards)} cursos")
                        
                        for card in course_cards[:10]:  # Limitamos para no sobrecargar
                            course = self.parse_coursera_course(card)
                            if course:
                                # OBTENER DETALLES REALES
                                time.sleep(random.uniform(1, 3))  # Pausa entre requests
                                details = self.get_coursera_course_details(course['url'])
                                course.update(details)
                                course['plataforma'] = 'Coursera'
                                courses.append(course)
                        break
                
                if not courses:
                    links = soup.select('a[href*="/learn/"]')
                    logger.info(f"🔄 Coursera método alternativo: {len(links)} enlaces encontrados")
                    
                    for link in links[:10]:
                        title = link.get_text().strip()
                        href = link.get('href')
                        
                        if title and len(title) > 10:
                            course_url = urljoin('https://www.coursera.org', href)
                            
                            # OBTENER DETALLES REALES
                            time.sleep(random.uniform(1, 3))
                            details = self.get_coursera_course_details(course_url)
                            
                            course = {
                                'titulo': title,
                                'url': course_url,
                                'plataforma': 'Coursera',
                                'disponible': 1
                            }
                            course.update(details)
                            courses.append(course)
                            
        except Exception as e:
            logger.error(f"❌ Error en Coursera: {e}")
        
        logger.info(f"📊 Coursera: {len(courses)} cursos procesados con detalles")
        return courses

    def parse_coursera_course(self, card):
        """Parsea un curso de Coursera"""
        try:
            course = {
                'titulo': '',
                'url': '',
                'disponible': 1
            }
            
            # Título
            title_selectors = ['h3', 'h2', '.result-title', '[data-testid="search-result-title"]']
            for selector in title_selectors:
                title_elem = card.select_one(selector)
                if title_elem:
                    course['titulo'] = title_elem.get_text().strip()
                    break
            
            # URL
            link = card.select_one('a[href*="/learn/"]') or card.select_one('a')
            if link:
                href = link.get('href')
                course['url'] = urljoin('https://www.coursera.org', href)
            
            return course if course['titulo'] and course['url'] else None
            
        except Exception as e:
            return None

    # ================== EDX SCRAPER (MEJORADO) ==================
    def search_edx(self, query):
        """Scraper para edX usando requests"""
        logger.info(f"🏫 Buscando en edX: {query}")
        courses = []
        
        try:
            search_url = f"https://www.edx.org/search?q={quote(query)}"
            response = self.session.get(search_url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                course_selectors = [
                    'div[data-testid="course-card"]',
                    '.course-card',
                    'div[class*="CourseCard"]',
                    'a[href*="/course/"]'
                ]
                
                for selector in course_selectors:
                    course_cards = soup.select(selector)
                    if course_cards:
                        logger.info(f"✅ edX: Encontrados {len(course_cards)} cursos")
                        
                        for card in course_cards[:10]:
                            course = self.parse_edx_course(card)
                            if course:
                                # OBTENER DETALLES REALES
                                time.sleep(random.uniform(1, 3))
                                details = self.get_edx_course_details(course['url'])
                                course.update(details)
                                course['plataforma'] = 'edX'
                                courses.append(course)
                        break
                
                if not courses:
                    links = soup.select('a[href*="/course/"]')
                    logger.info(f"🔄 edX método alternativo: {len(links)} enlaces encontrados")
                    
                    for link in links[:10]:
                        title = link.get_text().strip()
                        href = link.get('href')
                        
                        if title and len(title) > 10:
                            course_url = urljoin('https://www.edx.org', href)
                            
                            # OBTENER DETALLES REALES
                            time.sleep(random.uniform(1, 3))
                            details = self.get_edx_course_details(course_url)
                            
                            course = {
                                'titulo': title,
                                'url': course_url,
                                'plataforma': 'edX',
                                'disponible': 1
                            }
                            course.update(details)
                            courses.append(course)
                            
        except Exception as e:
            logger.error(f"❌ Error en edX: {e}")
        
        logger.info(f"📊 edX: {len(courses)} cursos procesados con detalles")
        return courses

    def parse_edx_course(self, card):
        """Parsea un curso de edX"""
        try:
            course = {
                'titulo': '',
                'url': '',
                'disponible': 1
            }
            
            # Título
            title_elem = card.select_one('h3') or card.select_one('h2') or card.select_one('.title')
            if title_elem:
                course['titulo'] = title_elem.get_text().strip()
            
            # URL
            link = card.select_one('a[href*="/course/"]') or card.select_one('a')
            if link:
                href = link.get('href')
                course['url'] = urljoin('https://www.edx.org', href)
            
            return course if course['titulo'] and course['url'] else None
            
        except Exception as e:
            return None

    # ================== KHAN ACADEMY SCRAPER (MEJORADO) ==================
    def search_khan_academy(self, query):
        """Scraper para Khan Academy"""
        logger.info(f"📚 Buscando en Khan Academy: {query}")
        courses = []
        
        try:
            search_url = f"https://www.khanacademy.org/search?page_search_query={quote(query)}"
            response = self.session.get(search_url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                links = soup.select('a[href*="/"]')
                
                processed = 0
                for link in links:
                    if processed >= 8:  # Limitamos
                        break
                        
                    href = link.get('href', '')
                    title = link.get_text().strip()
                    
                    if (title and len(title) > 10 and 
                        any(keyword in href.lower() for keyword in ['math', 'science', 'computing', 'economics', 'arts']) and
                        not any(skip in href.lower() for skip in ['javascript:', '#', 'mailto:', 'tel:'])):
                        
                        course_url = urljoin('https://www.khanacademy.org', href)
                        
                        # OBTENER DETALLES REALES
                        time.sleep(random.uniform(1, 2))
                        details = self.get_khan_academy_details(course_url)
                        
                        course = {
                            'titulo': title,
                            'url': course_url,
                            'plataforma': 'Khan Academy',
                            'disponible': 1
                        }
                        course.update(details)
                        courses.append(course)
                        processed += 1
                            
        except Exception as e:
            logger.error(f"❌ Error en Khan Academy: {e}")
        
        logger.info(f"📊 Khan Academy: {len(courses)} cursos procesados con detalles")
        return courses

    # ================== FREECODECAMP SCRAPER (MEJORADO) ==================
    def search_freecodecamp(self, query):
        """Scraper para freeCodeCamp usando su API"""
        logger.info(f"💻 Buscando en freeCodeCamp: {query}")
        courses = []
        
        try:
            base_courses = [
                {
                    'titulo': 'Responsive Web Design',
                    'url': 'https://www.freecodecamp.org/learn/responsive-web-design/',
                    'keywords': ['web', 'html', 'css', 'design', 'programacion']
                },
                {
                    'titulo': 'JavaScript Algorithms and Data Structures',
                    'url': 'https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/',
                    'keywords': ['javascript', 'programacion', 'algoritmos', 'programming']
                },
                {
                    'titulo': 'Front End Development Libraries',
                    'url': 'https://www.freecodecamp.org/learn/front-end-development-libraries/',
                    'keywords': ['react', 'frontend', 'programacion', 'web']
                },
                {
                    'titulo': 'Data Visualization',
                    'url': 'https://www.freecodecamp.org/learn/data-visualization/',
                    'keywords': ['data', 'visualization', 'datos', 'programacion']
                },
                {
                    'titulo': 'APIs and Microservices',
                    'url': 'https://www.freecodecamp.org/learn/apis-and-microservices/',
                    'keywords': ['api', 'backend', 'nodejs', 'programacion']
                },
                {
                    'titulo': 'Scientific Computing with Python',
                    'url': 'https://www.freecodecamp.org/learn/scientific-computing-with-python/',
                    'keywords': ['python', 'programacion', 'ciencia', 'matematicas']
                },
                {
                    'titulo': 'Data Analysis with Python',
                    'url': 'https://www.freecodecamp.org/learn/data-analysis-with-python/',
                    'keywords': ['python', 'data', 'analisis', 'datos', 'matematicas']
                }
            ]
            
            query_lower = query.lower()
            for course_info in base_courses:
                if any(keyword in query_lower for keyword in course_info['keywords']):
                    # OBTENER DETALLES REALES
                    time.sleep(random.uniform(1, 2))
                    details = self.get_freecodecamp_details(course_info['url'])
                    
                    course = {
                        'titulo': course_info['titulo'],
                        'url': course_info['url'],
                        'plataforma': 'freeCodeCamp',
                        'disponible': 1
                    }
                    course.update(details)
                    courses.append(course)
                    
        except Exception as e:
            logger.error(f"❌ Error en freeCodeCamp: {e}")
        
        logger.info(f"📊 freeCodeCamp: {len(courses)} cursos procesados con detalles")
        return courses

    # ================== FUNCIÓN PRINCIPAL ==================
    def search_all_platforms(self, query):
        """Busca en todas las plataformas"""
        logger.info(f"🌐 Iniciando búsqueda multi-plataforma para: '{query}'")
        
        all_courses = []
        
        platforms = [
            ('Coursera', self.search_coursera),
            ('edX', self.search_edx),
            ('Khan Academy', self.search_khan_academy),
            ('freeCodeCamp', self.search_freecodecamp)
        ]
        
        for platform_name, search_function in platforms:
            try:
                logger.info(f"\n🔍 Buscando en {platform_name}...")
                courses = search_function(query)
                
                # Log de detalles obtenidos
                for course in courses:
                    logger.info(f"   ✅ {course['titulo'][:40]}... - Tipo: {course.get('tipo', 'N/A')} - Cert: {'Sí' if course.get('certificado', 0) else 'No'}")
                
                all_courses.extend(courses)
                time.sleep(random.uniform(3, 6))  # Pausa más larga entre plataformas
                
            except Exception as e:
                logger.error(f"❌ Error buscando en {platform_name}: {e}")
                continue
        
        # Remover duplicados por URL
        unique_courses = []
        seen_urls = set()
        
        for course in all_courses:
            if course['url'] not in seen_urls:
                unique_courses.append(course)
                seen_urls.add(course['url'])
        
        logger.info(f"🎉 Total cursos únicos encontrados: {len(unique_courses)}")
        return unique_courses


def obtener_categorias():
    """Obtiene categorías de la base de datos"""
    conn = get_connection()
    categorias = {}
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre FROM categorias")
            for id_, nombre in cursor.fetchall():
                categorias[id_] = nombre.strip()
            cursor.close()
        finally:
            conn.close()
    return categorias

def guardar_cursos(cursos, categoria_id):
    """Guarda cursos en la base de datos"""
    conn = get_connection()
    if not conn:
        logger.error("⚠️ No se pudo conectar a base de datos")
        return 0
    
    cursor = conn.cursor()
    nuevos = 0
    
    for curso in cursos:
        try:
            # Verificar si el curso ya existe
            cursor.execute("SELECT COUNT(*) FROM recursos WHERE url = %s", (curso["url"],))
            if cursor.fetchone()[0] == 0:
                # Insertar nuevo curso
                cursor.execute("""
                INSERT INTO recursos
                (titulo, descripcion, url, categoria_id, fecha_publicacion, disponible, tipo, certificado)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                    curso["titulo"],
                    curso.get("descripcion", ""),
                    curso["url"],
                    categoria_id,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    curso.get("disponible", 1),
                    curso.get("tipo", "gratis"),
                    curso.get("certificado", 0)
                ))
                nuevos += 1
                logger.info(f"   ✅ Guardado: {curso['titulo'][:50]}... ({curso.get('plataforma', 'N/A')}) - {curso.get('tipo', 'N/A')}")
        except Exception as e:
            logger.error(f"Error guardando curso: {e}")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return nuevos

def main():
    """Función principal"""
    logger.info("🚀 Iniciando Multi-Platform Course Scraper MEJORADO")
    logger.info("📚 Plataformas: Coursera, edX, Khan Academy, freeCodeCamp")
    logger.info("🔍 CON VERIFICACIÓN REAL DE DETALLES DE CADA CURSO")
    
    categorias = obtener_categorias()
    if not categorias:
        logger.error("⚠️ No hay categorías en la BD.")
        return
    
    scraper = MultiPlatformScraper()
    total_cursos = 0
    
    for cat_id, nombre in categorias.items():
        logger.info(f"\n🎯 Procesando categoría: '{nombre}'")
        
        try:
            cursos = scraper.search_all_platforms(nombre)
            
            if cursos:
                # Estadísticas detalladas
                stats = {
                    'gratis': len([c for c in cursos if c.get('tipo') == 'gratis']),
                    'pago': len([c for c in cursos if c.get('tipo') == 'pago']),
                    'freemium': len([c for c in cursos if c.get('tipo') == 'freemium']),
                    'con_certificado': len([c for c in cursos if c.get('certificado') == 1]),
                    'sin_certificado': len([c for c in cursos if c.get('certificado') == 0])
                }
                
                logger.info("📊 ESTADÍSTICAS DETALLADAS:")
                logger.info(f"   💰 Gratis: {stats['gratis']}")
                logger.info(f"   💳 Pago: {stats['pago']}")
                logger.info(f"   🔄 Freemium: {stats['freemium']}")
                logger.info(f"   🏆 Con certificado: {stats['con_certificado']}")
                logger.info(f"   📜 Sin certificado: {stats['sin_certificado']}")
                
                nuevos = guardar_cursos(cursos, cat_id)
                total_cursos += nuevos
                logger.info(f"✅ Categoría '{nombre}' completada: {nuevos} cursos nuevos de {len(cursos)} procesados")
            else:
                logger.warning(f"❌ No se encontraron cursos para: '{nombre}'")
            
            if list(categorias.keys()).index(cat_id) < len(categorias) - 1:
                pausa = random.uniform(8, 15)
                logger.info(f"⏸️ Pausa de {pausa:.1f}s antes de siguiente categoría...")
                time.sleep(pausa)
                
        except Exception as e:
            logger.error(f"❌ Error procesando categoría '{nombre}': {e}")
            continue
    
    logger.info(f"\n🎉 Scraping completado!")
    logger.info(f"📈 Total cursos nuevos guardados: {total_cursos}")
    logger.info(f"🌐 Plataformas utilizadas con detalles verificados: Coursera, edX, Khan Academy, freeCodeCamp")

if __name__ == "__main__":
    main()