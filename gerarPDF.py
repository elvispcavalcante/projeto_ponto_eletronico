from fpdf import FPDF
from datetime import datetime
import locale
import conexao_mysql as conector
import info_uteis as info


# Criando uma classe e criando as funções de cabeçalho e rodapé (header e footer) tenho acesso quando adicionar uma
# página (add_page()
class PDF(FPDF):
    # Definindo o local do Aplitivo para ter informações de hora, numeric
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF8')

    # Definindo um cabeçalho para o meu relatório
    def header(self):
        self.add_font('Fascinate', '', r"C:\Users\Elvis\PycharmProjects\gerarPDF\fonts\Fascinate-Regular.ttf", uni=True)
        self.add_font('Roboto-Light', '', r"C:\Users\Elvis\PycharmProjects\gerarPDF\fonts\Roboto-Light.ttf", uni=True)
        self.add_font('Roboto-Bold', '', r"C:\Users\Elvis\PycharmProjects\gerarPDF\fonts\Roboto-Bold.ttf", uni=True)
        self.add_font('Roboto-Italic', '', r"C:\Users\Elvis\PycharmProjects\gerarPDF\fonts\Roboto-Italic.ttf", uni=True)
        # x = Avança para esquerda
        # y = Avança na altura
        # w = Tamanho da imagem
        # h = Altura da imagem
        # link = especifica link para imagem
        self.image(r'imagens\logo_empresa.png', x=None, y=None, w=50)
        self.line(10, 30, 200, 30)
        """cell (width, height, texto, border: 0 ou 1, ln: 0 ou 1 ou 2, align: L ou C ou R, fill: False ou True
        link: adicionando o link
        """
        # Setando a posição do texto seguinte
        self.set_xy(115, 21)

        # Setando a fonte que vou usar nos textos seguintes
        self.set_font('Roboto-Bold', '', 16)  # B - bold / I - Italico / U - Underline / Vazio é regular
        self.cell(w=40, h=10, txt='Registros de Frequência Eletrônica', border=0, ln=2, align='R', fill=False)

    # Definindo um rodapé para o meu relatório
    def footer(self):
        self.add_font('Fascinate', '', r"C:\Users\Elvis\PycharmProjects\gerarPDF\fonts\Fascinate-Regular.ttf", uni=True)
        self.add_font('Roboto-Light', '', r"C:\Users\Elvis\PycharmProjects\gerarPDF\fonts\Roboto-Light.ttf", uni=True)
        self.add_font('Roboto-Bold', '', r"C:\Users\Elvis\PycharmProjects\gerarPDF\fonts\Roboto-Bold.ttf", uni=True)
        self.add_font('Roboto-Italic', '', r"C:\Users\Elvis\PycharmProjects\gerarPDF\fonts\Roboto-Italic.ttf", uni=True)

        self.set_y(280)
        self.set_text_color(0, 0, 0)
        self.line(x1=10, y1=280, x2=200, y2=280)
        self.set_font('Roboto-Italic', '', 11)  # B - bold / I - Italico / U - Underline / Vazio é regular
        self.cell(w=70, h=10, txt=f"Empresa TechIdeas - Ponto Eletrônico", border=0, ln=0, align='L',
                  fill=False)
        self.cell(w=50, h=10, txt=f"Data: {datetime.today().strftime('%d de %B de %Y')}", border=0, ln=0, align='L',
                  fill=False)
        self.cell(w=30, h=10, txt=f"Hora: {datetime.now().strftime('%H:%M:%S')}", border=0, ln=0, align='L',
                  fill=False)
        self.cell(w=40, h=10, txt=f"Página 1 de 1", border=0, ln=0, align='R', fill=False)


