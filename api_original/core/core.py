####################
### DEPENDÊNCIAS ###
####################

import requests
import xmltodict

###############################
### EXCEÇÕES PERSONALIZADAS ###
###############################

from .custom_exceptions import ProposicaoAcessoria

#########################
## PARÂMETROS GLOBAIS ###
#########################

# Dicionário que contem os serviços da velha API
# os parâmetros permitidos/obrigatórios para cada
# um deles.

WEBSERVICES = {
  
  'proposicoes' : {
                  'ListarProposicoes'                   : {
                                                           'url_ending'       : "/ListarProposicoes?",
                                                           'allowed_params'   : [ 
                                                                                'Sigla', 'Numero', 'Ano', 'datApresentacaoIni', 
                                                                                'datApresentacaoFim', 'IdTipoAutor', 'ParteNomeAutor',
                                                                                'SiglaPartidoAutor', 'SiglaUfAutor', 'GeneroAutor',
                                                                                'IdSituacaoProposicao', 'IdOrgaoSituacaoProposicao',
                                                                                'EmTramitacao', 'codEstado', 'codOrgaoEstado'
                                                                                ],
                                                           'mandatory_params' : [ ]
                                                          },

                  'ListarSiglasTipoProposicao'          : {
                                                           'url_ending'      : "/ListarSiglasTipoProposicao",
                                                           'allowed_params'  : [ ],
                                                           'mandatory_params': [ ]
                                                          },

                  'ListarSituacoesProposicao'           : {
                                                           'url_ending'      : "/ListarSituacoesProposicao",
                                                           'allowed_params'  : [ ],
                                                           'mandatory_params': [ ]
                                                          }, 

                  'ListarTiposAutores'                  : {
                                                           'url_ending'      : "/ListarTiposAutores",
                                                           'allowed_params'  : [ ],
                                                           'mandatory_params': [ ]
                                                          }, 

                  'ObterProposicao'                     : {
                                                           'url_ending'       : "/ObterProposicao?",
                                                           'allowed_params'   : [ 'Tipo', 'Numero', 'Ano' ],
                                                           'mandatory_params' : [ 'Tipo', 'Numero', 'Ano' ]
                                                          }, 

                  'ObterProposicaoPorID'                : {
                                                           'url_ending'      : "/ObterProposicaoPorID?",
                                                           'allowed_params'  : [ 'IdProp' ],
                                                           'mandatory_params': [ 'IdProp' ]
                                                          }, 

                  'ObterVotacaoProposicao'              : {
                                                           'url_ending'       : "/ObterVotacaoProposicao?",
                                                           'allowed_params'   : [ 'Tipo', 'Numero', 'Ano' ],
                                                           'mandatory_params' : [ 'Tipo', 'Numero', 'Ano' ]
                                                          }, 

                  'ListarProposicoesVotadasEmPlenario'  : {
                                                           'url_ending'       : "/ListarProposicoesVotadasEmPlenario?",
                                                           'allowed_params'   : [ 'Ano', 'Tipo' ],
                                                           'mandatory_params' : [ 'Ano' ]
                                                          }, 

                  'ListarProposicoesTramitadasNoPeriodo': {
                                                           'url_ending'       : "/ListarProposicoesTramitadasNoPeriodo?",
                                                           'allowed_params'   : [ 'dtInicio', 'dtFim' ],
                                                           'mandatory_params' : [ 'dtInicio', 'dtFim' ]
                                                          }
                  },

  'deputado' : {
                  'ObterDeputados'         : {
                                            'url_ending'       : "/ObterDeputados",
                                            'allowed_params'   : [ ],
                                              'mandatory_params' : [ ]
                                             },

                  'ObterDetalhesDeputados' : {
                                              'url_ending'      : "/ObterDetalhesDeputado?",
                                              'allowed_params'  : [ "ideCadastro", "numLegislatura" ],
                                              'mandatory_params': [ "ideCadastro"]
                                             },

                  'ObterLideresBancadas'   : {
                                            'url_ending'      : "/ObterLideresBancadas",
                                            'allowed_params'  : [ ],
                                            'mandatory_params': [ ]
                                             },

                  'ObterPartidosCD'        : {
                                              'url_ending'      : "/ObterPartidosCD",
                                               'allowed_params'  : [ ],
                                               'mandatory_params': [ ]
                                             },

                  'ObterPartidosBlocoCD'   : {
                                              'url_ending'      : "/ObterPartidosBlocoCD?",
                                              'allowed_params'  : [ "idBloco", "numLegislatura"],
                                              'mandatory_params': [ ]
                                             }
                  },

  'orgaos' : {

              'ListarCargosOrgaosLegislativosCD'     : {
                                                       'url_ending'      : "/ListarCargosOrgaosLegislativosCD",
                                                       'allowed_params'  : [ ],
                                                       'mandatory_params': [ ]
                                                        },

              'ListarTiposOrgaos'                     : {
                                                        'url_ending'      : "/ListarTiposOrgaos",
                                                        'allowed_params'  : [ ], 
                                                        'mandatory_params': [ ]
                                                       },

              'ObterAndamento'                       : {
                                                       'url_ending'      : "/ObterAndamento?",
                                                       'allowed_params'  : [ "Sigla", "Numero", "Ano", "dataIni", "CodOrgao" ], 
                                                       'mandatory_params': [ "Numero", "Ano" ]
                                                       },
              
              'ObterEmendasSubstitutivoRedacaoFinal' : {
                                                        'url_ending'      : "/ObterEmendasSubstitutivoRedacaoFinal?",
                                                        'allowed_params'  : [ "Tipo", "Numero", "Ano" ], 
                                                        'mandatory_params': [ "Tipo", "Numero", "Ano" ]
                                                        },

              'ObterIntegraComissoesRelator'          : {
                                                        'url_ending'      : "/ObterIntegraComissoesRelator?",
                                                        'allowed_params'  : [ "Tipo", "Numero", "Ano" ], 
                                                        'mandatory_params': [ "Tipo", "Numero", "Ano" ]
                                                        },

              'ObterMembrosOrgao'                     : {
                                                        'url_ending'      : "/ObterMembrosOrgao?",
                                                        'allowed_params'  : [ "idOrgao" ], 
                                                        'mandatory_params': [ "idOrgao" ]
                                                        },

              'ObterOrgaos'                           : {
                                                        'url_ending'      : "/ObterOrgaos",
                                                        'allowed_params'  : [ ], 
                                                        'mandatory_params': [ ]
                                                        },

              'ObterPauta'                           : {
                                                        'url_ending'      : "/ObterPauta?",
                                                        'allowed_params'  : [ 'IdOrgao', 'datIni', 'datFim' ], 
                                                        'mandatory_params': [ 'IdOrgao' ]
                                                        },

              'ObterRegimeTramitacaoDespacho'        : {
                                                        'url_ending'      : "/ObterRegimeTramitacaoDespacho?",
                                                        'allowed_params'  : [ 'IdOrgao', 'datIni', 'datFim' ], 
                                                        'mandatory_params': [ 'IdOrgao' ]
                                                        }

              },

  'SessoesReunioes' : {

              'ListarDiscursosPlenario'     : {
                                              'url_ending'      : "/ListarDiscursosPlenario?",
                                              'allowed_params'  : [ 'dataIni', 'dataFim', 'CodigoSessao', 'ParteNomeParlamentar', 'SiglaPartido', 'SiglaUF' ],
                                              'mandatory_params': [ 'dataIni', 'dataFim' ]
                                              },

              'ListarPresencasDia'          : {
                                              'url_ending'      : "/ListarPresencasDia?",
                                              'allowed_params'  : [ 'data', 'numMatriculaParlamentar', 'siglaPartido', 'siglaUF' ],
                                              'mandatory_params': [ 'data' ]
                                              },

              'ListarPresencasParlamentar'  : {
                                              'url_ending'      : "/ListarPresencasParlamentar?",
                                              'allowed_params'  : [ 'dataIni', 'dataFim', 'numMatriculaParlamentar' ],
                                              'mandatory_params': [ 'dataIni', 'dataFim', 'numMatriculaParlamentar' ]
                                              },

              'ListarSituacoesReuniaoSessao' : {
                                               'url_ending'      : "/ListarSituacoesReuniaoSessao",
                                               'allowed_params'  : [ ],
                                               'mandatory_params': [ ]
                                               },



  }

}

