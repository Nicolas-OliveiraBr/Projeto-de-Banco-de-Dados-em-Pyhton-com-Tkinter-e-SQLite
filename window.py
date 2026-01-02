import tkinter as tk
from tkinter import ttk
import sqlite3
import customtkinter as ctk
from tkinter import messagebox

# Criando o banco de dados (em SQLite)

with sqlite3.connect("banco_de_dados_MFDS.db") as conn: # Criando uma pasta e um arquivo DATABASE onde os dados serão armazenados
    conn.execute("PRAGMA foreign_keys = ON") # Comando para que o SQLite leia chaves estrangeiras
    cursor = conn.cursor() # Criando um cursor para executar os comandos
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY,
                nome VARCHAR(150) NOT NULL,
                idade INTEGER,
                cpf VARCHAR(11) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE,
                endereco TEXT,
                localidade VARCHAR(100),
                data_nascimento DATE,
                status BOOLEAN
            )"""
    )

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS cliente_telefones (
                    id INTEGER PRIMARY KEY,
                    numero VARCHAR(100),
                    tipo VARCHAR(100),
                    clientes_id INTEGER,
                   
                    FOREIGN KEY (clientes_id)
                        REFERENCES clientes(id)
            )"""
    )
    conn.commit() # Comitando as alterações (necessário e obrigatório para o registro de novos valores)

# Criando uma array para o nome dos rótulos de cada uma das entries

tabela_clientes_atr = [
    "ID", 
    "Nome", 
    "Idade", 
    "CPF", 
    "E-mail", 
    "Endereço", 
    "Cidade", 
    "Data de Nascimento", 
    "Status"
]

# Criando um dicionário para reservar todas as entradas registradas

entries = {}

# Criando uma função para mostrar os dados registrados no banco de dados em uma tabela em uma nova janela

clientes_tabela = None # Definindo uma variável global com valor None para gerenciar a exibição de janelas

def carregar_clientes():
   global clientes_tabela # Puxando-a, para que seja possível alterá-la globalmente

   if clientes_tabela and clientes_tabela.winfo_exists(): # Conferindo se há uma janela clientes_tabela já aberta e se ela não foi destruída
       clientes_tabela.lift() # Colocando no topo (sobreposição de janelas)
       clientes_tabela.focus_force() # Garantindo que ela fique na posição de foco
       return

   clientes_tabela = tk.Toplevel(root) # Criando uma janela á parte para a exibição da tabela de Clientes
   clientes_tabela.title("Mostrar Clientes")
   clientes_tabela.geometry("600x600")
   clientes_tabela.transient(root) # Tornando a janela criada uma filha da janela root criada, associação

# Criando uma função interna que altera o valor da variável 'clientes_tabela' para None quando o usuãrio fechã-la
   
   def on_close():
       global clientes_tabela
       clientes_tabela.destroy() # Fecha a janela
       clientes_tabela = None

   clientes_tabela.protocol("WM_DELETE_WINDOW", on_close) # Criando um interceptador que verifica qaundo o usuário fechou a aba e realiza o comando à direita

# Criando uma divisão na janela para que a tabela que será criada não ocupe todo o espaço da janela

   frame_tabela = tk.Frame(clientes_tabela, width=600, height=400)
   frame_tabela.pack(padx=10, pady=10)
   frame_tabela.pack_propagate(False)  # Método '.pack_propagate(False)' impede que o frame cresça

# Aplicando a função Treeview, da biblioteca ttk, para construção de uma tabela com a referência de colunas

   arvore = ttk.Treeview(
       frame_tabela, 
       columns=("id", 
               "nome",
               "idade",
               "cpf",
               "email",
               "endereco",
               "localidade",
               "data_nascimento",
               "status"),
        show="headings",
        height=5
               )

# Definindo o tamanho de cada coluna da tabela

   arvore.column("id", width=100)
   arvore.column("nome", width=160)
   arvore.column("idade", width=100)
   arvore.column("cpf", width=100)
   arvore.column("email", width=200)
   arvore.column("endereco", width=200)
   arvore.column("localidade", width=160)
   arvore.column("data_nascimento", width=100)
   arvore.column("status", width=100)

# Atribuindo o nome de cada coluna de acordo com o seu identificador

   arvore.heading("id", text="ID")
   arvore.heading("nome", text="Nome")
   arvore.heading("idade", text="Idade")
   arvore.heading("cpf", text="CPF")
   arvore.heading("email", text="E-mail")
   arvore.heading("endereco", text="Endereço")
   arvore.heading("localidade", text="Cidade")
   arvore.heading("data_nascimento", text="Data de Nascimento")
   arvore.heading("status", text="Status")

