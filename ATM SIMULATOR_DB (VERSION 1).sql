create database ATM;

use ATM;

create table users(
VCN INT PRIMARY KEY,
PHN CHAR(10) UNIQUE NOT NULL,
PIN CHAR(4) NOT NULL,
BALANCE float(2));
