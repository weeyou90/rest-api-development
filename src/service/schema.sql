create table if not exists users (
  username varchar (255) not null unique primary key,
  fullname varchar (255) not null,
  salt varchar (255) not null,
  hashed_password varchar (255) not null,
  age int not null 
);

create table if not exists diary_entries (
  id int primary key, 
  title varchar (255) not null,
  author varchar (255) not null,
  publish_date datetime not null, 
  public boolean not null, 
  text: text
);

create table if not exists members {
  name varchar (255) not null
};