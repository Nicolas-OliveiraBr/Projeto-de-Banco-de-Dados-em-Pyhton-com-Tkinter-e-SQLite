import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from dataBaseConn import salvar_dados_clientes
from dataBaseConn import atualizar_dados_clientes
from components.entry import Entry
from components.label import Label
from components.btn_IconText import BtnIconText

window = ctk.CTk()
window.state('zoomed')
window.title("Adicionar / Editar Cliente")
ctk.set_appearance_mode("light")
window.configure(fg_color="#FDE6F0")

window.geometry("800x500")
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.minsize(400, 250)

entries = {}

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
        entries[label_text.replace(":", "").strip()] = self.entry

class LabelEntryButton(ctk.CTkFrame):
    def __init__(self, master, label_text, placeholder, button_text, entries, command):
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
            command=command
        )
        self.button.grid(row=0, column=2)

        entries[label_text.replace(":", "").strip()] = self.entry

class LabelCheckbox(ctk.CTkFrame):
    def __init__(self, master, label_text, default=False):
        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure(0, weight=0)
        self.label = Label(
            self,
            text=label_text,
            label_width=155
        )
        self.label.grid(row=0, column=0, padx=(0, 15), sticky="w")

        self.container = ctk.CTkFrame(
            self,
            fg_color="transparent",
            corner_radius=5,
            border_width=2,
            border_color="#CFA4B5"
        )
        # container envolve checkbox + state_label
        self.container.grid(row=0, column=1, sticky="w")
        self.container.grid_columnconfigure(0, weight=0)
        self.container.grid_columnconfigure(1, weight=0)

        self.var = tk.BooleanVar(value=default)

        def atualiza_label():
            state_label = "Ativo" if self.var.get() else "Inativo"
            # exibe "Status: Ativo" ou "Status: Inativo"
            self.state_label.configure(text=state_label)

        self.checkbox = ctk.CTkCheckBox(
            self.container,
            text="",  # remove o texto padrão "CTKcheckbox"
            variable=self.var,
            border_color="#CFA4B5",
            border_width=2,
            corner_radius=15,
            hover_color="#F385AA",
            command=atualiza_label
        )
        self.checkbox.grid(row=0, column=0, padx=(8, 5), pady=4, sticky="w")

        self.state_label = Label(self.container, text="", label_width=25)
        self.state_label.grid(row=0, column=1, padx=(5, 8), pady=4, sticky="e")

        entries[label_text.replace(":", "").strip()] = self.var

        atualiza_label()

form = ctk.CTkFrame(window, fg_color="transparent")
form.grid(row=0, column=0, padx=50, pady=25)

form.grid_columnconfigure(0, weight=1)

labels_entry = [
    ("Nome:", "Ex: Pantera"),
    ("Idade:", "Ex: 30"),
    ("Data de Nascimento:", "Ex: 01/01/1990"),
    ("CPF:", "Ex: 000.000.000-00"),
    ("Endereço:", "Ex: Rua das Rosas, 123"),
    ("Cidade/UF:", "Ex: Fortaleza/CE"),
    ("E-mail:", "Ex: pantera.rosa@email.com"),
]

for i, (label, placeholder) in enumerate(labels_entry):
    LabelEntry(form, label, placeholder)\
        .grid(row=i, column=0, sticky="ew", pady=8)


LabelEntryButton(
    form,
    "Telefones:",
    "Ex: (85) 9 0000-0000",
    "Adicionar telefone",
    entries,
    command=lambda:print("estou aqui")
).grid(row=7, column=0, sticky="ew", pady=8)

LabelCheckbox(form, "Status:").grid(row=9, column=0, padx=5, pady=(8), sticky="nsew")

frame_telefones = ctk.CTkFrame(form, fg_color= "transparent")
frame_telefones.grid(row=8, column=0, pady=8, padx=0, sticky="ew")
frame_telefones.grid_columnconfigure(1,weight=1)

frame_listaTelefones = ctk.CTkScrollableFrame(frame_telefones, width=127, fg_color="transparent",border_width=2, border_color="#CFA4B5", corner_radius=5)
frame_listaTelefones.grid(row=0, column=0, padx=(170,10))
frame_listaTelefones.grid_columnconfigure(0, weight=1)

telefonesStr = ["1254523452345", "9620394869381", "1243459704739"]#lista telefônica que será retirada do banco de dados
telefonesButtons = []#lista de botões com os número telefônicos para que possam ser deletados
numberSlc = []#número da lista de descarte de números telefonicos selecionado num momento

def selecionarBotao(index):
    global numberSlc
    for i in range(len(telefonesButtons)):
        telefonesButtons[i].configure(fg_color="transparent",text_color="#D4A6B9")
    telefonesButtons[index].configure(fg_color="#CFA4B5", text_color="#61223D")
    numberSlc = [telefonesButtons[index].cget("text"),index]

def criarListaTelefones():
    for i,telefone in enumerate(telefonesStr):
        btn = ctk.CTkButton(
            frame_listaTelefones,
            height=23,
            text=telefone,
            font=ctk.CTkFont(weight="bold"),
            text_color="#D4A6B9",
            fg_color="transparent",
            corner_radius=5,
            command=lambda i=i: 
                selecionarBotao(i)
        )
        btn.grid(row=i, column=0, sticky="ew")
        telefonesButtons.append(btn)

def removerTelefone():
    global numberSlc
    telefonesStr.remove(numberSlc[0])
    telefonesButtons[numberSlc[1]].destroy()

criarListaTelefones()

removeTelBtn = BtnIconText(frame_telefones, text="Remover telefone", command=lambda: removerTelefone())
removeTelBtn.grid(row=0, column=1, sticky="new")

buttons_frame = ctk.CTkFrame(form, fg_color="transparent")
buttons_frame.grid(row=10, column=0, pady=(0, 8))

BtnIconText(
    buttons_frame,
    text="Salvar",
    command=lambda: salvar_dados_clientes(entries)
).grid(row=0, column=0, padx=8)

BtnIconText(
    buttons_frame,
    text="Cancelar",
    command=lambda: print("clicou cancelar")
).grid(row=0, column=1, padx=8)

window.mainloop()