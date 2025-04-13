drop database projetoautomoveis;
create database projetoAutomoveis;
use projetoAutomoveis;

create table usuarios(
id_usuario int auto_increment primary key,
email_usuario varchar(120) unique not null,
pass_usuario varchar(300) not null,
verificado datetime,
typeUser int null
);

create table enderecos(
id int auto_increment primary key,
cep char(8),
rua varchar(65),
nmr int,
bairro varchar(40),
cidade varchar(40),
uf char(2),
complemento varchar(200) null,
latitude varchar(50),
longitude varchar(50),
id_usuario int,
foreign key (id_usuario) references usuarios(id_usuario)
);

create table tokens(
id_token varchar(300) unique,
id_user int not null,
dt_cr datetime not null,
usado bool not null,
foreign key(id_user) references usuarios(id_usuario)
);

create table lojas(
id_loja int auto_increment primary key,
cnpj char(14) unique not null,
nomeFantasia varchar(65) not null,
razaoSocial varchar(65) not null,
telefone varchar(20) not null,
celular varchar(20) null,
abertura date not null,
id_usuario int not null,
foreign key(id_usuario) references usuarios(id_usuario)
);

create table clientes(
id_cliente int auto_increment primary key,
cpf char(11) not null unique,
nome varchar(65) not null,
telefone varchar(20) not null,
dtNascimento date not null,
genero int not null,
carro int not null,
id_usuario int not null,
foreign key(id_usuario) references usuarios(id_usuario)
);


create table administradores(
id_adm int auto_increment primary key,
nome varchar(65) not null,
id_usuario int not null,
foreign key(id_usuario) references usuarios(id_usuario)
);

create table produtos(
id_produto int auto_increment primary key,
nome_produto varchar(150),
categoria varchar(50),
img varchar(300)
);

create table produto_loja(
id_produto_loja int auto_increment primary key,
id_produto int,
id_loja int,
foreign key(id_produto) references produtos(id_produto),
foreign key(id_loja) references lojas(id_loja)
);
select * from enderecos;


insert into usuarios (email_usuario,pass_usuario,verificado,typeUser) values("adminColiseu@admin.com","$2b$10$BnWF6mS/AuZp//2B67uMiO8XlbrIZE1pSch7zh04lMptxQdbrXxNq","20250303",1);
update usuarios set typeUser = 1 where id_usuario = 1;
insert into administradores (nome, id_usuario) values ("Pedro", 1);


