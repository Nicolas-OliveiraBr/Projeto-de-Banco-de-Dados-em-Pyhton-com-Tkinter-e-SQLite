import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from components.btn_IconText import BtnIconText
from dataBaseConn import getTuples, deletar_cliente_db
from tkinter import ttk
from window_AddUpd import abrir_tela_AddUpd_Cliente


root = ctk.CTk() # Criação de uma janela raíz, a principal do programa
root.title("Banco de Dados - Clientes") # Definindo um nome para a janela
ctk.set_appearance_mode("light") # Definindo o modo de aparência da janela (claro/escuro/sistema)
root.configure(fg_color="#FBB5CD") # Definindo a cor de fundo da janela

root.after(0, lambda: root.state("zoomed")) # Maximiza a janela após a inicialização

# Dividindo a janela principal em frames, recorte de tamanho fixo/variãvel dentro da janela raíz

# Frame topo (título)
frame_topo = ctk.CTkFrame(root, fg_color="#FEE9F0", corner_radius=0)
frame_topo.pack(fill="x", padx=10, pady=(25, 0)) # Método '.pack()' exibe/apresenta um objeto criado em Tkinter em ordem de exibição, argumento 'fill' define em que direção a área aumentará/diminuirá se a tela aumentar/diminuir
frame_topo.grid_columnconfigure(0, weight=1)

# Container do topo
topo_container = ctk.CTkFrame(frame_topo, fg_color="transparent")
topo_container.grid_columnconfigure(1, weight=1)
topo_container.grid(row=1, column=0, columnspan=2, sticky="w", padx=20, pady=(10))

# Frame meio (tabela)
frame_meio = ctk.CTkFrame(root, fg_color="#FEE9F0", corner_radius=0)
frame_meio.pack(fill="both", expand=True, padx=10)

# Frame inferior (botões)
frame_baixo = ctk.CTkFrame(root, fg_color="#FEE9F0", height=80, corner_radius=0)
frame_baixo.pack(fill="x", pady=(0, 10), padx=10)

#Botões do frame infeirior
buttons_frame = ctk.CTkFrame(frame_baixo, fg_color="transparent")
buttons_frame.pack(padx=20, pady=10)

#Frame topo - Titulo da Janela
script_dir = os.path.dirname(os.path.abspath(__file__)) # Diretório do script atual
icon_path = os.path.join(script_dir, "IconPanteraRosa.png") # Caminho da imagem do ícone
img_Icon = Image.open(icon_path) # Carregando a imagem do ícone

# Ajustando o tamanho mantendo proporção
w, h = img_Icon.size
nova_altura = 80
nova_largura = int(w * (nova_altura / h)) # Calculando a nova largura proporcional à nova altura

img_Icon = img_Icon.resize(
    (nova_largura, nova_altura), 
    Image.LANCZOS # Filtro de qualidade para redimensionamento
)

icon_image = ctk.CTkImage(
    light_image=img_Icon,
    size=(nova_largura, nova_altura) 
)

#Carregando a imagem das patinhas
paw_image_path = os.path.join(script_dir, "patinhas.png")

paw_image = ctk.CTkImage(
    light_image=Image.open(paw_image_path),
    size=(250, 50)
)

paw_image_frame = ctk.CTkFrame(topo_container, fg_color="transparent")
paw_image_frame.grid(row=0, column=1, padx=25, sticky="w")

ctk.CTkLabel(
    paw_image_frame,
    image=paw_image,
    text=""
).pack()

IconLbl = ctk.CTkLabel(
    topo_container,
    image=icon_image,
    text=" Clientes",
    font=ctk.CTkFont("Calibri", 64, "bold"),
    text_color="#E24C6C",
    compound="left"
)

IconLbl.grid(row=0, column=0, sticky="w", padx=(50,0))

#Frame meio - Tabela de clientes

def criar_tabela_clientes(parent):
    # Frame externo com cor e cantos arredondados
    frame_card = ctk.CTkFrame(
        parent, # Frame pai
        fg_color="#FCBDD0",
        corner_radius=5
    )
    frame_card.pack(fill="both", expand=True, padx=10)

    # Frame interno para dar padding
    frame_tabela = ctk.CTkFrame(
        frame_card, 
        fg_color="#FEE9F0",
    )
    frame_tabela.pack(fill="both", expand=True, padx=5, pady=5)

    frame_tree = ctk.CTkFrame(frame_tabela, fg_color="transparent") # Frame que conterá a Treeview
    frame_tree.pack(fill="both", expand=True)

    arvore = ttk.Treeview(
        frame_tree,
        columns=("id", "nome", "cpf", "email"),
        show="headings"
    )

    colunas = {
        "id": "ID",
        "nome": "Nome",
        "cpf": "CPF",
        "email": "E-mail",
    }

    # Definindo os cabeçalhos das colunas
    for key, texto in colunas.items(): 
        arvore.heading(key, text=texto)
        arvore.column("id", width=50, minwidth=30, anchor="center", stretch=False)
        arvore.column("cpf", width=150, minwidth=120, anchor="center", stretch=False)
        arvore.column("email", width=200, minwidth=150, anchor="center", stretch=True)
        arvore.column("nome", width=200, minwidth=150, anchor="center", stretch=True)

    # Criando uma barra de rolagem para melhor visualização dos atributos e dos valores das tuplas
    scroll_y = ttk.Scrollbar(frame_tree, orient="vertical", command=arvore.yview) 
    scroll_x = ttk.Scrollbar(frame_tree, orient="horizontal", command=arvore.xview)

    arvore.configure(
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )
    scroll_y.pack(side="right", fill="y") 
    arvore.pack(side="top", fill="both", expand=True) # Preenchendo todo o espaço disponível no frame pai
    scroll_x.pack(side="bottom", fill="x")

    for cliente in getTuples("clientes", "id, nome, cpf, email"):
        arvore.insert("", "end", values=cliente)

    return arvore