# Criando uma barra de rolagem para melhor visualização dos atributos e dos valores das tuplas

   scroll = ttk.Scrollbar(frame_tabela, orient="horizontal", command=arvore.xview) # Criando a Scrollbar que desliza na direção horizontal
   arvore.configure(xscrollcommand=scroll.set) # Atribuindo a barra de rolagem à tabela

   arvore.pack(side="top", fill="both", expand=True) # Permitindo que a Janela tenha responsividade ao aumentar ou diminuir o tamanho de tela
   scroll.pack(side="bottom", fill="x", pady=5)

   cursor.execute("""SELECT 
                  id, 
                  nome, 
                  idade, 
                  cpf, 
                  email, 
                  endereco, 
                  localidade, 
                  data_nascimento, 
                  status 
                  FROM clientes""") # Pegando as informações diretamente da tabela 'clientes' do banco de dados
   
# Iterando os valores para cada uma das colunas definidas na Treeview 
  
   for cliente in cursor.fetchall(): # Método '.fetchall()' pega todas as linhas retornadas do último 'SELECT' (o acima) e retorna as tuplas (linhas) da tabela
       arvore.insert("", "end", values=cliente)
   
# Atribuindo/mapeando nomes amigáveis às chaves do array tabela_clientes_atr para que a função 'salvar_dados_clientes' não rejeite palavras com espaços

mapa = {
    "Nome": "nome", 
    "Idade": "idade", 
    "CPF": "cpf", 
    "E-mail": "email", 
    "Endereço": "endereco", 
    "Cidade": "localidade", 
    "Data de Nascimento": "data_nascimento", 
    "Status": "status"
}

# Criando uma função para um botão que manda os valores enviados pelo usuário para o banco de dados

def salvar_dados_clientes(entries):
    atributos_lista = []
    valores = []

    # Percorre o dicionário 'mapa', que relaciona o rótulo da interface com a coluna do banco
    for rotulo, coluna in mapa.items():
        atributos_lista.append(coluna) # Adiciona o nome da coluna na lista
        valores.append(entries[rotulo].get()) # Obtém o valor digitado pelo usuário no campo da interface

    atributos = ", ".join(atributos_lista)
    subst = ", ".join("?" for _ in atributos_lista)

    sql = f"""
        INSERT INTO clientes ({atributos})
        VALUES ({subst})
    """

    try:
        cursor.execute(sql, tuple(valores)) # Executa a query SQL passando os valores como tupla
        
        conn.commit() # Comitando as alterações
        print("Dados salvos! :D")
    except sqlite3.IntegrityError as e: 
        conn.rollback() # Caso ocorra algum erro, desfaz todas as alterações feitas no banco de dados

        msg = str(e).lower()
        if "unique constraint failed" in msg: # Verifica se o erro foi causado por violar a restrição UNIQUE do atributo
            if "cpf" in msg:
                messagebox.showerror("Erro ao salvar", "CPF já cadastrado. Use outro CPF e tente novamente.") # Mensagem de erro
                return False
            if "email" in msg:
                messagebox.showerror("Erro ao salvar", "E-mail já cadastrado. Use outro e‑mail e tente novamente.")
                return False
        raise  # Repete o erro novamente caso seja um problema não tratado acima
    carregar_clientes() # Atualizando a tabela

# Comandos de definição da tela criada e desligamento

root = ctk.CTk() # Criação de uma janela raíz, a principal do programa
root.title("Banco de Dados") # Definindo um nome para a janela
root.overrideredirect(True) # Definindo que a janela não terá os botões correspondentes a Minimizar, Maximizar/Restaurar e Fechar

def fechar_app(): # Criando uma função que desliga a conexão com o banco de dados e desliga a janela
    conn.close() # Método '.close()' determina o desligamento da conexão
    if clientes_tabela and clientes_tabela.winfo_exists():
        clientes_tabela
        clientes_tabela.destroy() # Fecha a janela da tabela de clientes caso essa esteja ativada
        clientes_tabela = None # Atualiza o valor da variável global
    root.destroy() # Método '.destroy()' apaga/desliga uma tela 

root.protocol("WM_DELETE_WINDOW", fechar_app) # Método '.protocol.("WM_DELETE_WINDOW", )' executa uma ação em um objeto específico quando é identificado que uma tela será apagada
    

# Dividindo a janela principal em frames, recorte de tamanho fixo/variãvel dentro da janela raíz

frame_topo = tk.Frame(root)
frame_topo.pack(fill="x") # Método '.pack()' exibe/apresenta um objeto criado em Tkinter em ordem de exibição, argumento 'fill' define em que direção a área aumentará/diminuirá se a tela aumentar/diminuir

frame_meio = ctk.CTkFrame(root, fg_color="#FDE6F0") # Definindo um frame com uma cor de backgound diferente, definida em hexadecimais
frame_meio.pack(expand=True, fill="both") # Definindo que

# Definindo o espaço ocupado pela tela

w, h = 800, 600 # Definindo variãveis com os valores do tamanho, em pixels, da janela principal
screen_w = root.winfo_screenwidth() # Pegando as informações do comprimento de tela 
screen_h = root.winfo_screenheight() # Pegando as informações da altura de tela 
x = (screen_w - w) // 2 # Tirando uma média aritmética do tamanho do comprimento da tela e da janela para determinar a distância exata entre a janela e a borda da tela
y = (screen_h - h) // 2 # Tirando uma média aritmética do tamanho da altura da tela e da janela
root.geometry(f"{w}x{h}+{x}+{y}") # Definindo o tamanho da tela com os valores encontrados, e então posicionando-a exatamente no centro

