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
('109','Chinese','Chen');


INSERT INTO teacher VALUES
('10000','骆玉明','100','professor','123456','1-101','13456789101','LYM@fudan.edu.cn');
INSERT INTO teacher VALUES
('10001','段怀清','106','lecturer','123456','2-103','13456789103','DHQ@fudan.edu.cn');
INSERT INTO teacher VALUES
('10002','王东明','109','associate professor','123456','4-103','13452789103','DMW@fudan.edu.cn');
INSERT INTO teacher VALUES
('10003','李祥年','104','associate professor','123456','3-103','134568659103','LXN@fudan.edu.cn');
INSERT INTO teacher VALUES
('10004','戴燕','106','professor','123456','2-203','13456782903','DY@fudan.edu.cn');
INSERT INTO teacher VALUES
('10005','陆力强','101','associate professor','123456','7-103','13456789103','LLQ@fudan.edu.cn');
INSERT INTO teacher VALUES
('10006','王宇芳','101','lecturer','123456','9-103','13456569103','WYF@fudan.edu.cn');
INSERT INTO teacher VALUES
('10007','沈皓','106','professor','123456','8-103','13456569123','SH@fudan.edu.cn');
INSERT INTO teacher VALUES
('10008','何健','107','lecturer','123456','7-103','13456569876','HJ@fudan.edu.cn');
INSERT INTO teacher VALUES
('10009','王向荣','103','lecturer','123456','9-103','13909569103','WXR@fudan.edu.cn');
INSERT INTO teacher VALUES
('10010','杨晓光','108','professor','123456','10-103','13456569103','YXG@fudan.edu.cn');
INSERT INTO teacher VALUES
('10011','叶建楠','105','professor','123456','10-103','13456569103','YJN@fudan.edu.cn');



INSERT INTO student VALUES
('100000000','杨鑫','CS-1','M','G','2015','106','123456');
INSERT INTO student VALUES
('100000001','张彦斌','CS-2','F','S','2014','106','123456');
INSERT INTO student VALUES
('100000002','陈忠民','CS-1','M','G','2015','106','123456');
INSERT INTO student VALUES
('100000003','付杰','HIS-2','F','S','2014','104','123456');
INSERT INTO student VALUES
('100000004','田雪婷','NATH-1','M','G','2015','100','123456');
INSERT INTO student VALUES
('100000005','朱慧敏','PHYS-2','F','S','2014','101','123456');
INSERT INTO student VALUES
('100000006','张奇','PHYS-1','M','G','2015','101','123456');
INSERT INTO student VALUES
('100000007','张静','LAW-2','F','S','2014','108','123456');
INSERT INTO student VALUES
('100000008','吴新明','CHIN-1','M','G','2015','109','123456');
INSERT INTO student VALUES
('100000009','徐慧萍','LAW-2','F','S','2014','108','123456');
INSERT INTO student VALUES
('100000010','梁振国','CS-1','M','G','2015','106','123456');
INSERT INTO student VALUES
('100000011','姚轩','HIS-2','F','S','2014','104','123456');
INSERT INTO student VALUES
('100000012','陈超','CHEM-1','M','G','2015','102','123456');
INSERT INTO student VALUES
('100000013','任国栋','BIOL-2','F','S','2014','103','123456');



INSERT INTO admin_info VALUES
('admin','root');


INSERT INTO course VALUES
('1000000','数据库引论',32,34,'2-209',3,10,4,'10001','106');
INSERT INTO course VALUES
('1000001','数据结构',15,17,'2-207',4,40,3,'10001','106');
INSERT INTO course VALUES
('1000002','中国当代小说选读',50,51,'3-303',2,20,1,'10002','109');
INSERT INTO course VALUES
('1000003','计算机原理',49,51,'2-303',4,20,2,'10004','106');
INSERT INTO course VALUES
('1000004','算法设计与分析',37,39,'1-303',4,10,3,'10004','106');
INSERT INTO course VALUES
('1000005','国际投资法',2,5,'6-303',4,10,4,'10010','108');
INSERT INTO course VALUES
('1000006','刑事政策',6,9,'3-301',5,5,5,'10010','108');
INSERT INTO course VALUES
('1000007','编译原理',60,63,'2-303',4,20,6,'10007','106');
INSERT INTO course VALUES
('1000008','复变函数',27,29,'2-303',4,20,7,'10000','100');
INSERT INTO course VALUES
('1000009','拓扑学',40,42,'2-303',4,20,8,'10000','100');
INSERT INTO course VALUES
('1000010','热力学与统计物理',27,29,'2-303',4,20,1,'10005','101');
INSERT INTO course VALUES
('1000011','固体物理',50,52,'2-303',4,20,2,'10006','101');
INSERT INTO course VALUES
('1000012','计量经济学',55,57,'1-303',4,5,3,'10008','107');
INSERT INTO course VALUES
('1000013','财政学',28,30,'2-303',4,5,4,'10008','107');
INSERT INTO course VALUES
('1000014','中国文学经典',29,31,'1-303',4,5,5,'10002','109');



INSERT INTO selectcourse VALUES
('1000000','100000000');
INSERT INTO selectcourse VALUES
('1000001','100000001');


INSERT INTO textbook VALUES
('1000000','10001','DB system');

INSERT INTO applicationforcourse(sno,cno,reason) VALUES
('100000000','1000001','申请');




