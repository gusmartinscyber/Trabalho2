# Trabalho 2 — Inventário de Ativos e Vulnerabilidades

Segunda atividade avaliativa da disciplina de Cibersegurança (UFU).

Este repositório é a evolução em orientação a objetos do Trabalho 1: mesma ideia de inventário de ativos e vulnerabilidades, com persistência em JSON e execução em container Docker.

**Status:** Fases 1–7 concluídas.

## Requisitos

- Python 3.12 ou superior
- `pip` (geralmente incluso no Python)

## Ambiente virtual

Clone o repositório e entre na pasta criada (por padrão `Trabalho2/`):

```bash
git clone https://github.com/gusmartinscyber/Trabalho2.git
cd Trabalho2
```

Na **raiz do repositório** (onde ficam `README.md`, `requirements.txt` e `src/`):

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

A pasta `venv/` está no `.gitignore` e não deve ser commitada.

Para desativar o ambiente:

```bash
deactivate
```

## Execução

Com o `venv` ativado, na raiz do repositório:

```bash
python3 -m src.main
```

A aplicação exibe o painel de inicialização (Rich) e o **menu interativo** para gerenciar ativos e vulnerabilidades:

| Opção |                      Função                             |
|-------|---------------------------------------------------------|
|   1   | Cadastrar ativo (+ vulnerabilidades iniciais opcionais) |
|   2   | Buscar ativo (por ID ou hostname)                       |
|   3   | Listar ativos                                           |
|   4   | Atualizar ativo                                         |
|   5   | Remover ativo                                           |
|   6   | Cadastrar vulnerabilidade                               |
|   7   | Visualizar vulnerabilidades                             |
|   8   | Exportar inventário (relatório `.txt`)                  |
|   0   | Sair                                                    |

Os dados são persistidos em `data/inventario.json` (array JSON) após cada operação de cadastro, atualização, remoção ou registro de vulnerabilidade.

### Exportação textual (opção 8)

A opção 8 gera `data/inventario.txt` — relatório legível derivado do estado atual do inventário. O arquivo é **gitignored** e **não** substitui o JSON como fonte de verdade; use o menu 8 quando precisar do relatório.

Variável de ambiente opcional para alterar o caminho do inventário JSON (o `.txt` é gerado no mesmo diretório):

```bash
INVENTARIO_JSON_PATH=/caminho/inventario.json python3 -m src.main
```

## Docker

Pré-requisitos: Docker e Docker Compose instalados.

Na raiz do repositório:

```bash
docker compose build
docker compose up -d
```

Verificar se o container está em execução:

```bash
docker compose ps
```

Para usar o menu interativo dentro do container:

```bash
docker exec -it trabalho2-inventario python -m src.main
```

Os dados são persistidos em `./data/inventario.json` no host (volume montado em `/app/data`).

Para reiniciar o container mantendo os dados:

```bash
docker compose restart
```

Para encerrar:

```bash
docker compose down
```

O container usa `restart: unless-stopped` e um loop no `entrypoint.sh` para permanecer em execução por pelo menos 24 horas no servidor do docente. O deploy no servidor deve ser feito com `docker compose up -d` em modo detached.

## Repositório

- GitHub: `https://github.com/gusmartinscyber/Trabalho2.git`
