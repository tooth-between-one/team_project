use cardb;

-- reg_info에 데이터를 넣기 위함 임시 스키마 생성
CREATE TABLE reg_tmp (
  reg_date   DATE,
  local_name VARCHAR(20),
  car_type   VARCHAR(10),
  fuel_name  VARCHAR(20),
  car_num    INT
);

-- csv파일을 mysql의 db에 삽입하기 위한 권한 파악 코드 실행
SHOW GLOBAL VARIABLES LIKE 'local_infile';

-- 위 코드 실행 후 value가 off이면 아래 코드 실행 (on이면 실행 필요x)
SET GLOBAL local_infile = 1;

-- 삽입할 데이터의 파일을 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads' 에 넣은 후, 아래 코드 실행
LOAD DATA INFILE 
'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/data.csv'
INTO TABLE reg_tmp
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(reg_date, local_name, fuel_name, car_type, car_num);


-- reg_tmp, local_info, fuel_info, car_info를 조인하여 reg_info에 데이터 삽입
INSERT INTO reg_info (fuel_id, local_id, car_id, reg_date, car_num)
SELECT
    f.fuel_id,
    l.local_id,
    c.car_id,
    r.reg_date,
    r.car_num
FROM reg_tmp r
JOIN local_info l
    ON r.local_name = l.local_name
JOIN fuel_info f
    ON r.fuel_name = f.fuel_name
JOIN car_info c
    ON r.car_type = c.car_type;