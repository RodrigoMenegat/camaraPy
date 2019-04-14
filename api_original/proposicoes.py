from camaraPy.api_original.tools import tools

def ListarProposicoes(parameters = { }):
  return tools.make_request('ListarProposicoes', parameters, 'proposicoes')

def ListarSiglasTipoProposicao(parameters = { }):
  return tools.make_request('ListarSiglasTipoProposicao', parameters, 'proposicoes')

def ListarSituacoesProposicao(parameters = { }):
  return tools.make_request('ListarSituacoesProposicao', parameters, 'proposicoes')

def ListarTiposAutores(parameters = { }):
  return tools.make_request('ListarTiposAutores', parameters, 'proposicoes')

def ObterProposicao(parameters = { }):
  return tools.make_request('ObterProposicao', parameters, 'proposicoes')

def ObterProposicaoPorID(parameters = { }):
  return tools.make_request('ObterProposicaoPorID', parameters, 'proposicoes')

def ObterVotacaoProposicao(parameters = { }):
  return tools.make_request('ObterVotacaoProposicao', parameters, 'proposicoes')

def ListarProposicoesVotadasEmPlenario(parameters = { }):
  return tools.make_request('ListarProposicoesVotadasEmPlenario', parameters, 'proposicoes')

def ListarProposicoesTramitadasNoPeriodo(parameters = { }):
  return tools.make_request('ListarProposicoesTramitadasNoPeriodo', parameters, 'proposicoes')
