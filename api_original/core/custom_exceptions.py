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