CREATE DATABASE IF NOT EXISTS db_loja;

USE db_loja;

CREATE TABLE IF NOT EXISTS produtos (
    id_produto int auto_increment primary key,
    nome_produto varchar(50) not null,
    preco decimal (10, 2)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id int auto_increment primary key,
    usuario varchar(50) not null unique,
    senha varchar(50) not null
    nivel_acesso enum('admin', 'funcionario') default 'funcionario'
)

insert into usuarios (usuario, senha, nivel_acesso) values ('admin', 'admin123', 'admin');