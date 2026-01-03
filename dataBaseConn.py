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

def getTuples(tabela, atributos):
    tuples = []

    cursor.execute(f"SELECT {atributos} FROM {tabela}") # Pegando as informações diretamente da tabela 'clientes' do banco de dados

    for tuple in cursor.fetchall():
        tuples.append(tuple)
    return tuples

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

# Criando uma função para atualizar os dados de um cliente específico no banco de dados
def atualizar_dados_clientes(cliente_id, entries): 
    atributos_lista = []
    valores = []

    for rotulo, coluna in mapa.items(): # Percorrendo o dicionário 'mapa' para obter os nomes das colunas e os valores correspondentes
        atributos_lista.append(f"{coluna} = ?")
        valores.append(entries[rotulo].get()) # Obtendo o valor digitado pelo usuário no campo da interface

    valores.append(cliente_id) # Adicionando o ID do cliente ao final da lista de valores para a cláusula WHERE

    sql = f"""
        UPDATE clientes
        SET {', '.join(atributos_lista)}
        WHERE id = ? 
    """
    cursor.execute(sql, tuple(valores)) 
    conn.commit()
# print(getTuples("clientes", "*"))