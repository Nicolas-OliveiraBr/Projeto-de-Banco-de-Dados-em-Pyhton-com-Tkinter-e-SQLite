import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

class BtnIconText(ctk.CTkButton):
    def __init__(self, master, text, command, icon_path=None):

        kwargs = {}
        if icon_path:
            icon = Image.open(icon_path)
            kwargs["image"] = ctk.CTkImage(icon, size=(20, 20))

        super().__init__(
            master,
            text=text if not icon_path else f" {text}",
            font=ctk.CTkFont(family="Inter Medium", size=20, weight="normal"),
            **kwargs,
            command=command,
            corner_radius=5,
            fg_color="#FDDBE9",
            text_color="#61223D",
            hover_color="#F385AA",
            height=30,
            border_width=2,
            border_color="#CFA4B5",
        )

