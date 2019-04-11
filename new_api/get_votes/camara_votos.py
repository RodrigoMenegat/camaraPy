'''

Esse arquivo contém funções auxiliares para a coleta de dados
da matéria que foram separadas por questão de legibilidade.

OBSERVAÇÕES

>> O sufixo _, como em 'data_', indica que a variável
   em questão é uma cópia feita dentro do escopo de uma
   função para evitar alterações inplace indesejadas (ou,
   no caso de 'id_', para diferenciar de uma palavra reservada)

'''

####################
### DEPENDÊNCIAS ###
####################
#           ||
#    (\__/) ||
#    ( O.O) ||
#    / 　  づ


# Análise de dados
import pandas as pd
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype

# Métodos matemáticos
import numpy as np

# Envio de requisições
import requests

# Trabalhar com formatos específicos de arquivo
import json

# Para fazer deep copys e evitar mutar dicionários inplace
import copy

# Regex
import re

###############
### CLASSES ###
###############
#           ||
#    (\__/) ||
#    ( O.O) ||
#    / 　  づ

class EmptyRequest(Exception):
  pass
  '''
  Exceção que deve ser levantada quando
  a requisição feita pelo usuário não
  retornar dados válidos.
  '''

class InvalidRequest(Exception):
    
    '''
    >> DESCRIÇÃO
    
    Exceção que deve ser levantada quando o tipo de
    requisição feito não pode ser realizado na função.
    
    '''
    pass

class AmbiguousRequest(Exception):
    
    '''
    >> DESCRIÇÃO
    
    Exceção que deve ser levantada quando a requisição
    que devia retornar um único item retorna mais de 
    um valor.
    
    '''
    pass

class NotImplemented(Exception):
  '''

  Exceção que deve ser levantada quando
  o usuário tenta acessar uma funcionalidade
  ainda não implementada no módulo. Geralmente
  aparece quando se tenta fazer tarefas com XML.

  '''

class InvalidOperation(Exception):
  '''
  Exceção que deve ser levantada quando o usuário
  solicita uma operação não implementada ou impossível.
  Por exemplo, quando pede para retornar um dataframe de
  um objeto que não pode ser convertido.
  '''
  pass

class NoOrientation(Exception):

  '''
  Exceção que deve ser levantada quando o usuário pede para
  calcular a taxa de apoio ao governo por partido em uma
  votação na qual não houve orientação da situação.
  '''
  pass

class ApiError(Exception):
  '''
  Exceção que deve ser levantada quando a API retorna uma
  mensagem de status 500, descrita como 'Erro no servidor'.
  Ocorre em votações para as quais não há dados.
  '''
  pass

##########################
### FUNÇÕES AUXILIARES ###
###  PARA REQUISIÇÕES  ###
##########################
#           ||
#    (\__/) ||
#    ( O.O) ||
#    / 　  づ


def type_check(var, var_type):
    
    '''
    >> DESCRIÇÃO:
    
    Checa se 'var' é do tipo 'var_type'.
    Caso contrário, faz o cast.
    Retorna o valor, transformado ou não.
    
    >> PARÂMETROS
    
    var -> A variável cujo tipo desejamos checar
    
    var_type -> O tipo que desejamos checar..
    
    '''
    
    try:
        
        if not isinstance(var, var_type):
            var = var_type(var)

        return var
    
    except ValueError as e:
        raise(e)

def is_req_type_valid(req_type, valid_req_list):
    
    '''
    >> DESCRIÇÃO:
    Checa se o tipo de requisição é permitido
    dentro da função específica. Retorna um
    valor booleano.
    
    >> PARÂMETROS
    req_type-> O tipo da requisição em formato string.
    
    valid_req_list -> Uma lista dos tipos de requisição
    válidos para a função específica.
    '''
    
    if req_type in valid_req_list:
        return True
    
    else:
        return False

def build_url(url, req_id, req_type):
    
    '''
    >> DESCRIÇÃO
    Constrói a url que deve ser enviada para a API
    de acordo com o valor de req_type. Se for passada
    uma string válida, ela é adicionada ao fim da url.
    Caso contrário, termina a requisição apenas com o id.
    
    
    >> PARÂMETROS
    url -> A url base da API, que será complementada como retorno
    da função.
    
    req_id -> O id da requisição em questão
    
    req_type -> Que tipo de requisição está sendo feita, nos moldes
    definidos pela documentação da API da Câmara. Sempre usar um
    tipo de requisição consistente com a URL passada. Por exemplo, para
    a URL "https://dadosabertos.camara.leg.br/api/v2/deputados/", as 
    opções seriam 'despesas', 'discursos', 'eventos', 'orgaos' ou 'mesa'.
    Verificar documentação em "https://dadosabertos.camara.leg.br/swagger/api.html".
    '''
    
    if req_type != '':
        url += (req_id + '/' + req_type)
        
    else:
        url += req_id
        
    return url

