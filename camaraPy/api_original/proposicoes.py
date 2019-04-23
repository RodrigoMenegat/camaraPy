from camaraPy.api_original.core import core, custom_exceptions

def ListarProposicoes(parameters = { }):
  return core.make_request('ListarProposicoes', parameters, 'proposicoes')

def ListarSiglasTipoProposicao(parameters = { }):
  return core.make_request('ListarSiglasTipoProposicao', parameters, 'proposicoes')

def ListarSituacoesProposicao(parameters = { }):
  return core.make_request('ListarSituacoesProposicao', parameters, 'proposicoes')

def ListarTiposAutores(parameters = { }):
  return core.make_request('ListarTiposAutores', parameters, 'proposicoes')

def ObterProposicao(parameters = { }):
  return core.make_request('ObterProposicao', parameters, 'proposicoes')

def ObterProposicaoPorID(parameters = { }):
  return core.make_request('ObterProposicaoPorID', parameters, 'proposicoes')

def ListarProposicoesVotadasEmPlenario(parameters = { }):
  return core.make_request('ListarProposicoesVotadasEmPlenario', parameters, 'proposicoes')

def ListarProposicoesTramitadasNoPeriodo(parameters = { }):
  return core.make_request('ListarProposicoesTramitadasNoPeriodo', parameters, 'proposicoes')

def ObterVotacaoProposicao(parameters = { }):

  try:
    return core.make_request('ObterVotacaoProposicao', parameters, 'proposicoes')

  except custom_exceptions.ProposicaoAcessoria as e:
    raise custom_exceptions.ProposicaoAcessoria(custom_exceptions.ProposicaoAcessoria.err_message)
