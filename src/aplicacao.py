from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.cli import InventarioCLI
from src.inventario import Inventario
from src.models import TipoAtivo


@dataclass(frozen=True)
class ResumoInicializacao:
    caminho_json: Path
    total_ativos: int
    total_vulnerabilidades: int
    catalogo_tipos: dict[int, str]


class Aplicacao:
    """Bootstrap da aplicacao: carrega inventario JSON e executa a CLI."""

    def __init__(self) -> None:
        self._inventario = Inventario()
        self._resumo: ResumoInicializacao | None = None

    @property
    def inventario(self) -> Inventario:
        return self._inventario

    def inicializar(self) -> None:
        self._inventario.carregar()
        self._resumo = ResumoInicializacao(
            caminho_json=self._inventario.repositorio.caminho,
            total_ativos=self._inventario.total_ativos(),
            total_vulnerabilidades=self._inventario.total_vulnerabilidades(),
            catalogo_tipos=TipoAtivo.choices(),
        )

    def executar(self) -> int:
        if self._resumo is None:
            self.inicializar()

        resumo = self._resumo
        assert resumo is not None

        cli = InventarioCLI(self._inventario)
        cli.exibir_startup(
            resumo.caminho_json,
            resumo.total_ativos,
            resumo.total_vulnerabilidades,
            resumo.catalogo_tipos,
        )
        return cli.executar()
