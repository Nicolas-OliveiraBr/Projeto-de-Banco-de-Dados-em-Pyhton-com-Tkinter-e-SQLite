import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

#imports dos componentes de components/ não funciona
# import components.entry as entry
# import components.label as label
# import components.btn_IconText as btn_IconText

#importando os componentes diretamente aqui
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
            command=lambda: print("clicou")
        )
        self.button.grid(row=0, column=2)

form = ctk.CTkFrame(window, fg_color="transparent")
form.grid(row=0, column=0, padx=50, pady=50)

form.grid_columnconfigure(0, weight=1)

labels_entry = [
    ("Nome:", "Ex: Pantera"),
    ("Idade:", "Ex: 30"),
    ("Data de nascimento:", "Ex: 01/01/1990"),
    ("CPF:", "Ex: 000.000.000-00"),
    ("Endereço:", "Ex: Rua das Rosas, 123"),
    ("Cidade/UF:", "Ex: Fortaleza/CE"),
    ("Email:", "Ex: pantera.rosa@email.com"),
]

for i, (label, placeholder) in enumerate(labels_entry):
    LabelEntry(form, label, placeholder)\
        .grid(row=i, column=0, sticky="ew", pady=8)

LabelEntryButton(
    form,
    "Telefone:",
    "Ex: (85) 9 0000-0000",
    "Adicionar telefone"
).grid(row=7, column=0, sticky="ew", pady=8)

buttons_frame = ctk.CTkFrame(form, fg_color="transparent")
buttons_frame.grid(row=8, column=0, pady=(20, 0))
buttons_frame.grid_columnconfigure((0, 1), weight=0)

BtnIconText(
    buttons_frame,
    text="Salvar",
    command=lambda: print("clicou salvar")
).grid(row=0, column=0, padx=8)

BtnIconText(
    buttons_frame,
    text="Cancelar",
    command=lambda: print("clicou cancelar")
).grid(row=0, column=1, padx=8)

window.mainloop()