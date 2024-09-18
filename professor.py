from tkinter import *
from tkinter import ttk
from banco import conectar, close_connection, selectCidades, selectCurso

class Professor:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Inserir Professores")

        # Frame para o título
        self.janela1 = Frame(master)
        self.janela1.pack(padx=10, pady=10)
        self.msg1 = Label(self.janela1, text="Cadastre um Professor:")
        self.msg1["font"] = ("Verdana", "14", "bold")
        self.msg1.pack()

        # Frame para o nome
        self.janela2 = Frame(master)
        self.janela2["padx"] = 20
        self.janela2.pack()
        self.nome_label = Label(self.janela2, text="Nome completo:")
        self.nome_label.pack(side="left")
        self.nome = Entry(self.janela2, width=30)
        self.nome.pack(side="left")

        # Frame para o endereço
        self.janela3 = Frame(master)
        self.janela3["padx"] = 20
        self.janela3.pack(pady=5)
        self.endereco_label = Label(self.janela3, text="Endereco:")
        self.endereco_label.pack(side="left")
        self.endereco = Entry(self.janela3, width=30)
        self.endereco.pack(side="left")

        # Frame para o e-mail
        self.janela4 = Frame(master)
        self.janela4["padx"] = 20
        self.janela4.pack(pady=5)
        self.email_label = Label(self.janela4, text="E-mail:")
        self.email_label.pack(side="left")
        self.email = Entry(self.janela4, width=30)
        self.email.pack(side="left")

        # Frame para o telefone
        self.janela5 = Frame(master)
        self.janela5["padx"] = 20
        self.janela5.pack(pady=5)
        self.telefone_label = Label(self.janela5, text="Telefone:")
        self.telefone_label.pack(side="left")
        self.telefone = Entry(self.janela5, width=30)
        self.telefone.pack(side="left")

        # Frame para o CPF
        self.janela6 = Frame(master)
        self.janela6["padx"] = 20
        self.janela6.pack(pady=5)
        self.cpf_label = Label(self.janela6, text="CPF:")
        self.cpf_label.pack(side="left")
        self.cpf = Entry(self.janela6, width=30)
        self.cpf.pack(side="left")

        # Frame para a data de nascimento
        self.janela7 = Frame(master)
        self.janela7["padx"] = 20
        self.janela7.pack(pady=5)
        self.nascimento_label = Label(self.janela7, text="Nascimento:")
        self.nascimento_label.pack(side="left")
        self.nascimento = Entry(self.janela7, width=30)
        self.nascimento.pack(side="left")

        # Frame para a cidade
        self.janela8 = Frame(master)
        self.janela8["padx"] = 20
        self.janela8.pack()
        self.cidade_label = Label(self.janela8, text="Cidade:")
        self.cidade_label.pack(side="left")
        self.cidade_combobox = ttk.Combobox(self.janela8, width=27)
        self.cidade_combobox.pack(side="left")
        self.carregarCidades()

        # Frame para o curso
        self.janela9 = Frame(master)
        self.janela9["padx"] = 20
        self.janela9.pack(pady=5)
        self.curso_label = Label(self.janela9, text="Curso:")
        self.curso_label.pack(side="left")
        self.curso_combobox = ttk.Combobox(self.janela9, width=27)
        self.curso_combobox.pack(side="left")
        self.carregarCurso()

        self.janela10 = Frame(master)
        self.janela10["padx"] = 20
        self.janela10.pack(pady=5)
        self.botao = Button(self.janela10, width=10, text="Inserir", command=self.inserir_professor)
        self.botao.pack(side="left")

        self.janela11 = Frame(master)
        self.janela11["padx"] = 20
        self.janela11.pack(pady=10)
        self.mensagem = Label(self.janela11, text="")
        self.mensagem["font"] = ("Verdana", "10", "italic", "bold")
        self.mensagem.pack()

        self.janela12 = Frame(master)
        self.janela12["padx"] = 20
        self.janela12.pack(pady=10)
        self.tree = ttk.Treeview(self.janela12, columns=("ID", "Nome", "Endereço", "Email", "Telefone", "CPF", "Nascimento", "Cidade", "Curso"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Endereço", text="Endereço")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.heading("CPF", text="CPF")
        self.tree.heading("Nascimento", text="Nascimento")
        self.tree.heading("Cidade", text="Cidade")
        self.tree.heading("Curso", text="Curso")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nome", width=150, anchor="w")
        self.tree.column("Endereço", width=150, anchor="w")
        self.tree.column("Email", width=150, anchor="w")
        self.tree.column("Telefone", width=100, anchor="w")
        self.tree.column("CPF", width=100, anchor="w")
        self.tree.column("Nascimento", width=100, anchor="w")
        self.tree.column("Cidade", width=100, anchor="w")
        self.tree.column("Curso", width=100, anchor="w")
        self.tree.pack(fill=BOTH, expand=True)

        self.tree.bind("<ButtonRelease-1>", self.selecionar_linha)

        self.db = conectar()
        self.atualizarTabela()

    def carregarCidades(self):
        cidades = selectCidades()
        self.cidade_combobox['values'] = [cidade[1] for cidade in cidades]
        self.cidades_dicionario = {cidade[1]: cidade[0] for cidade in cidades}

    def carregarCurso(self):
        cursos = selectCurso()
        self.curso_combobox['values'] = [curso[1] for curso in cursos]
        self.cursos_dicionario = {curso[1]: curso[0] for curso in cursos}

    def inserir_professor(self):
        professor = self.nome.get()
        endereco = self.endereco.get()
        email = self.email.get()
        telefone = self.telefone.get()
        cpf = self.cpf.get()
        nascimento = self.nascimento.get()
        cidade_nome = self.cidade_combobox.get()
        cidade_codigo = self.cidades_dicionario.get(cidade_nome)  # Obtém o código da cidade
        curso_nome = self.curso_combobox.get()
        curso_codigo = self.cursos_dicionario.get(curso_nome)  # Obtém o código do curso

        if not self.db:
            self.mensagem.config(text="Erro: Sem conexão com o banco de dados", fg="red")
            return

        try:
            cursor = self.db.cursor()
            query = """
                INSERT INTO tbl_professores (pro_nome, pro_endereco, pro_email, pro_telefone, pro_cpf, pro_nascimento, cid_codigo, cur_codigo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (professor, endereco, email, telefone, cpf, nascimento, cidade_codigo, curso_codigo))
            self.db.commit()
            self.mensagem.config(text="Professor cadastrado com sucesso!", fg="green")
            self.atualizarTabela()  # Atualiza a tabela após a inserção

        except Exception as e:
            self.mensagem.config(text=f"Erro: {e}", fg="red")

        finally:
            cursor.close()

    def fechar(self):
        close_connection(self.db)
        self.master.destroy()

    def atualizarTabela(self):
        professores = self.selectAllProfessor()
        self.tree.delete(*self.tree.get_children())
        for p in professores:
            self.tree.insert("", "end", values=(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]))

    def selecionar_linha(self, event):
        item_selecionado = self.tree.selection()
        if item_selecionado:
            valores = self.tree.item(item_selecionado[0], 'values')
            self.nome.delete(0, END)
            self.nome.insert(END, valores[1])
            self.endereco.delete(0, END)
            self.endereco.insert(END, valores[2])
            self.email.delete(0, END)
            self.email.insert(END, valores[3])
            self.telefone.delete(0, END)
            self.telefone.insert(END, valores[4])
            self.cpf.delete(0, END)
            self.cpf.insert(END, valores[5])
            self.nascimento.delete(0, END)
            self.nascimento.insert(END, valores[6])
            self.cidade_combobox.set(self.cidade_nome_por_codigo(valores[7]))
            self.curso_combobox.set(self.curso_nome_por_codigo(valores[8]))

    def selectAllProfessor(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM tbl_professores")
            linhas = cursor.fetchall()
            cursor.close()
            return linhas
        except Exception as e:
            self.mensagem.config(text=f"Erro na recuperação dos professores: {e}", fg="red")
            return []

    def cidade_nome_por_codigo(self, codigo):
        for nome, cod in self.cidades_dicionario.items():
            if cod == codigo:
                return nome
        return ""

    def curso_nome_por_codigo(self, codigo):
        for nome, cod in self.cursos_dicionario.items():
            if cod == codigo:
                return nome
        return []