def make_request(url):
    
    '''
    >> DESCRIÇÃO
    
    Define o header com o formato de resposta desejado e
    faz a requisição para a url, usando o pacote Requests.
    
    
    >> PARÂMETROS
    
    url -> A url para a qual será feita a requisição, 
    já composta com os parâmetros necessários

    '''
    
    headers = {
            'accept':'application/json'
        }    

    data = requests.get(url, headers=headers)
    
    return data.json()

def go_through_vote_pages(id_, data):
  '''
  >> DESCRIÇÃO

  Vai, página por página, salvando os dados referentes à votação,
  que tem um limite máximo de cem usuários por página.


  >> PARÂMETROS
  id_ -> O id da votação

  data -> O primeiro objeto json, que contém também os links para
  as demais páginas.

  '''

  # Salva informações que constam apenas no primeiro objeto,
  # assim é possível fazer a reinserção posteriormente
  data_hora = data['dataHora'].copy()
  prop_id = data['idProposicao']

  whole_data = data['dados'].copy()

  # Acessa a parte do objeto que contém todos 
  all_urls = data['links']

  # Usa gerador para encontar item cuja chave 'rel' retorna 'self'
  # Abaixo, é aplicado o mesmo princípio com valores diferentes
  this_url = next(item for item in all_urls if item['rel'] == 'self')['href']
  next_url = next(item for item in all_urls if item['rel'] == 'next')['href']
  last_url = next(item for item in all_urls if item['rel'] == 'last')['href']

  # Passa para a próxima página até encontrar o final, expandindo o objeto no processo
  while this_url != last_url:

    # Avança de página
    this_url = next_url

    #print('Current url:', this_url)

    # Faz e formata a requisição
    new_data = make_request(this_url)

    # Atualiza as urls possíveis
    all_urls = new_data['links']

    # Pega apenas os dados de interesse
    new_data = new_data['dados']

    whole_data.extend(new_data)

    # Enquanto houver uma nova página possível, pega o novo endereço
    if 'next' in [ item['rel'] for item in all_urls ]:
      next_url = next(item for item in all_urls if item['rel'] == 'next')['href']

  # Adiciona identificador
  whole_data = { id_ : {
      'dados'        : whole_data,
      'dataHora'     : data_hora,
      'idProposicao' : prop_id
     }
  }

  # Retorna dados expandidos
  return whole_data

def get_vote_date(id_):

  '''
  >> DESCRIÇÃO:

  Função que faz uma requisição a mais, a mesma
  que make_vote_request(id_, req_type = ''), mas
  não retorna um objeto json completo e sim apenas
  a data do evento. Isso é necessário porque quando
  uma solicitação do tipo 'votos' é feita, a data
  não está no objeto retornado.

  >> PARÂMETROS

  id_ -> O id da votação

  '''


  data =  make_vote_request(id_, req_type = '')

  data = data['dados']

  data_hora_inicio = data['dataHoraInicio']
  data_hora_fim    = data['dataHoraFim']

  return {
            'dataHoraInicio':data_hora_inicio,
            'dataHoraFim':data_hora_fim,
         }

def get_prop_id(id_):

  '''
  >> DESCRIÇÃO:

  A partir do identificador da votação, recupera 
  o identificador da proposição relacionada

  >> PARÂMETROS

  id_ -> O id da votação

  '''

  data =  make_vote_request(id_, req_type = '')

  data = data['dados']['uriProposicaoPrincipal']

  reg_exp = ".*proposicoes/(\d+)"

  data = re.search(reg_exp, data)[1]

  return data

def is_content_there(data):
  '''
  >> DESCRIÇÃO
  A função checa se a resposta da API contém dados
  ou se é um código 404, inserido quando a URL não
  contém dados específicos. Algumas votações, mesmo
  contendo um id, não tem informações detalhadas.

  >> PARÂMETROS
  data -> Um objeto retornado de make_request(url)
  '''

  if 'status' in data.keys():    
    if data['status'] == 404 or data['status'] == 500:
      return False

  else:
      return True

