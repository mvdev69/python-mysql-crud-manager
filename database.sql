CREATE DATABASE IF NOT EXISTS db_loja;

USE db_loja;

CREATE TABLE IF NOT EXISTS produtos (
    id_produto int auto_increment primary key,
    nome_produto varchar(50) not null,
    preco decimal (10, 2)
);