#Estilizando a tabela
style = ttk.Style()
style.theme_use("default")

style.configure(
    "Treeview",
    background="#FEE9F0",
    foreground="#A34257",
    rowheight=32,
    fieldbackground="#FEE9F0",
    font=("Segoe UI", 12),
    borderwidth=0,
    relief="flat"
)

style.configure(
    "Treeview.Heading",
    background="#FCBDD0",
    foreground="white",
    font=("Segoe UI", 14, "bold")
)

#Cor ao selecionar linha
style.map( 
    "Treeview",
    background=[("selected", "#FCBDD0")],   # fundo ao selecionar
    foreground=[("selected", "white")]     # texto ao selecionar
)

#Função que retorna que o id do cliente na linha selecionada
def getLineSelection():
    selecionado = tabela_clientes.selection()

    if not selecionado:
        return None

    valores = tabela_clientes.item(selecionado[0], "values")
    return valores[0]

#Função da janela modal de confirmação
def modal_confirmacao(master):
    resposta = {"valor": False}

    modal = ctk.CTkToplevel(master)

    largura = 420
    altura = 280

    #Centralizando a janela modal
    x = (modal.winfo_screenwidth() // 2) - (largura // 2)
    y = (modal.winfo_screenheight() // 2) - (altura // 2)
    modal.geometry(f"{largura}x{altura}+{x}+{y}")

    modal.configure(fg_color="#FFC0D9")
    modal.resizable(False, False)

    modal.transient(master)
    modal.grab_set()


    ctk.CTkLabel(
        modal,
        text=""
    ).pack(pady=(20, 10))

    #texto de confirmação
    ctk.CTkLabel(
        modal,
        text="Você tem certeza?",
        font=("Segoe UI", 20, "bold"),
        text_color="#61223D"
    ).pack(pady=(0, 20))

    #botões de confirmação
    frame_btn = ctk.CTkFrame(modal, fg_color="transparent")
    frame_btn.pack()

    def sim():
        resposta["valor"] = True
        modal.destroy()

    def nao():
        modal.destroy()

    ctk.CTkButton(
        frame_btn,
        text="Sim",
        width=120,
        fg_color="#FEE9F0",
        text_color="#61223D"
    , command=sim).grid(row=0, column=0, padx=10)

    ctk.CTkButton(
        frame_btn,
        text="Não",
        width=120,
        fg_color="#FEE9F0",
        text_color="#61223D"
    , command=nao).grid(row=0, column=1, padx=10)

    modal.wait_window()
    return resposta["valor"]


#Função para deletar cliente
def deletar_cliente():
    id_cliente = getLineSelection()

    if id_cliente is None:
        messagebox.showwarning("Atenção", "Selecione um cliente para deletar!")
        return

    confirmar = modal_confirmacao(root)


    if not confirmar:
        return

    try:
        deletar_cliente_db(id_cliente)

        tabela_clientes.delete(tabela_clientes.selection()[0])

        messagebox.showinfo("Sucesso", "Cliente deletado com sucesso!")

    except Exception as erro:
        messagebox.showerror("Erro", f"Erro ao deletar cliente:\n{erro}")

#Criando a tabela clientes
tabela_clientes = criar_tabela_clientes(frame_meio)

#Frame baixo - botões
BtnIconText(
    buttons_frame,
    text="Adicionar cliente",
    command=lambda: abrir_tela_AddUpd_Cliente("Adicionar Cliente", None)
).grid(row=0, column=0, padx=4)

btnViewCliente = BtnIconText(
    buttons_frame,
    text="Visualizar",
    command=lambda: print("visualizar")
)
btnViewCliente.grid(row=0, column=1, padx=4)

btnUpdCliente = BtnIconText(
    buttons_frame,
    text="Editar",
    command=lambda: abrir_tela_AddUpd_Cliente("Editar cliente", getLineSelection())
)
btnUpdCliente.grid(row=0, column=2, padx=4)

btnDltCliente = BtnIconText(
    buttons_frame,
    text="Deletar",
    command=deletar_cliente
)
btnDltCliente.grid(row=0, column=3, padx=4)

#Função que muda a cor do botão se nada for selecionado
def mudarCorBtn(event= None): 
    if tabela_clientes.selection():
        btnUpdCliente.configure(fg_color="#FDDBE9", state="normal")
        btnDltCliente.configure(fg_color="#FDDBE9", state="normal")
        btnViewCliente.configure(fg_color="#FDDBE9", state="normal")
    else:
        btnUpdCliente.configure(fg_color="#C7B6BD", text_color_disabled = "#795A67", state="disabled")
        btnDltCliente.configure(fg_color="#C7B6BD", text_color_disabled = "#795A67", state="disabled")
        btnViewCliente.configure(fg_color="#C7B6BD", text_color_disabled = "#795A67", state="disabled")

#Monitorando seleções na tabela cliente
tabela_clientes.bind("<<TreeviewSelect>>", mudarCorBtn)

#Inicializando os botões como inativos
mudarCorBtn()
root.mainloop()