###############################
### REQUISIÇÕES ESPECÍFICAS ###
###############################
#           ||
#    (\__/) ||
#    ( O.O) ||
#    / 　  づ



def find_proposition(no, year, prop_type = None, which_data = None):
    '''
    >> DESCRIÇÃO
    
    Com base no número, ano e tipo de um projeto de lei,
    encontra o id ou a descrição da proposição.
    
    >> PARÂMETROS
    
    prop_type -> Tipo da proposição, em formato string.
    Pode ser qualquer uma das descritas na url abaixo,
    no campo 'sigla':
    https://dadosabertos.camara.leg.br/api/v2/referencias/tiposProposicao
    Alguns exemplos comuns:
    - 'PEC' (Proposta de Emenda à Constituição)
    - 'DTQ' (Destaque)
    - 'PL' ('Projeto de lei')
    
    no -> Número da proposição, em formato string.
    
    year -> Ano da proposição, em formato string.
    
    dataLabel -> Que tipo de dado deve ser puxado do json resultante da requisição.
    Por padrão, retorna o id. Outras possibilidades úteis são:
    - 'ementa'
    - 'idTipo'
    '''
    
    # Checa se tipos são corretos
    
    no = type_check(no, str)
    year = type_check(year, str)
    
    # Caso tenha sido especificado o tipo da proposição
    if prop_type:
        
        # Verifica o tipo
        prop_type = type_check(prop_type, str)
        
        # Chega se prop_type está em uppercase, como deve ser
        if not prop_type.isupper():
            prop_type = prop_type.upper()
    
        # Checa validade do tipo de proposição
        
        valid_prop_types = [
            'AA', 'ADD', 'ANEXO', 'APJ', 'ATA', 'ATC', 'ATOP', 'AV', 'AVN', 'CAC', 'CAE', 'CCN', 'COI', 'CON', 
            'CRVITAEDOC', 'CST', 'CVO', 'CVR', 'DCR', 'DEC', 'DEN', 'DIS', 'DOC', 'DOCCPI', 'DTQ', 'DVT', 'EAG',
            'EMA', 'EMC', 'EMC-A', 'EMD', 'EML', 'EMO', 'EMP', 'EMPV', 'EMR', 'EMRP', 'EMS', 'EPP', 'ERD', 'ERD-A', 
            'ERR', 'ESB', 'ESP', 'EXP', 'IAN', 'INA', 'INC', 'MAD', 'MAN', 'MCN', 'MMP', 'MPV', 'MSC', 'MSF', 'MSG', 
            'MST', 'MTC', 'NIC', 'NINF', 'OBJ', 'OF', 'OF.', 'OFE', 'OFJ', 'OFN', 'OFS', 'OFT', 'P.C', 'PAR', 'PARF',
            'PCA', 'PDA', 'PDC', 'PDN', 'PDS', 'PEA', 'PEC', 'PEP', 'PES', 'PET', 'PFC', 'PIN', 'PL', 'PLC', 'PLN', 
            'PLP', 'PLS', 'PLV', 'PPP', 'PPR', 'PR/CNJ', 'PR/CNMP', 'PRA', 'PRC', 'PRF', 'PRL', 'PRN', 'PRO', 'PRP', 
            'PRR', 'PRST', 'PRT', 'PRV', 'PRVP', 'PSS', 'R.C', 'RAT', 'RCM', 'RCP', 'RDF', 'RDV', 'REC', 'REL', 'REM', 
            'REP', 'REQ', 'RFP', 'RIC', 'RIN', 'RLF', 'RLP', 'RLP(R)', 'RLP(V)', 'RPA', 'RPL', 'RPLE', 'RPLOA', 'RPR', 
            'RQA', 'RQC', 'RQN', 'RQP', 'RRC', 'RRL', 'RST', 'RTV', 'SAP', 'SBE', 'SBE-A', 'SBR', 'SBT', 'SBT-A', 'SDL', 
            'SGM', 'SIP', 'SIT', 'SLD', 'SOA', 'SOR', 'SPA', 'SPA-R', 'SPP', 'SPP-R', 'SRAP', 'SRL', 'SSP', 'STF', 'SUC', 
            'SUG', 'SUM', 'TER', 'TVR', 'VTS'
        ]
        
        if not is_req_type_valid(prop_type, valid_prop_types):
            err_message = '''
            A requisição é inválida para essa função. 
            
            Por favor, insira uma das opções da lista a seguir realizar a consulta por tipo de proposição:
            
            ''' + str(valid_prop_types)
            raise InvalidRequest(err_message)
            
        # Caso seja válido, define a URL
        
        url = "https://dadosabertos.camara.leg.br/api/v2/proposicoes?siglaTipo={prop_type}&numero={no}&ano={year}&ordem=ASC&ordenarPor=id".format( 
            prop_type = prop_type, no = no, year = year 
        )
        
    # Caso o valor de prop_type seja None, é seguro ignorar
        
    else:
        
        url = "https://dadosabertos.camara.leg.br/api/v2/proposicoes?numero={no}&ano={year}&ordem=ASC&ordenarPor=id".format( 
            no = no, year = year 
        )
        
    # Faz requisição com a url definida acima, qualquer que seja
    
    data = make_request(url)

    # Adiciona chegagem para contornar erro do servidor da Câmara
    if not is_content_there(data):
      err_message = "A API retornou erros de status 500 ou 404. \\_(ツ)_/¯"
      raise ApiError(err_message)

    # Checa para ver se a consulta foi de fato única
    if len( data['dados'] ) != 1:
        err_message = '''
        A requisição encontrou mais de um resultado para os parâmetros passados.
        Verifique se há redundâncias na solicitação. Considere especificar o
        tipo de proposição, caso não tenha o feito.
        '''
        raise AmbiguousRequest(err_message)

    if len( data['dados'] )== 0:
      err_message = "Não foi encontrada matéria alguma para estes valores. Verifique se os parâmetros estão corretos."
        

    # Caso tenha sido especificado um tipo de dado para extrair
    if which_data != None:
      # Caso tenha sido, retorna o id 
      data = data['dados'][0][which_data]
    
    return data

