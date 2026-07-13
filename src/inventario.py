from __future__ import annotations

from src.equipamento import Equipamento
from src.erros import ErroValidacao
from src.factory import EquipamentoFactory
from src.models import TIPOS_ATIVO_POR_CODIGO, TipoAtivo
from src.repositorio_json import RepositorioJson
from src.vulnerabilidade import Vulnerabilidade


class Inventario:
    """Gerencia a colecao de equipamentos e sua persistencia em JSON."""

    def __init__(self, repositorio: RepositorioJson | None = None) -> None:
        self._repositorio = repositorio or RepositorioJson()
        self._equipamentos: list[Equipamento] = []
        self._por_id: dict[int, Equipamento] = {}
        self._por_hostname: dict[str, Equipamento] = {}

    @property
    def equipamentos(self) -> list[Equipamento]:
        return list(self._equipamentos)

    @property
    def repositorio(self) -> RepositorioJson:
        return self._repositorio

    def carregar(self) -> None:
        self._equipamentos = self._repositorio.carregar()
        self.reconstruir_indices()

    def salvar(self) -> None:
        self._repositorio.salvar(self._equipamentos)

    def reconstruir_indices(self) -> None:
        self._por_id = {equipamento.id: equipamento for equipamento in self._equipamentos}
        self._por_hostname = {
            equipamento.hostname.lower(): equipamento for equipamento in self._equipamentos
        }

    def adicionar(self, equipamento: Equipamento) -> None:
        equipamento.validar()
        self._equipamentos.append(equipamento)
        self.reconstruir_indices()

    def total_ativos(self) -> int:
        return len(self._equipamentos)

    def total_vulnerabilidades(self) -> int:
        return sum(len(equipamento.vulnerabilidades) for equipamento in self._equipamentos)

    def listar(self) -> list[Equipamento]:
        return list(self._equipamentos)

    def obter_por_id(self, ativo_id_value: str | int) -> Equipamento:
        ativo_id = self._normalizar_ativo_id(ativo_id_value)
        equipamento = self._por_id.get(ativo_id)
        if equipamento is None:
            raise ErroValidacao("Ativo nao encontrado para o identificador informado.")
        return equipamento

    def obter_por_hostname(self, hostname_value: str) -> Equipamento:
        hostname = self._normalizar_texto(hostname_value, "Hostname")
        equipamento = self._por_hostname.get(hostname.lower())
        if equipamento is None:
            raise ErroValidacao("Ativo nao encontrado para o hostname informado.")
        return equipamento

    def cadastrar(
        self,
        ativo_id_value: str | int,
        hostname_value: str,
        responsavel_value: str,
        setor_value: str,
        tipo_value: str | int,
        descricao_value: str = "",
    ) -> Equipamento:
        ativo_id = self._normalizar_ativo_id(ativo_id_value)
        if ativo_id in self._por_id:
            raise ErroValidacao("Ja existe um ativo com esse identificador.")

        hostname = self._normalizar_texto(hostname_value, "Hostname")
        if hostname.lower() in self._por_hostname:
            raise ErroValidacao("Ja existe um ativo com esse hostname.")

        tipo = self._normalizar_tipo(tipo_value)
        equipamento = EquipamentoFactory.criar(
            tipo,
            id=ativo_id,
            hostname=hostname,
            responsavel=self._normalizar_texto(responsavel_value, "Responsavel"),
            setor=self._normalizar_texto(setor_value, "Setor ou localizacao"),
            descricao=self._normalizar_texto(descricao_value, "Descricao", required=False),
        )
        equipamento.validar()
        self._equipamentos.append(equipamento)
        self.reconstruir_indices()
        self.salvar()
        return equipamento

    def atualizar(
        self,
        ativo_id_value: str | int,
        hostname_value: str,
        responsavel_value: str,
        setor_value: str,
        tipo_value: str | int,
        descricao_value: str = "",
    ) -> Equipamento:
        ativo_id = self._normalizar_ativo_id(ativo_id_value)
        if ativo_id not in self._por_id:
            raise ErroValidacao("Nao existe ativo cadastrado com esse identificador.")

        hostname = self._normalizar_texto(hostname_value, "Hostname")
        existente_hostname = self._por_hostname.get(hostname.lower())
        if existente_hostname is not None and existente_hostname.id != ativo_id:
            raise ErroValidacao("Ja existe outro ativo com esse hostname.")

        tipo_codigo = self._normalizar_tipo(tipo_value)
        dados = self._por_id[ativo_id].to_dict()
        dados.update(
            {
                "id": ativo_id,
                "hostname": hostname,
                "responsavel": self._normalizar_texto(responsavel_value, "Responsavel"),
                "setor": self._normalizar_texto(setor_value, "Setor ou localizacao"),
                "tipo": tipo_codigo,
                "descricao": self._normalizar_texto(
                    descricao_value, "Descricao", required=False
                ),
            }
        )

        equipamento = EquipamentoFactory.from_dict(dados)
        equipamento.validar()

        for indice, atual in enumerate(self._equipamentos):
            if atual.id == ativo_id:
                self._equipamentos[indice] = equipamento
                break
        else:
            raise ErroValidacao("Nenhum ativo foi atualizado.")

        self.reconstruir_indices()
        self.salvar()
        return equipamento

    def remover(self, ativo_id_value: str | int) -> Equipamento:
        ativo_id = self._normalizar_ativo_id(ativo_id_value)
        equipamento = self._por_id.get(ativo_id)
        if equipamento is None:
            raise ErroValidacao("Nao existe ativo cadastrado com esse identificador.")

        self._equipamentos = [
            atual for atual in self._equipamentos if atual.id != ativo_id
        ]
        self.reconstruir_indices()
        self.salvar()
        return equipamento

    def _proximo_id_vulnerabilidade(self) -> int:
        maximo = 0
        for equipamento in self._equipamentos:
            for vulnerabilidade in equipamento.vulnerabilidades:
                maximo = max(maximo, vulnerabilidade.id)
        return maximo + 1

    def adicionar_vulnerabilidade(
        self,
        ativo_id_value: str | int,
        descricao_value: str,
        categoria_value: str,
        severidade_value: str | int,
        status_value: str | int,
    ) -> Vulnerabilidade:
        ativo_id = self._normalizar_ativo_id(ativo_id_value)
        equipamento = self._por_id.get(ativo_id)
        if equipamento is None:
            raise ErroValidacao("Nao existe ativo cadastrado com esse identificador.")

        vulnerabilidade = Vulnerabilidade(
            id=self._proximo_id_vulnerabilidade(),
            descricao=descricao_value,
            categoria=categoria_value,
            severidade=Vulnerabilidade._resolver_severidade(severidade_value),
            status=Vulnerabilidade._resolver_status(status_value),
        )
        equipamento.adicionar_vulnerabilidade(vulnerabilidade)
        self.salvar()
        return vulnerabilidade

    @staticmethod
    def _normalizar_ativo_id(value: str | int) -> int:
        try:
            ativo_id = int(str(value).strip())
        except ValueError as exc:
            raise ErroValidacao(
                "O identificador do ativo deve ser um numero inteiro."
            ) from exc

        if ativo_id <= 0:
            raise ErroValidacao("O identificador do ativo deve ser maior que zero.")

        return ativo_id

    @staticmethod
    def _normalizar_tipo(value: str | int) -> TipoAtivo:
        try:
            tipo_codigo = int(str(value).strip())
        except ValueError as exc:
            raise ErroValidacao(
                "O tipo de ativo deve ser informado pelo codigo numerico."
            ) from exc

        tipo = TIPOS_ATIVO_POR_CODIGO.get(tipo_codigo)
        if tipo is None:
            raise ErroValidacao("Tipo de ativo invalido.")

        return tipo

    @staticmethod
    def _normalizar_texto(value: str, field_name: str, required: bool = True) -> str:
        text = value.strip()
        if required and not text:
            raise ErroValidacao(f"{field_name} nao pode ficar vazio.")
        return text
