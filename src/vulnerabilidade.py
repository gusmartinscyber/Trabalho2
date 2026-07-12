from __future__ import annotations

from src.erros import ErroValidacao
from src.models import (
    SEVERIDADES_POR_CODIGO,
    SEVERIDADES_POR_VALOR,
    STATUS_POR_CODIGO,
    STATUS_POR_VALOR,
    Severidade,
    StatusTratamento,
)


class Vulnerabilidade:
    """Representa uma vulnerabilidade associada a um equipamento."""

    def __init__(
        self,
        id: int,
        descricao: str,
        categoria: str,
        severidade: Severidade,
        status: StatusTratamento,
    ) -> None:
        self._id = id
        self._descricao = descricao
        self._categoria = categoria
        self._severidade = severidade
        self._status = status

    @property
    def id(self) -> int:
        return self._id

    @property
    def descricao(self) -> str:
        return self._descricao

    @property
    def categoria(self) -> str:
        return self._categoria

    @property
    def severidade(self) -> Severidade:
        return self._severidade

    @property
    def status(self) -> StatusTratamento:
        return self._status

    def validar(self) -> None:
        if self._id <= 0:
            raise ErroValidacao("O identificador da vulnerabilidade deve ser positivo.")

        self._descricao = self._normalizar_texto(
            self._descricao, "Descricao da vulnerabilidade"
        )
        self._categoria = self._normalizar_texto(
            self._categoria, "Categoria da vulnerabilidade"
        )

        if not isinstance(self._severidade, Severidade):
            raise ErroValidacao("Severidade invalida.")

        if not isinstance(self._status, StatusTratamento):
            raise ErroValidacao("Status de tratamento invalido.")

    def to_dict(self) -> dict[str, str | int]:
        return {
            "id": self._id,
            "descricao": self._descricao,
            "categoria": self._categoria,
            "severidade": self._severidade.value,
            "status": self._status.value,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str | int]) -> Vulnerabilidade:
        return cls(
            id=int(data["id"]),
            descricao=str(data["descricao"]),
            categoria=str(data["categoria"]),
            severidade=cls._resolver_severidade(data["severidade"]),
            status=cls._resolver_status(data["status"]),
        )

    @staticmethod
    def _normalizar_texto(value: str, field_name: str) -> str:
        text = value.strip()
        if not text:
            raise ErroValidacao(f"{field_name} nao pode ficar vazio.")
        return text

    @staticmethod
    def _resolver_severidade(value: str | int) -> Severidade:
        raw_value = str(value).strip()
        if not raw_value:
            raise ErroValidacao("A severidade deve ser informada.")

        try:
            codigo = int(raw_value)
        except ValueError:
            severidade = SEVERIDADES_POR_VALOR.get(raw_value.lower())
        else:
            severidade = SEVERIDADES_POR_CODIGO.get(codigo)

        if severidade is None:
            raise ErroValidacao("Severidade invalida.")

        return severidade

    @staticmethod
    def _resolver_status(value: str | int) -> StatusTratamento:
        raw_value = str(value).strip()
        if not raw_value:
            raise ErroValidacao("O status de tratamento deve ser informado.")

        try:
            codigo = int(raw_value)
        except ValueError:
            status = STATUS_POR_VALOR.get(raw_value.lower())
        else:
            status = STATUS_POR_CODIGO.get(codigo)

        if status is None:
            raise ErroValidacao("Status de tratamento invalido.")

        return status