BASE_URLS = {
  
  'proposicoes'     : "https://www.camara.leg.br/SitCamaraWS/Proposicoes.asmx",

  'deputado'        : "http://www.camara.gov.br/SitCamaraWS/Deputados.asmx",

  'orgaos'          : "http://www.camara.gov.br/SitCamaraWS/Orgaos.asmx",

  'SessoesReunioes' : "http://www.camara.gov.br/SitCamaraWS/SessoesReunioes.asmx"

}

################################
### FUNCIONALIDADES CENTRAIS ###
################################

# Função genérica para construir a URL da solicitação
def build_url(request_type, parameters, webservice):

  ''' 
  Essa é uma função genérica que constrói a URL
  de qualquer solicitação possível para a API.

  Parâmetros:
  request_type -> O tipo de requisição, que deve estar entre as chaves
  da variável global REQUEST_TYPES

  parameters -> Um objeto que contém os pares nome:valor que serão passados
  para a URL. Exemplo: { "DtInicio":01/01/1901, "DtFim":'DtFim:01/01/2001 },
  que virariam uma string '[url]?DtInicio=01/01/1901&dtFim=01/01/2001.'

  webservice -> String usada para selecionar os parâmetros permitidos e obrigatórios 
  em cada tipo de requisição. É, na prática, uma chave usada para acessar os dados do
  dicionário global WEBSERVICES.
  '''

  # Seleciona o webservice desejado para a requisição
  request_types = WEBSERVICES[webservice]

  # Checa se o tipo de requisição é válido
  if request_type not in request_types.keys():
    raise Exception(f"O tipo de requisição que você enviou é inválido. Os tipos válidos são: { list(request_types.keys()) }")

  # Para economizar operações e tornar o código mais claro, salva o subdicionário 
  # referente a esse tipo de requisição em uma variável.
  this_request_type = request_types[request_type]

  # Salva também os parâmetros permitidos/obrigatórios para essa requisição
  allowed_params = this_request_type["allowed_params"]
  mandatory_params = this_request_type["mandatory_params"]

  # Checa se os argumentos passados são válidos para esse tipo da requisição.
  wrong_params = [ item for item in parameters.keys() if item not in allowed_params ]

  if any(wrong_params):
    
    if len(allowed_params) > 0:
      err_message = f"Ao menos um dos parâmetros que você escolheu para essa requisição é inválido: {wrong_params}.\nOs parâmetros permitidos são {allowed_params}"
    
    else:
      err_message = f"Ao menos um dos parâmetros que você escolheu para essa requisição é inválido: {wrong_params}.\nEssa requisição não permite nenhum parâmetro."
      raise Exception(err_message)
  
  # Checa se todos os parâmetros obrigatórios foram enviados
  missing_params = [ item for item in mandatory_params if item not in parameters.keys() ]

  if any(missing_params):
    err_message = f"Faltam parâmetros obrigatórios na sua requisição: {missing_params}"
    raise Exception(err_message)

  # Essa versão da API da Câmara exige que __todos__ os parâmetros possíveis estejam presentes 
  # na URL, ainda que o valor seja nulo. ¯\_(ツ)_/¯ Vamos adicionar:
  for item in allowed_params:

    if item not in parameters:
      parameters[item] = ""

  # Cria uma string para a url com base na request_type
  url = BASE_URLS[webservice] + this_request_type["url_ending"]

  # Criar uma string com os parâmetros passados para a URL
  string = ""

  for k,v in parameters.items():
    substring = f"&{k}={v}"
    string += substring

  string = string.strip("&")

  # Concatena url e parâmetros
  url += string
  
  return url

