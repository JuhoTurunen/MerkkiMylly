--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4
-- Dumped by pg_dump version 16.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;


-- Create account called merkkimylly

DO $$ BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_roles WHERE rolname = 'merkkimylly'
    ) THEN
        CREATE ROLE merkkimylly LOGIN PASSWORD 'merkkimylly';
    END IF;
END $$;

--
-- Name: score_data; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.score_data (
    id integer NOT NULL,
    user_id integer NOT NULL,
    clicks bigint DEFAULT 0,
    points bigint DEFAULT 0
);


--
-- Name: score_data_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.score_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: score_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.score_data_id_seq OWNED BY public.score_data.id;


--
-- Name: upgrades; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.upgrades (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description character varying(255) NOT NULL,
    price integer DEFAULT 0 NOT NULL,
    click_power integer DEFAULT 0 NOT NULL,
    passive_power integer DEFAULT 0 NOT NULL
);


--
-- Name: upgrades_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.upgrades_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: upgrades_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.upgrades_id_seq OWNED BY public.upgrades.id;


--
-- Name: user_upgrades; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_upgrades (
    id integer NOT NULL,
    user_id integer NOT NULL,
    upgrade_id integer NOT NULL,
    amount integer NOT NULL
);


--
-- Name: user_upgrades_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.user_upgrades_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_upgrades_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.user_upgrades_id_seq OWNED BY public.user_upgrades.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    password_hash character varying(255) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



-- Grant privileges to merkkimylly
GRANT ALL ON TABLE public.score_data TO merkkimylly;
GRANT ALL ON TABLE public.upgrades TO merkkimylly;
GRANT ALL ON TABLE public.user_upgrades TO merkkimylly;
GRANT ALL ON TABLE public.users TO merkkimylly;
GRANT ALL ON SEQUENCE public.score_data_id_seq TO merkkimylly;
GRANT ALL ON SEQUENCE public.upgrades_id_seq TO merkkimylly;
GRANT ALL ON SEQUENCE public.user_upgrades_id_seq TO merkkimylly;
GRANT ALL ON SEQUENCE public.users_id_seq TO merkkimylly;

-- Set default privileges merkkimylly
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO merkkimylly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO merkkimylly;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: score_data id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.score_data ALTER COLUMN id SET DEFAULT nextval('public.score_data_id_seq'::regclass);


--
-- Name: upgrades id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.upgrades ALTER COLUMN id SET DEFAULT nextval('public.upgrades_id_seq'::regclass);


--
-- Name: user_upgrades id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_upgrades ALTER COLUMN id SET DEFAULT nextval('public.user_upgrades_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: score_data score_data_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.score_data
    ADD CONSTRAINT score_data_pkey PRIMARY KEY (id);


--
-- Name: upgrades upgrades_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.upgrades
    ADD CONSTRAINT upgrades_pkey PRIMARY KEY (id);


--
-- Name: user_upgrades user_upgrades_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_upgrades
    ADD CONSTRAINT user_upgrades_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: score_data score_data_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.score_data
    ADD CONSTRAINT score_data_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- Name: user_upgrades user_upgrades_upgrade_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_upgrades
    ADD CONSTRAINT user_upgrades_upgrade_id_fkey FOREIGN KEY (upgrade_id) REFERENCES public.upgrades(id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- Name: user_upgrades user_upgrades_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_upgrades
    ADD CONSTRAINT user_upgrades_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4
-- Dumped by pg_dump version 16.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: upgrades; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.upgrades (id, name, description, price, click_power, passive_power) FROM stdin;
2	Fresher	Buy a fresher to click for you.	100	0	1
1	New mouse	Buy another mouse to click faster.	20	1	0
3	Programming course	Write an automated script for clicking.	300	0	2
4	Laptop	Buy a new laptop to click on.	200	2	0
\.


--
-- Name: upgrades_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.upgrades_id_seq', 4, true);


--
-- PostgreSQL database dump complete
--

