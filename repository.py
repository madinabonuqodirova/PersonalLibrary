# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 06:24:39 2026

@author: User-Pk
"""

import json
import os
from abc import ABC, abstractmethod
from typing import List
from models import Book

class IBookRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Book]:
        pass

    @abstractmethod
    def save_all(self, books: List[Book]) -> None:
        pass

class JsonBookRepository(IBookRepository):
    def __init__(self, file_path: str = "books.json"):
        self.file_path = file_path

    def get_all(self) -> List[Book]:
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
                return [Book.from_dict(item) for item in raw]
        except (json.JSONDecodeError, KeyError, ValueError):
            return []

    def save_all(self, books: List[Book]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([b.to_dict() for b in books], f, ensure_ascii=False, indent=2)