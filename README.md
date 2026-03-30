# Lab-BDD

## Visão geral

O Lab-BDD é um MVP de livraria focado em busca de livros, consulta de estoque por unidade, reserva e geração de QR Code para retirada.

A proposta do projeto é oferecer uma experiência simples para o usuário encontrar um livro, verificar onde ele está disponível e reservar um exemplar de forma rápida.

Atualmente, o projeto conta com:

- uma base lógica em Python;
- um frontend em HTML, CSS e JavaScript;
- uma integração via Flask para comunicação entre a interface e a lógica de negócio.

---

## Objetivo do projeto

Permitir que um usuário:

1. pesquise um livro por título, autor ou editora;
2. veja os resultados em uma apresentação clara e visual;
3. consulte em quais unidades o livro está disponível;
4. escolha uma unidade específica;
5. realize a reserva;
6. receba um QR Code simples como confirmação da reserva.

---

## Escopo do MVP

### O que o sistema já contempla
- Busca de livros por termo livre.
- Listagem de unidades com estoque disponível.
- Consulta de estoque por unidade.
- Criação de reservas.
- Geração de QR Code mínimo em formato textual.
- Interface frontend simples para navegação e reserva.

### O que ainda não está pronto
- Persistência em banco real.
- Login de usuário.
- Controle de retirada/devolução.
- Integração com API externa.
- Geração de QR Code visual real.
- Atualização automática do estoque após reserva.

---

## Arquivos principais

### livraria_app/dados.py
Contém o banco mockado do MVP:
- lista de livros;
- estoque por loja;
- lista de reservas.

### livraria_app/busca.py
Contém as regras de negócio do sistema:
- busca de livros;
- listagem de unidades disponíveis;
- consulta de estoque;
- realização de reserva;
- geração de QR Code textual.

### livraria_app/teste_busca.py
Contém testes simples para validar:
- busca por título;
- busca por autor;
- busca por editora;
- comportamento para termo vazio;
- estoque por unidade;
- reserva;
- QR Code.

### livraria_app/main.py
Ponto de entrada do backend. Expõe a lógica do sistema por meio de uma aplicação Flask e serve o frontend.

### frontend/index.html
Estrutura principal da interface.

### frontend/styles.css
Estilização da aplicação.

### frontend/app.js
Lógica de interação com a interface e consumo dos endpoints do backend.

---

## Regras do domínio

### Busca
A busca deve aceitar qualquer termo e retornar livros que contenham o texto informado em:
- título;
- autor;
- editora.

Se a busca estiver vazia, o comportamento esperado é retornar erro.

### Estoque
Cada livro possui um dicionário de estoque por unidade, por exemplo:

{
    "Loja Centro": 3,
    "Loja Norte": 0,
    "Loja Sul": 5
}

### Unidades disponíveis
A lista de unidades deve exibir apenas as lojas com quantidade maior que zero, priorizando as de maior estoque.

### Reserva
Ao reservar um livro, o sistema registra:
- livro_id
- unidade
- status
- usuario (opcional)
- data (opcional)
- qr_code

### QR Code
No MVP, o QR Code é representado por uma string no formato:

RESERVA-{livro_id}-{unidade}

Exemplo:
RESERVA-1-LOJACENTRO

---

## Base de dados mockada

O projeto trabalha atualmente com três livros fictícios para fins de teste e demonstração:

- Harry Potter e a Pedra Filosofal — J.K. Rowling — Rocco
- O Senhor dos Anéis — J.R.R. Tolkien — Martins Fontes
- Dom Casmurro — Machado de Assis — Globo

Cada livro possui estoque distribuído entre:
- Loja Centro
- Loja Norte
- Loja Sul

---

## Jornada principal do usuário

### Fluxo esperado
1. O usuário entra na página inicial.
2. Digita um termo na barra de busca.
3. O sistema exibe os livros encontrados.
4. O usuário abre um livro específico.
5. O sistema mostra as unidades disponíveis.
6. O usuário escolhe uma unidade.
7. O sistema confirma a reserva.
8. O QR Code é exibido como comprovante.

