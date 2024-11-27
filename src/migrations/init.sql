create table authors
(
    id bigint auto_increment primary key,
    name         varchar(255) not null,
    stage_name   varchar(255) null,
    birth_date   varchar(255) null,
    death_date   varchar(255) null,
    birth_place  varchar(255) null,
    nationality  varchar(255) null,
    website      varchar(255) null,
    description  text         null,
    image        varchar(255) not null,
    goodreads_id varchar(100) not null,
    uuid         varchar(36)  not null
);

alter table authors
    add unique index uq_authors_id (id),
    add unique index uq_authors_goodreads_id (goodreads_id),
    add unique index uq_authors_uuid (uuid);

create table books
(
    id           bigint auto_increment primary key,
    title        varchar(255) not null,
    publisher    varchar(255) null,
    total_pages  int          null,
    published_at varchar(255) null,
    language     varchar(255) null,
    description  text         null,
    image        varchar(255) null,
    book_link    varchar(255) null,
    goodreads_id varchar(255) not null,
    uuid         varchar(36)  not null
);

alter table books
    add unique index uq_books_id (id),
    add unique index uq_books_goodreads_id (goodreads_id),
    add unique index uq_books_uuid (uuid);


create table genres
(
    id           bigint auto_increment primary key,
    name         varchar(255) null,
    goodreads_id varchar(255) not null,
    uuid         varchar(36)  not null
);

alter table genres
    add unique index uq_genres_id (id),
    add unique index uq_genres_goodreads_id (goodreads_id),
    add unique index uq_genres_uuid (uuid);

create table books_authors
(
    id       bigint auto_increment primary key,
    book_id  bigint not null,
    author_id bigint not null
);

alter table books_authors
    add unique index uq_books_authors_id (id),
    add index idx_books_authors_book_id (book_id),
    add index idx_books_authors_author_id (author_id),
    add constraint fk_books_authors_books_id
        foreign key (book_id) references books (id),
    add constraint fk_books_authors_authors_id
        foreign key (author_id) references authors (id);

create table books_genres
(
    id      bigint auto_increment primary key,
    book_id bigint not null,
    genre_id bigint not null
);

alter table books_genres
    add unique index uq_books_genres_id (id),
    add index idx_books_genres_book_id (book_id),
    add index idx_books_genres_genre_id (genre_id),
    add constraint fk_books_genres_books_id
        foreign key (book_id) references books (id),
    add constraint fk_books_genres_genres_id
        foreign key (genre_id) references genres (id);