def make_proposition_request(id_, req_type = ''):
    
    '''
    >> DESCRIÇÃO
    Função genérica que faz uma requisição para a API da
    Câmara e retorna os dados no formato especificado.
    
    >> PARÂMETROS
    id_no -> Número identificador da proposição
    
    req_type -> Tipo de consulta que se deseja fazer.
    Pode ser um dos seguintes valores, cujos retornos
    correspondem aos formatos especificados na documentação
    da API (https://dadosabertos.camara.leg.br/swagger/api.html)
        - 'autores'
        - 'relacionadas'
        - 'tramitacoes'
        - 'votacoes'
  
    Caso nenhum valor seja determinado, a consulta é feita apenas 
    com o id, que retorna dados gerais sobre a proposição.
    '''

    # Transforma os valores passados para string, se necessário
    id_ = type_check(id_, str)
    
    # Checa se a requisição está entre as permitidas para esta função
    valid_req_list = ['autores', 'relacionadas', 'tramitacoes', 'votacoes', '']
    if not is_req_type_valid(req_type, valid_req_list):
        
        # TO DO - Será que existe uma maneira de colocar essa mensagem de erro na própria classe?
        
        err_message = '''
        A requisição é inválida para essa função. Por favor, insira uma das seguintes opções para fazer a consulta de dados sobre as proposições:
            - "autores"
            - "relacionadas"
            - "tramitacoes"
            - "votacoes"
        Você também pode deixar o parâmetro 'req_type' em branco para ver mais detalhes sobre a proposição desejada.
        '''
        raise InvalidRequest(err_message)
        
            
    # Define dados para fazer a requisição
    url = "https://dadosabertos.camara.leg.br/api/v2/proposicoes/" 
    url = build_url( url, id_, req_type )
        
    # Faz a requisição
    data = make_request(url)

    # Adiciona chegagem para contornar erro do servidor da Câmara
    if not is_content_there(data):
      err_message = "A API retornou erros de status 500 ou 404. \\_(ツ)_/¯"
      raise ApiError(err_message)


    # Checa se há itens na lista de votações
    if req_type == 'votacoes' and len( data['dados'] ) < 1:
      err_message = "A requisição não encontrou registros de nenhuma votação para esse id de proposição."
      raise EmptyRequest(err_message)
        
    # Retorna valores
    return data

