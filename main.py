# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 06:26:17 2026

@author: User-Pk
"""

import tkinter as tk
from tkinter import ttk, messagebox
from repository import JsonBookRepository
from service import LibraryService, VALID_STATUSES

class LibraryApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Shaxsiy kutubxona (PersonalLibrary)")
        self.root.geometry("820x540")
        self.service = LibraryService(JsonBookRepository("books.json"))
        self.selected_id = None

        self._build_ui()
        self.refresh_table()

    def _build_ui(self):
        # Kiritish paneli
        form_frame = ttk.LabelFrame(self.root, text="Kitob ma'lumotlari", padding=10)
        form_frame.pack(fill="x", padx=10, pady=6)

        ttk.Label(form_frame, text="Kitob nomi:").grid(row=0, column=0, sticky="w", padx=4)
        self.title_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.title_var, width=28).grid(row=0, column=1, padx=4)

        ttk.Label(form_frame, text="Muallif:").grid(row=0, column=2, sticky="w", padx=4)
        self.author_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.author_var, width=25).grid(row=0, column=3, padx=4)

        ttk.Label(form_frame, text="Yil:").grid(row=1, column=0, sticky="w", padx=4, pady=6)
        self.year_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.year_var, width=12).grid(row=1, column=1, sticky="w", padx=4)

        ttk.Label(form_frame, text="Holati:").grid(row=1, column=2, sticky="w", padx=4)
        self.status_var = tk.StringVar(value=VALID_STATUSES[0])
        ttk.Combobox(form_frame, textvariable=self.status_var, values=VALID_STATUSES, state="readonly", width=22).grid(row=1, column=3, sticky="w", padx=4)

        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=6, sticky="w")
        ttk.Button(btn_frame, text="Qo'shish", command=self.add_book).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Tahrirlash", command=self.update_book).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="O'chirish", command=self.delete_book).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Tozalash", command=self.clear_inputs).pack(side="left", padx=4)

        # Qidiruv va filtr paneli
        search_frame = ttk.LabelFrame(self.root, text="Qidirish va filtrlash", padding=8)
        search_frame.pack(fill="x", padx=10, pady=4)

        ttk.Label(search_frame, text="Qidiruv (nom/muallif):").pack(side="left", padx=4)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.refresh_table())
        ttk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side="left", padx=4)

        ttk.Label(search_frame, text="Holat bo'yicha:").pack(side="left", padx=8)
        self.filter_var = tk.StringVar(value="Barchasi")
        filter_box = ttk.Combobox(search_frame, textvariable=self.filter_var, values=("Barchasi",) + VALID_STATUSES, state="readonly", width=16)
        filter_box.pack(side="left", padx=4)
        filter_box.bind("<<ComboboxSelected>>", lambda *_: self.refresh_table())

        # Jadval
        columns = ("id", "title", "author", "year", "status")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=12)
        for col, text, w in [("id", "ID", 50), ("title", "Kitob nomi", 270), ("author", "Muallif", 220), ("year", "Yil", 80), ("status", "Holati", 130)]:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=w, anchor="center" if col in ("id", "year", "status") else "w")
        self.tree.pack(fill="both", expand=True, padx=10, pady=6)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Statistika paneli
        self.stats_label = ttk.Label(self.root, text="", font=("Segoe UI", 10, "bold"))
        self.stats_label.pack(fill="x", padx=12, pady=6)

    def add_book(self):
        try:
            self.service.add_book(self.title_var.get(), self.author_var.get(), self.year_var.get(), self.status_var.get())
            self.clear_inputs()
            self.refresh_table()
        except ValueError as e:
            messagebox.showerror("Xatolik", str(e))

    def update_book(self):
        if self.selected_id is None:
            messagebox.showwarning("Ogohlantirish", "Tahrirlash uchun jadvaldan kitob tanlang!")
            return
        try:
            self.service.update_book(self.selected_id, self.title_var.get(), self.author_var.get(), self.year_var.get(), self.status_var.get())
            self.clear_inputs()
            self.refresh_table()
        except ValueError as e:
            messagebox.showerror("Xatolik", str(e))

    def delete_book(self):
        if self.selected_id is None:
            messagebox.showwarning("Ogohlantirish", "O'chirish uchun jadvaldan kitob tanlang!")
            return
        if messagebox.askyesno("Tasdiqlash", "Tanlangan kitobni o'chirishga ishonchingiz komilmi?"):
            self.service.delete_book(self.selected_id)
            self.clear_inputs()
            self.refresh_table()

    def on_select(self, _event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        self.selected_id = int(values[0])
        self.title_var.set(values[1])
        self.author_var.set(values[2])
        self.year_var.set(values[3])
        self.status_var.set(values[4])

    def clear_inputs(self):
        self.selected_id = None
        self.title_var.set("")
        self.author_var.set("")
        self.year_var.set("")
        self.status_var.set(VALID_STATUSES[0])

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        books = self.service.search_books(self.search_var.get(), self.filter_var.get())
        for b in books:
            self.tree.insert("", "end", values=(b.id, b.title, b.author, b.year, b.status))
        stats = self.service.get_statistics()
        self.stats_label.config(
            text=f"Jami: {stats['total']}  |  O'qilgan: {stats['read']}  |  O'qilmoqda: {stats['reading']}  |  Rejada: {stats['planned']}"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()