---

## Como executar o projeto

### Pré-requisitos
- Python 3.10 ou superior;
- pip instalado;
- navegador moderno.

### 1. Criar e ativar um ambiente virtual

No diretório raiz do projeto:

python -m venv .venv

Ativação no Windows:

.venv\Scripts\activate

Ativação no Linux/macOS:

source .venv/bin/activate

### 2. Instalar a dependência do backend

O backend utiliza Flask.

pip install flask

Se preferir, você pode registrar a dependência em um arquivo requirements.txt e instalar com:

pip install -r requirements.txt

### 3. Iniciar o servidor

Execute o backend a partir da pasta raiz do projeto:

python livraria_app/main.py

O servidor será iniciado em:

http://127.0.0.1:5000

### 4. Abrir a aplicação

Acesse no navegador:

http://127.0.0.1:5000

O backend serve automaticamente o frontend localizado na pasta frontend/.

---

## Como executar os testes

Para validar a lógica de negócio:

python -m pytest

Se o pytest ainda não estiver instalado:

pip install pytest

Os testes cobrem:
- busca por título;
- busca por autor;
- busca por editora;
- comportamento para termo vazio;
- estoque por unidade;
- reserva;
- QR Code.

---

## Endpoints da aplicação

A aplicação expõe os seguintes endpoints:

### GET /
Retorna o frontend principal.

### GET /api/livros?termo=...
Busca livros por termo.

Exemplo:
/api/livros?termo=harry

Resposta esperada:
- lista de livros encontrados;
- total de resultados.

### GET /api/livros/<id>/unidades
Retorna as unidades com estoque disponível para um livro específico.

Exemplo:
/api/livros/1/unidades

### POST /api/reservas
Realiza a reserva de um livro em uma unidade.

Exemplo de corpo da requisição:

{
  "livro_id": 1,
  "unidade": "Loja Centro",
  "usuario": "Enzo",
  "data": "2026-03-29"
}

---

## Frontend

O frontend foi construído com foco em:
- clareza;
- organização;
- leitura rápida;
- navegação simples;
- boa apresentação dos resultados.

### Componentes principais
- Header: identidade da aplicação;
- SearchBar: campo principal de busca;
- BookGrid: listagem dos resultados;
- BookCard: exibição individual de cada livro;
- StoreModal: unidades disponíveis;
- ReservationPanel: confirmação da reserva;
- SuccessScreen: finalização com QR Code.

---

## Direção visual

O frontend deve transmitir:
- clareza;
- organização;
- confiança;
- leitura rápida;
- aspecto moderno e amigável.

### Estilo recomendado
- Layout limpo, com bastante espaço em branco.
- Tipografia forte para títulos e neutra para descrições.
- Cartões bem definidos para exibir livros.
- Botões destacados para ações principais.
- Feedback visual evidente para disponibilidade, erro e confirmação.

---

## Melhorias futuras

Depois do MVP, o sistema pode evoluir com:
- autenticação de usuário;
- banco de dados real;
- histórico de reservas;
- cancelamento de reserva;
- atualização automática do estoque;
- QR Code visual gerado por biblioteca externa;
- filtros avançados por gênero, autor e editora;
- favoritos e lista de desejos;
- layout responsivo para celular.

---

## Critérios de aceitação do MVP

O projeto pode ser considerado funcional quando o usuário conseguir:

- pesquisar livros;
- visualizar resultados;
- consultar unidades disponíveis;
- reservar um livro;
- visualizar um QR Code de confirmação.

---

## Observação final

Este projeto foi pensado como um MVP didático e evolutivo.

A prioridade agora é transformar a lógica existente em uma interface clara, bonita e fácil de usar, mantendo o fluxo simples e direto para o usuário.

## Estrutura atual do repositório

```text
Lab-BDD/
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── livraria_app/
│   ├── busca.py
│   ├── dados.py
│   ├── main.py
│   └── teste_busca.py
├── .gitignore
├── .gitattributes
└── README.md

