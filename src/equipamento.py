from __future__ import annotations

from abc import ABC, abstractmethod

from src.erros import ErroValidacao
from src.models import TipoAtivo
from src.vulnerabilidade import Vulnerabilidade


class Equipamento(ABC):
    """Classe base abstrata para ativos de TI do inventario."""

    def __init__(
        self,
        id: int,
        hostname: str,
        responsavel: str,
        setor: str,
        descricao: str | None = None,
        vulnerabilidades: list[Vulnerabilidade] | None = None,
    ) -> None:
        self._id = id
        self._hostname = hostname
        self._responsavel = responsavel
        self._setor = setor
        self._descricao = descricao or ""
        self._vulnerabilidades = list(vulnerabilidades or [])

    @property
    def id(self) -> int:
        return self._id

    @property
    def hostname(self) -> str:
        return self._hostname

    @property
    def responsavel(self) -> str:
        return self._responsavel

    @property
    def setor(self) -> str:
        return self._setor

    @property
    def descricao(self) -> str:
        return self._descricao

    @property
    def vulnerabilidades(self) -> list[Vulnerabilidade]:
        return list(self._vulnerabilidades)

    @abstractmethod
    def tipo(self) -> TipoAtivo:
        """Retorna o tipo numerico do ativo."""

    @abstractmethod
    def resumo(self) -> str:
        """Retorna representacao resumida polimorfica do ativo."""

    def validar_especifico(self) -> None:
        """Valida regras especificas da subclasse (extensivel)."""

    def validar(self) -> None:
        if self._id <= 0:
            raise ErroValidacao("O identificador do ativo deve ser positivo.")

        self._hostname = self._normalizar_texto(self._hostname, "Hostname")
        self._responsavel = self._normalizar_texto(self._responsavel, "Responsavel")
        self._setor = self._normalizar_texto(
            self._setor, "Setor ou localizacao"
        )
        self._descricao = self._normalizar_texto(
            self._descricao, "Descricao", required=False
        )

        self.validar_especifico()

        for vulnerabilidade in self._vulnerabilidades:
            vulnerabilidade.validar()

    def adicionar_vulnerabilidade(self, vulnerabilidade: Vulnerabilidade) -> None:
        vulnerabilidade.validar()
        self._vulnerabilidades.append(vulnerabilidade)

    def remover_vulnerabilidades(self) -> None:
        self._vulnerabilidades.clear()

    def to_dict(self) -> dict[str, str | int | list[dict[str, str | int]]]:
        return {
            "id": self._id,
            "hostname": self._hostname,
            "responsavel": self._responsavel,
            "setor": self._setor,
            "tipo": self.tipo().value,
            "descricao": self._descricao,
            "vulnerabilidades": [
                vulnerabilidade.to_dict() for vulnerabilidade in self._vulnerabilidades
            ],
        }

    def formatar_detalhes(self) -> str:
        linhas = [
            f"ID: {self._id}",
            f"Hostname: {self._hostname}",
            f"Responsavel: {self._responsavel}",
            f"Setor: {self._setor}",
            f"Tipo: {self.tipo().label}",
            f"Descricao: {self._descricao or '-'}",
            f"Vulnerabilidades: {len(self._vulnerabilidades)}",
        ]
        return "\n".join(linhas)

    @staticmethod
    def _normalizar_texto(value: str, field_name: str, required: bool = True) -> str:
        text = value.strip()
        if required and not text:
            raise ErroValidacao(f"{field_name} nao pode ficar vazio.")
        return text


class Notebook(Equipamento):
    def tipo(self) -> TipoAtivo:
        return TipoAtivo.NOTEBOOK

    def resumo(self) -> str:
        return f"[NOTEBOOK] {self._hostname} — {self._setor}"


class Servidor(Equipamento):
    def tipo(self) -> TipoAtivo:
        return TipoAtivo.SERVIDOR

    def resumo(self) -> str:
        return f"[SERVIDOR] {self._hostname} — {self._setor}"


class Roteador(Equipamento):
    def tipo(self) -> TipoAtivo:
        return TipoAtivo.ROTEADOR

    def resumo(self) -> str:
        return f"[ROTEADOR] {self._hostname} — {self._setor}"


class AplicacaoWeb(Equipamento):
    def tipo(self) -> TipoAtivo:
        return TipoAtivo.APLICACAO_WEB

    def resumo(self) -> str:
        return f"[APP WEB] {self._hostname} — {self._responsavel}"


class BancoDeDados(Equipamento):
    def tipo(self) -> TipoAtivo:
        return TipoAtivo.BANCO_DE_DADOS

    def resumo(self) -> str:
        return f"[BANCO DE DADOS] {self._hostname} — {self._setor}"


class ImpressoraRede(Equipamento):
    def tipo(self) -> TipoAtivo:
        return TipoAtivo.IMPRESSORA_REDE

    def resumo(self) -> str:
        return f"[IMPRESSORA] {self._hostname} — {self._setor}"


class EstacaoTrabalho(Equipamento):
    def tipo(self) -> TipoAtivo:
        return TipoAtivo.ESTACAO_TRABALHO

    def resumo(self) -> str:
        return f"[ESTACAO] {self._hostname} — {self._responsavel}"
