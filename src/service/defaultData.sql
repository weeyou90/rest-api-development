insert into members (name) values ('LAU Wee You');
insert into members (name) values ('LEE Zi Shan');
insert into members (name) values ('SIA Wei Kiat Jason');
insert into members (name) values ('ZHOU Zhi Zhong');
-- sample adding into database

insert into users (username, fullname, salt, hashed_password, age) values ('admin', 'admin', 'salt', 'hashed_password', 20);
insert into diary_entries (title, author, published_date, public, text) values ('admin first post', 'admin', '20180220T155300+0800', 0, 'admin rubbish text post'); 
--iso 8601 with timezone yyyymmddThhmmss+|-hhmm
--datetime format are store as text in sqlite
--boolean value store as integer 0: false, 1: true