def make_vote_request(id_, req_type = ''):
    
    '''
    >> DESCRIÇÃO
    
    A partir do id de uma votação específica,
    que pode ser obtido ao executar prop_votes()
    ou de outra maneira, retorna os detalhes 
    
    >> PARÂMETROS
    
    id_ -> O número identificador da votação
    req_type -> Tipo de consulta que se deseja fazer.
    Pode ser o seguinte valore, cujo retornos
    correspondem aos formatos especificados na documentação
    da API (https://dadosabertos.camara.leg.br/swagger/api.html)
        - 'votos'
  
    Caso nenhum valor seja determinado, a consulta é feita apenas 
    com o id, que retorna dados gerais sobre a proposição.
    '''
                      
    # Transforma os valores passados para string, se necessário
    id_ = type_check(id_, str)
    
    # Checa se a requisição está entre as permitidas para esta função
    valid_req_list = ['votos', '']
    if not is_req_type_valid(req_type, valid_req_list):
        
        # TO DO - Será que existe uma maneira de colocar essa mensagem de erro na própria classe?
        
        err_message = '''
        A requisição é inválida para essa função. Por favor, insira uma das seguintes opções para fazer a consulta de dados sobre as votações:
            - "votos"
        Você também pode deixar o parâmetro 'req_type' em branco para ver mais detalhes sobre a proposição desejada.
        '''
        raise InvalidRequest(err_message)
        
            
    # Define dados para fazer a requisição
    url = "https://dadosabertos.camara.leg.br/api/v2/votacoes/" 
    url = build_url( url, id_, req_type )

    # Adiciona complemento da url para pegar todos os votos possíveis,
    # caso a requisicão seja para 'votos'.
    # Aparentemente não faz diferença nenhuma, pode ser que a API
    # da Câmara ainda não tenha implementado essa funcionalidade
    if req_type == 'votos':
      url += "?itens=513"

    # Faz a requisição
    data = make_request(url)

    # Adiciona chegagem para contornar erro do servidor da Câmara
    if not is_content_there(data):
      err_message = "A API retornou erros de status 500 ou 404. \\_(ツ)_/¯"
      raise ApiError(err_message)

    # Adiciona os dados de data e hora, se preciso
    if req_type == 'votos':

      data['dataHora']     = get_vote_date(id_)
      data['idProposicao'] = get_prop_id(id_)

        
    # Retorna valores
    return data


################################
###    FUNÇÕES AUXILIARES    ###
###  PROCESSAMENTO DE DADOS  ###
################################
#           ||
#    (\__/) ||
#    ( O.O) ||
#    / 　  づ

def find_all_vote_types(id_, data):

  '''
  >> DESCRIÇÃO

  Diante de um objeto json-like, retornado
  por get_all_votes(..., return-df = False),
  itera por todos os itens e retorna um array 
  com os tipos de voto ("Abstenção", "Ausência", 
  "Obstrução", "Sim", "Não", etc) que ocorream
  naquela votação.

  >> PARÂMETROS:

  id -> O id da votação

  data -> O objeto json-like retornado por
  get_all_votes(return_df = False)


  '''
  id_ = type_check(id_, str)

  vote_types = [ ]
  
  for item in data[id_]['dados']:
    
    if item[ 'voto' ] not in vote_types:

      vote_types.append( item['voto'] )

  return vote_types

def find_all_parties(id_, data):

  '''
  >> DESCRIÇÃO

  Diante de um objeto json-like, retornado
  por get_all_votes(..., return-df = False),
  itera por todos os itens e retorna um array 
  com os partidos envovlidos naquela votação.

  >> PARÂMETROS:

  id -> O id da votação

  data -> O objeto json-like retornado por
  get_all_votes(return_df = False)


  '''
  id_ = type_check(id_, str)

  all_parties = [ ]
  
  for item in data[id_]['dados']:
    
    if item['parlamentar']['siglaPartido'] not in all_parties:

      all_parties.append( item['parlamentar']['siglaPartido'] )

  return all_parties

