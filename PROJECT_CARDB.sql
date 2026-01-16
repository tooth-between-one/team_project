-- create user ohgiraffers@'%' identified by 'ohgiraffers';

-- create database cardb;

-- show databases;

-- grant all privileges on cardb.* to ohgiraffers@'%';

-- show grants for ohgiraffers@'%';


use cardb;

CREATE TABLE car_info
(
  car_id   INT          NOT NULL PRIMARY KEY,
  car_type VARCHAR (10) NOT NULL
);

CREATE TABLE fuel_info
(
  fuel_id   INT          NOT NULL PRIMARY KEY,
  fuel_name VARCHAR (20) NOT NULL
);

CREATE TABLE local_info
(
  local_id   INT          NOT NULL PRIMARY KEY,
  local_name VARCHAR (20) NOT NULL
);

CREATE TABLE reg_info
(
  reg_id   INT  NOT NULL,
  fuel_id  INT  NOT NULL,
  local_id INT  NOT NULL,
  car_id   INT  NOT NULL,
  reg_date DATE NOT NULL,
  car_num  INT  NULL    ,
  PRIMARY KEY (reg_id)
);

ALTER TABLE reg_info
  ADD CONSTRAINT FK_fuel_
    FOREIGN KEY (fuel_id)
    REFERENCES fuel_info (fuel_id);

ALTER TABLE reg_info
  ADD CONSTRAINT FK_local
    FOREIGN KEY (local_id)
    REFERENCES local_info (local_id);

ALTER TABLE reg_info
  ADD CONSTRAINT FK_car
    FOREIGN KEY (car_id)
    REFERENCES car_info (car_id);