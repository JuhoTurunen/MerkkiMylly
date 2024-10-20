CREATE TABLE public.users (
    id integer NOT NULL PRIMARY KEY,
    username character varying(50) NOT NULL UNIQUE,
    email character varying(100) NOT NULL UNIQUE,
    password_hash character varying(255) NOT NULL
);

CREATE TABLE public.upgrades (
    id integer NOT NULL PRIMARY KEY,
    name character varying(50) NOT NULL,
    description character varying(255) NOT NULL,
    base_price integer DEFAULT 0 NOT NULL,
    click_power integer DEFAULT 0 NOT NULL,
    passive_power integer DEFAULT 0 NOT NULL
);

CREATE TABLE public.user_profile (
    id integer NOT NULL PRIMARY KEY,
    user_id integer NOT NULL UNIQUE,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP(0) NOT NULL,
    CONSTRAINT user_profile_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users (id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE public.user_score (
    id integer NOT NULL PRIMARY KEY,
    user_id integer NOT NULL UNIQUE,
    clicks bigint DEFAULT 0,
    points bigint DEFAULT 0,
    CONSTRAINT score_data_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users (id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE public.user_session (
    id integer NOT NULL PRIMARY KEY,
    user_id integer NOT NULL UNIQUE,
    last_update_timestamp timestamp with time zone DEFAULT CURRENT_TIMESTAMP(0) NOT NULL,
    CONSTRAINT user_session_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users (id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE public.user_upgrades (
    id integer NOT NULL PRIMARY KEY,
    user_id integer NOT NULL,
    upgrade_id integer NOT NULL,
    amount integer NOT NULL,
    CONSTRAINT user_upgrades_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users (id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT user_upgrades_upgrade_id_fkey FOREIGN KEY (upgrade_id) REFERENCES public.upgrades (id) ON UPDATE CASCADE ON DELETE CASCADE
);