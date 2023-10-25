create database ATM;

use ATM;

create table users(
VCN INT,
PHN CHAR(10),
PIN CHAR(4) UNIQUE NOT NULL,
PRIMARY KEY(VCN, PHN));
