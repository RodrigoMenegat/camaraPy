# Importa pacotes necessários
import requests
import xmltodict

# Define URL base
BASE_URL = "https://www.camara.leg.br/SitCamaraWS/Proposicoes.asmx"

# Define um dicionário com os possíveis complementos para a URL base
REQUEST_TYPES = {
  'ListarProposicoes'                   : {
                                           'url_ending'     : "/ListarProposicoes?",
                                           'allowed_params' : [ 
                                                                'Sigla', 'Numero', 'Ano', 'datApresentacaoIni', 
                                                                'datApresentacaoFim', 'IdTipoAutor', 'ParteNomeAutor',
                                                                'SiglaPartidoAutor', 'SiglaUfAutor', 'GeneroAutor',
                                                                'IdSituacaoProposicao', 'IdOrgaoSituacaoProposicao',
                                                                'EmTramitacao', 'codEstado', 'codOrgaoEstado'
                                                              ],
                                          },

  'ListarSiglasTipoProposicao'          : {
                                           'url_ending'     : "/ListarSiglasTipoProposicao",
                                           'allowed_params' : [ ],
                                           },

  'ListarSituacoesProposicao'           : {
                                           'url_ending'     : "/ListarSituacoesProposicao",
                                           'allowed_params' : [ ],
                                           }, 

  'ListarTiposAutores'                  : {
                                           'url_ending'     : "/ListarTiposAutores",
                                           'allowed_params' : [ ],
                                           }, 

  'ObterProposicao'                     : {
                                           'url_ending'     : "/ObterProposicao",
                                           'allowed_params' : [ 'Tipo', 'Numero', 'Ano' ],
                                           }, 

  'ObterProposicaoPorID'                : {
                                           'url_ending'     : "/ObterProposicaoPorID?",
                                           'allowed_params' : [ 'IdProp' ],
                                           }, 

  'ObterVotacaoProposicao'              : {
                                           'url_ending'     : "/ObterVotacaoProposicao?",
                                           'allowed_params' : [ 'Tipo', 'Numero', 'Ano' ],
                                           }, 

  'ListarProposicoesVotadasEmPlenario'  : {
                                           'url_ending'     : "/ListarProposicoesVotadasEmPlenario?",
                                           'allowed_params' : [ 'Ano', 'Tipo' ]
                                           }, 

  'ListarProposicoesTramitadasNoPeriodo': {
                                           'url_ending'     : "/ListarProposicoesTramitadasNoPeriodo?",
                                           'allowed_params' : [ 'dtInicio', 'dtFim' ]
                                           }, 

} 


# Função genérica para construir a URL da solicitação
def build_url(request_type, **kwargs):

  ''' 
  Essa é uma função genérica que constrói a URL
  de qualquer solicitação possível para o endpoint
  de proposições da API.

  Parâmetros:
  request_type -> O tipo de requisição, deve estar entre as chaves
  da variável global REQUEST_TYPES

  **kwargs -> Um objeto que contém os pares nome:valor que serão passados
  para a URL. Exemplo: { "DtInicio":01/01/1901, "DtFim":'DtFim:01/01/2001 },
  que virariam [url]?DtInicio=01/01/1901&dtFim=01/01/2001.
  '''

  # Checar se o tipo de requisição é válida
  if request_type not in REQUEST_TYPES.keys():
    raise Exception("O tipo de requisição que você enviou é inválido")

  # Para economizar operações e tornar o código claro, salva o item em uma variável 
  this_request_type = REQUEST_TYPES[request_type]

  # Checar se os argumentos passados são válidos para o tipo da requisição
  wrong_params = [ True for item in kwargs.keys() if item not in this_request_type["allowed_params"] ]
  if any(wrong_params):
    raise Exception("Pelo menos um dos parâmetros que você escolheu para essa requisição é inálido")

  # Agora vamos preencher os kwargs faltantes - essa versão da API da Câmara exige que 
  # __todos__ os parâmetros estejam presentes na URL, ainda que o valor seja nulo ¯\_(ツ)_/¯
  for item in this_request_type["allowed_params"]:
    if item not in kwargs:
      kwargs[item] = ""

  # Caso passe por ambos os testes, criar uma string para a url com base na request_type
  url = BASE_URL + this_request_type['url_ending']

  # Criar uma string com os parâmetros passados para a URL
  string = ""
  for k,v in kwargs.items():
    substring = f"&{k}={v}"
    string += substring
  string = string.strip("&")


  # Concatena ambas as strings
  url += string
  
  return url

# Função para executar uma requisição
def make_request(request_type, **kwargs):

  '''
  Essa função faz uma requisição usando o módulo
  requests. Na versão antiga da API da Câmara, o
  valor de retorno sempre é em XML. Aqui, usamos
  o módulo xmltodict para converter os dados em
  um objeto json-like e facilitar o processamento.


  '''

  url = build_url(request_type, **kwargs)
  headers = { 'Accept':'application/json' }
  response = requests.get(url, headers=headers)

  # Levanta exeção HTTPError caso a resposta tenha código 4xx ou 5xx
  response.raise_for_status()

  data = response.text
  if 'Missing parameter' in data:
    raise Exception(f"Faltaram parâmetros na sua requisição. O servidor respondeu com: '{data.text}'")

  return xmltodict.parse(data)

