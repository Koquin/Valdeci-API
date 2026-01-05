# API Vendas Fiado

Sistema de gestao de vendas fiadas com controle de dividas, pagamentos e assinaturas digitais desenvolvido com FastAPI e MongoDB.

## Tecnologias Utilizadas

- Python 3.8+
- FastAPI
- MongoDB
- Motor (driver assincrono para MongoDB)
- Pydantic
- Uvicorn

## Arquitetura

O projeto segue uma arquitetura em camadas:

- **Routers**: Camada de entrada que recebe as requisicoes HTTP
- **Services**: Camada de logica de negocio
- **Repository**: Camada de comunicacao com o banco de dados
- **Models**: Modelos de dados do MongoDB
- **DTOs**: Objetos de transferencia de dados para validacao
- **Exceptions**: Excecoes customizadas para tratamento de erros

## Instalacao

### Pre-requisitos

- Python 3.8 ou superior
- MongoDB instalado e em execucao
- pip (gerenciador de pacotes Python)

### Passos para Instalacao

1. Clone o repositorio:

```bash
git clone <url-do-repositorio>
cd API
```

2. Configure as variaveis de ambiente no arquivo `.env`:

```env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=vendas_fiado
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=True
SECRET_KEY=your-secret-key-here
```

3. Instale as dependencias:

```bash
pip install -r requirements.txt
```

## Execucao

### Windows

Execute o arquivo batch:

```bash
run.bat
```

### Linux/Mac

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

A API estara disponivel em `http://localhost:8000`

## Documentacao da API

Apos iniciar o servidor, acesse a documentacao interativa:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints Principais

### Produtos

- `GET /produtos` - Lista todos os produtos
- `GET /produtos/search?q=texto` - Busca produtos por nome ou codigo de barras
- `GET /produtos/codigo/{codigo}` - Busca produto por codigo de barras
- `POST /produtos` - Cadastra novo produto
- `PUT /produtos/{id}` - Atualiza produto existente
- `DELETE /produtos/{id}` - Exclui produto

### Clientes

- `GET /clientes` - Lista todos os clientes
- `GET /clientes/search?q=texto` - Busca clientes por nome ou CPF
- `POST /clientes` - Cadastra novo cliente

### Compras

- `POST /compras` - Registra compra normal
- `GET /compras/{id}` - Retorna detalhes de uma compra

### Dividas

- `GET /dividas` - Lista clientes com dividas em aberto
- `GET /dividas/search?q=texto` - Busca devedores por nome ou CPF
- `POST /dividas` - Registra compra fiada com assinatura

### Historico

- `GET /historico/{id_divida}` - Retorna historico completo de uma divida
- `POST /historico/pagamento` - Registra pagamento com assinatura

## Estrutura de Diretorios

```
API/
├── app/
│   ├── config/
│   │   └── database.py
│   ├── dtos/
│   │   ├── cliente_dto.py
│   │   ├── compra_dto.py
│   │   ├── divida_dto.py
│   │   ├── historico_dto.py
│   │   └── produto_dto.py
│   ├── exceptions/
│   │   └── custom_exceptions.py
│   ├── models/
│   │   ├── cliente.py
│   │   ├── compra.py
│   │   ├── divida.py
│   │   ├── historico.py
│   │   └── produto.py
│   ├── repository/
│   │   ├── cliente_repository.py
│   │   ├── compra_repository.py
│   │   ├── divida_repository.py
│   │   ├── historico_repository.py
│   │   └── produto_repository.py
│   ├── routers/
│   │   ├── cliente_router.py
│   │   ├── compra_router.py
│   │   ├── divida_router.py
│   │   ├── historico_router.py
│   │   └── produto_router.py
│   └── services/
│       ├── cliente_service.py
│       ├── compra_service.py
│       ├── divida_service.py
│       ├── historico_service.py
│       └── produto_service.py
├── .env
├── .gitignore
├── main.py
├── requirements.txt
└── run.bat
```

## Configuracao do MongoDB

Certifique-se de que o MongoDB esta em execucao antes de iniciar a API. A string de conexao pode ser configurada no arquivo `.env`.

Por padrao, a API tenta se conectar em `mongodb://localhost:27017` e utiliza o banco de dados `vendas_fiado`.

## Tratamento de Erros

A API retorna os seguintes codigos de status HTTP:

- `200` - Sucesso
- `201` - Criado com sucesso
- `204` - Excluido com sucesso (sem conteudo)
- `400` - Requisicao invalida
- `404` - Recurso nao encontrado
- `409` - Conflito (recurso ja existe)
- `500` - Erro interno do servidor

## Logs

Cada metodo da aplicacao gera logs no formato:

```
Using method {nome_do_metodo}, in module {nome_do_arquivo}, with the variables: [{variavel: valor}]
```

Estes logs facilitam o rastreamento de requisicoes e debug da aplicacao.

## Contribuicao

Para contribuir com o projeto:

1. Faca um fork do repositorio
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudancas (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licenca

Este projeto esta sob a licenca MIT.
