###############################
### EXCEÇÕES PERSONALIZADAS ###
###############################

# Classe de erro específica para proposições secundárias
class ProposicaoAcessoria(Exception):
  '''
  Exceção que deve ser levantada quando for solicitada
  uma proposição acessória para a qual não há dados de
  votação.
  '''
  err_message = "Essa é uma proposição acessória, atrelada a outra principal. Este método apenas suporta proposições principais."

class SemDados(Exception):
  '''
  Quando a API não encontra dados em  algumas requisições, em vez de retornar
  um array ou objeto vazio, o servidor responde com um código de erro e uma 
  mensagem de texto. Quando isso acontece,vamos capturar o comportamento 
  e levantar uma exceção condizente.
  '''
  err_message = "Não foram encontrados dados para essa solicitação."