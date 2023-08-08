# Import for the Web Bot
from botcity.web import WebBot, Browser, By
from botcity.maestro import *
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import unicodedata
from sqlalchemy import create_engine
import cx_Oracle
import pandas as pd
import re
import os






##################################################################

#email e senha
email = 'freedom.tecnologia@freedomhonda.com.br'
senha = 'Freedom.9!'
        
###################################################################




def main():

    bot = WebBot()

    # Configure whether or not to run on headless mode
    bot.headless = False

    # Uncomment to set the WebDriver path
    bot.driver_path = bot.get_resource_abspath('chromedriver.exe')

    # Opens the BotCity website.
    bot.browse("https://app.dealerup.com.br/leads/analysis")
    # Maximizando a janela 
    bot.maximize_window()
     
    #acessando o Duleads
    while True:
        try:
            # Inserindo as credenciais
            bot.find_element('//*[@id="app-root"]/div[3]/div/div/form/div[2]/input', By.XPATH).send_keys(email)
            bot.find_element('//*[@id="app-root"]/div[3]/div/div/form/div[3]/input', By.XPATH).send_keys(senha)
            # Clicando em entrar
            bot.find_element('//*[@id="app-root"]/div[3]/div/div/form/div[4]/button', By.XPATH).click()
            bot.wait_for_element_visibility()

        except:
            break
        print('Não foi possível acessar com as credenciais')
    print('Logado com sucesso!')

    # Acessando o lead
    while True:
        try:
            bot.find_element('//*[@id="app-root"]/div[3]/div[4]/div/div[1]/div/div/div/div/div[1]/a', By.XPATH).click()
            bot.wait_for_element_visibility()
        except:
            break
        print('Não foi possível acessar os leads')
    print('Acessando a opção leads.')

    # Clicando em manager
    while True:
        try:
            bot.sleep(8000)
            bot.find_element('//*[@id="app-root"]/div[3]/div[4]/div/div[1]/div/div/div/div[1]/div[1]/div[1]/span[3]/button',By.XPATH).click()
            bot.wait_for_element_visibility()

        except:
            break
        print('Não foi possível selecionar a opção manager')
    print('Opção manager selecionada.')

    # Selecionando análises
    while True:
        try:
            bot.find_element('//*[@id="app-root"]/div[3]/div[4]/div/div[1]/div/div/div/div[1]/div[1]/div[1]/span[3]/div/div[2]',By.XPATH).click()
            bot.wait_for_element_visibility()

        except:
            break
        print('Não foi possível selecionar a opção análises')
    print('Opção análises selecionada.')

    # Clicando em data da venda
    bot.sleep(5000)
    bot.find_element('//*[@id="app-root"]/div[3]/div[4]/div/div[1]/div/div/div[1]/div/div[1]/div[1]/span[3]/button',By.XPATH).click()
    bot.sleep(5000)
    bot.find_element('//*[@id="app-root"]/div[3]/div[4]/div/div[1]/div/div/div[1]/div/div[1]/div[1]/span[3]/div/div[4]',By.XPATH).click()
    bot.sleep(5000)
    print('Data Venda selecionada')

    #clicando em periodo
    bot.find_element('//*[@id="app-root"]/div[3]/div[4]/div/div[1]/div/div/div[1]/div/div[1]/div[1]/span[4]/button',By.XPATH).click()
    bot.sleep(5000)
    # Selecionando a opção mês passado
    bot.find_element('//*[@id="app-root"]/div[3]/div[4]/div/div[1]/div/div/div[1]/div/div[1]/div[1]/span[4]/div/div[1]/span[6]',By.XPATH).click()
    bot.sleep(5000)
    print('Opção mês passado selecionada.')
        
    # clicando em confirmar
    bot.find_element('//*[@id="app-root"]/div[3]/div[4]/div/div[1]/div/div/div[1]/div/div[1]/div[1]/button[3]',By.XPATH).click()
    bot.wait(5000)
    print('Filtrado com sucesso')   

    # Expandindo as opções
    while True:
        try:
            bot.find_element('tr:nth-child(1) > td.table-b-table-default.b-table-sticky-column.text-center.cursor-pointer',By.CSS_SELECTOR).click()
            bot.page_down()
            bot.find_element('tr:nth-child(4) > td.table-b-table-default.b-table-sticky-column.text-center.cursor-pointer',By.CSS_SELECTOR).click()
            bot.page_down()
            bot.find_element('tr:nth-child(7) > td.table-b-table-default.b-table-sticky-column.text-center.cursor-pointer',By.CSS_SELECTOR).click()
            bot.page_down()
            bot.wait_for_element_visibility()
        except:
            break
        print('Não foi possível expandir as opções')
    print('Opções expandidas')

    # Selecionando a tabela para raspagem de dados
    bot.sleep(5000)
    tabela = bot.find_element('app-table-index', By.CLASS_NAME)
    # Encontrar o elemento tbody dentro da tabela
    tbody = tabela.find_element(By.TAG_NAME, 'tbody')

    # Encontrar todas as linhas da tabela
    linhas = tbody.find_elements(By.TAG_NAME, 'tr')

    # Criar uma lista para armazenar os dados
    dados = []
    
    # Iterar sobre as linhas da tabela
    for linha in linhas:
        # Encontrar as colunas da linha
        colunas = linha.find_elements(By.TAG_NAME, 'td')

        # Extrair o texto das colunas e adicionar à lista de dados
        dados_linha = [coluna.text for coluna in colunas]

        # Verificar se a linha contém dados
        if any(dados_linha):
            # Realizar o tratamento dos dados antes de adicionar à lista
            dados_linha_tratados = [dado.replace('(', '').replace(')', '').replace(',', '.') for dado in dados_linha]

            # Adicionar a linha tratada à lista de dados
            dados.append(dados_linha_tratados)

    # Remover linhas vazias
    dados = [linha for linha in dados if any(linha)]

    # Categorias
    categorias = {
        'DIGITAL': ['FACEBOOKLEADADS', 'INSTAGRAMLEADADS', 'SFC-MYHONDA'],
        'PROSPECCAO': ['INDICAÇÃO', 'TELEFONE', 'WHATSAPP', 'INSTAGRAM', 'JÁ É CLIENTE'],
        'FLUXO_DE_LOLJA' : ['SHOWROOM', 'WHATSAPP']
    }

    # Colunas do DataFrame
    colunas = ['MIDIA', 'TEMPO_MEDIO_RESPOSTA', 'RECEBIDO', 'EM_ANDAMENTO', 'AGENDAMENTO',
               'TESTDRIVE', 'NAO_ATENDIDO', 'PERDIDOS_TOTAL', 'CONVERTIDO'] + list(range(9, 37))

    # Criar DataFrame
    df1 = pd.DataFrame(dados, columns=colunas)

    # Excluir as linhas 1, 2, 3, 7, 8 do DataFrame
    df1 = df1.drop([0, 1, 5, 6, 11, 12])
    # Excluir as colunas de 9 a 27 do DataFrame
    df1 = df1.drop(df1.columns[9:37], axis=1)

    def extrair_informacoes(valor):
        partes = valor.split()  # Separar valor e porcentagem
        numero = partes[0].replace('.', '')  # Remover o ponto decimal, se presente
        numero = str(int(numero))  # Converter o número em inteiro e, em seguida, em string
    

        if len(partes) > 1:
            porcentagem = partes[1].replace('(', '').replace(')', '').replace('%', '')  # Remover parênteses e sinal de porcentagem
            porcentagem = float(porcentagem) / 100  # Dividir a porcentagem por 100
        else:
            porcentagem = None

        return numero, porcentagem


    # Separando as informações em colunas distintas
    df1[['EM_ANDAMENTO', 'EM_ANDAMENTO_PORCENTAGEM']] = df1['EM_ANDAMENTO'].apply(extrair_informacoes).apply(pd.Series)
    df1[['AGENDAMENTO', 'AGENDAMENTO_PORCENTAGEM']] = df1['AGENDAMENTO'].apply(extrair_informacoes).apply(pd.Series)
    df1[['TESTDRIVE', 'TESTDRIVE_PORCENTAGEM']] = df1['TESTDRIVE'].apply(extrair_informacoes).apply(pd.Series)
    df1[['NAO_ATENDIDO', 'NAO_ATENDIDO_PORCENTAGEM']] = df1['NAO_ATENDIDO'].apply(extrair_informacoes).apply(pd.Series)
    df1[['PERDIDOS_TOTAL', 'PERDIDOS_TOTAL_PORCENTAGEM']] = df1['PERDIDOS_TOTAL'].apply(extrair_informacoes).apply(pd.Series)
    df1[['CONVERTIDO', 'CONVERTIDO_PORCENTAGEM']] = df1['CONVERTIDO'].apply(extrair_informacoes).apply(pd.Series)

    # Limitar o número de casas decimais
    df1['EM_ANDAMENTO_PORCENTAGEM'] = df1['EM_ANDAMENTO_PORCENTAGEM'].round(4)
    df1['AGENDAMENTO_PORCENTAGEM'] = df1['AGENDAMENTO_PORCENTAGEM'].round(4)
    df1['TESTDRIVE_PORCENTAGEM'] = df1['TESTDRIVE_PORCENTAGEM'].round(4)
    df1['NAO_ATENDIDO_PORCENTAGEM'] = df1['NAO_ATENDIDO_PORCENTAGEM'].round(4)
    df1['PERDIDOS_TOTAL_PORCENTAGEM'] = df1['PERDIDOS_TOTAL_PORCENTAGEM'].round(4)
    df1['CONVERTIDO_PORCENTAGEM'] = df1['CONVERTIDO_PORCENTAGEM'].round(4)



    # Definir a nova ordem das colunas
    nova_ordem_colunas = ['MIDIA', 'TEMPO_MEDIO_RESPOSTA', 'RECEBIDO', 'EM_ANDAMENTO', 'EM_ANDAMENTO_PORCENTAGEM',
                          'AGENDAMENTO', 'AGENDAMENTO_PORCENTAGEM', 'TESTDRIVE', 'TESTDRIVE_PORCENTAGEM',
                          'NAO_ATENDIDO', 'NAO_ATENDIDO_PORCENTAGEM', 'PERDIDOS_TOTAL', 'PERDIDOS_TOTAL_PORCENTAGEM',
                          'CONVERTIDO', 'CONVERTIDO_PORCENTAGEM', 'TIPO', 'DATA_HORA_ATUALIZACAO','LOTE']
    
    # Obter a data e hora atual
    data_atual = datetime.now()

    # Formatar a data e hora no formato desejado para inserção no banco de dados
    data_hora_atual_banco = data_atual.strftime("%Y-%m-%d %H:%M:%S")

    #gerando lote
    numero_lote = data_atual.strftime('%Y%m%d%H%M%S')
    df1['LOTE'] = numero_lote 
    # Adicionar a nova coluna ao DataFrame com o valor da data e hora atual
    df1['DATA_HORA_ATUALIZACAO'] = data_hora_atual_banco

    # Adicionar a coluna "TIPO"
    df1['TIPO'] = df1['MIDIA'].apply(lambda x: next((k for k, v in categorias.items() if x in v), None))

    # Função para remover acentos e substituir caracteres especiais
    def remover_acentos_substituir(texto):
        texto_sem_acentos = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
        texto_substituido = re.sub(r'[^a-zA-Z0-9_]', '_', texto_sem_acentos)
        return texto_substituido
    #Formatando nomes
    df1['MIDIA'] = df1['MIDIA'].str.replace('FACEBOOKLEADADS', 'FACEBOOK_LEAD_ADS')
    df1['MIDIA'] = df1['MIDIA'].str.replace('INSTAGRAMLEADADS', 'INSTAGRAM_LEAD_ADS')
    df1['MIDIA'] = df1['MIDIA'].apply(remover_acentos_substituir)
    #df1['EM_ANDAMENTO'] = df1['EM_ANDAMENTO'].fillna(0)


    # Reorganizar as colunas do DataFrame
    df1 = df1.reindex(columns=nova_ordem_colunas)
    
