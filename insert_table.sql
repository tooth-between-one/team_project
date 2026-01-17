use cardb;

-- car_info에 데이터 삽입
INSERT INTO car_info (car_type) VALUES ('승용'), ('승합'), ('화물'), ('특수');

-- fuel_info 데이터 삽입
INSERT INTO fuel_info (fuel_name) VALUES ('CNG'), ('경유'), ('휘발유'), ('하이브리드'), ('기타연료'), ('수소'), ('엘피지');

-- local_info 데이터 삽입
INSERT INTO local_info (local_name) VALUES
('종로구'), ('중구'), ('용산구'), ('성동구'), ('광진구'), 
('동대문구'), ('중랑구'), ('성북구'), ('강북구'), ('도봉구'),
('노원구'), ('은평구'), ('서대문구'), ('마포구'), ('양천구'),
('강서구'), ('구로구'), ('금천구'), ('영등포구'), ('동작구'),
('관악구'), ('서초구'), ('강남구'), ('송파구'), ('강동구');

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

-- SHOW VARIABLES LIKE 'secure_file_priv'; 입력해서 value 값에 해당하는 주소 
-- -> 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads'
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
