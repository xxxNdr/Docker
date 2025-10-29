drop database if exists negozio;
create database negozio;
use negozio;

create table users(
id int auto_increment primary key,
nome varchar(100) not null,
password int not null
);

create table prodotti(
id int auto_increment primary key,
nome varchar(50) not null,
descrizione varchar(255),
prezzo decimal(7,2)
);

create table carrello(
id int auto_increment primary key,
idp int not null,
quantita int,
foreign key (idp) references prodotti(id)
);

-- INSERIMENTO PRODOTTI
insert into prodotti values (default,'cotoletta', 'buonissima e croccantissima', 4.12),
(default, 'tofu','molto umami', 5.61),
(default,'acqua', 'sottomarca', 0.17),
(default, 'padella','antiaderente', 12.99);

-- insert into carrello values (default,1,10),(default,2,8);

-- VEDI TABELLA
select * from carrello;
select * from prodotti;
select * from users;

-- MODIFICA TABELLA
truncate carrello;
truncate prodotti;
delete from prodotti where id > 0;
drop table carrello;
drop table prodotti;