######################################################################################################################################
    
    
    
    
    # conexão com o banco de dados.
    cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_3")
    dsn = cx_Oracle.makedsn(host='10.1.1.25', port=1521, service_name='XEPDB1')
    username = 'DMUSER'
    password = 'DMUSER'
    
    # Convertendo o DataFrame para uma lista de dicionários
    dados = df1.to_dict('records')

    # Query de INSERT
    query = "INSERT INTO tbl_rb_fato_duleads (MIDIA, TEMPO_MEDIO_RESPOSTA, RECEBIDO, EM_ANDAMENTO, EM_ANDAMENTO_PORCENTAGEM, AGENDAMENTO, AGENDAMENTO_PORCENTAGEM, TESTDRIVE, TESTDRIVE_PORCENTAGEM, NAO_ATENDIDO, NAO_ATENDIDO_PORCENTAGEM, PERDIDOS_TOTAL, PERDIDOS_TOTAL_PORCENTAGEM, CONVERTIDO, CONVERTIDO_PORCENTAGEM, TIPO, DATA_HORA_ATUALIZACAO, LOTE) VALUES (:MIDIA, :TEMPO_MEDIO_RESPOSTA, :RECEBIDO, :EM_ANDAMENTO, :EM_ANDAMENTO_PORCENTAGEM, :AGENDAMENTO, :AGENDAMENTO_PORCENTAGEM, :TESTDRIVE, :TESTDRIVE_PORCENTAGEM, :NAO_ATENDIDO, :NAO_ATENDIDO_PORCENTAGEM, :PERDIDOS_TOTAL, :PERDIDOS_TOTAL_PORCENTAGEM, :CONVERTIDO, :CONVERTIDO_PORCENTAGEM, :TIPO, :DATA_HORA_ATUALIZACAO, :LOTE)"

    # Tentar estabelecer a conexão e executar o INSERT
    try:
        connection = cx_Oracle.connect(username, password, dsn)
        cursor = connection.cursor()
        cursor.executemany(query, dados)
        connection.commit()
        print('Dados inseridos com sucesso!')
        connection.close()
    except cx_Oracle.DatabaseError as e:
        error_message = e.args[0]
        print(f'Erro ao conectar ao banco de dados: {error_message}')

   



    # Exibindo o DataFrame resultante
    print(df1)


    # Defina o nome do arquivo CSV usando a variável numero_lote
    nome_arquivo_csv = f"{numero_lote}.csv"

    # Defina o caminho completo do arquivo CSV
    caminho_arquivo_csv = fr"C:\Users\douglas.saraiva\Desktop\codigos\robo_duleads\{nome_arquivo_csv}"

    # Extrair o DataFrame para o arquivo CSV
    df1.to_csv(caminho_arquivo_csv, index=False)


 
    # Wait 3 seconds before closing
    bot.wait(300000)

    bot.stop_browser()

def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