# Barra superior com botão de Fechar personalizado

barra = tk.Frame(frame_topo, bg="#A34257", height=20)
barra.pack(fill="x")

btn_fechar = tk.Button(
    barra, 
    text="X",
    font=("Arial", 16, "bold"),
    bg="#FDE6F0", 
    padx="10", 
    fg="#A34257",
    command=root.destroy, 
    bd=0
)

btn_fechar.pack(side="right")

#Rótulo da Janela

lbl = tk.Label(
    frame_topo, 
    text="Clientes",
    font=("Arial", 16, "bold"),
    fg="#A34257",
    bg="#FDE6F0",
    width=20,
    height=1,
    padx=20,
    pady=10,
    anchor="nw",
    relief="flat",
    justify="left"
)

lbl.pack(expand=True, fill="both")

# Criando um laço for para a criação de campos de inserção de texto e um botão de check

ativo_var = ctk.BooleanVar(value=False) # Classe do CustomTkinter que permite com que haja a leitura de valores booleanos

for atributo in tabela_clientes_atr:
    frame_campo = ctk.CTkFrame(frame_meio, fg_color="#f385aa", corner_radius=20) # Criando um novo frame, que funciona como um espaço reservado para que as labels (rótulos) e as entries (entradas) fiquem juntas, lado a lado
    frame_campo.pack(pady="5") # Exibindo o frame com padding adicionado

    if atributo == "Status": # Condicional if que verifica se a chave do atributo é 'Status', para que esse seja um botão
            ctk.CTkLabel(
                frame_campo,
                text=atributo,
                font=("Segoe UI", 18, "bold"),
                width=200,
                anchor="w",
                text_color="#ffeef9",
            ).pack(side="left") # Criando uma label personalizada para o botão Check

            def atualizar_texto():
                if ativo_var.get():
                    btn_ativo.configure(text="Ativo")
                else:
                    btn_ativo.configure(text="Inativo")

            btn_ativo = ctk.CTkCheckBox(frame_campo, variable=ativo_var, text="Inativo", text_color="#ffeef9", command=atualizar_texto) # Criando um Check button, uma variação de botão que é possível marcar ou desmarcar, e que retorna, por padrão, o valor um (se marcado) e 0 (se não marcado)
            btn_ativo.pack(side="right", padx=5) # Exibe o botão com padding adicionado e posição ajustada
            entries[atributo] = ativo_var # Define o valor registrado do botão no dicionãrio 'entries'

    else: # Gera um campo de entrada com uma label (rótulo) própria
        ctk.CTkLabel(
            frame_campo, 
            text=atributo,
            font=("Segoe UI", 18, "bold"), 
            width=200, 
            anchor="w",
            text_color="#ffeef9",
        ).pack(side="left", padx=5) # Criando um rótulo e atribuindo sua posição 
        
        entry = ctk.CTkEntry(frame_campo, width=300, fg_color="#A34257") # Criando uma entrada de texto, sem bordas
        entry.pack(side="right") # Exibindo a entrada com sua posição ajustada
        entries[atributo] = entry # Define o valor do campo registrado no dicionãrio 'entries'

# Criando um botão que envia as informações dos clientes para o banco de dados

btn_entry = tk.Button(
    frame_meio, 
    text="Enviar dados",
    command=salvar_dados_clientes
)

btn_entry.pack(side="top", pady=10)

# Entradas feitas manualmente para definição dos valores (pode ser usada futuramente caso haja mudanças no cõdigo)

# ent_id = tk.Entry(frame_meio, bd=0)
# ent_id.pack(side="top", pady=5)

# ent_nome = tk.Entry(frame_meio, bd=0)
# ent_nome.pack(side="top", pady=5)

# ent_idade = tk.Entry(frame_meio, bd=0)
# ent_idade.pack(side="top", pady=5)

# ent_cpf = tk.Entry(frame_meio, bd=0)
# ent_cpf.pack(side="top", pady=5)

# ent_email = tk.Entry(frame_meio, bd=0)
# ent_email.pack(side="top", pady=5)

# ent_endereco = tk.Entry(frame_meio, bd=0)
# ent_endereco.pack(side="top", pady=5)

# ent_cidade = tk.Entry(frame_meio, bd=0)
# ent_cidade.pack(side="top", pady=5)

# ent_data_nasc = tk.Entry(frame_meio, bd=0)
# ent_data_nasc.pack(side="top", pady=5)

# ent_status = tk.Entry(frame_meio, bd=0)
# ent_status.pack(side="top", pady=5)

# Abrindo a janela para exibição dos valores registrados no banco de dados

btn_mostrar_clientes = tk.Button(
    frame_meio,
    text="Mostrar Clientes",
    command=carregar_clientes)
btn_mostrar_clientes.pack(side="top", pady=5)

root.mainloop() # Liga a interface gráfica e a mantém ativa