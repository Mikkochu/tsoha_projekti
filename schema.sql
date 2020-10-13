
create table restaurant_images
(
    id            serial primary key,
    restaurant_id integer,
    data          bytea
);



create table reviews
(
    id            serial primary key,
    review        text,
    restaurant_id integer,
    grade         integer,
    user_id       integer
);



create table users
(
    id       serial primary key,
    username text,
    password text,
    auth     text
);


create table user_images
(
    id      serial primary key,
    user_id integer,
    data    bytea
);



create table restaurants
(
    id      serial primary key,
    name    text,
    address text,
    intro   text,
    lat     double precision,
    lng     double precision
);



