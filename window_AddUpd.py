import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
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
        self.button.grid(row=1, column=0, sticky="ew", pady=(8,0), columnspan=2)

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
            self.state_label.configure(text=state_label) # Altera a exibição da label quando ativo => .configure ajusta alguma propriedade, determinada durante a cosntrução do código

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

# class TelefoneButton(ctk.CTkButton):
#     def selecionarBotao(index):
#         global numberSlc
#         for btn in telefonesButtons:
#             btn.configure(fg_color="transparent",text_color="#D4A6B9")
#         self.configure(fg_color="#CFA4B5", text_color="#61223D")
#         numberSlc = self._text

#     def __init__(self, master, text):
#         super().__init__(
#             master,
#             height=23,
#             text=text,
#             font=ctk.CTkFont(family="Inter Medium", weight="bold"),
#             text_color="#D4A6B9",
#             fg_color="transparent",
#             corner_radius=5,
#         )

class TelefoneButton(ctk.CTkButton):
    def __init__(self, master, text):
        super().__init__(
            master,
            height=23,
            text=text,
            font=ctk.CTkFont(family="Inter Medium", weight="bold"),
            text_color="#D4A6B9",
            fg_color="transparent",
            corner_radius=5,
            command=self.selecionar
        )

    def selecionar(self):
        global numberSlc  # Desmarca todos os botões
        for btn in telefonesButtons:
            btn.configure(fg_color="transparent", text_color="#D4A6B9")
        self.configure(fg_color="#CFA4B5", text_color="#61223D") # Marca o selecionado
        numberSlc = self.cget("text")


# Criação de um frame rolável para que seja possível evitar que o conteúdo vaze da tela ao adicionar mais widgets

form = ctk.CTkScrollableFrame(
    window, 
    fg_color="transparent",
    border_width=5,
    border_color="#F385AA",
    corner_radius=20,
    width=window.winfo_width(),
    height=window.winfo_height(),
    scrollbar_button_color="#FDDBE9",
    scrollbar_button_hover_color="#F385AB"
)

form.grid(row=0, column=0, padx=50, pady=25, sticky="nsew")
form.grid_columnconfigure(0, weight=1) # Define que a coluna onde o frame se encontra poderá se esticar em mais uma coluna; o efeito visual criado é que o conteúdo está centralizado

# Título do frame

label_titulo = ctk.CTkLabel(
    form, 
    text="Adicionar / Editar Cliente", 
    corner_radius=10,
    font=ctk.CTkFont(size=20, weight="bold"),
    text_color="#61223D",
    fg_color="#F385AA",
    anchor="w",
    padx=10,
    pady=6
).grid(row=0, column=0, pady=(0, 4), sticky="ew")

# Criando um array de tuplas, cada uma com o texto de cada label e sua respectiva sugestão (placeholder)

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
        .grid(row=i+1, column=0, sticky="ew", pady=8)

def adicionarTelefone():
    global telefonesButtons
    newTel = button_addNum.entry.get()
    if len(newTel) == 10 and newTel not in telefonesStr:
        telefonesStr.append(newTel)
        for btn in telefonesButtons:
            telefonesButtons.remove(btn)
        criarListaTelefones()

 # Adicionando um frame para que o campo de entrada de Telefone fique na mesma linha do Combox

# frame_entrada_telefones = ctk.CTkFrame(
#     form,
#     fg_color="transparent",
# )
# frame_entrada_telefones.grid(row=8, column=0, pady=8, sticky="ew")
# frame_entrada_telefones.grid_columnconfigure(0, weight=1)
# frame_entrada_telefones.grid_columnconfigure(1, weight=1)

tipo_telefone = ctk.CTkComboBox(
    form,
    values=["Celular","Fixo","WhatsApp"],
    fg_color="#FDE6F0", 
    border_color="#CFA4B5", 
    button_color="#CFA4B5", 
    dropdown_fg_color="#CFA4B5",
    font=ctk.CTkFont(size=16)
)
tipo_telefone.grid(row=8, column=0, sticky="ew")
tipo_telefone.configure(0, width=1)
tipo_telefone.set("Selecione o tipo de telefone")

button_addNum = LabelEntryButton(
    form,
    "Telefone",
    "Ex: (85) 9 0000-0000",
    "Adicionar telefone",
    entries,
    command=lambda: adicionarTelefone())
button_addNum.grid(row=9, column=0, sticky="ew", padx=(0,4), pady=8)


# Criando um novo botão para adicionar telefones

# frame_addNum = ctk.CTkFrame(form, fg_color="transparent")
# frame_addNum.grid(row=9, column=0, sticky="ew")
# frame_addNum.grid_columnconfigure(1, weight=1)

# button_addNum_label = ctk.CTkLabel(
#     frame_addNum, 
#     text="",
#     width=155
# )
# button_addNum_label.grid(row=0, column=0, sticky="ew")

frame_telefones = ctk.CTkFrame(form, fg_color= "transparent")
frame_telefones.grid(row=10, column=0, pady=8, padx=8, sticky="ew")
frame_telefones.grid_columnconfigure(0,weight=1)

frame_listaTelefones = ctk.CTkScrollableFrame(
    frame_telefones,
    height=200, 
    fg_color="#FDDBB9",
    border_width=2, 
    border_color="#CFA4B5", 
    corner_radius=5,
    scrollbar_button_color="#FDDBE9",
    scrollbar_button_hover_color="#F385AB"
)
frame_listaTelefones.grid(row=0, column=0, padx=(0, 0), sticky="we")
frame_listaTelefones.grid_columnconfigure(0, weight=1)
frame_listaTelefones._scrollbar.configure(height=0)

telefonesStr = ["1254523452345", "9620394869381", "1243459704739"] # Lista telefônica que será retirada do banco de dados
telefonesButtons = [] # Lista de botões com os número telefônicos para que possam ser deletados
numberSlc = None # Número da lista de descarte de números telefonicos selecionado num momento

def removerTelefone():
    global numberSlc
    if not numberSlc:
        return  # Nada selecionado

    telefonesStr[:] = [t for t in telefonesStr if t != numberSlc]
    
    for btn in telefonesButtons[:]:
        if btn.cget("text") == numberSlc:
            btn.destroy()
            telefonesButtons.remove(btn)
    numberSlc = None


def criarListaTelefones():
    for i, telefone in enumerate(telefonesStr):
        btn = TelefoneButton(
            frame_listaTelefones, 
            text=telefonesStr[i]
        )
        btn.grid(row=i, column=0, sticky="ew")
        telefonesButtons.append(btn)

criarListaTelefones()

removeTelBtn = BtnIconText(form, text="Remover telefone", command=lambda: removerTelefone())
removeTelBtn.grid(row=11, column=0, sticky="ew", padx=(4,0), pady=8)

LabelCheckbox(form, "Status:").grid(row=12, column=0, padx=5, pady=(8), sticky="nsew")

buttons_frame = ctk.CTkFrame(form, fg_color="transparent")
buttons_frame.grid(row=13, column=0, pady=(0, 8))

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