import mysql.connector


def criarConexaoDB(host_name: str, user_name: str, user_password: str, db_name: str) -> object:
    conexao = None
    try:
        conexao = mysql.connector.connect(
            host=host_name,  # localhost
            user=user_name,  # root
            passwd=user_password, # senha do banco
            database=db_name,  # ponto_eletronico
        )
        # print("A conexão com o banco de dados foi realizada!")
    except mysql.connector.Error as err:
        return f"Erro: '{err}'"

    return conexao


def executar_query_alteracao(conexao: object, query: str):
    cursor = conexao.cursor()
    try:
        cursor.execute(query)
        conexao.commit()
        return "A consulta foi realizado com sucesso!"
    except mysql.connector.Error as err:
        return f"Erro: '{err}'"


def executar_query_selecao(conexao: object, query: str) -> tuple:
    cursor = conexao.cursor()
    resultado = None
    try:
        cursor.execute(query)
        resultado = cursor.fetchall()
        return resultado
    except mysql.connector.Error as err:
        print(f"Erro: '{err}'")


def encerrar_conexao(conexao):
    conexao.close()
