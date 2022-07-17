from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import ponto_registrar as ponto
import tkinter.font as tkFont
import gerarPDF
import os
import enviarEmail as envio_email


# função para chamar a função de registrar o ponto e controle das mensagens
def registro():
    # Chamando a função registrar ponto da biblioteca
    resultado = ponto.registrar_ponto(cpf_entrada.get(), senha_entrada.get())
    if resultado[0] == 0:
        messagebox.showerror("Erro", resultado[1])
    elif resultado[0] == 2:
        messagebox.showinfo("Registro Ponto", resultado[1])
    elif resultado[0] == 3:
        messagebox.showwarning("Aviso", resultado[1])


def relatorio():
    resultado = gerarPDF.criarPDF(mes_entrada.get(), ano_entrada.get(), cpf_entrada.get(), senha_entrada.get())
    if resultado[0] == 0:
        messagebox.showerror("Erro", resultado[1])
    elif resultado[0] == 1:
        messagebox.showinfo("Relatório", resultado[1])

    os.system(r'C:\Users\Elvis\Videos\relatorio.pdf')


def enviarEmailRelatorio():
    resultado = envio_email.enviarEmail(email_entrada.get())
    if resultado[0] == 0:
        messagebox.showerror("Erro", resultado[1])
    else:
        messagebox.showinfo("Envio E-mail", resultado[1])

# função para chamar quando apertar a tecla enter
def callback():
    registro()


# Iniciando a Janela
janela = Tk()

# Colocando o título da Janela
janela.title('Ponto eletrônico')

# Não deixando a janela mudar de tamanho
janela.resizable(width=True, height=True)

# Tamanho da tela
janela.geometry('610x700+400+40')

# função para iniciar quando apertar a tecla enter
janela.bind('<Return>', callback)

# Colocando uma logo na janela
logo = Image.open("imagens/logo_empresa.png")
# Redimensionando a imagem dividindo a largura e altura por 10 e convertendo para inteiro
logo = logo.resize((int(logo.width/10), int(logo.height/10)))
# Transformando a Imagem Utilizada compatível com o Tkinter
logo = ImageTk.PhotoImage(logo)
# Criando um Label com a Imagem
imagem = Label(janela, text="logo_empresa", image=logo)
# Adicionando a imagem a tela com o grid
imagem.grid(column=0, row=0, padx=20, pady=5, columnspan=2)

# Utilizando um fontstyle para utilizar nos textos
fontStyle = tkFont.Font(size=25, weight='bold')
# Definindo um label
texto_orientacao = Label(janela, text="Ponto Eletrônico da Empresa", font=fontStyle)
# Acrescentando o label na tela
texto_orientacao.grid(column=0, row=1, padx=30, pady=10, columnspan=2)

# Utilizando um fontstyle para utilizar nos textos
fontStyle = tkFont.Font(size=15)
# Definindo um label
texto_orientacao = Label(janela, text="Para registrar informe os dados abaixo e clique no botão", font=fontStyle)
# Acrescentando o label na tela
texto_orientacao.grid(column=0, row=2, padx=15, pady=15, columnspan=2)

# Utilizando um fontstyle para utilizar nos textos
fontStyle = tkFont.Font(size=14)

# Criando campo para digitar o CPF
cpf_entrada = Entry(janela, width=20, font=fontStyle)
# Forçando com que o cursor inicie no campo
cpf_entrada.focus_force()
# Criando campo para digitar a senha
senha_entrada = Entry(janela, show='*', width=15, font=fontStyle)

# Utilizando um fontstyle para utilizar nos textos
fontStyle = tkFont.Font(size=13)

# Criando um label para os campos de CPF e Senha
label_cpf = Label(janela, text="Digite o seu CPF", font=fontStyle)
label_senha = Label(janela, text="Digite a sua senha", font=fontStyle)

# Adicionando o label na tela
label_cpf.grid(column=0, row=3, padx=15, pady=15)
# Adicionando o cpf na tela
cpf_entrada.grid(column=1, row=3, padx=0, pady=15, sticky=W)

# Adicionando o label na tela
label_senha.grid(column=0, row=4, padx=15, pady=15)
# Adicionando a senha na tela
senha_entrada.grid(column=1, row=4, padx=0, pady=15, sticky=W)

# Utilizando um fontstyle para utilizar no texto do botão
fontStyle = tkFont.Font(size=15, weight='bold')
# Criando um botão e chamando a função de registro no botão ao clicar
botao = Button(janela, text="REGISTRAR PONTO", command=registro, font=fontStyle)
# Colocando a cor no botão
botao['bg'] = '#00e676'
# Adicionando o botão na tela
botao.grid(column=0, row=5, padx=15, pady=15, columnspan=2)


# Utilizando um fontstyle para utilizar nos textos
fontStyle = tkFont.Font(size=14)
# Criando o campo para ler o mês e o ano
mes_entrada = Entry(janela, width=6, font=fontStyle)
ano_entrada = Entry(janela, width=10, font=fontStyle)

# Utilizando um fontstyle para utilizar nos textos
fontStyle = tkFont.Font(size=13)
# Criando um label para os campos de Ano e Mês
label_mes = Label(janela, text="Digite o Mês", font=fontStyle)
label_ano = Label(janela, text="Digite o Ano", font=fontStyle)

# Adicionando o label na tela
label_mes.grid(column=0, row=7, padx=2, pady=15)
# Adicionando o mês na tela
mes_entrada.grid(column=1, row=7, padx=0, pady=15, sticky=W)

# Adicionando o label na tela
label_ano.grid(column=0, row=8, padx=2, pady=15, sticky=N)
# Adicionando o ano na tela
ano_entrada.grid(column=1, row=8, padx=0, pady=5, sticky=W)

# Utilizando um fontstyle para utilizar nos textos
fontStyle = tkFont.Font(size=14)
# Criando o campo para ler o mês e o ano
email_entrada = Entry(janela, width=25, font=fontStyle)
# Utilizando um fontstyle para utilizar nos textos
fontStyle = tkFont.Font(size=13)
# Criando um label para os campos de Ano e Mês
label_email = Label(janela, text="Digite o seu e-mail", font=fontStyle)
# Adicionando o label na tela
label_email.grid(column=0, row=9, padx=2, pady=15)
# Adicionando o ano na tela
email_entrada.grid(column=1, row=9, padx=0, pady=5, sticky=E)


# Utilizando um fontstyle para utilizar no texto do botão
fontStyle = tkFont.Font(size=15, weight='bold')
# Criando um botão e chamando a função de registro no botão ao clicar
rel = Button(janela, text="GERAR RELATÓRIO", command=relatorio, font=fontStyle)
# Colocando a cor no botão
rel['bg'] = '#00e676'
# Adicionando o botão na tela
rel.grid(column=0, row=11, padx=40, pady=40)

eml = Button(janela, text="ENVIAR E-MAIL", command=enviarEmailRelatorio, font=fontStyle)
eml['bg'] = '#00e676'
eml.grid(column=1, row=11, padx=15, pady=15)


# para manter a tela aberta
janela.mainloop()
