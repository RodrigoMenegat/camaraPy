# camaraPy

## O que é?

O pacote camaraPy é um wrapper, ainda em estágio inicial de desenvolvido, para as APIs da [Câmara dos Deputados](https://dadosabertos.camara.leg.br/).

Agora, em vez de montar a requisição manualmente usando pacotes como `urrlib` ou `requests`, você pode simplesmente instalar o **camaraPy** e fazer tudo em poucas linhas de código:

```
from camaraPy.api_original import proposicoes

# Define parâmetros para a consulta
params = {
    "Tipo"   : prop['@tipo'].strip(),
    "Numero" : prop['@numero'].strip(),
    "Ano"    : prop['@ano'].strip()
  }
        
# Acessa as votações da proposta
voting_sessions = proposicoes.ObterVotacaoProposicao(params)
```

Por enquanto, o módulo funciona apenas com a [API original](https://www2.camara.leg.br/transparencia/dados-abertos/dados-abertos-legislativo), que é mais estável e inclui o resultado das votações em plenário, dado que ainda não está disponível no novo serviço.

## Como usar?

Todos as requsições descritas na [documentação da Câmara](https://www2.camara.leg.br/transparencia/dados-abertos/dados-abertos-legislativo/dados-abertos-legislativo) foram implementadas, exatamente com a mesma grafia. O nome dos webservices, porém, é grafado seguindo um padrão `lowercase_com_underlines`.

Assim, por exemplo, para acessar o método *ListarDiscursosPlenario* do Webservice *SessoesReunioes*, o usuário precisa executar o seguinte código, no qual a variável `params` é um dicionário com os parâmetros que devem ser feitos na requisição.

```
from camaraPy.api_original import sessoes_reunioes

parames = { "DataIni" : "10/10/2018", "DataFim" : "10/10/2018" }
dados = sessoes_reunioes.ListarDiscursosPlenario(parametros)
```

De maneira semelhante, para acessar o método *ObterDeputados* do Webservice *Deputados*, o código seria o seguinte:
```
from camaraPy.api_original import deputados

dados = deputados.ObterDeputados()
```

## Coisas técnicas:

O código, consiste, basicamente, em um script genérico que faz solicitações variadas para a API. Ele está disponível no diretório `core`. A partir desse programa, foram criadas funções encapsuladoras em `deputados.py`, `orgaos.py`, `sessoes_reunioes.py` e `votacoes.py`. Elas apenas chamam as funções definidas em `core.py` com os parâmetros corretos.