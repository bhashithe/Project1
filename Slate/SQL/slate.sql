\c ckhan3

drop table department cascade;
create table department (
  university varchar(40),
  dname  varchar(40),
  primary key (university,dname)
);
insert into department values ('GSU','CSC');
insert into department values ('GSU','PHYS');

drop table program cascade;
create table program (
  university varchar(40) not null,
  dname    varchar(40) not null,
  program  varchar(10) not null check (program in ('MS','PhD')),
  primary key (university,dname,program),
  foreign key (university,dname) references department
);
insert into program values ('GSU','CSC','MS');
insert into program values ('GSU','CSC','PhD');
insert into program values ('GSU','PHYS','MS');
insert into program values ('GSU','PHYS','PhD');

drop table applicant cascade;
create table applicant (
  aid      serial unique not null check (aid > 999 and aid < 10000),
  email    varchar(40) not null,
  password varchar(20) not null,
  fname    varchar(20) not null,
  lname    varchar(20) not null,
  address1 varchar(40),
  address2 varchar(40),
  city     varchar(40),
  state    varchar(40),
  zip      int,
  GREQ     int,
  GREV     int,
  GREA     numeric(3,1),
  TOEFL    int,
  primary key (email)
);
ALTER sequence applicant_aid_seq RESTART WITH 1000;
insert into applicant(email,password,fname,lname) values
  ('a1@gmail.com','a1','Tony','Romo');
insert into applicant(email,password,fname,lname) values
  ('a2@gmail.com','a2','Michael','Stone');
insert into applicant(email,password,fname,lname) values
  ('a3@gmail.com','a3','John','Jones');
insert into applicant(email,password,fname,lname) values
  ('a4@gmail.com','a4','James','Smith');
update applicant set GREQ=170, GREV=155, GREA=4.5, TOEFL=90 where email='a1@gmail.com';
update applicant set GREQ=150, GREV=145, GREA=2.5, TOEFL=70 where email='a2@gmail.com';

drop table application cascade;
create table application (
  email        varchar(40) not null,
  university   varchar(40) not null,
  dname        varchar(40) not null,
  program      varchar(10) not null check (program in ('MS','PhD')),
  dateOfApp    date not null,
  termOfAdmission   char(2) not null check (termOfAdmission in ('FA','SP','SU')),
  yearOfAdmission int not null check (yearOfAdmission > 1999 and yearOfAdmission < 2100),
  admissionStatus varchar(10) check (admissionStatus in ('ACCEPT','REJECT','PENDING')),
  dataSentToPaws char(3) check (dataSentToPaws in ('Yes','No')),
  primary key (email,university,dname,program),
  foreign key (email) references applicant,
  foreign key (university,dname,program) references program
);
insert into application values
  ('a1@gmail.com','GSU','CSC','MS','2018-12-22','FA',2019,null,null);
insert into application values
  ('a2@gmail.com','GSU','CSC','MS','2018-12-22','FA',2019,null,null);
insert into application values
  ('a3@gmail.com','GSU','CSC','PhD','2018-12-22','FA',2019,null,null);
update application set admissionStatus = 'ACCEPT' where email='a1@gmail.com';
update application set admissionStatus = 'ACCEPT' where email='a2@gmail.com';
update application set admissionStatus = 'PENDING' where email='a3@gmail.com';
