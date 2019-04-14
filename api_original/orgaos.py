from camaraPy.api_original.core import core, custom_exceptions

def ListarCargosOrgaosLegislativosCD(parameters = { }):
  return core.make_request('ListarCargosOrgaosLegislativosCD', parameters, 'orgaos')

def ListarTiposOrgaos(parameters = { }):
  return core.make_request('ListarTiposOrgaos', parameters, 'orgaos')

def ObterAndamento(parameters = { }):
  return core.make_request('ObterAndamento', parameters, 'orgaos')

def ObterEmendasSubstitutivoRedacaoFinal(parameters = { }):
  return core.make_request('ObterEmendasSubstitutivoRedacaoFinal', parameters, 'orgaos')

def ObterIntegraComissoesRelator(parameters = { }):
  return core.make_request('ObterIntegraComissoesRelator', parameters, 'orgaos')

def ObterMembrosOrgao(parameters = { }):
  return core.make_request('ObterMembrosOrgao', parameters, 'orgaos')

def ObterOrgaos(parameters = { }):
  return core.make_request('ObterOrgaos', parameters, 'orgaos')

def ObterPauta(parameters = { }):
  return core.make_request('ObterPauta', parameters, 'orgaos')

def ObterRegimeTramitacaoDespacho(parameters = { }):
  return core.make_request('ObterRegimeTramitacaoDespacho', parameters, 'orgaos')