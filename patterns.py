# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 06:25:14 2026

@author: User-Pk
"""

from abc import ABC, abstractmethod
from typing import List
from models import Book

class ISearchStrategy(ABC):
    @abstractmethod
    def filter(self, books: List[Book], query: str) -> List[Book]:
        pass

class TitleOrAuthorSearch(ISearchStrategy):
    def filter(self, books: List[Book], query: str) -> List[Book]:
        q = query.strip().lower()
        if not q:
            return books
        return [b for b in books if q in b.title.lower() or q in b.author.lower()]

class StatusFilterStrategy(ISearchStrategy):
    def filter(self, books: List[Book], status: str) -> List[Book]:
        if not status or status == "Barchasi":
            return books
        return [b for b in books if b.status == status]