from __future__ import annotations

from src.equipamento import (
    AplicacaoWeb,
    BancoDeDados,
    Equipamento,
    EstacaoTrabalho,
    ImpressoraRede,
    Notebook,
    Roteador,
    Servidor,
)
from src.erros import ErroValidacao
from src.models import TIPOS_ATIVO_POR_CODIGO, TipoAtivo
from src.vulnerabilidade import Vulnerabilidade


class EquipamentoFactory:
    """Fabrica de equipamentos para criacao e reconstrucao a partir de JSON."""

    _MAPEAMENTO: dict[TipoAtivo, type[Equipamento]] = {
        TipoAtivo.NOTEBOOK: Notebook,
        TipoAtivo.SERVIDOR: Servidor,
        TipoAtivo.ROTEADOR: Roteador,
        TipoAtivo.APLICACAO_WEB: AplicacaoWeb,
        TipoAtivo.BANCO_DE_DADOS: BancoDeDados,
        TipoAtivo.IMPRESSORA_REDE: ImpressoraRede,
        TipoAtivo.ESTACAO_TRABALHO: EstacaoTrabalho,
    }

    @classmethod
    def criar(cls, tipo: TipoAtivo, **dados: object) -> Equipamento:
        classe = cls._MAPEAMENTO.get(tipo)
        if classe is None:
            raise ErroValidacao("Tipo de ativo invalido.")

        return classe(
            id=int(dados["id"]),  # type: ignore[arg-type]
            hostname=str(dados["hostname"]),
            responsavel=str(dados["responsavel"]),
            setor=str(dados["setor"]),
            descricao=str(dados.get("descricao", "")),
            vulnerabilidades=cls._desserializar_vulnerabilidades(
                dados.get("vulnerabilidades", [])
            ),
        )

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Equipamento:
        tipo_codigo = int(data["tipo"])  # type: ignore[arg-type]
        tipo = TIPOS_ATIVO_POR_CODIGO.get(tipo_codigo)
        if tipo is None:
            raise ErroValidacao("Tipo de ativo invalido.")

        dados = dict(data)
        dados.pop("tipo", None)
        return cls.criar(tipo, **dados)

    @staticmethod
    def _desserializar_vulnerabilidades(
        vulnerabilidades: object,
    ) -> list[Vulnerabilidade]:
        if not isinstance(vulnerabilidades, list):
            return []

        return [
            Vulnerabilidade.from_dict(item)  # type: ignore[arg-type]
            for item in vulnerabilidades
        ]
