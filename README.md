# Arquitetura e Construção do Projeto WhatsApp AI
O projeto consiste em uma aplicação web de inteligência artificial voltada para a análise automatizada de casos jurídicos recebidos via webhooks de mensagens. A solução foi estruturada com uma arquitetura moderna baseada em microrcontainers, priorizando o processamento assíncrono e a separação de responsabilidades.

## 1. Tecnologias Utilizadas
Backend & API: Python com FastAPI, escolhido pela sua alta performance, validação automática de dados via Pydantic e documentação interativa integrada.

Processamento Assíncrono & Filas: Celery em conjunto com Redis, permitindo o manuseio de tarefas em segundo plano (background tasks) para garantir que o recebimento de webhooks não cause gargalos na aplicação.

Banco de Dados & ORM: SQLAlchemy para o mapeamento objeto-relacional (ORM) e gerenciamento de persistência de dados.

Orquestração de Ambiente: Docker e Docker Compose, garantindo que todos os serviços (API, worker de tarefas e broker) rodem em ambientes isolados, consistentes e fáceis de subir.

Frontend: Interface leve em HTML/CSS/JavaScript servida diretamente pela própria API através de arquivos estáticos (StaticFiles), integrada por meio de rotas parametrizadas e estilização moderna.

## 2. Resumo da Construção
Estruturação Modular: O projeto foi organizado separando a camada de rotas/serviços web, os modelos de banco de dados e as tarefas assíncronas do Celery.

Integração de Webhooks: Desenvolvimento de endpoints robustos (/webhook/whatsapp) capazes de interceptar cargas úteis de mensagens, extrair o conteúdo textual de forma segura e acionar análises automatizadas de IA.

Resolução de Conflitos de Ambiente: Durante o desenvolvimento, ajustou-se o mapeamento de diretórios do Uvicorn e o fluxo de build do Docker Compose para garantir a recarga em tempo real (live reload) e a perfeita execução dos scripts Python sem erros de sintaxe ou de importação de módulos.
