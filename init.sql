CREATE TABLE department(
dno char(10) NOT NULL,
dname char(20) NOT NULL,
leader char(30),
PRIMARY KEY(dno)
);

CREATE TABLE teacher(
tno char(10) NOT NULL,
tname char(30) NOT NULL,
dno char(10) NOT NULL,
prof char(20) NOT NULL,
password char(50) NOT NULL,
office char(50),
tel char(20),
mail char(30),
PRIMARY KEY(tno),
FOREIGN KEY(dno) REFERENCES department(dno)
);

CREATE TABLE student(
sno char(10) NOT NULL,
sname char(30) NOT NULL,
sclass char(20) NOT NULL,
sex char(10) NOT NULL,
education_level char(2) NOT NULL,
attendence_year char(5) NOT NULL,
dno char(10) NOT NULL,
password char(50) NOT NULL,
PRIMARY KEY(sno),
FOREIGN KEY(dno) REFERENCES department(dno)
);

CREATE TABLE admin_info(
username char(10) NOT NULL,
password char(50) NOT NULL
);

CREATE TABLE course(
cno char(10) NOT NULL,
cname char(30) NOT NULL,
begintime INTEGER NOT NULL,
endtime INTEGER NOT NULL,
cplace char(50),
point INTEGER NOT NULL,
limits INTEGER,
term INTEGER,
tno char(10),
dno char(10),
PRIMARY KEY(cno),
FOREIGN KEY(tno) REFERENCES teacher(tno),
FOREIGN KEY(dno) REFERENCES department(dno)
);

CREATE TABLE selectcourse(
cno char(10) NOT NULL,
sno char(10) NOT NULL,
PRIMARY KEY(cno,sno),
FOREIGN KEY(cno) REFERENCES course(cno),
FOREIGN KEY(sno) REFERENCES student(sno)
);

CREATE TABLE textbook(
cno char(10) NOT NULL,
tno char(10) NOT NULL,
bookname char(50),
PRIMARY KEY(cno,tno),
FOREIGN KEY(cno) REFERENCES course(cno),
FOREIGN KEY(tno) REFERENCES teacher(tno)
);

CREATE TABLE applicationforcourse(
sno char(10) NOT NULL,
cno char(10) NOT NULL,
results char(10),
reason varchar(100),
reply varchar(100),
PRIMARY KEY(sno,cno),
FOREIGN KEY(sno) REFERENCES student(sno),
FOREIGN KEY(cno) REFERENCES course(cno)
);

INSERT INTO department VALUES
('100','Maths','Zhao');
INSERT INTO department VALUES
('101','Physics','Qian');
INSERT INTO department VALUES
('102','Chemistry','Sun');
INSERT INTO department VALUES
('103','Biology','Lee');
INSERT INTO department VALUES
('104','History','Zhou');
INSERT INTO department VALUES
('105','Philosophy','Wu');
INSERT INTO department VALUES
('106','Computer Science','Zheng');
INSERT INTO department VALUES
('107','Economics','Wang');
INSERT INTO department VALUES
('108','Law','Feng');
INSERT INTO department VALUES
('109','Psychology','Chen');


INSERT INTO teacher VALUES
('10000','Zhao1','100','professor','123456','1-101','13456789101','Zhao1@fudan.edu.cn');
INSERT INTO teacher VALUES
('10001','Qian1','106','lecturer','123456','2-103','13456789103','Qian1@fudan.edu.cn');


INSERT INTO student VALUES
('100000000','Zhao2','CS-1','M','G','2015','106','123456');
INSERT INTO student VALUES
('100000001','Qian2','HIS-2','F','S','2014','104','123456');


INSERT INTO admin_info VALUES
('admin','root');


INSERT INTO course VALUES
('1000000','Database',32,34,'2-209',3,80,4,'10001','106');
INSERT INTO course VALUES
('1000001','Data Structure',15,17,'2-207',4,40,3,'10001','106');


INSERT INTO selectcourse VALUES
('1000000','100000000');
INSERT INTO selectcourse VALUES
('1000001','100000001');


INSERT INTO textbook VALUES
('1000000','10001','DB system');

INSERT INTO applicationforcourse(sno,cno,reason) VALUES
('100000000','1000001','申请');




