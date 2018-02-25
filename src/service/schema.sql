create table if not exists users (
  id int primary key, 
  name varchar (255) not null, 
  password varchar(255) not null, 
  fullname varchar(255) not null, 
  age int, 
  token varchar(100) not null unique
);

create table if not exists diary_entries (
  id int primary key, 
  title varchar (255) not null,
  author varchar (255) not null,
  publish_date datetime not null, 
  public boolean not null, 
  text text
);

create table if not exists members (
  name varchar (255) not null
);

