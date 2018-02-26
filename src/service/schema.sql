create table if not exists users (
  id integer primary key not null, 
  name varchar (255) not null, 
  password varchar(255) not null, 
  fullname varchar(255) not null, 
  age int, 
  token varchar(100) not null
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

create table if not exists user_tokens(
  id integer primary key not null, 
  token varchar(100) not null,
  --hashed varchar(100) not null,
  expired_at datetime,
  created_at  default current_timestamp,
  --constraint UNQ_0 unique (hashed),
  constraint user_id FOREIGN KEY (id) references users(id) ON update CASCADE ON delete CASCADE
);

