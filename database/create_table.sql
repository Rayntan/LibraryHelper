BEGIN;


CREATE TABLE IF NOT EXISTS public.books
(
    id bigserial NOT NULL,
    name varchar(256) NOT NULL,
    register_date date NOT NULL,
    PRIMARY KEY (id),
	UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS public.authors
(
    id bigserial NOT NULL,
    full_name varchar(256) NOT NULL,
    PRIMARY KEY (id),
	UNIQUE (full_name)
);

CREATE TABLE IF NOT EXISTS public.genres
(
    id bigserial NOT NULL,
    name varchar(128) NOT NULL,
    PRIMARY KEY (id),
	UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS public.authors_for_books
(
    id bigserial NOT NULL,
    author_id bigint NOT NULL,
    book_id bigint NOT NULL,
    PRIMARY KEY (id),
	UNIQUE (author_id, book_id)
);

CREATE TABLE IF NOT EXISTS public.genres_for_books
(
    id bigserial NOT NULL,
    genre_id bigint NOT NULL,
    book_id bigint NOT NULL,
    PRIMARY KEY (id),
	UNIQUE (genre_id, book_id)
);

CREATE TABLE IF NOT EXISTS public.users
(
    id bigserial NOT NULL,
    firstname varchar(128) NOT NULL,
    lastname varchar(128) NOT NULL,
    middlename varchar(128) NOT NULL,
    phone varchar(20) NOT NULL,
    register_date date,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.books_for_users
(
    id bigserial NOT NULL,
    user_id bigint NOT NULL,
    book_id bigint NOT NULL,
    take_date date NOT NULL,
    expected_return_date date NOT NULL,
    real_return_date date,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.authors_for_books
    ADD FOREIGN KEY (author_id)
    REFERENCES public.authors (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public.authors_for_books
    ADD FOREIGN KEY (book_id)
    REFERENCES public.books (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public.genres_for_books
    ADD FOREIGN KEY (genre_id)
    REFERENCES public.genres (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public.genres_for_books
    ADD FOREIGN KEY (book_id)
    REFERENCES public.books (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public.books_for_users
    ADD FOREIGN KEY (user_id)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public.books_for_users
    ADD FOREIGN KEY (book_id)
    REFERENCES public.books (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;

END;