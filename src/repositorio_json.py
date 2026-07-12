from __future__ import annotations

import json
import os
from pathlib import Path

from src.equipamento import Equipamento
from src.erros import ErroValidacao
from src.factory import EquipamentoFactory

BASE_DIR = Path(__file__).resolve().parent.parent
CAMINHO_PADRAO = BASE_DIR / "data" / "inventario.json"


class RepositorioJson:
    """Persistencia do inventario em arquivo JSON com raiz em array."""

    def __init__(self, caminho: Path | None = None) -> None:
        if caminho is not None:
            self._caminho = Path(caminho)
            return

        env_path = os.environ.get("INVENTARIO_JSON_PATH")
        if env_path:
            self._caminho = Path(env_path)
            return

        self._caminho = CAMINHO_PADRAO

    @property
    def caminho(self) -> Path:
        return self._caminho

    def existe(self) -> bool:
        return self._caminho.is_file()

    def carregar(self) -> list[Equipamento]:
        if not self.existe():
            return []

        conteudo = self._caminho.read_text(encoding="utf-8").strip()
        if not conteudo:
            return []

        try:
            dados = json.loads(conteudo)
        except json.JSONDecodeError as exc:
            raise ErroValidacao(
                f"Arquivo JSON invalido em {self._caminho}: {exc.msg}"
            ) from exc

        if not isinstance(dados, list):
            raise ErroValidacao(
                "O arquivo de inventario deve conter um array JSON na raiz."
            )

        return [EquipamentoFactory.from_dict(item) for item in dados]

    def salvar(self, equipamentos: list[Equipamento]) -> None:
        self._caminho.parent.mkdir(parents=True, exist_ok=True)
        payload = [equipamento.to_dict() for equipamento in equipamentos]
        self._caminho.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
