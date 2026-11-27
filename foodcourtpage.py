import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
from datetime import datetime 

class FoodCourtPage(tk.Frame):
    def __init__(self, master, username=""):
        super().__init__(master, bg="#F4F6FA")
        self.username = username

        lokasi = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(lokasi, "database.db")
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor