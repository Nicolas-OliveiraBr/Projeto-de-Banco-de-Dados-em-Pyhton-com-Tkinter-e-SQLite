import tkinter as tk
from tkinter import ttk
import sqlite3
import customtkinter as ctk
from tkinter import messagebox

with sqlite3.connect("banco_de_dados_MFDS.db") as conn: # Criando uma pasta e um arquivo DATABASE onde os dados serão armazenados
    conn.execute("PRAGMA foreign_keys = ON") # Comando para que o SQLite leia chaves estrangeiras
    cursor = conn.cursor() # Criando um cursor para executar os comandos
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY,
                nome VARCHAR(150) NOT NULL,
                idade INTEGER,
                data_nascimento DATE,
                cpf VARCHAR(11) UNIQUE NOT NULL,
                endereco TEXT,
                localidade VARCHAR(100),
                email VARCHAR(100) UNIQUE,
                status BOOLEAN
            )"""
    )

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS cliente_telefones (
                    id INTEGER PRIMARY KEY,
                    numero VARCHAR(20),
                    tipo VARCHAR(100),
                    clientes_id INTEGER,
                   
                    FOREIGN KEY (clientes_id)
                        REFERENCES clientes(id)
            )""")
    conn.commit() # Comitando as alterações (necessário e obrigatório para o registro de novos valores)

def getTuples(tabela, atributos, onde = None):
    tuples = []
    if onde == None:
        cursor.execute(f"SELECT {atributos} FROM {tabela}") # Pegando as informações diretamente da tabela 'clientes' do banco de dados
    else:
        cursor.execute(f"SELECT {atributos} FROM {tabela} WHERE {onde}")

    for tuple in cursor.fetchall():
        tuples.append(tuple)
    return tuples

# Atribuindo/mapeando nomes amigáveis às chaves do array tabela_clientes_atr para que a função 'salvar_dados_clientes' não rejeite palavras com espaços

mapaClientes = {
    "Nome": "nome", 
    "Idade": "idade", 
    "Data de Nascimento": "data_nascimento", 
    "CPF": "cpf",
    "Endereço": "endereco", 
    "Cidade": "localidade",  
    "E-mail": "email", 
    "Status": "status"
}

def salvar_dados_clientes(entries, entriesTel):
    atributos_lista = []
    valores = []

    # Percorre o dicionário 'mapaClientes', que relaciona o rótulo da interface com a coluna do banco
    for rotulo, coluna in mapaClientes.items():
        atributos_lista.append(coluna) # Adiciona o nome da coluna na lista
        valores.append(entries[rotulo].get()) # Obtém o valor digitado pelo usuário no campo da interface

    atributos = ", ".join(atributos_lista)
    subst = ", ".join("?" for _ in atributos_lista)

    sqlClientes = f"""
        INSERT INTO clientes ({atributos})
        VALUES ({subst})
    """
    # tuples_CliTel = getTuples("cliente_telefones", "numero, tipo, clientes_id")

    try:
        cursor.execute(sqlClientes, tuple(valores)) # Executa a query SQL passando os valores como tupla
        cliente_id = cursor.lastrowid

        for tupleTel in entriesTel:
            # tpCompleta = tupleTel + (cliente_id)
            cursor.execute(f"""
                INSERT INTO cliente_telefones (numero, tipo, clientes_id)
                VALUES (?, ?, ?)
            """, (tupleTel[0],tupleTel[1],cliente_id))
        conn.commit() # Comitando as alterações
        print("Dados salvos! :D")
    except sqlite3.IntegrityError as e: 
        conn.rollback() # Caso ocorra algum erro, desfaz todas as alterações feitas no banco de dados

        # msg = str(e).lower()
        # if "unique constraint failed" in msg: # Verifica se o erro foi causado por violar a restrição UNIQUE do atributo
        #     if "cpf" in msg:
        #         messagebox.showerror("Erro ao salvar", "CPF já cadastrado. Use outro CPF e tente novamente.") # Mensagem de erro
        #         return False
        #     if "email" in msg:
        #         messagebox.showerror("Erro ao salvar", "E-mail já cadastrado. Use outro e‑mail e tente novamente.")
        #         return False
        # raise  # Repete o erro novamente caso seja um problema não tratado acima



# Criando uma função para atualizar os dados de um cliente específico no banco de dados
def atualizar_dados_clientes(cliente_id, entries, entriesTel):
    atributos_lista = []
    valores = []

    for rotulo, coluna in mapaClientes.items():
        atributos_lista.append(f"{coluna} = ?")
        valores.append(entries[rotulo].get())

    valores.append(cliente_id)

    cursor.execute(f"""
        UPDATE clientes
        SET {', '.join(atributos_lista)}
        WHERE id = ?
    """, tuple(valores))

    # Remove telefones antigos
    cursor.execute(
        "DELETE FROM cliente_telefones WHERE clientes_id = ?",
        (cliente_id,)
    )

    # Insere os novos
    for numero, tipo in entriesTel:
        cursor.execute("""
            INSERT INTO cliente_telefones (numero, tipo, clientes_id)
            VALUES (?, ?, ?)
        """, (numero, tipo, cliente_id))

    conn.commit()
# print(getTuples("clientes", "*"))

def deletar_cliente_db(cliente_id):
    try:
        cursor.execute(
            "DELETE FROM cliente_telefones WHERE clientes_id = ?",
            (cliente_id,)
        )

        cursor.execute(
            "DELETE FROM clientes WHERE id = ?",
            (cliente_id,)
        )

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

# Função para obter o cliente selecionado na tabela
def get_cliente_selecionado(arvore):
    selecionado = arvore.selection()

    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um cliente primeiro.")
        return None

    valores = arvore.item(selecionado[0], "values")
    return valores 

# Função para buscar os dados completos de um cliente pelo ID
def buscar_dados_cliente(cliente_id):
    cliente = getTuples(
        tabela="clientes",
        atributos="nome, idade, cpf, email, endereco, localidade, data_nascimento, status",
        onde=f"id = {cliente_id}"
    )[0]

    telefones = getTuples(
        tabela="cliente_telefones",
        atributos="numero, tipo",
        onde=f"clientes_id = {cliente_id}"
    )

    return cliente, telefones
