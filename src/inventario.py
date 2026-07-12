from __future__ import annotations

from src.equipamento import Equipamento
from src.repositorio_json import RepositorioJson


class Inventario:
    """Gerencia a colecao de equipamentos e sua persistencia em JSON."""

    def __init__(self, repositorio: RepositorioJson | None = None) -> None:
        self._repositorio = repositorio or RepositorioJson()
        self._equipamentos: list[Equipamento] = []

    @property
    def equipamentos(self) -> list[Equipamento]:
        return list(self._equipamentos)

    @property
    def repositorio(self) -> RepositorioJson:
        return self._repositorio

    def carregar(self) -> None:
        self._equipamentos = self._repositorio.carregar()

    def salvar(self) -> None:
        self._repositorio.salvar(self._equipamentos)

    def adicionar(self, equipamento: Equipamento) -> None:
        equipamento.validar()
        self._equipamentos.append(equipamento)

    def total_ativos(self) -> int:
        return len(self._equipamentos)

    def total_vulnerabilidades(self) -> int:
        return sum(len(equipamento.vulnerabilidades) for equipamento in self._equipamentos)