def get_json_vote_count(id_, data):

  '''
  >> DESCRIÇÃO

  Soma os votos de todos os parlamentares
  de cada partido em determinada votação
  quando o input for um objeto json-like

  >> PARÂMETROS

  id_ -> O id da votação

  data -> Um objeto json-like retornado por
  get_all_votes()

  '''

  id_ = type_check(id_, str)

  data_ = copy.deepcopy(data) # Deepcopy porque vamos alterar uma parte específica do dicionário

  # Novo json
  new_data = [ ]

  # Pega todos os votos que ocorreram naquela votação
  vote_types = find_all_vote_types(id_, data)
  all_parties = find_all_parties(id_, data)

  # Começa a contar os votos que ocorreram e preecher o novo objeto
  for party in all_parties:

    # Cria a estrutura externa do json
    sub_object = {}
    sub_object['partido'] = party
    sub_object['votacao'] = {}

    # Adiciona detalhes sobre votação usando um dict comprehension que será preencido abaixo
    sub_object['votacao'] = { vote_type : 0 for vote_type in vote_types }

    # Adiciona objeto para a lista recém criada
    new_data.append(sub_object)

  # Faz a contagem da ocorrência de cada voto:

  # Para cada parlamentar
  for item in data_[id_]['dados']:

    # Pegue os dados
    party = item['parlamentar']['siglaPartido']
    vote = item['voto']

    # Procure o partido correto
    for index, obj in enumerate(new_data):

      # Ao encontrar...
      if obj['partido'] == party:

      # ...adicione um na contagem daquele voto específico para o partido
        new_data[index]['votacao'][vote] += 1

  # Adiciona novamente o índice na parte exterior do objeto
  data_[id_]['dados'] = new_data.copy()

  return data_

def normalize_json_vote_count(id_, data):

  '''
  
  >> DESCRIÇÃO

  Recebe um objeto json-like, retornado pela
  função get_json_vote_count(), e transforma
  os valores absolutos em percentuais. Retorna
  uma cópia do objeto.

  >> PARÂMETROS

  id_ -> O id da votação

  data -> Objeto json-like retornado pela função
  get_json_vote_count()

  '''


  data_ = copy.deepcopy(data)
  #print(data)

  for index, item in enumerate(data_[id_]['dados']):

    #print(item)

    # Acessa o dicionário com os votos
    vote_count = item['votacao']

    # Soma para descobrir o total de votos
    total = sum( vote_count.values() )

    # Para cada tipo de voto, faz o cálculo de percentual e altera inplace
    for key, value in vote_count.items():
      data_[id_]['dados'][index]['votacao'][key] = round ( value / total, 4)

  return data_

def pandas_count_normalize(df):

  '''
  >> DESCRIÇÃO

  Função que transforma os valores
  de cada célula em percentuais relativos ao total
  da linha.

  >> PARÂMETROS

  df -> O dataframe inteiro

  '''

  df_ = df.copy() # Perceba que aqui deepcopy é desnecessário porque não há esruturas mutáveis dentro do dataframe

  for index, row in df_.iterrows():

    # Seleciona os campos numéricos pré-existentes
    to_sum =   [ k for k,v in row.items() if isinstance( row[k], (int, float) ) ] # Note que row.items() se comporta como um dicionário

    # Soma as colunas selecionadas
    total = sum( [ row[label] for label in to_sum ] )

    # Substitui uma a uma pelo valor percentual relativo ao total
    for label in to_sum:

      df_.loc[index, label] = round( row[label] / total, 4)

  return df_

##############################
### PROCESSAMENTO DE DADOS ###
##############################
#           ||
#    (\__/) ||
#    ( O.O) ||
#    / 　  づ

# TO DO
# Implementar função de retornar dataframe para get_proposition_votes

def get_proposition_votes_ids(data):
    
    '''
    >> DESCRIÇÃO
    
    A partir do id de uma proposição, recupera os ids das votações
    relacionadas uma lista.
    
    >> PARÂMETROS
    data -> O valor retornado por make_proposition_request()
    '''
    
    
    # Retorna ids das votações no formato de lista]
    data_ = data['dados']
    data_ = [ str(item['id']) for item in data_ ]
    
    return data_

def get_party_orientation(id_, data, return_df = False):
    
    '''
    >> DESCRIÇÃO
    
    Pega a orientação de voto de cada uma das bancadas
    envolvidas em uma votação específica. Retorna
    como objeto json-like, string de texto xml ou 
    um dataframe do pandas, caso o parâmetro seja especificado.
    
    >> PARÂMETROS
    
    data -> O valor retornado por make_vote_request

    
    return_df  -> booleano que dertermina se o json
    resultante da request deve ser transformado em
    um dataframe, formato parecido com um csv.
    '''

    data_ = data.copy()

    # Salva dados necessários para inserir depois
    data_hora = {
                'dataHoraInicio' : data_['dados']['dataHoraInicio'],
                'dataHoraFim'    : data_['dados']['dataHoraFim']
                }
    id_proposicao = data_['dados']['proposicao']['id']

    data_ = data_['dados']['orientacoes']

    if return_df:

      data_ = pd.DataFrame(data_)

      data_['voteId']         = id_
      data_['idProposicao']   = id_proposicao
      data_['dataHoraInicio'] = data_hora['dataHoraInicio']
      data_['dataHoraFim']    = data_hora['dataHoraFim']

    else:

      data_ = {
        id_ : 
        {
          'dados'        : data_.copy(),
          'dataHora'     : data_hora.copy(),
          'idProposicao' : id_proposicao
        }
      }

    return data_

