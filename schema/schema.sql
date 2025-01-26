create database soulscan;

create table user(
    id int primary key,
    name varchar(100) ,
    password varchar(100)
);

create table mst_dates(
    id int primary key,
    notdate date unique
);

create table result(
    id int primary key,
    user_id int references user(id),
    gad_result int ,
    phq_result int 
);

create table journal(
    id int primary key,
    user_id int references user(id),
    mst_dates_id int references mst_dates(id),
    text varchar(200)
);
