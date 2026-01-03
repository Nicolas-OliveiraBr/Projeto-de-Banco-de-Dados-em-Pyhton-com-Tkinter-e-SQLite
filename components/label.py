import tkinter as tk
import customtkinter as ctk

class Label(ctk.CTkLabel):
    def __init__(self, master, text, label_width):
        super().__init__(
            master,
            text=text,
            font=ctk.CTkFont("Inter Medium", 16, "bold"),
            text_color="#61223D",
            width=label_width,
            anchor="w"
        )