def get_all_votes(id_, data, return_df = False):

    '''
    >> DESCRIÇÃO
    De posse dos dados iniciais de uma votação, retorna a lista de votantes e seus resepctivos
    dados como objeto json-like, string de texto xml ou um dataframe do pandas, 
    caso o parâmetro seja especificado.

    >> PARÂMETROS

    data -> Objeto retornado por make_vote_request(req_type = 'votos')
    
    id -> O id da votação

    return_df  -> booleano que dertermina se o json
    resultante da request deve ser transformado em
    um dataframe, formato parecido com um csv.

    '''

    id_ = type_check(id_, str)


    # Avança pela paginação da resposta até chegar ao final
    data_ = go_through_vote_pages(id_, data)

    # Se o usuário pedir para retornar um dataframe, parsear e retornar
    if return_df:

      columns = [
                  'id', 'idLegislatura', 'nome', 'siglaPartido', 
                  'siglaUf', 'uri', 'uriPartido', 'urlFoto', 'voto',
                  'dataHoraInicio', 'dataHoraFim', 'idProposicao', 
                ]

      df = pd.DataFrame(columns = columns)

      for column in columns:

        if column == 'dataHoraInicio':
          df[column] = data_[id_]['dataHora']['dataHoraInicio']

        elif column == 'dataHoraFim':
          df[column] = data_[id_]['dataHora']['dataHoraFim']

        elif column == 'idProposicao':
          df[column] = data_[id_]['idProposicao']

        elif column == 'voto':
          df[column] = [ item[column] for item in data_[id_]['dados'] ]

        else: 
          df[column] = [ item['parlamentar'][column] for item in data_[id_]['dados'] ]


      df = df.replace('null', 'Ausência')

      df['voteId'] = id_

      return df

    else:

      # Substitui todas as labels 'null' por 'Ausência' na descrição dos votos
      for item in data_[id_]['dados']:

        if item['voto'] == 'null':
          item['voto'] = 'Ausência'

      # Se não precisar parsear, apenas retorne os dados
      return data_

def get_party_vote_count(id_, data, normalize = False):

  '''
  >> DESCRIÇÃO

  A partir do resultado de get_all_votes, faz
  uma contagem dos votos por partido. Pode retornar
  a contagem absoluta ou em valores percentuais, tanto
  em formato json quanto em formato dataframe, dependendo
  do tipo do parâmetro data que for passado.

  >> PARÂMETROS

  id_ -> O id numérico da votação

  data -> O dataframe ou objeto json-like que deve ser contado,
  que foi retornado pela função get_all_votes()

  normalize -> Booleano que determina se devem ser calculados
  os valores percentuais. Default é False

  '''

  id_ = type_check(id_, str)

  data_ = data.copy()

  if isinstance(data_, pd.core.frame.DataFrame):

    ### Agrupa, conta e formata
    data_ = data_.groupby(['siglaPartido', 'voto', 'voteId', 'idProposicao', 'dataHoraInicio', 'dataHoraFim'])
    data_ = data_.size().unstack(level=1, fill_value = 0).reset_index()
    
    if normalize:

      data_ = pandas_count_normalize(data_)

  else:

    data_ = get_json_vote_count(id_, data_)

    if normalize:
      data_ = normalize_json_vote_count(id_, data_)


  return data_

