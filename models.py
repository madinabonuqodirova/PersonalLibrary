# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 06:23:24 2026

@author: User-Pk
"""

from dataclasses import dataclass, asdict

@dataclass
class Book:
    id: int
    title: str
    author: str
    year: int
    status: str  # "Rejada", "O'qilmoqda", "O'qilgan"

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Book":
        return Book(
            id=int(data["id"]),
            title=str(data["title"]),
            author=str(data["author"]),
            year=int(data["year"]),
            status=str(data["status"]),
        )