# Trabalho 2 — Inventário de Ativos e Vulnerabilidades

Segunda atividade avaliativa da disciplina de Cibersegurança (UFU).

Este repositório é a evolução em orientação a objetos do Trabalho 1: mesma ideia de inventário de ativos e vulnerabilidades, com persistência em JSON e execução em container Docker.

**Status:** em desenvolvimento (Fase 5 concluída — menu CLI com CRUD de ativos e vulnerabilidades; exportação na Fase 7; Docker na Fase 6).

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

|  Opção  |                   Função                                |
|---------|---------------------------------------------------------|
|    1    | Cadastrar ativo (+ vulnerabilidades iniciais opcionais) |
|    2    | Buscar ativo (por ID ou hostname)                       |
|    3    | Listar ativos                                           |
|    4    | Atualizar ativo                                         |
|    5    | Remover ativo                                           |
|    6    | Cadastrar vulnerabilidade                               |
|    7    | Visualizar vulnerabilidades                             |
|    0    | Sair                                                    |

A opção 8 (exportação de inventário) será habilitada na Fase 7.

Os dados são persistidos em `data/inventario.json` (array JSON) após cada operação de cadastro, atualização, remoção ou registro de vulnerabilidade.

Variável de ambiente opcional para alterar o caminho do inventário:

```bash
INVENTARIO_JSON_PATH=/caminho/inventario.json python3 -m src.main
```

## Repositório

- GitHub: `https://github.com/gusmartinscyber/Trabalho2.git`
