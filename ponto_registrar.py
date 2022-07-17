from datetime import datetime, timedelta
import conexao_mysql as conector
from datetime import datetime
import info_uteis as info


def registrar_ponto(cpf_digitado, senha_digitada):
    # criação da conexão com o banco de dados
    conexao = conector.criarConexaoDB(info.host, info.usuario, info.senha, info.database)

    retorno = []
    mensagem = ''

    # Fazer função registrar ponto depois
    id_funcionario = 0

    # Dados do usuário
    cpf = cpf_digitado
    senha = senha_digitada
    query = f"SELECT id_funcionario FROM login WHERE login='{cpf}' and senha='{senha}'"
    login = conector.executar_query_selecao(conexao, query)

    # Verificação se o usuário digitado encontra-se na base de dados
    if len(login) == 0:
        mensagem = "Usuário ou senha não foi digitado ou Usuário ou Senha inválidos.\n" \
                   "Digite os campos corretamente e clique no botão"
        retorno.append(0)
        retorno.append(mensagem)
        return retorno
    if len(login) != 0:
        loginLista = list(login[0])
        id_funcionario = loginLista[0]

    # lancamentos dos registros de ponto

    # DATA ATUAL
    data_atual = datetime.today().strftime('%Y-%m-%d')
    # HORA ATUAL
    hora_atual = datetime.now().strftime('%H:%M:%S')

    # VARIAVEIS QUE ARMAZERÃO O REGISTRO DO PONTO
    registro1 = None
    registro2 = None
    registro3 = None
    registro4 = None

    # VERIFICAR SE FUNCIONÁRIO JÁ POSSUI REGISTRO NO DIA ATUAL
    query = f"SELECT * FROM registros_pontos WHERE id_funcionario = {id_funcionario} and data_registro='{data_atual}'"
    resultado_banco = conector.executar_query_selecao(conexao, query)
    if len(resultado_banco) == 0:
        # print("Não existe registro no dia atual")
        resultado = registrar(data_atual, hora_atual, registro1, registro2, registro3, registro4)
        query = ''
        if resultado[0] is not None:
            query = f"INSERT INTO registros_pontos (id_funcionario, data_registro, registro_turno_manha_inicial, " \
                    f"registro_turno_manha_final, registro_turno_tarde_inicial, registro_turno_tarde_final) VALUES" \
                    f"({id_funcionario}, '{data_atual}', '{resultado[0]}', null, null, null)"
            retorno.append(2)
            mensagem = resultado[4]
            retorno.append(mensagem)
            conector.executar_query_alteracao(conexao, query)
        elif resultado[1] is not None:
            query = f"INSERT INTO registros_pontos (id_funcionario, data_registro, registro_turno_manha_inicial, " \
                    f"registro_turno_manha_final, registro_turno_tarde_inicial, registro_turno_tarde_final) VALUES" \
                    f"({id_funcionario}, '{data_atual}', '{resultado[0]}', '{resultado[1]}', null, null)"
            retorno.append(2)
            mensagem = resultado[4]
            retorno.append(mensagem)
            conector.executar_query_alteracao(conexao, query)
        elif resultado[2] is not None:
            query = f"INSERT INTO registros_pontos (id_funcionario, data_registro, registro_turno_manha_inicial, " \
                    f"registro_turno_manha_final, registro_turno_tarde_inicial, registro_turno_tarde_final) VALUES" \
                    f"({id_funcionario}, '{data_atual}', '{resultado[0]}', '{resultado[1]}', '{resultado[2]}', null)"
            retorno.append(2)
            mensagem = resultado[4]
            retorno.append(mensagem)
            conector.executar_query_alteracao(conexao, query)
        elif resultado[3] is not None and resultado[0] is None and resultado[1] is None and resultado[2] is None:
            query = f"INSERT INTO registros_pontos (id_funcionario, data_registro, registro_turno_manha_inicial, " \
                    f"registro_turno_manha_final, registro_turno_tarde_inicial, registro_turno_tarde_final) VALUES" \
                    f"({id_funcionario}, '{data_atual}', null, null, null, '{resultado[3]}')"
            retorno.append(2)
            mensagem = resultado[4]
            retorno.append(mensagem)
            conector.executar_query_alteracao(conexao, query)
        elif resultado[3] is not None:
            query = f"INSERT INTO registros_pontos (id_funcionario, data_registro, registro_turno_manha_inicial, " \
                    f"registro_turno_manha_final, registro_turno_tarde_inicial, registro_turno_tarde_final) VALUES" \
                    f"({id_funcionario}, '{data_atual}', '{resultado[0]}', '{resultado[1]}', '{resultado[2]}', '{resultado[3]}')"
            retorno[0] = 2
            mensagem = resultado[4]
            retorno.append(mensagem)
            conector.executar_query_alteracao(conexao, query)
        else:
            query = f"INSERT INTO registros_pontos (id_funcionario, data_registro, registro_turno_manha_inicial, " \
                    f"registro_turno_manha_final, registro_turno_tarde_inicial, registro_turno_tarde_final) VALUES" \
                    f"({id_funcionario}, '{data_atual}', null, null, null, null)"
            retorno[0] = 3
            mensagem = "Como hoje você não registrou em nenhum horário nenhum registro foi lançado."
            retorno.append(mensagem)
            conector.executar_query_alteracao(conexao, query)

    else:
        # Resultado do Banco e conversão de tupla para lista
        resultado_lista = list(resultado_banco[0])

        # Atribuindo o resultado do banco as variáveis
        funcionario_id = resultado_lista[1]
        data_registro = resultado_lista[2]
        registro1 = resultado_lista[3]
        registro2 = resultado_lista[4]
        registro3 = resultado_lista[5]
        registro4 = resultado_lista[6]

        resultado = registrar(data_atual, hora_atual, registro1, registro2, registro3, registro4)
        query = ''
        # if resultado[0] != None:
        #     query = f"UPDATE registros_pontos SET registro_turno_manha_inicial = '{resultado[0]}' " \
        #             f"(WHERE id_funcionario = {id_funcionario} and data_registro = '{data_registro}')"
        #     conector.executar_query_alteracao(conexao, query)
        if resultado[1] is not None:
            query = f"UPDATE registros_pontos SET registro_turno_manha_final = '{resultado[1]}' " \
                    f"WHERE id_funcionario = {id_funcionario} and data_registro = '{data_registro}'"
            retorno.append(2)
            mensagem = resultado[4]
            retorno.append(mensagem)
            conector.executar_query_alteracao(conexao, query)
        if resultado[2] is not None:
            query = f"UPDATE registros_pontos SET registro_turno_tarde_inicial = '{resultado[2]}' " \
                    f"WHERE id_funcionario = {id_funcionario} and data_registro='{data_registro}'"
            retorno.append(2)
            mensagem = resultado[4]
            retorno.append(mensagem)
            conector.executar_query_alteracao(conexao, query)
        if resultado[3] is not None:
            query = f"UPDATE registros_pontos SET registro_turno_tarde_final = '{resultado[3]}' " \
                    f"WHERE id_funcionario = {id_funcionario} and data_registro='{data_registro}'"
            retorno.append(2)
            mensagem = resultado[4]
            retorno.append(mensagem)
            conector.executar_query_alteracao(conexao, query)

    conector.encerrar_conexao(conexao)
    return retorno


