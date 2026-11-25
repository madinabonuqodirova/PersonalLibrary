# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 06:27:04 2026

@author: User-Pk
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import os
import tempfile
import unittest
from repository import JsonBookRepository
from service import LibraryService


class TestPersonalLibrary(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp.close()
        self.repo = JsonBookRepository(self.tmp.name)
        self.service = LibraryService(self.repo)

    def tearDown(self):
        if os.path.exists(self.tmp.name):
            os.remove(self.tmp.name)

    def test_unit_validation_empty_title(self):
        with self.assertRaises(ValueError):
            self.service.add_book("", "Cho'lpon", "1936", "Rejada")

    def test_unit_validation_invalid_year(self):
        with self.assertRaises(ValueError):
            self.service.add_book("Test kitob", "Muallif", "999", "Rejada")

    def test_unit_statistics_and_search(self):
        self.service.add_book("Kecha va kunduz", "Cho'lpon", "1936", "Rejada")
        self.service.add_book("O'tkan kunlar", "Abdulla Qodiriy", "1926", "O'qilmoqda")
        self.service.add_book("Ikki eshik orasi", "O'tkir Hoshimov", "1986", "O'qilgan")

        stats = self.service.get_statistics()
        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["planned"], 1)
        self.assertEqual(stats["reading"], 1)
        self.assertEqual(stats["read"], 1)

        found = self.service.search_books("Qodiriy", "Barchasi")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].title, "O'tkan kunlar")

    def test_integration_add_persist_and_reload(self):
        self.service.add_book("Ikki eshik orasi", "O'tkir Hoshimov", "1986", "O'qilgan")

        reloaded_service = LibraryService(JsonBookRepository(self.tmp.name))
        books = reloaded_service.search_books("Ikki eshik", "O'qilgan")
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].author, "O'tkir Hoshimov")


if __name__ == "__main__":
    unittest.main()