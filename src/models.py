from __future__ import annotations

from enum import Enum, IntEnum


class TipoAtivo(IntEnum):
    NOTEBOOK = 1
    SERVIDOR = 2
    ROTEADOR = 3
    APLICACAO_WEB = 4
    BANCO_DE_DADOS = 5
    IMPRESSORA_REDE = 6
    ESTACAO_TRABALHO = 7

    @property
    def label(self) -> str:
        labels = {
            TipoAtivo.NOTEBOOK: "Notebook",
            TipoAtivo.SERVIDOR: "Servidor",
            TipoAtivo.ROTEADOR: "Roteador",
            TipoAtivo.APLICACAO_WEB: "Aplicacao Web",
            TipoAtivo.BANCO_DE_DADOS: "Banco de Dados",
            TipoAtivo.IMPRESSORA_REDE: "Impressora de Rede",
            TipoAtivo.ESTACAO_TRABALHO: "Estacao de Trabalho",
        }
        return labels[self]

    @classmethod
    def choices(cls) -> dict[int, str]:
        return {tipo.value: tipo.label for tipo in cls}


class Severidade(str, Enum):
    BAIXA = "Baixa"
    MEDIA = "Media"
    ALTA = "Alta"
    CRITICA = "Critica"

    @classmethod
    def choices(cls) -> dict[int, str]:
        return {index: item.value for index, item in enumerate(cls, start=1)}


class StatusTratamento(str, Enum):
    ABERTA = "Aberta"
    EM_TRATAMENTO = "Em tratamento"
    CORRIGIDA = "Corrigida"
    ACEITA_COMO_RISCO = "Aceita como risco"

    @classmethod
    def choices(cls) -> dict[int, str]:
        return {index: item.value for index, item in enumerate(cls, start=1)}


TIPOS_ATIVO_POR_CODIGO = {tipo.value: tipo for tipo in TipoAtivo}
TIPOS_ATIVO_POR_NOME = {tipo.name.lower(): tipo for tipo in TipoAtivo}
SEVERIDADES_POR_CODIGO = {
    index: item for index, item in enumerate(Severidade, start=1)
}
SEVERIDADES_POR_VALOR = {item.value.lower(): item for item in Severidade}
STATUS_POR_CODIGO = {
    index: item for index, item in enumerate(StatusTratamento, start=1)
}
STATUS_POR_VALOR = {item.value.lower(): item for item in StatusTratamento}
