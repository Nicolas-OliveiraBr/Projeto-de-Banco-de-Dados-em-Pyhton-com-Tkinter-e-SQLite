import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

#imports dos componentes de components/ não funciona
# import components.entry as entry
# import components.label as label
# import components.btn_IconText as btn_IconText

#importando os componentes diretamente aqui
class BtnIconText(ctk.CTkButton):
    def __init__(self, master, text, icon_path, command):
        icon = Image.open(icon_path)

        super().__init__(
            master,
            text=f" {text}",
            font=ctk.CTkFont(family="Inter Medium", size=20, weight="normal"),
            image=ctk.CTkImage(icon, size=(20, 20)),
            command=command,
            corner_radius=5,
            fg_color="#FDDBE9",
            text_color="#61223D",
            hover_color="#F385AA",
            height=30,
            border_width=2,
            border_color="#CFA4B5",
        )

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

class Entry(ctk.CTkEntry):
    def __init__(self, master, placeholder):
        super().__init__(
            master,
            placeholder_text=placeholder,
            font=ctk.CTkFont("Inter Medium", 16),
            fg_color="#FDF4F7",
            height=30,
            border_width=2,
            border_color="#CFA4B5"
        )

window = ctk.CTk()
window.state('zoomed')
window.title("Adicionar / Editar Cliente")
ctk.set_appearance_mode("light")
window.configure(fg_color="#FDE6F0")

window.geometry("800x500")
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.minsize(400, 250)

class LabelEntry(ctk.CTkFrame):
    def __init__(self, master, label_text, placeholder):
        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure(1, weight=1)

        self.label = Label(
            self,
            text=label_text,
            label_width=155
        )
        self.label.grid(row=0, column=0, padx=(0, 15), sticky="nsew")

        self.entry = Entry(
            self,
            placeholder,
        )
        self.entry.grid(row=0, column=1, sticky="ew", ipadx=5)

class LabelEntryButton(ctk.CTkFrame):
    def __init__(self, master, label_text, placeholder, button_text):
        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure(1, weight=1)

        self.label = Label(
            self,
            text=label_text,
            label_width=155
        )
        self.label.grid(row=0, column=0, padx=(0, 10), sticky="w")

        self.entry = Entry(
            self,
            placeholder
        )

        self.entry.grid(row=0, column=1, sticky="ew", padx=(6, 10), ipadx=5)

        self.button = BtnIconText(
            self,
            text=button_text,
            icon_path="grinch1.png",
            command=lambda: print("clicou")
        )
        self.button.grid(row=0, column=2)

form = ctk.CTkFrame(window, fg_color="transparent")
form.grid(row=0, column=0, padx=50, pady=50)

form.grid_columnconfigure(0, weight=1)

labels_entry = [
    ("Nome:", "Digite seu nome"),
    ("Idade:", "Digite sua idade"),
    ("Data de nascimento:", "Digite sua data de nascimento"),
    ("CPF:", "Digite seu CPF"),
    ("Endereço:", "Digite seu endereço"),
    ("Cidade/UF:", "Digite sua cidade"),
    ("Email:", "Digite seu email"),
]

for i, (label, placeholder) in enumerate(labels_entry):
    LabelEntry(form, label, placeholder)\
        .grid(row=i, column=0, sticky="ew", pady=8)


LabelEntryButton(
    form,
    "Telefone:",
    "Digite seu telefone",
    "Adicionar telefone"
).grid(row=7, column=0, sticky="ew", pady=8)

window.mainloop()