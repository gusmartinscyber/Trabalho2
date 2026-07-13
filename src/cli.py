from __future__ import annotations

from pathlib import Path

from src.equipamento import Equipamento
from src.erros import ErroValidacao
from src.inventario import Inventario
from src.models import Severidade, StatusTratamento, TipoAtivo
from src.vulnerabilidade import Vulnerabilidade

from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.table import Table


class InventarioCLI:
    """Interface de linha de comando para o inventario de ativos."""

    def __init__(self, inventario: Inventario, console: Console | None = None) -> None:
        self._inventario = inventario
        self._console = console or Console()

    def executar(self) -> int:
        while True:
            self._render_menu()
            try:
                opcao = self._prompt_text("Opcao", default="0").strip()
            except EOFError:
                self._render_info("Entrada encerrada.")
                return 0

            if opcao == "0":
                self._render_info("Encerrando aplicacao.")
                return 0

            try:
                self._processar_opcao(opcao)
            except EOFError:
                self._render_info("Entrada encerrada.")
                return 0
            except ErroValidacao as exc:
                self._render_error(str(exc))
            except Exception as exc:
                self._render_error(f"Falha inesperada: {exc}")

    def exibir_startup(
        self,
        caminho_json: Path,
        total_ativos: int,
        total_vulnerabilidades: int,
        catalogo_tipos: dict[int, str],
    ) -> None:
        with Progress(
            SpinnerColumn(style="cyan"),
            TextColumn("[cyan]Preparando ambiente da aplicacao..."),
            BarColumn(bar_width=24, complete_style="green", finished_style="green"),
            console=self._console,
            transient=True,
        ) as progress:
            task_id = progress.add_task("startup", total=3)
            progress.advance(task_id)
            progress.advance(task_id)
            progress.advance(task_id)

        tipos = "\n".join(
            f"[{codigo}] {descricao}" for codigo, descricao in catalogo_tipos.items()
        )
        conteudo = (
            "[bold white]Inventario de Seguranca[/bold white]\n"
            "Ativos de TI e Vulnerabilidades\n\n"
            f"[cyan]Arquivo JSON:[/cyan] {caminho_json}\n"
            f"[cyan]Ativos cadastrados:[/cyan] {total_ativos}\n"
            f"[cyan]Vulnerabilidades cadastradas:[/cyan] {total_vulnerabilidades}\n\n"
            "[bold]Catalogo de tipos de ativo[/bold]\n"
            f"{tipos}"
        )
        self._console.print(Panel(conteudo, border_style="green", title="Inicializacao"))

    def _processar_opcao(self, opcao: str) -> None:
        acoes = {
            "1": self._cadastrar_ativo,
            "2": self._buscar_ativo,
            "3": self._listar_ativos,
            "4": self._atualizar_ativo,
            "5": self._remover_ativo,
            "6": lambda: self._render_info(
                "Funcionalidade disponivel na Fase 5 (cadastro de vulnerabilidades)."
            ),
            "7": lambda: self._render_info(
                "Funcionalidade disponivel na Fase 5 (visualizacao de vulnerabilidades)."
            ),
            "8": lambda: self._render_info(
                "Funcionalidade disponivel na Fase 7 (exportacao de inventario)."
            ),
        }

        acao = acoes.get(opcao)
        if acao is None:
            self._render_error("Opcao de menu invalida.")
            return

        acao()

    def _cadastrar_ativo(self) -> None:
        self._render_tipo_ativos()
        equipamento = self._inventario.cadastrar(
            self._prompt_text("Identificador unico"),
            self._prompt_text("Hostname ou nome"),
            self._prompt_text("Responsavel"),
            self._prompt_text("Setor ou localizacao"),
            self._prompt_text("Codigo do tipo de ativo"),
            self._prompt_text("Descricao", default=""),
        )
        self._render_success("Ativo cadastrado.")
        self._render_ativo(equipamento)

        while self._prompt_confirm(
            "Cadastrar vulnerabilidade inicial para este ativo?", default=False
        ):
            self._coletar_vulnerabilidade(equipamento.id)

    def _buscar_ativo(self) -> None:
        criterio = self._prompt_text(
            "Buscar por [1] identificador ou [2] hostname", default="1"
        )
        if criterio == "1":
            equipamento = self._inventario.obter_por_id(
                self._prompt_text("Identificador")
            )
        elif criterio == "2":
            equipamento = self._inventario.obter_por_hostname(
                self._prompt_text("Hostname")
            )
        else:
            raise ErroValidacao("Opcao de busca invalida.")

        self._render_ativo(equipamento)

    def _listar_ativos(self) -> None:
        ativos = self._inventario.listar()
        if not ativos:
            self._render_info("Nenhum ativo cadastrado.")
            return

        table = Table(title="Ativos cadastrados", border_style="green")
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("Hostname")
        table.add_column("Responsavel")
        table.add_column("Setor/localizacao")
        table.add_column("Tipo")
        table.add_column("Resumo")
        for equipamento in ativos:
            table.add_row(
                str(equipamento.id),
                equipamento.hostname,
                equipamento.responsavel,
                equipamento.setor,
                equipamento.tipo().label,
                equipamento.resumo(),
            )
        self._console.print(table)

    def _atualizar_ativo(self) -> None:
        equipamento_atual = self._inventario.obter_por_id(
            self._prompt_text("Identificador do ativo")
        )
        self._render_ativo(equipamento_atual)
        self._render_info("Pressione Enter para manter o valor atual.")
        self._render_tipo_ativos()

        equipamento = self._inventario.atualizar(
            equipamento_atual.id,
            self._prompt_text("Hostname ou nome", default=equipamento_atual.hostname),
            self._prompt_text("Responsavel", default=equipamento_atual.responsavel),
            self._prompt_text("Setor ou localizacao", default=equipamento_atual.setor),
            self._prompt_text(
                "Codigo do tipo de ativo", default=str(equipamento_atual.tipo().value)
            ),
            self._prompt_text("Descricao", default=equipamento_atual.descricao),
        )
        self._render_success("Ativo atualizado.")
        self._render_ativo(equipamento)

    def _remover_ativo(self) -> None:
        equipamento = self._inventario.obter_por_id(
            self._prompt_text("Identificador do ativo")
        )
        self._render_ativo(equipamento)
        if not self._prompt_confirm(
            "Confirmar remocao do ativo e vulnerabilidades associadas?", default=False
        ):
            self._render_info("Remocao cancelada.")
            return

        removido = self._inventario.remover(equipamento.id)
        self._render_success(f"Ativo {removido.hostname} removido.")

    def _coletar_vulnerabilidade(self, ativo_id: int) -> None:
        self._render_opcoes_vulnerabilidade()
        vulnerabilidade = self._inventario.adicionar_vulnerabilidade(
            ativo_id,
            self._prompt_text("Descricao da vulnerabilidade"),
            self._prompt_text("Categoria ou tipo"),
            self._prompt_text("Codigo da severidade"),
            self._prompt_text("Codigo do status"),
        )
        self._render_success("Vulnerabilidade cadastrada.")
        self._render_vulnerabilidade(vulnerabilidade, ativo_id)

    def _render_menu(self) -> None:
        menu = (
            "[1] Cadastrar ativo\n"
            "[2] Buscar ativo\n"
            "[3] Listar ativos\n"
            "[4] Atualizar ativo\n"
            "[5] Remover ativo\n"
            "[6] Cadastrar vulnerabilidade\n"
            "[7] Visualizar vulnerabilidades\n"
            "[8] Exportar inventario\n"
            "[0] Sair"
        )
        self._console.print(Panel(menu, title="Menu principal", border_style="cyan"))

    def _render_tipo_ativos(self) -> None:
        table = Table(title="Tipos de ativo", border_style="cyan")
        table.add_column("Codigo", justify="right", style="cyan")
        table.add_column("Tipo")
        for codigo, descricao in TipoAtivo.choices().items():
            table.add_row(str(codigo), descricao)
        self._console.print(table)

    def _render_opcoes_vulnerabilidade(self) -> None:
        severidades = Table(title="Severidades", border_style="yellow")
        severidades.add_column("Codigo", justify="right", style="yellow")
        severidades.add_column("Severidade")
        for codigo, descricao in Severidade.choices().items():
            severidades.add_row(str(codigo), descricao)

        status_table = Table(title="Status de tratamento", border_style="cyan")
        status_table.add_column("Codigo", justify="right", style="cyan")
        status_table.add_column("Status")
        for codigo, descricao in StatusTratamento.choices().items():
            status_table.add_row(str(codigo), descricao)

        self._console.print(severidades)
        self._console.print(status_table)

    def _render_ativo(self, equipamento: Equipamento) -> None:
        self._console.print(
            Panel(
                equipamento.formatar_detalhes(),
                title="Ativo",
                border_style="green",
            )
        )

    def _render_vulnerabilidade(
        self, vulnerabilidade: Vulnerabilidade, ativo_id: int
    ) -> None:
        conteudo = (
            f"ID: {vulnerabilidade.id}\n"
            f"Ativo: {ativo_id}\n"
            f"Descricao: {vulnerabilidade.descricao}\n"
            f"Categoria: {vulnerabilidade.categoria}\n"
            f"Severidade: {vulnerabilidade.severidade.value}\n"
            f"Status: {vulnerabilidade.status.value}"
        )
        self._console.print(
            Panel(conteudo, title="Vulnerabilidade", border_style="yellow")
        )

    def _render_error(self, message: str) -> None:
        self._console.print(f"[bold red]Erro:[/bold red] {message}")

    def _render_success(self, message: str) -> None:
        self._console.print(f"[bold green]OK:[/bold green] {message}")

    def _render_info(self, message: str) -> None:
        self._console.print(f"[cyan]{message}[/cyan]")

    def _prompt_text(self, message: str, default: str | None = None) -> str:
        return Prompt.ask(message, default=default, console=self._console)

    def _prompt_confirm(self, message: str, default: bool = False) -> bool:
        return Confirm.ask(message, default=default, console=self._console)
