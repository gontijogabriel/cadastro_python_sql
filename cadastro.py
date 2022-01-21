from tkinter import *
from tkinter import ttk
import sqlite3

root = Tk()

class Funcs():
    def limpaTela(self):
        self.cdEntry.delete(0, END)
        self.nomeEntry.delete(0, END)
        self.telefoneEntry.delete(0, END)
        self.cidadeEntry.delete(0, END)
    def conectaDb(self):
        self.conn = sqlite3.connect('clientes.bd')
        self.cursor = self.conn.cursor(); print('Conectando ao banco de dados')
    def desconectaDb(self):
        self.conn.close(); print('Desconectando ao banco de dados')
    def montaTabelas(self):
        self.conectaDb()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cod INTEGER PRIMARY KEY,
                nome_cliente CHAR(40) NOT NULL,
                telefone INTEGER (20),
                cidade CHAR (40)
            );
        """)
        self.conn.commit(); print('Banco de dados criado')
        self.desconectaDb()
    def variaveis(self):
        self.codigo = self.cdEntry.get()
        self.nome = self.nomeEntry.get()
        self.telefone = self.telefoneEntry.get()
        self.cidade = self.cidadeEntry.get()
    def addCliente(self):
        self.variaveis()
        self.conectaDb()
        self.cursor.execute(""" INSERT INTO clientes (nome_cliente, telefone, cidade)
            VALUES (?, ?, ?)""", (self.nome, self.telefone, self.cidade))
        self.conn.commit()
        self.desconectaDb()
        self.selectLista()
        self.limpaTela()
    def selectLista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conectaDb()
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes
            ORDER BY nome_cliente ASC; """)
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconectaDb()
    def onDoubleClick(self, event):
        self.limpaTela()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4 = self.listaCli.item(n, 'values')
            self.cdEntry.insert(END, col1)
            self.nomeEntry.insert(END, col2)
            self.telefoneEntry.insert(END, col3)
            self.cidadeEntry.insert(END, col4)

    def deletaCliente(self):
        self.variaveis()
        self.conectaDb()
        self.cursor.execute(""" DELETE FROM clientes WHERE cod = ? """, self.codigo)
        self.conn.commit()
        self.desconectaDb()
        self.limpaTela()
        self.selectLista()
    def alterarCliente(self):
        self.variaveis()
        self.conectaDb()
        self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, telefone = ?, cidade = ?
            WHERE cod = ? """, (self.nome, self.telefone, self.cidade, self.codigo))
        self.conn.commit()
        self.desconectaDb()
        self.selectLista()
        self.limpaTela()
    def buscaCliente(self):
        self.conectaDb()
        self.listaCli.delete(*self.listaCli.get_children())

        self.nomeEntry.insert(END, '%')
        nome = self.nomeEntry.get()
        self.cursor.execute(
            """ SELECT cod, nome_cliente, telefone, cidade FROM clientes 
            WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC""" % nome)
        buscaNomeCli = self.cursor.fetchall()
        for i in buscaNomeCli:
            self.listaCli.insert("", END, values=i)
        self.limpaTela()
        self.desconectaDb()

class Application(Funcs):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames()
        self.widgetsFrame1()
        self.listaFrame2()
        self.montaTabelas()
        self.selectLista()
        self.menu()

        root.mainloop()
    def tela(self):
        self.root.title('Cadastro de Clientes')
        self.root.configure(background= '#ccc')
        self.root.geometry('768x588')
        self.root.resizable(True, True)
        self.root.maxsize(width=900, height=700)
        self.root.minsize(width=600, height=400)
    def frames(self):
        self.frame1 = Frame(self.root, bd=4, bg='#fff', highlightbackground='black', highlightthickness=2)
        self.frame1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame2 = Frame(self.root, bd=4, bg='#fff', highlightbackground='black', highlightthickness=2)
        self.frame2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)
    def widgetsFrame1(self):

        # Botao Limpar
        self.btLimpar = Button(self.frame1, text='Limpar', bd=2, bg='white', fg='red', command=self.limpaTela)
        self.btLimpar.place(relx=0.2, rely=0.1, relwidth=0.07, relheight=0.1)

        # Botao Buscar
        self.btBuscar = Button(self.frame1, text='Buscar', bd=2, bg='blue', fg='white', command=self.buscaCliente)
        self.btBuscar.place(relx=0.3, rely=0.1, relwidth=0.07, relheight=0.1)

        # Botao Novo
        self.btNovo = Button(self.frame1, text='Novo', bd=2, bg='green', command= self.addCliente)
        self.btNovo.place(relx=0.7, rely=0.1, relwidth=0.07, relheight=0.1)

        # Botao Alterar
        self.btAlterar = Button(self.frame1, text='Alterar', bd=2, bg='yellow', command= self.alterarCliente)
        self.btAlterar.place(relx=0.8, rely=0.1, relwidth=0.07, relheight=0.1)

        # Botao Apagar
        self.btApagar = Button(self.frame1, text='Apagar', bd=2, bg='red', font=('verdana', 8, 'bold'), command=self.deletaCliente)
        self.btApagar.place(relx=0.9, rely=0.1, relwidth=0.07, relheight=0.1)

        # Label e Entrada Codigo
        self.lbCodigo = Label(self.frame1, text='Código', bg='white')
        self.lbCodigo.place(relx=0.055, rely=0.03)
        self.cdEntry = Entry(self.frame1, bd=2)
        self.cdEntry.place(relx=0.05, rely=0.12, relwidth=0.07, relheight=0.1)

        # Label e Entrada Nome
        self.lbNome = Label(self.frame1, text='Nome', bg='white')
        self.lbNome.place(relx=0.055, rely=0.33)
        self.nomeEntry = Entry(self.frame1, bd=2)
        self.nomeEntry.place(relx=0.05, rely=0.42, relwidth=0.25, relheight=0.1)

        # Label e Entrada Telefone
        self.lbTelefone = Label(self.frame1, text='Telefone', bg='white')
        self.lbTelefone.place(relx=0.355, rely=0.33)
        self.telefoneEntry = Entry(self.frame1, bd=2)
        self.telefoneEntry.place(relx=0.35, rely=0.42, relwidth=0.15, relheight=0.1)

        # Label e Entrada Cidade
        self.lbCidade = Label(self.frame1, text='Cidade', bg='white')
        self.lbCidade.place(relx=0.555, rely=0.33)
        self.cidadeEntry = Entry(self.frame1, bd=2)
        self.cidadeEntry.place(relx=0.55, rely=0.42, relwidth=0.1, relheight=0.1)

    def listaFrame2(self):
        self.listaCli = ttk.Treeview(self.frame2, height=3, column=('col1', 'col2', 'col3', 'col4'))
        self.listaCli.heading('#0', text='')
        self.listaCli.heading('#1', text="Codigo")
        self.listaCli.heading('#2', text="Nome")
        self.listaCli.heading('#3', text="Telefone")
        self.listaCli.heading('#4', text="Cidade")

        self.listaCli.column('#0', width=1)
        self.listaCli.column('#1', width=50)
        self.listaCli.column('#2', width=200)
        self.listaCli.column('#3', width=125)
        self.listaCli.column('#4', width=125)

        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroolLista = Scrollbar(self.frame2, orient='vertical')
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)

        #Double Click
        self.listaCli.bind("<Double-1>", self.onDoubleClick)
        
    def menu(self):
        menuBar = Menu(self.root)
        self.root.config(menu=menuBar)
        fileMenu1 = Menu(menuBar)
        fileMenu2 = Menu(menuBar)

        def quit(): self.root.destroy()

        menuBar.add_cascade(label = 'Opções', menu= fileMenu1)
        menuBar.add_cascade(label='Sobre', menu= fileMenu2)

        fileMenu1.add_command(label = 'Sair', command= quit)
        fileMenu2.add_command(label="Limpa Cliente", command= self.limpaTela)


Application()