def criarPDF(mes_digitado, ano_digitado, cpf_digitado, senha_digitada):

    # criando a conexão
    conexao = conector.criarConexaoDB(info.host, info.usuario, info.senha, info.database)

    retorno = []
    id_funcionario = 0
    mes = 0
    ano = 0
    # Dados do usuário
    cpf = cpf_digitado
    senha = senha_digitada
    query = f"SELECT id_funcionario FROM login WHERE login='{cpf}' and senha='{senha}'"
    login = conector.executar_query_selecao(conexao, query)

    # Verificação se o usuário digitado encontra-se na base de dados
    if len(login) == 0:
        mensagem = "Usuário ou senha não foi digitado ou Usuário ou Senha inválidos.\n " \
                   "Digite os campos corretamente e clique no botão"
        retorno.append(0)
        retorno.append(mensagem)
        return retorno
    if len(login) != 0:
        loginLista = list(login[0])
        id_funcionario = loginLista[0]

    if 0 < int(mes_digitado) <= 12 and int(ano_digitado) >= 2022:
        mes = int(mes_digitado)
        ano = int(ano_digitado)
    else:
        mensagem = "Mês ou Ano Inválidos"
        retorno.append(0)
        retorno.append(mensagem)
        return retorno

    # A partir desse momento estou criando o arquivo do relatório
    # Criação de um documento PDF
    pdf = PDF('P', 'mm', 'A4')  # P - Portrait / L - Landscape
    # Colocando o autor do Relatório
    pdf.set_author('Elvis Ponte Cavalcante')
    # Definindo um zoom quando abrir a página do relatório
    pdf.set_display_mode('fullpage', 'single')
    # Quebra automática de página
    pdf.set_auto_page_break(auto=True, margin=2.0)
    # Adicionando uma página
    pdf.add_page()
    # Adicionando Fontes no meu relatório
    pdf.add_font('Fascinate', '', r"C:\Users\Elvis\PycharmProjects\gerarPDF\fonts\Fascinate-Regular.ttf", uni=True)
    pdf.add_font('Roboto-Light', '', r"C:\Users\Elvis\PycharmProjects\gerarPDF\fonts\Roboto-Light.ttf", uni=True)
    pdf.add_font('Roboto-Bold', '', r"C:\Users\Elvis\PycharmProjects\gerarPDF\fonts\Roboto-Bold.ttf", uni=True)

    # Posso adicionar páginas que quando necessitar
    # pdf.add_page()

    sql = f"SELECT * FROM relatorio_registros where mes = {mes} and ano = {ano} and id_funcionario = " \
          f"{id_funcionario} ORDER BY id_funcionario, data_mensal"

    resultado_view = conector.executar_query_selecao(conexao, sql)
    lista_resultado = []

    if len(resultado_view) == 0:
        mensagem = "A pesquisa de ano e mês do funcionário não retornou resultados para geração do relatório"
        retorno.append(0)
        retorno.append(mensagem)
        return retorno
    else:
        for registro in resultado_view:
            lista_resultado.append(list(registro))

        qtde_registros = len(lista_resultado)

        funcionario = lista_resultado[0][4]
        mes_referencia = lista_resultado[0][1]
        if mes_referencia < 10:
            mes_referencia = '0'+str(mes_referencia)

        ano_referencia = lista_resultado[0][2]
        matricula = lista_resultado[0][6]

        pdf.set_xy(150, 35)
        pdf.cell(50, 6, f'Referência: {mes_referencia}/{ano_referencia}', 0, 0, 'R', fill=False)

        pdf.set_xy(10, 50)
        pdf.set_font('Roboto-Bold', 'U', 14)
        pdf.cell(200, 10, f'Colaborador: {funcionario}', 0, 1, 'L', fill=False)
        pdf.cell(30, 10, f'Matrícula: {matricula}', 0, 0, 'L', fill=False)

        # cabeçalho da tabela
        pdf.set_xy(30, 80)
        pdf.set_font('Roboto-Bold', '', 10)
        pdf.cell(25, 6, 'Data Mensal', 1, 0, 'C', fill=False)
        pdf.cell(25, 6, 'Início Manhã', 1, 0, 'C', fill=False)
        pdf.cell(25, 6, 'Final Manhã', 1, 0, 'C', fill=False)
        pdf.cell(25, 6, 'Início Tarde', 1, 0, 'C', fill=False)
        pdf.cell(25, 6, 'Final Tarde', 1, 0, 'C', fill=False)
        pdf.cell(25, 6, 'Total Hs Trab.', 1, 0, 'C', fill=False)
        pdf.ln(6)

        # conteúdo da tabela
        for i in range(qtde_registros):
            data_mensal = lista_resultado[i][0]
            mes = lista_resultado[i][1]
            ano = lista_resultado[i][2]
            # id_funcionario = lista_resultado[i][3]
            # nome_funcionario = lista_resultado[i][4]
            # cpf = lista_resultado[i][5]
            # matricula = lista_resultado[i][6]
            # data_registro = lista_resultado[i][7]

            registro_manha_inicial = None
            if lista_resultado[i][8] is None:
                registro_manha_inicial = '00:00:00'
            else:
                registro_manha_inicial = lista_resultado[i][8]

            registro_manha_final = None
            if lista_resultado[i][9] is None:
                registro_manha_final = '00:00:00'
            else:
                registro_manha_final = lista_resultado[i][9]

            registro_tarde_inicial = None
            if lista_resultado[i][10] is None:
                registro_tarde_inicial = '00:00:00'
            else:
                registro_tarde_inicial = lista_resultado[i][10]

            registro_tarde_final = None
            if lista_resultado[i][11] is None:
                registro_tarde_final = '00:00:00'
            else:
                registro_tarde_final = lista_resultado[i][11]

            total_horas_manha = lista_resultado[i][12]
            total_horas_tarde = lista_resultado[i][13]
            total_horas_trabalhadas = lista_resultado[i][14]
            total_horas_decimal = lista_resultado[i][15]

            pdf.set_x(30)
            pdf.set_font('Roboto-Light', '', 10)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(25, 6, datetime.strptime(f"{data_mensal}", '%Y-%m-%d').strftime('%d/%m/%Y'), 1, 0, 'C', fill=False)
            pdf.cell(25, 6, str(registro_manha_inicial), 1, 0, 'C', fill=False)
            pdf.cell(25, 6, str(registro_manha_final), 1, 0, 'C', fill=False)
            pdf.cell(25, 6, str(registro_tarde_inicial), 1, 0, 'C', fill=False)
            pdf.cell(25, 6, str(registro_tarde_final), 1, 0, 'C', fill=False)
            if total_horas_decimal < 8.0:
                pdf.set_text_color(245, 51, 7)
                pdf.cell(25, 6, str(total_horas_trabalhadas), 1, 0, 'C', fill=False)
            else:
                pdf.set_text_color(0, 0, 0)
                pdf.cell(25, 6, str(total_horas_trabalhadas), 1, 0, 'C', fill=False)
            pdf.ln(6)

        sql = 'SELECT sum(total_horas_trabalhadas_decimal) FROM relatorio_registros;'
        resultado_view = conector.executar_query_selecao(conexao, sql)
        total_horas_trabalhadas_decimal = resultado_view[0][0]

        sql = 'SELECT sum(total_horas_trabalhadas_decimal) FROM relatorio_registros;'
        resultado_view = conector.executar_query_selecao(conexao, sql)
        total_horas_trabalhadas_decimal = resultado_view[0][0]

        sql = f'SELECT qtde_horas_a_trabalhar FROM qtde_horas_mes WHERE mes={mes} and ano={ano}'
        resultado_view = conector.executar_query_selecao(conexao, sql)
        total_de_horas_a_trabalhar_no_mes = resultado_view[0][0]

        saldo = total_de_horas_a_trabalhar_no_mes - total_horas_trabalhadas_decimal

        pdf.ln(12)
        pdf.set_font('Roboto-Bold', '', 16)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(30, 10, f'Total de horas trabalhadas: {total_horas_trabalhadas_decimal}', 0, 1, 'L', fill=False)
        pdf.cell(30, 10, f'Total de horas a trabalhar no mês: {total_de_horas_a_trabalhar_no_mes}', 0, 1, 'L', fill=False)
        if saldo < 0:
            saldo = 'Você cumpriu com as horas trabalhadas no mês'
            pdf.set_text_color(0, 0, 0)
            pdf.cell(30, 10, f'Você cumpriu com as horas a trabalhar no mês!', 0, 1, 'L', fill=False)
        else:
            pdf.set_text_color(245, 51, 7)
            pdf.cell(30, 10, f'Você ainda não cumpriu com as horas trabalhadas. Faltam {saldo}', 0, 1, 'L', fill=False)

        # F - salva no local(pasta) do código - pdf.output('teste.pdf', 'F')
        # destino= Salva no diretorio escolhido - pdf.output(r'C:\Users\Elvis\Videos\teste.pdf')
        pdf.output(r'C:\Users\Elvis\Videos\relatorio.pdf')
        conector.encerrar_conexao(conexao)

        retorno.append(1)
        retorno.append('A geração do relatório PDF foi realizada com sucesso')
        return retorno
