lfc database

CREATE TABLE public.roles
(
    id varchar(50) PRIMARY KEY,
	role varchar(30)
);

CREATE TABLE public.users
(
    id varchar(50) PRIMARY KEY,
	name varchar(50),
    username varchar(50),
	password varchar(50)
);

CREATE TABLE public.userroles
(
    id varchar(50) PRIMARY KEY,
    userid varchar(50),
	roleid varchar(50)
);

INSERT INTO roles (
	id , role) 
	VALUES ('9b44a1da45d14bf190775a8a1c218a86',	'USER'),
		   ('a83618b2915447688156f1106b7be702',	'ADMIN');
		  
INSERT INTO users (
	id , name, username, password) 
	VALUES ('b83618b2915447688156f1106b7be703',	'Кузьма', 'Administrator', 'Administrator');
	
INSERT INTO userroles (
	id , userid, roleid) 
	VALUES ('9a55a1da45d14bf190775a8a1c218a86',	'b83618b2915447688156f1106b7be703', 'a83618b2915447688156f1106b7be702');	


CREATE TABLE public.words
(
    id varchar(50) PRIMARY KEY,
	title varchar(50),
    dataofexp timestamp
	userid VARCHAR REFERENCES users(id)
);

