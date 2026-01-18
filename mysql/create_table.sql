-- (auto_increment 설정 위해) 기존 테이블 삭제 후 재생성

USE cardb;

-- 기존 테이블 삭제 (FK 순서 고려)
DROP TABLE IF EXISTS reg_info;
DROP TABLE IF EXISTS car_info;
DROP TABLE IF EXISTS fuel_info;
DROP TABLE IF EXISTS local_info;


-- car_info
CREATE TABLE car_info
(
  car_id   INT AUTO_INCREMENT PRIMARY KEY,
  car_type VARCHAR(10) NOT NULL
);


-- fuel_info
CREATE TABLE fuel_info
(
  fuel_id   INT AUTO_INCREMENT PRIMARY KEY,
  fuel_name VARCHAR(20) NOT NULL
);


-- local_info
CREATE TABLE local_info
(
  local_id   INT AUTO_INCREMENT PRIMARY KEY,
  local_name VARCHAR(20) NOT NULL
);


-- reg_info
CREATE TABLE reg_info
(
  reg_id   INT AUTO_INCREMENT PRIMARY KEY,
  fuel_id  INT NOT NULL,
  local_id INT NOT NULL,
  car_id   INT NOT NULL,
  reg_date DATE NOT NULL,
  car_num  INT NULL,

  CONSTRAINT FK_reg_fuel
    FOREIGN KEY (fuel_id)
    REFERENCES fuel_info (fuel_id),

  CONSTRAINT FK_reg_local
    FOREIGN KEY (local_id)
    REFERENCES local_info (local_id),

  CONSTRAINT FK_reg_car
    FOREIGN KEY (car_id)
    REFERENCES car_info (car_id)
);
