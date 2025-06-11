# Sistema de Gestão - Mercado Livre

Este é um sistema de gestão inspirado no Mercado Livre, desenvolvido em Python, que permite gerenciar usuários, vendedores, produtos e compras. O sistema suporta múltiplos bancos de dados (MongoDB e Cassandra) para persistência de dados e Redis para cache/sessões.

## Funcionalidades

- 🏪 **Área de Clientes**: Gerenciamento de usuários cadastrados
- 📦 **Área de Produtos**: Controle de inventário e catálogo
- 👥 **Área de Vendedores**: Gestão de vendedores da plataforma
- 🛒 **Área de Compras**: Controle de transações e pedidos
- 🔐 **Sistema de Autenticação**: Login administrativo para acesso ao sistema
- 🗄️ **Suporte Multi-Database**: Alternância entre MongoDB e Cassandra em tempo de execução

## Pré-requisitos

- Python 3.8 ou superior
- Docker e Docker Compose
- Git

## Configuração do Ambiente

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd ml-mongo
```

### 2. Crie um ambiente virtual

```bash
python3 -m venv .venv
```

### 3. Ative o ambiente virtual

**Linux/Mac:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

### 4. Instale as dependências do projeto

```bash
pip install -r requirements.txt
```

### 5. Suba os containers dos bancos de dados

```bash
docker compose up -d
```

Isso iniciará os seguintes serviços:
- MongoDB (porta 27017)
- Redis (porta 6379)
- Cassandra (porta 9042)

## Executando a Aplicação

```bash
python3 src/main.py
```

## Credenciais de Acesso

Para acessar o sistema administrativo, utilize as seguintes credenciais:

- **Email**: `admin@gmail.com`
- **Senha**: `admin123`

> ⚠️ **Importante**: Estas credenciais estão definidas no arquivo `src/commands/command.py` e devem ser alteradas em ambiente de produção.

## Configuração dos Bancos de Dados

### MongoDB
- **Host**: localhost
- **Porta**: 27017
- **Usuário**: admin
- **Senha**: root

### Cassandra
- **Host**: localhost
- **Porta**: 9042
- **Usuário**: admin
- **Senha**: root
- **Cluster**: MercadoLivreCluster

### Redis
- **Host**: localhost
- **Porta**: 6379

## Seleção de Banco de Dados

O sistema permite alternar entre MongoDB e Cassandra através do menu principal da aplicação. Para trocar o banco de dados:

1. Execute a aplicação
2. Faça login com as credenciais administrativas
3. Selecione a opção "5 - Selecionar banco de dados"
4. Escolha entre MongoDB ou Cassandra

A seleção ficará ativa durante toda a sessão da aplicação.

## Estrutura do Projeto

```
src/
├── commands/          # Comandos da aplicação
│   ├── users/         # Comandos relacionados a usuários
│   ├── sellers/       # Comandos relacionados a vendedores
│   ├── products/      # Comandos relacionados a produtos
│   ├── purchases/     # Comandos relacionados a compras
│   └── database/      # Comandos de banco de dados
├── entities/          # Modelos de dados
├── repositories/      # Camada de acesso a dados
│   ├── mongodb/       # Implementação para MongoDB
│   ├── cassandra/     # Implementação para Cassandra
│   └── redis/         # Implementação para Redis
├── validators/        # Validadores de entrada
├── formatters/        # Formatadores de saída
├── utils/             # Utilitários gerais
└── main.py           # Ponto de entrada da aplicação
```
