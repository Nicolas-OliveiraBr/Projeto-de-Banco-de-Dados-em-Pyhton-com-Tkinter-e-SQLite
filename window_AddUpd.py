import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from window import salvar_dados_clientes
from window import atualizar_dados_clientes

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
    def __init__(self, master, label_text, placeholder, button_text, entries):
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
form.grid(row=0, column=0, padx=50, pady=50)

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
    entries
).grid(row=7, column=0, sticky="ew", pady=8)

LabelCheckbox(form, "Status:").grid(row=8, column=0, padx=5, pady=(8), sticky="nsew")

frame_telefones = ctk.CTkScrollableFrame(form, width=100, fg_color="transparent",border_width=2, border_color="#CFA4B5", corner_radius=5)
frame_telefones.grid(row=9, column=0, sticky="ew",pady=(8,16), padx=(170,0))
frame_telefones.grid_columnconfigure(0, weight=1)


telefonesStr = ["1254523452345", "9620394869381", "1243459704739"]#lista telefônica que será retirada do banco de dados
telefonesButtons = []#lista de botões com os número telefônicos para que possam ser deletados
numberSlc = ""#número da lista de descarte de números telefonicos selecionado num momento

def selecionarBotao(index):
    global numberSlc
    for i in range(len(telefonesButtons)):
        telefonesButtons[i].configure(fg_color="transparent",text_color="#D4A6B9")
    telefonesButtons[index].configure(fg_color="#CFA4B5", text_color="#61223D")
    numberSlc = telefonesButtons[index].cget("text")

for i,telefone in enumerate(telefonesStr):
    btn = ctk.CTkButton(
        frame_telefones,
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

buttons_frame = ctk.CTkFrame(form, fg_color="transparent")
buttons_frame.grid(row=10, column=0, pady=(0, 8)) #não aparece botões devido passar do tamanho da janela, ajustar com scroll?
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