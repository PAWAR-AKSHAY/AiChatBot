The .dump Command
You can use .dump dot command to export complete database in a text file using the following SQLite command at the command prompt.

$sqlite3 aidb.db .dump > aidb.sql

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE statistics(uid integer references user_register1(id) on update set null on delete cascade,que_cnt integer);
CREATE TABLE IF NOT EXISTS "user_register1" (
	"id"	integer PRIMARY KEY AUTOINCREMENT,
	"fname"	text,
	"lname"	text,
	"email"	text,
	"pwd"	text,
	"que_cnt"	INTEGER,
	"date"	NUMERIC
);
INSERT INTO user_register1 VALUES(2,'akshay','pawar','akshay@gmail.com','password',88,'2019-04-10');
INSERT INTO user_register1 VALUES(3,'Shreyas','Mahajan','shreyas44@gmail.com','password',21,'2019-04-10');
INSERT INTO user_register1 VALUES(4,'Sharoo','Deshmukh','sharoo45@gmail.com','password',15,'2019-04-10');
INSERT INTO user_register1 VALUES(5,'Shefali','Bhavekar','shefali34@gmail.com','password',27,'2019-04-10');
INSERT INTO user_register1 VALUES(6,'Gaurav','Joshi','gjoshi46@gmail.com','password',1,'2019-04-10');
INSERT INTO user_register1 VALUES(7,'sanket','bhagane','sanket@gmail.com','password',7,'2019-04-12');
INSERT INTO user_register1 VALUES(8,'rohan','chaughule','rohan@gmail.com','password',0,NULL);
INSERT INTO user_register1 VALUES(9,'JayBhai','Vyas','jay@gmail.com','password',1,NULL);
INSERT INTO user_register1 VALUES(10,'viraj','holmukhe','viraj@gmail.com','password',1,'2019-04-10');
INSERT INTO user_register1 VALUES(17,'siddhesh','kand','siddheshkand123@gmail.com','password',13,'2019-04-09');
INSERT INTO user_register1 VALUES(18,'Pranali','Margaj','pranali@gmail.com','qwertyuiop',6,'2019-04-10');
INSERT INTO user_register1 VALUES(19,'kalyani','wani','kwani5041@gmail.com','123456',7,'2019-04-12');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('user_register1',19);
COMMIT;
