# python-mysql-crud-manager
Sistema simples de gerenciamento de registros desenvolvido em Python com integração direta ao MySQL. A aplicação permite o ciclo completo de manipulação de dados (CRUD).

1.Pré-requisitos:

Python 3.x instalado.
Servidor MySQL rodando.
Bibliotecas necessárias (instale via terminal):

pip install -r requirements.txt

2.Configuração do Banco:

Execute o script database.sql no seu console MySQL para criar o banco db_loja e a tabela produtos.

3.Configuração de Segurança:

Crie um arquivo chamado .env na raiz do projeto.

Adicione suas credenciais:

HOST = localhost
USER = seu_usuario
PASSWORD = sua_senha
DATABASE = db_loja

Desafios Técnicos:

Integração de Driver: Durante o desenvolvimento, enfrentei um erro de incompatibilidade de tipos (Could not process parameters: int) ao passar variáveis inteiras para o driver MySQL.

Resolução: Realizei o debugging da comunicação entre o Python e o banco, optando pela atualização do driver (mysql-connector-python v9.6.0) e ajustando a passagem de parâmetros via tuplas estruturadas (valor,), o que garantiu a estabilidade e a segurança da aplicação.
