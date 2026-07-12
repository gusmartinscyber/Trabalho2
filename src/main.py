"""Ponto de entrada do inventario de ativos — Trabalho 2."""

from src.aplicacao import Aplicacao


def main() -> int:
    app = Aplicacao()
    app.inicializar()
    return app.executar()


if __name__ == "__main__":
    raise SystemExit(main())
