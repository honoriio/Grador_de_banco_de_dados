# Gerador de Banco de Dados para Testes

Script em Python desenvolvido para gerar e popular um banco SQLite com dados fictícios de transações financeiras, com foco em testes e desenvolvimento do projeto Walleto.

## Sobre o projeto

Este repositório contém uma ferramenta simples para criação e preenchimento de um banco de dados com informações simuladas, permitindo testar funcionalidades que dependem de volume de dados, como:

- listagem de transações
- filtros por categoria e data
- exportação de dados
- dashboards
- validações de desempenho com maior quantidade de registros

## O que o script faz

O script:

- cria as tabelas `usuarios`, `categorias` e `transacoes`
- popula categorias financeiras automaticamente
- cria ou reutiliza um usuário
- gera transações aleatórias com:
  - categoria
  - nome da transação
  - valor
  - tipo (`entrada` ou `saida`)
  - data
  - descrição
- insere a quantidade de transações informada pelo usuário
- exibe progresso da inserção com `tqdm`

## Tecnologias utilizadas

- Python
- SQLite
- tqdm

## Estrutura dos dados gerados

As transações simuladas incluem categorias como:

- Alimentação
- Transporte
- Moradia
- Saúde
- Lazer
- Compras

Os valores são gerados dentro de faixas coerentes para cada categoria, com algumas entradas simulando salário.

## Objetivo

Este projeto foi criado como ferramenta de apoio para testes durante o desenvolvimento do Walleto, ajudando a gerar massa de dados de forma rápida e prática.

## Como executar

1. Clone o repositório:
```bash
git clone https://github.com/honoriio/Grador_de_banco_de_dados.git
