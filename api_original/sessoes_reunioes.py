from camaraPy.api_original.core import core, custom_exceptions

def ListarDiscursosPlenario(parameters = { }):
  return core.make_request('ListarDiscursosPlenario', parameters, 'SessoesReunioes')

def ListarPresencasDia(parameters = { }):
  return core.make_request('ListarPresencasDia', parameters, 'SessoesReunioes')

def ListarPresencasParlamentar(parameters = { }):
  return core.make_request('ListarPresencasParlamentar', parameters, 'SessoesReunioes')

def ListarSituacoesReuniaoSessao(parameters = { }):
  return core.make_request('ListarSituacoesReuniaoSessao', parameters, 'SessoesReunioes')