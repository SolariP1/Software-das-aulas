from tkinter import *
from tkinter import ttk
from banco import conectar, close_connection

class Curso:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Cadastro de Curso")

        self.janela1 = Frame(master)
        self.janela1.pack()
        self.msg1 = Label(self.janela1, text="Cadastre um curso:")
        self.msg1["font"] = ("Verdana", "14", "bold")
        self.msg1.pack()

        self.janela2 = Frame(master)
        self.janela2["padx"] = 20
        self.janela2.pack()
        self.curso_label = Label(self.janela2, text="Nome do curso:")
        self.curso_label.pack(side="left")
        self.curso = Entry(self.janela2, width=30)
        self.curso.pack(side="left")

        self.janela3 = Frame(master)
        self.janela3["padx"] = 20
        self.janela3.pack(pady=5)
        self.valor_label = Label(self.janela3, text="Valor do curso:")
        self.valor_label.pack(side="left")
        self.valor = Entry(self.janela3, width=28)
        self.valor.pack(side="left")

        self.janela5 = Frame(master)
        self.janela5["padx"] = 20
        self.janela5.pack(pady=10)
        self.botao1 = Button(self.janela5, width=10, text="Cadastrar", command=self.inserir_curso)
        self.botao1.pack(side="left")

        self.janela6 = Frame(master)
        self.janela6["padx"] = 20
        self.janela6.pack(pady=10)
        self.mensagem = Label(self.janela6, text="")
        self.mensagem["font"] = ("Verdana", "10", "italic", "bold")
        self.mensagem.pack()

        self.janela12 = Frame(master)
        self.janela12["padx"] = 20
        self.janela12.pack(pady=10)
        self.tree = ttk.Treeview(self.janela12, columns=("ID", "Curso", "Valor"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Curso", text="Curso")
        self.tree.heading("Valor", text="Valor")
        self.tree.pack()

        self.tree.bind("<ButtonRelease-1>", self.selecionar_linha)

        self.db = conectar()
        self.atualizarTabela()

        self.db = conectar()

    def inserir_curso(self):
        nome = self.curso.get()
        valor = self.valor.get()

        if not self.db:
            self.mensagem.config(text="Erro: Sem conexão com o banco de dados", fg="red")
            return

        try:
            cursor = self.db.cursor()
            query = "INSERT INTO tbl_curso (cur_nome, cur_valor) VALUES (%s, %s)"
            cursor.execute(query, (nome, valor))
            self.db.commit()
            self.mensagem.config(text="Curso cadastrado com sucesso!", fg="green")

        except Exception as e:
            self.mensagem.config(text=f"Erro: {e}", fg="red")

        finally:
            cursor.close()

    def fechar(self):
        close_connection(self.db)
        self.master.destroy()

    def atualizarTabela(self):
        curso = self.selectAllCursos()
        self.tree.delete(*self.tree.get_children())
        for c in curso:
            self.tree.insert("", "end", values=(c[0], c[1], c[2]))

    def selecionar_linha(self, event):
        item_selecionado = self.tree.selection()
        if item_selecionado:
            valores = self.tree.item(item_selecionado[0], 'values')
            self.curso.delete(0, END)
            self.curso.insert(END, valores[1])
            self.valor.delete(0, END)
            self.valor.insert(END, valores[2])

    def selectAllCursos(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM tbl_curso")
            linhas = cursor.fetchall()
            cursor.close()
            return linhas
        except Exception as e:
            self.mensagem.config(text=f"Erro na recuperação das cursos: {e}", fg="red")
            return []
