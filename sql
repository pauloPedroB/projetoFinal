create database projetoAutomoveis;
use projetoAutomoveis;

create table usuarios(
id_usuario int auto_increment primary key,
email_usuario varchar(120) unique not null,
pass_usuario varchar(300) not null,
verificado datetime
);

select * from usuarios;
create table enderecos(
id int auto_increment primary key,
rua varchar(50),
nmr int,
latitude varchar(50),
longitude varchar(50)
);

create table tokens(
id_token varchar(300) unique,
id_user int not null,
dt_cr datetime not null,
usado bool not null,
foreign key(id_user) references usuarios(id_usuario)
);