def get_government_support_count(id_, party_vote_count, party_orientation, normalize = False):

  '''
  >> DESCRIÇÃO
  A partir da contagem de votos (já normalizada) por partido
  de uma determinada votação, transforma a contagem por tipo
  de voto em 'apoiou o governo' ou 'não apoiou o governo', de
  acordo com a orientação do governo para a bancada aliada.

  A função checa o tipo dos dados que recebe e retorna um
  objeto condizente, em formato json-like ou dataframe.


  >> PARÂMETROS

  id_ -> O id da votação em questão

  party_vote_count -> A contagem de votos retornada por 
  get_party_vote_count(..., normalize - True), normalizada ou não

  party_orientation -> A orientação das bancadas, retornada por get_party_orientation()
  

  normalize -> Booleano que determina se devem ser calculados
  os valores percentuais. Default é False

  '''

  # Checa se os dados passados são do mesmo formato e
  # levanta exceção caso contrário


  if type(party_vote_count) != type(party_orientation):
    err_message = "Essa operação só pode se realizada quando os parâmetros 'party_vote_count' e 'party_orientation' são do mesmo tipo. Favor verificar."
    raise InvalidOperation(err_message)

  id_ = type_check(id_, str)
  new_data = copy.deepcopy(party_vote_count) # Deepcopy porque vai ser alterado posteriormente

  # Checa se a operação vai ser em dataframe
  if isinstance(party_vote_count, pd.core.frame.DataFrame):

    # Seleciona orientação do governo
    orientation_df = party_orientation[ party_orientation.nomeBancada == 'GOV.' ].reset_index()
    
    # Checagem – há orientação do governo?
    if orientation_df.shape[0] < 1 or orientation_df.loc[0, 'voto'] == 'Liberado':

      # Como não há orientação do governo, adiciona nans
      new_data['com_governo']    = np.nan
      new_data['contra_governo'] = np.nan

    else:

      orientation = orientation_df.loc[0, 'voto']

      # Cria listas que serão preenchidas com os valores
      govt_aligned_totals = [ ]
      not_govt_aligned_totals = [ ]

      # Seleciona as colunas de partido que contém os votos de orientação
      for index, row in new_data.iterrows():

        # Seleciona nomes dos campos com dados numéricos
        to_sum = [ item for item in new_data.columns if item != orientation and is_numeric_dtype( new_data[ item ] ) and item != 'Ausência' ] 

        # Calcula totais de apoio e não apoio
        total_govt     = row[ orientation ]
        total_not_govt = sum ( row[ to_sum ] )

        # Adiciona para a lista
        govt_aligned_totals.append(total_govt)
        not_govt_aligned_totals.append(total_not_govt)

      # As listas acimas viram colunas
      new_data['com_governo']    = govt_aligned_totals
      new_data['contra_governo'] = not_govt_aligned_totals

    # Adiciona dados de horário

    # Derruba as colunas desnecessárias
    new_data = new_data.drop(
      [ 
        col for col in new_data.columns if col not in (
                                                      'siglaPartido', 'voteId', 'idProposicao',
                                                      'dataHoraInicio', 'dataHoraFim',
                                                      'com_governo', 'contra_governo',
                                                      ) 
      ],
      axis = 1
    )

    # Adiciona colunas identificadoras

    if normalize:
      new_data = pandas_count_normalize(new_data)

  # Caso contrário, a operação vai ser sobre json
  else:

    # Descobre a orientação usando um gerador next
    # Note que, caso não seja encontrado, vamos preencher a variável com o valor padrão 'Liberado'
    orientation = next( (item['voto'] for item in party_orientation[id_]['dados'] if item['nomeBancada'] == 'GOV.'), 'Liberado' )

    # Itera por todos os itens, primeiro salvando
    # os novos valores em uma variável e depois
    # substitui um dos dicionários internos

    for index, item in enumerate( new_data[id_]['dados'] ):

      # Se a orientação for diferente de 'Liberado', calcule os valores
      if orientation != 'Liberado':
        
        # Calcula as somas totais
        govt_aligned_totals     = sum( [ value for key, value in item['votacao'].items() if key == orientation ] )
        not_govt_aligned_totals = sum( [ value for key, value in item['votacao'].items() if key != orientation and key != "Ausência"] )

      else:

        # Caso contrário, coloque um valor nulo para preencher
        govt_aligned_totals = None
        not_govt_aligned_totals = None

      # Salva os valores em um novo objeto
      new_votes = { 
                    'com_governo'    : govt_aligned_totals, 
                    'contra_governo' : not_govt_aligned_totals 
                  }

      # Substiui o objeto interno 'votação' pelo novo, recém calculado
      new_data[id_]['dados'][index]['votacao'] = new_votes.copy()

    # Se for feita uma tentativa de normalizar dados sem orientação do governo,
    # será retornado o mesmo dado – ou seja, preenchido com Nones.
    if normalize and orientation != 'Liberado':

      new_data = normalize_json_vote_count(id_, new_data)


  # RETORNA

  return new_data


