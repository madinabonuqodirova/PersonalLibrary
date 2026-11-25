# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 06:25:49 2026

@author: User-Pk
"""

from datetime import datetime
from typing import List, Dict
from models import Book
from repository import IBookRepository
from patterns import TitleOrAuthorSearch, StatusFilterStrategy

VALID_STATUSES = ("Rejada", "O'qilmoqda", "O'qilgan")

class BookValidator:
    @staticmethod
    def validate(title: str, author: str, year_str: str, status: str) -> int:
        if not title or not title.strip():
            raise ValueError("Kitob nomi bo'sh bo'lishi mumkin emas!")
        if not author or not author.strip():
            raise ValueError("Muallif nomi bo'sh bo'lishi mumkin emas!")
        try:
            year = int(year_str)
        except ValueError:
            raise ValueError("Nashr yili butun son bo'lishi kerak!")
        current_year = datetime.now().year
        if year < 1400 or year > current_year:
            raise ValueError(f"Nashr yili 1400 dan {current_year} gacha bo'lishi kerak!")
        if status not in VALID_STATUSES:
            raise ValueError("Noto'g'ri o'qish holati tanlandi!")
        return year

class LibraryService:
    def __init__(self, repository: IBookRepository):
        self.repository = repository
        self.books: List[Book] = self.repository.get_all()
        self.search_strategy = TitleOrAuthorSearch()
        self.status_strategy = StatusFilterStrategy()

    def _next_id(self) -> int:
        return max((b.id for b in self.books), default=0) + 1

    def add_book(self, title: str, author: str, year_str: str, status: str) -> Book:
        year = BookValidator.validate(title, author, year_str, status)
        book = Book(
            id=self._next_id(),
            title=title.strip(),
            author=author.strip(),
            year=year,
            status=status,
        )
        self.books.append(book)
        self.repository.save_all(self.books)
        return book

    def update_book(self, book_id: int, title: str, author: str, year_str: str, status: str) -> bool:
        year = BookValidator.validate(title, author, year_str, status)
        for book in self.books:
            if book.id == book_id:
                book.title = title.strip()
                book.author = author.strip()
                book.year = year
                book.status = status
                self.repository.save_all(self.books)
                return True
        return False

    def delete_book(self, book_id: int) -> bool:
        initial_len = len(self.books)
        self.books = [b for b in self.books if b.id != book_id]
        if len(self.books) < initial_len:
            self.repository.save_all(self.books)
            return True
        return False

    def search_books(self, query: str = "", status: str = "Barchasi") -> List[Book]:
        result = self.search_strategy.filter(self.books, query)
        return self.status_strategy.filter(result, status)

    def get_statistics(self) -> Dict[str, int]:
        return {
            "total": len(self.books),
            "read": sum(1 for b in self.books if b.status == "O'qilgan"),
            "reading": sum(1 for b in self.books if b.status == "O'qilmoqda"),
            "planned": sum(1 for b in self.books if b.status == "Rejada"),
        }