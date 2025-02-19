create database projetoAutomoveis;
use projetoAutomoveis;

create table usuarios(
id_usuario int auto_increment primary key,
email_usuario varchar(120) unique not null,
pass_usuario varchar(300) not null,
verificado datetime
);

create table enderecos(
id int auto_increment primary key,
rua varchar(50),
nmr int,
latitude varchar(50),
longitude varchar(50)
);

