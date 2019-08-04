--drop table carts
--drop table users
--drop table items

CREATE TABLE public.users
(
    user_id serial,
    email text COLLATE pg_catalog."default" NOT NULL,
    password text COLLATE pg_catalog."default" NOT NULL,
    created_on timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    admin boolean,
    CONSTRAINT users_pkey PRIMARY KEY (user_id),
    CONSTRAINT users_email_key UNIQUE (email)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

CREATE TABLE public.coupons
(
    coupon_id serial,
    code text COLLATE pg_catalog."default" NOT NULL,
    start_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_date timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP + interval '2 weeks',
    CONSTRAINT coupon_pkey PRIMARY KEY (coupon_id),
    CONSTRAINT coupon_code_key UNIQUE (code)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

CREATE TABLE public.items
(
    item_id serial,
    name text COLLATE pg_catalog."default" NOT NULL,
    price numeric NOT NULL,
    description text COLLATE pg_catalog."default",
	total_amount integer NOT NULL
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

CREATE TABLE public.carts
(
	user_id integer REFERENCES users(user_id) ON DELETE CASCADE,
	items_in_cart integer[] DEFAULT '{}'::integer[]
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.items
    OWNER to postgres;

ALTER TABLE public.users
    OWNER to postgres;

ALTER TABLE public.carts
    OWNER to postgres;