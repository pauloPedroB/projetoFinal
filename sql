create database projetoAutomoveis;
use projetoAutomoveis;

create table enderecos(
id int auto_increment primary key,
rua varchar(50),
nmr int,
latitude varchar(50),
longitude varchar(50)
);

select * from enderecos;