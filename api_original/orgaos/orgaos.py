from camaraPy.api_original.tools import tools

def ListarCargosOrgaosLegislativosCD(parameters = { }):
  return tools.make_request('ListarCargosOrgaosLegislativosCD', parameters, 'orgaos')

def ListarTiposOrgaos(parameters = { }):
  return tools.make_request('ListarTiposOrgaos', parameters, 'orgaos')

def ObterAndamento(parameters = { }):
  return tools.make_request('ObterAndamento', parameters, 'orgaos')

def ObterEmendasSubstitutivoRedacaoFinal(parameters = { }):
  return tools.make_request('ObterEmendasSubstitutivoRedacaoFinal', parameters, 'orgaos')

def ObterIntegraComissoesRelator(parameters = { }):
  return tools.make_request('ObterIntegraComissoesRelator', parameters, 'orgaos')

def ObterMembrosOrgao(parameters = { }):
  return tools.make_request('ObterMembrosOrgao', parameters, 'orgaos')

def ObterOrgaos(parameters = { }):
  return tools.make_request('ObterOrgaos', parameters, 'orgaos')

def ObterPauta(parameters = { }):
  return tools.make_request('ObterPauta', parameters, 'orgaos')

def ObterRegimeTramitacaoDespacho(parameters = { }):
  return tools.make_request('ObterRegimeTramitacaoDespacho', parameters, 'orgaos')