-- auto-generated definition
create table restaurant_images
(
    id            serial not null
        constraint pictures_pk
            primary key,
    restaurant_id integer,
    data          bytea
);



-- auto-generated definition
create table reviews
(
    id            serial not null
        constraint reviews_pk
            primary key,
    review        text,
    restaurant_id integer,
    grade         integer,
    user_id       integer
);



-- auto-generated definition
create table users
(
    id       integer default nextval('projekti.users_id_seq'::regclass),
    username text,
    password text,
    auth     text
);


create unique index users_username_uindex
    on users (username);

-- auto-generated definition
create table user_images
(
    id      serial not null
        constraint user_images_pk
            primary key,
    user_id integer,
    data    bytea
);


create unique index user_images_user_id_uindex
    on user_images (user_id);

-- auto-generated definition
create table restaurants
(
    id      serial not null
        constraint restaurants_pk
            primary key,
    name    text,
    address text,
    intro   text,
    lat     double precision,
    lng     double precision
);


create unique index restaurants_name_uindex
    on restaurants (name);

