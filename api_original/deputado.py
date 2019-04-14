from camaraPy.api_original.tools import tools

def ObterDeputados(parameters = { }):
  return tools.make_request('ObterDeputados', parameters, 'deputado')

def ObterDetalhesDeputados(parameters = { }):
  return tools.make_request('ObterDetalhesDeputados', parameters, 'deputado')

def ObterLideresBancadas(parameters = { }):
  return tools.make_request('ObterLideresBancadas', parameters, 'deputado')

def ObterPartidosCD(parameters = { }):
  return tools.make_request('ObterPartidosCD', parameters, 'deputado')

def ObterPartidosBlocoCD(parameters = { }):
  return tools.make_request('ObterPartidosBlocoCD', parameters, 'deputado')
