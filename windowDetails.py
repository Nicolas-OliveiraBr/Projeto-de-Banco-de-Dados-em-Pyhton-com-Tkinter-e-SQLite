import customtkinter as ctk
from components.label import Label
from components.btn_IconText import BtnIconText
from dataBaseConn import get_cliente_selecionado, buscar_dados_cliente

class LabelInfo(ctk.CTkFrame):
    def __init__(self, master, label_text, value_text):
        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure(1, weight=1)

        self.label = Label(
            self,
            text=label_text,
            label_width=155
        )
        self.label.grid(row=0, column=0, padx=(0, 15), sticky="nsew")

        self.value = ctk.CTkLabel(
            self,
            text=value_text,
            anchor="w",
            font=ctk.CTkFont(size=16),
            text_color="#61223D",
            fg_color="#FDE6F0",
            corner_radius=8,
            padx=10,
            pady=6
        )
        self.value.grid(row=0, column=1, sticky="ew")

class TelefoneView(ctk.CTkLabel):
    def __init__(self, master, text):
        super().__init__(
            master,
            text=text,
            anchor="w",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#61223D",
            fg_color="#FDE6F0",
            corner_radius=8,
            padx=10,
            pady=6
        )

class LabelStatus(ctk.CTkFrame):
    def __init__(self, master, label_text, status=True):
        super().__init__(master, fg_color="transparent")

        self.label = Label(self, text=label_text, label_width=155)
        self.label.grid(row=0, column=0, padx=(0, 15), sticky="w")

        if status:
            texto = "Ativo"
            cor = "#FABBD5"
        else:
            texto = "Inativo"
            cor = "#FD7C7C"

        self.status_label = ctk.CTkLabel(
            self,
            text=texto,
            fg_color=cor,
            text_color="#61223D",
            corner_radius=15,
            padx=20,
            pady=6,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.status_label.grid(row=0, column=1, sticky="w")

# Função para abrir a tela de visualização dos dados do cliente
def abrir_tela_visualizar(dados, telefones):
    window = ctk.CTk()
    window.state('zoomed')
    window.title("Visualizar Cliente")
    ctk.set_appearance_mode("light")
    window.configure(fg_color="#FDE6F0")

    window.geometry("800x500")
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.minsize(400, 250)

    form = ctk.CTkScrollableFrame(
    window, 
    fg_color="transparent",
    border_width=5,
    border_color="#F385AA",
    corner_radius=20,
    scrollbar_button_color="#FDDBE9",
    scrollbar_button_hover_color="#F385AB"
    )

    form.grid(row=0, column=0, padx=50, pady=25, sticky="nsew")
    form.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
    form, 
    text="Visualizar Cliente", 
    corner_radius=10,
    font=ctk.CTkFont(size=20, weight="bold"),
    text_color="#61223D",
    fg_color="#F385AA",
    anchor="w",
    padx=10, pady=6
    ).grid(row=0, column=0, pady=(0, 4), sticky="ew")


    dados_cliente = [
    ("Nome:", dados[0]),
    ("Idade:", dados[1]),
    ("CPF:", dados[2]),
    ("E-mail:", dados[3]),
    ("Endereço:", dados[4]),
    ("Cidade/UF:", dados[5]),
    ("Data de Nascimento:", dados[6]),
    ]

    for i, (label, value) in enumerate(dados_cliente):
        LabelInfo(form, label, value)\
            .grid(row=i+1, column=0, sticky="ew", pady=8)
        
    frame_telefones = ctk.CTkFrame(form, fg_color="transparent")
    frame_telefones.grid(row=8, column=0, pady=10, sticky="ew")
    frame_telefones.grid_columnconfigure(0, weight=1)

    frame_listaTelefones = ctk.CTkScrollableFrame(
        frame_telefones,
        height=180,
        fg_color="#FDDBB9",
        border_width=2,
        border_color="#CFA4B5",
        corner_radius=10,
        scrollbar_button_color="#FDDBE9",
        scrollbar_button_hover_color="#F385AB"
    )
    frame_listaTelefones.grid(row=0, column=0, sticky="ew", padx=5)
    frame_listaTelefones.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        frame_listaTelefones,
        text="Telefones Registrados",
        font=ctk.CTkFont("Segoe UI", 20, "bold"),
        text_color="#61223D",
        fg_color="#F5C89A",
        corner_radius=10,
        padx=10, pady=6,
        anchor="w"
    ).grid(row=0, column=0, sticky="ew", padx=8, pady=(6,8))

    
    for numero, tipo in telefones:
        texto = f"{numero} - {tipo}"
        TelefoneView(frame_listaTelefones, texto)\
            .grid(sticky="ew", padx=8, pady=4)
        
    LabelStatus(form, "Status:", status=bool(dados[7]))\
        .grid(row=12, column=0, pady=10, sticky="w")
    
    buttons_frame = ctk.CTkFrame(form, fg_color="transparent")
    buttons_frame.grid(row=20, column=0, pady=(10, 8))

    BtnIconText(
        buttons_frame,
        text="Cancelar",
        command=lambda: print("deletar")
    ).grid(row=0, column=0, padx=8)

    window.mainloop()


#Função para visualizar os dados do cliente selecionado na tabela da tela principal
def visualizar_cliente(arvore):
    cliente = get_cliente_selecionado(arvore)
    
    if not cliente:
        return

    cliente_id = cliente[0]

    dados, telefones = buscar_dados_cliente(cliente_id)

    abrir_tela_visualizar(dados, telefones)
