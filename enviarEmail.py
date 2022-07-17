import win32com.client as win32
import os.path
import re
import os


def enviarEmail(email_para):
    retorno = []

    # criar a integração com o outlook
    outlook = win32.Dispatch('outlook.application')
    # criar um e-mail
    email = outlook.CreateItem(0)

    r = re.compile(r'^[\w-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$')

    # criar configurações do e-mail
    if email_para is None or email_para == '':
        retorno.append(0)
        retorno.append('Não foi informado o e-mail')
        return retorno
    elif r.match(email_para):
        email.to = email_para
    else:
        retorno.append(0)
        retorno.append('Não foi informado um e-mail válido')
        return retorno

    email.Subject = "Relatório da sua Frequência"
    email.HTMLBody = """
    <p>Oi, tudo bem?</p>
    <br />
    <p>Não vou tomar o seu tempo, apenas estou enviando o arquivo do relatório de frequência que você solicitou!</p>
    <br />
    <p>Abraço e até mais!</p>
    """

    anexo = r'C:\Users\Elvis\Videos\relatorio.pdf'
    if os.path.exists(anexo):
        email.Attachments.Add(anexo)
        email.Send()
        os.remove(anexo)
        retorno.append(1)
        retorno.append('E-mail enviado com sucesso')
        return retorno
    else:
        retorno.append(0)
        retorno.append('O arquivo do relatório não existe. Por favor clique no botão Gerar Relatório para criar o arquivo!')
        return retorno
