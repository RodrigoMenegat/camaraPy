from camaraPy.api_original.tools import tools

def ListarDiscursosPlenario(parameters = { }):
  return tools.make_request('ListarDiscursosPlenario', parameters, 'SessoesReunioes')

def ListarPresencasDia(parameters = { }):
  return tools.make_request('ListarPresencasDia', parameters, 'SessoesReunioes')

def ListarPresencasParlamentar(parameters = { }):
  return tools.make_request('ListarPresencasParlamentar', parameters, 'SessoesReunioes')

def ListarSituacoesReuniaoSessao(parameters = { }):
  return tools.make_request('ListarSituacoesReuniaoSessao', parameters, 'SessoesReunioes')