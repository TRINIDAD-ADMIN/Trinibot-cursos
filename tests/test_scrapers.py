# Unit test for scraper functionality
import unittest
from data.scraper_udemy import scrapear_cursos_udemy

class TestScraper(unittest.TestCase):
    def test_scrapear_udemy(self):
        try:
            scrapear_cursos_udemy()
        except Exception as e:
            self.fail(f"Scraper Udemy falló: {e}")

if __name__ == '__main__':
    unittest.main()