# Função para executar uma requisição
def make_request(request_type, parameters, webservice):

  '''
  Essa função faz uma requisição usando o módulo
  requests. Na versão antiga da API da Câmara, o
  valor de retorno sempre é em XML. Aqui, usamos
  o módulo xmltodict para converter os dados em
  um objeto json-like e facilitar o processamento.


  Parâmetros:
  request_type -> O tipo de requisição, que deve estar entre as chaves
  da variável global REQUEST_TYPES

  parameters -> Um objeto que contém os pares nome:valor que serão passados
  para a URL. Exemplo: { "DtInicio":01/01/1901, "DtFim":'DtFim:01/01/2001 },
  que virariam [url]?DtInicio=01/01/1901&dtFim=01/01/2001.

  webservice -> String usada para selecionar os parâmetros permitidos e obrigatórios 
  em cada tipo de requisição. É, na prática, uma chave usada para acessar os dados do
  dicionário global WEBSERVICES.
  '''

  # Monta url e faz requisicão
  url = build_url(request_type, parameters, webservice)
  response = requests.get(url)
  data = response.text

  # Levanta exceção HTTPError caso a resposta tenha código 4xx ou 5xx
  # TO DO: vale a pena lidar de forma diferente com erros 404, que
  # denotam que não foram encontrados dados para uma busca específica?
  if response.status_code in range(400, 501):

    if 'proposicao e acessoria' in data:
      raise ProposicaoAcessoria(ProposicaoAcessoria.err_message)

    else:
      raise requests.HTTPError(f"Houve um erro na sua requisição. O servidor respondeu com: '{data}'")

  # Transforma em JSON
  data = xmltodict.parse(data)

  # Checa se retornou erro em formato xml (o que acontece sem explicação do motivo, 
  # de vez em quando ¯\_(ツ)_/¯
  if 'erro' in data.keys():
    server_message = data['erro']['descricao']
    raise Exception(f"Houve um erro na sua requisição. O servidor respondeu com: \"{server_message}\"")

  return data
