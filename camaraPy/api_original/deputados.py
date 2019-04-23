from camaraPy.api_original.core import core, custom_exceptions

def ObterDeputados(parameters = { }):
  return core.make_request('ObterDeputados', parameters, 'deputado')

def ObterDetalhesDeputados(parameters = { }):
  return core.make_request('ObterDetalhesDeputados', parameters, 'deputado')

def ObterLideresBancadas(parameters = { }):
  return core.make_request('ObterLideresBancadas', parameters, 'deputado')

def ObterPartidosCD(parameters = { }):
  return core.make_request('ObterPartidosCD', parameters, 'deputado')

def ObterPartidosBlocoCD(parameters = { }):
  return core.make_request('ObterPartidosBlocoCD', parameters, 'deputado')
