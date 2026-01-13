import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from tkinter import ttk
from PIL import Image, ImageTk
from dataBaseConn import salvar_dados_clientes, atualizar_dados_clientes, getTuples
from components.entry import Entry
from components.label import Label
from components.btn_IconText import BtnIconText
import re
def abrir_tela_AddUpd_Cliente(titulo, id_cliente = None):
    window = ctk.CTk()
    window.state('zoomed')
    window.title(titulo)
    ctk.set_appearance_mode("light")
    window.configure(fg_color="#FDE6F0")

    window.geometry("800x500")
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.minsize(400, 250)

    entries = {}
    entriesTelefones = []

    if id_cliente != None:
        tupla_cliente = getTuples("CLIENTES", "nome, idade, data_nascimento, cpf, endereco, localidade, email, status", f"id = {id_cliente}")[0]
        print(tupla_cliente)
        lista_telefones = getTuples("CLIENTE_TELEFONES", "numero, tipo", f"clientes_id = {id_cliente}")
        print(lista_telefones)

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

    def apenasNumeros(char, max):
        if char == "":
            return True
    
        # Verifica se é número e se respeita o limite passado
        if char.isdigit() and len(char) <= int(max):
            return True
        
        return False


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

            validador = window.register(apenasNumeros)

            self.entry = Entry(
                self,
                placeholder=placeholder
            )
            self.entry.configure(
                validate="key",
                validatecommand=(validador, "%P")
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
        def atualiza_label(self):
                state_label = "Ativo" if self.var.get() else "Inativo"
                # exibe "Status: Ativo" ou "Status: Inativo"
                self.state_label.configure(text=state_label) # Altera a exibição da label quando ativo => .configure ajusta alguma propriedade, determinada durante a cosntrução do código


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

            self.checkbox = ctk.CTkCheckBox(
                self.container,
                text="",  # remove o texto padrão "CTKcheckbox"
                variable=self.var,
                border_color="#CFA4B5",
                border_width=2,
                corner_radius=15,
                hover_color="#F385AA",
                command=self.atualiza_label
            )
            self.checkbox.grid(row=0, column=0, padx=(8, 5), pady=4, sticky="w")

            self.state_label = Label(self.container, text="", label_width=25)
            self.state_label.grid(row=0, column=1, padx=(5, 8), pady=4, sticky="e")

            entries[label_text.replace(":", "").strip()] = self.var

            self.atualiza_label()

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
                font=ctk.CTkFont(family="Inter Medium", size=15, weight="bold"),
                text_color="#A97456",
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
        text=titulo, 
        corner_radius=10,
        font=ctk.CTkFont(size=20, weight="bold"),
        text_color="#61223D",
        fg_color="#F385AA",
        anchor="w",
        padx=10, pady=6
    ).grid(row=0, column=0, pady=(0, 4), sticky="ew")

    # Criando um array de tuplas, cada uma com o texto de cada label e sua respectiva sugestão (placeholder)

    labels_entry = [
        ("Nome:", "Ex: Pantera"),
        ("Idade:", "Ex: 30"),
        ("Data de Nascimento:", "Ex: 01/01/1990"),
        ("CPF:", "Ex: 000.000.000-00"),
        ("Endereço:", "Ex: Rua das Rosas, 123"),
        ("Cidade:", "Ex: Fortaleza/CE"),
        ("E-mail:", "Ex: pantera.rosa@email.com"),
    ]

    for i, (label, placeholder) in enumerate(labels_entry):
        labelEntry = LabelEntry(form, label, placeholder)
        labelEntry.grid(row=i+1, column=0, sticky="ew", pady=8)
        if label == "CPF:" or label == "Data de Nascimento:" or label == "Idade:":
            validador = window.register(apenasNumeros)
            if label == "CPF:":
                limite = 11
            elif label == "Data de Nascimento:":
                limite = 6
            elif label == "Idade:":
                limite = 2
            labelEntry.entry.configure(
                validate="key",
                validatecommand=(validador, "%P", limite)
                )
        if id_cliente:
            labelEntry.entry.insert(0, tupla_cliente[i])
        

    def adicionarTelefone():
        # global telefonesButtons
        newTel = area_addNum.entry.get() # Obtém o valor digitado na entrada de telefone
        tipoTel = tipo_telefone.get()
        if 10 <= len(newTel) <= 13:# Definindo um tamanho mínimo e máximo para o número de telefone
            if tipoTel == "Selecione o tipo de telefone":
                messagebox.showerror("Erro: tipo telefônico não selecionado", "Selecione o tipo de telefone inserido")
            elif (newTel, tipoTel) in entriesTelefones:
                messagebox.showerror("Já existe", "Telefone ja existente selecione outro")
            else:
                formatar_telefone(newTel) # Após conferir o número, retorna o valor já editado
                telefonesStr.append(f"{newTel} - Telefone {tipoTel}") 
                criarListaTelefones()
                area_addNum.entry.delete(0, tk.END) # Limpando a entrada após adicionar o número
        


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
        font=ctk.CTkFont(size=16),
        state="readonly"
    )
    tipo_telefone.grid(row=8, column=0, sticky="ew")
    tipo_telefone.configure(0, width=1)
    tipo_telefone.set("Selecione o tipo de telefone")

    # Criando uma função que verifca em tempo real o tamanho da entrada do usuãrio e adiciona um tipo de "formatação" para que o número seja enviado para a tabela 

    def formatar_telefone(numero): # Definindo que a função tem um parâmetro event, que serve para identificar os eventos de tecla no teclado quando apertadas
        global tipo_telefone

        if len(numero) == 12: # Verificando se o número digitado possui 
            tipo_telefone.configure(values=["Fixo"]) # Definindo que o único tipo de telefone disponível para esse tamanho (12) é o 'Fixo', evitando que o número seja registrado como 'Celular' ou 'WhatsApp'
            tipo_telefone.set("Fixo")
            numero_local = numero[4:12] # Cortando os oito primeiros dígitos do número local (padrão), ignorando o valor de DDD e DDI
            ddi = numero[0:2] # Cortando os dois primeiros dígitos do número registrado para que sirva como o DDD]
            ddd = numero[2:4] # Cortando os dois próximos dígitos do número para que seja registrado como DDD do número
            telefone_formatado = f"+{ddi} ({ddd}) {numero_local[0:4]}-{numero_local[4:8]}"
            return telefone_formatado
        

    area_addNum = LabelEntryButton(
        form,
        "Número de telefone",
        "Ex: (85) 9 0000-0000",
        "Adicionar telefone",
        entries,
        command=lambda: adicionarTelefone())
    area_addNum.grid(row=9, column=0, sticky="ew", padx=(0,4), pady=8)
    # area_addNum.entry.insert(0, "+55 (85) 9 ") # Inserindo um início de telefone padrão para a entrada de telefone do usuário

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

    telefonesStr = [] # Lista telefônica que será retirada do banco de dados
    if id_cliente:
        for tuple in lista_telefones:
            telefonesStr.append(f"{tuple[0]} - {tuple[1]}")
    telefonesButtons = [] # Lista de botões com os número telefônicos para que possam ser deletados
    numberSlc = None # Número da lista de descarte de números telefonicos selecionado num momento

    def removerTelefone():
        global numberSlc

        if not numberSlc:
            return  # Nada selecionado

        telefonesStr[:] = [t for t in telefonesStr if t != numberSlc] # Cria uma cópia da lista telefonesStr, itera com ela e atualiza a lista original com o telefone deletado, a fim de evitar bugs na hora da iteração

        for btn in telefonesButtons[:]:
            if btn.cget("text") == numberSlc:
                num_tipo = btn.cget("text")
                num = re.sub(r"[\D]","",num_tipo)
                tipo = re.sub(r"[^a-zA-Z]","",(num_tipo.replace("Telefone", "")))
                entriesTelefones.remove((num, tipo))
                print(entriesTelefones)
                btn.destroy()
                telefonesButtons.remove(btn)
        numberSlc = None


    def criarListaTelefones():
        ctk.CTkLabel(
            frame_listaTelefones,
            text="Telefones Registrados",
            font=ctk.CTkFont("Segoe UI", 20, "bold"),
            text_color="#61223D",
            width=20,
            anchor="w",
            corner_radius=10,
            padx=10, pady=6,
            fg_color="#F5C89A"
        ).grid(row=0, column=0, sticky="ew", padx=8, pady=(4,8)) # Criando uma label como t'itulo da lista de telefones

        for i in range(len(telefonesStr)):
            btn = TelefoneButton(
                frame_listaTelefones, 
                text=telefonesStr[i]
            )
            btn.grid(row=i+1, column=0, sticky="ew")
            telefonesButtons.append(btn)
            num_tipo = btn.cget("text")
            num = re.sub(r"[\D]","",num_tipo)
            tipo = re.sub(r"[^a-zA-Z]","",(num_tipo.replace("Telefone", "")))
            entriesTelefones.append((num, tipo))

    criarListaTelefones()

    removeTelBtn = BtnIconText(form, text="Remover telefone", command=lambda: removerTelefone())
    removeTelBtn.grid(row=11, column=0, sticky="ew", padx=(4,0), pady=8)

    checkBox = LabelCheckbox(form, "Status:")
    checkBox.grid(row=12, column=0, padx=5, pady=(8), sticky="nsew")
    if id_cliente:
        if tupla_cliente[7] == 1:
            checkBox.checkbox.select()
            checkBox.atualiza_label()

    buttons_frame = ctk.CTkFrame(form, fg_color="transparent")
    buttons_frame.grid(row=13, column=0, pady=(0, 8))

    BtnIconText(
        buttons_frame,
        text="Salvar",
        command=lambda: salvar_dados_clientes(entries, entriesTelefones)
    ).grid(row=0, column=0, padx=8)

    BtnIconText(
        buttons_frame,
        text="Cancelar",
        command=lambda: print("clicou cancelar")
    ).grid(row=0, column=1, padx=8)

    window.mainloop()

