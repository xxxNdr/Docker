drop database if exists `21_10_2025`;

create database `21_10_2025`;
use `21_10_2025`;

create table users(
cf varchar(16),
nome varchar(25),
cognome varchar(25)
);

insert into users values
('bttmrc', 'mirco', 'botti'),
('lrnmch', 'michele', 'lorenzoni');