# Regras para o registrar do ponto
def registrar(data_atual, hora_atual, registro1=None, registro2=None, registro3=None, registro4=None):
    # mensagem para retornar no registro
    mensagem = ''

    # VARIAVEIS MARCANDO O INÍCIO DO HORÁRIO - DEPOIS TIRAR ESSAS INFORMAÇÕES DO BANCO
    # hora_inicio_manha = datetime.strptime(f'{data_atual} 08:00:00', '%Y-%m-%d %H:%M:%S')
    # hora_final_manha = datetime.strptime(f'{data_atual} 12:00:00', '%Y-%m-%d %H:%M:%S')
    # hora_inicio_tarde = datetime.strptime(f'{data_atual} 13:00:00', '%Y-%m-%d %H:%M:%S')
    # hora_final_tarde = datetime.strptime(f'{data_atual} 17:00:00', '%Y-%m-%d %H:%M:%S')

    # VARIAVEIS MARCANDO OS LIMITES DE HORÁRIOS
    limite_inicio_manha_1 = datetime.strptime(f'{data_atual} 07:45:00', '%Y-%m-%d %H:%M:%S')
    limite_inicio_manha_2 = datetime.strptime(f'{data_atual} 08:15:00', '%Y-%m-%d %H:%M:%S')
    limite_final_manha_1 = datetime.strptime(f'{data_atual} 11:45:00', '%Y-%m-%d %H:%M:%S')
    limite_final_manha_2 = datetime.strptime(f'{data_atual} 12:15:00', '%Y-%m-%d %H:%M:%S')
    limite_inicio_tarde_1 = datetime.strptime(f'{data_atual} 12:45:00', '%Y-%m-%d %H:%M:%S')
    limite_inicio_tarde_2 = datetime.strptime(f'{data_atual} 13:15:00', '%Y-%m-%d %H:%M:%S')
    limite_final_tarde = datetime.strptime(f'{data_atual} 16:45:00', '%Y-%m-%d %H:%M:%S')
    limite_fim_do_dia = datetime.strptime(f'{data_atual} 23:59:00', '%Y-%m-%d %H:%M:%S')

    # Variáveis de registro
    registro1 = registro1
    registro2 = registro2
    registro3 = registro3
    registro4 = registro4

    # formantando o dia e hora atual
    dia_e_hora_atual = datetime.strptime(f'{data_atual} {hora_atual}', '%Y-%m-%d %H:%M:%S')

    # lista para retornar os registros
    lista_registro = []

    # 1º registro
    if registro1 is None and dia_e_hora_atual < limite_inicio_manha_1:
        mensagem = "Ainda não chegou a hora de realizar o registro do dia. O registro inicia as 07:45hs"
    elif registro1 is None and limite_inicio_manha_1 < dia_e_hora_atual < limite_inicio_manha_2 and \
            dia_e_hora_atual < limite_final_manha_1:
        mensagem = "O 1º registro foi realizado com sucesso dentro do limite de tolerância"
        registro1 = dia_e_hora_atual.strftime("%H:%M:%S")
    elif registro1 is None and limite_inicio_manha_2 < dia_e_hora_atual < limite_final_manha_1:
        mensagem = f'O 1º registro foi realizado com sucesso, porém feito fora do limite de tolerância que é de ' \
                   f'07:45:00 a 08:15:00'
        registro1 = dia_e_hora_atual.strftime("%H:%M:%S")
    # 2º registro
    elif registro1 is not None and registro2 is None and dia_e_hora_atual < limite_final_manha_1:
        mensagem = "Ainda não chegou a hora de realizar o 2º registro do dia. O registro inicia as 11:45hs"
    elif registro1 is not None and registro2 is None and limite_final_manha_1 < dia_e_hora_atual < limite_final_manha_2 \
            and dia_e_hora_atual < limite_inicio_tarde_1:
        mensagem = "O 2º registro foi realizado com sucesso dentro do limite de tolerância"
        registro2 = dia_e_hora_atual.strftime("%H:%M:%S")
    elif registro1 is not None and registro2 is None and limite_final_manha_2 < dia_e_hora_atual < limite_inicio_tarde_1:
        mensagem = "O 2º registro foi realizado com sucesso, porém feito fora do limite de tolerância que é de " \
                   "11:45:00 a 12:15:00 "
        registro2 = dia_e_hora_atual.strftime("%H:%M:%S")
    # 3º registro
    elif registro1 is not None and registro2 is not None and registro3 is None and \
            dia_e_hora_atual < limite_inicio_tarde_1:
        mensagem = "Ainda não chegou a hora de realizar o 3º registro do dia. O registro inicia as 12:45hs"
    elif registro1 is not None and registro2 is not None and registro3 is None and \
            limite_inicio_tarde_1 < dia_e_hora_atual < limite_inicio_tarde_2 and dia_e_hora_atual < limite_final_tarde:
        mensagem = "O 3º registro foi realizado com sucesso dentro do limite de tolerância"
        registro3 = dia_e_hora_atual.strftime("%H:%M:%S")
    elif registro1 is not None and registro2 is not None and registro3 is None and \
            limite_final_manha_2 < dia_e_hora_atual < limite_final_tarde:
        mensagem = "O 3º registro foi realizado com sucesso, porém feito fora do limite de tolerância que é de " \
                   "12:45:00 a 13:15:00"
        registro3 = dia_e_hora_atual.strftime("%H:%M:%S")
    # 4º registro
    elif registro1 is not None and registro2 is not None and registro3 is not None and \
            registro4 is None and dia_e_hora_atual < limite_final_tarde:
        mensagem = "Ainda não chegou a hora de realizar o 4º registro do dia. O registro inicia as 16:45hs"
    elif registro1 is not None and registro2 is not None and registro3 is not None and \
            registro4 is None and limite_final_tarde < dia_e_hora_atual < limite_fim_do_dia:
        mensagem = "O 4º registro foi realizado com sucesso"
        registro4 = dia_e_hora_atual.strftime("%H:%M:%S")
    elif registro1 is None and registro2 is None and registro3 is None and \
            registro4 is None and limite_final_tarde < dia_e_hora_atual < limite_fim_do_dia:
        mensagem = "O 4º registro foi realizado com sucesso, no entanto outros registros não foram realizados."
        registro4 = dia_e_hora_atual.strftime("%H:%M:%S")
    elif registro1 is not None or registro2 is not None or registro3 is not None or registro4 is not None:
        mensagem = "Já existe um registro realizado. Não é possível inserir um novo registro!"

    # acrescentando na lista que irá retornar todos os registros de horas realizado
    lista_registro.append(registro1)
    lista_registro.append(registro2)
    lista_registro.append(registro3)
    lista_registro.append(registro4)
    lista_registro.append(mensagem)

    # retornando a lista
    return lista_registro
