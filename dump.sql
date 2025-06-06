--
-- PostgreSQL database dump
--

-- Dumped from database version 12.5 (Debian 12.5-1.pgdg100+1)
-- Dumped by pg_dump version 12.5 (Debian 12.5-1.pgdg100+1)

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

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: fastapi_taskman
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO fastapi_taskman;

--
-- Name: project; Type: TABLE; Schema: public; Owner: fastapi_taskman
--

CREATE TABLE public.project (
    project_id integer NOT NULL,
    project_name character varying NOT NULL,
    project_description character varying
);


ALTER TABLE public.project OWNER TO fastapi_taskman;

--
-- Name: project_project_id_seq; Type: SEQUENCE; Schema: public; Owner: fastapi_taskman
--

CREATE SEQUENCE public.project_project_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.project_project_id_seq OWNER TO fastapi_taskman;

--
-- Name: project_project_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: fastapi_taskman
--

ALTER SEQUENCE public.project_project_id_seq OWNED BY public.project.project_id;


--
-- Name: task; Type: TABLE; Schema: public; Owner: fastapi_taskman
--

CREATE TABLE public.task (
    task_description character varying(300) NOT NULL,
    assignee integer NOT NULL,
    task_id integer NOT NULL,
    due_date date NOT NULL,
    project integer
);


ALTER TABLE public.task OWNER TO fastapi_taskman;

--
-- Name: task_task_id_seq; Type: SEQUENCE; Schema: public; Owner: fastapi_taskman
--

CREATE SEQUENCE public.task_task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.task_task_id_seq OWNER TO fastapi_taskman;

--
-- Name: task_task_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: fastapi_taskman
--

ALTER SEQUENCE public.task_task_id_seq OWNED BY public.task.task_id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: fastapi_taskman
--

CREATE TABLE public."user" (
    user_id integer NOT NULL,
    email character varying,
    password character varying,
    name character varying NOT NULL
);


ALTER TABLE public."user" OWNER TO fastapi_taskman;

--
-- Name: user_user_id_seq; Type: SEQUENCE; Schema: public; Owner: fastapi_taskman
--

CREATE SEQUENCE public.user_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_user_id_seq OWNER TO fastapi_taskman;

--
-- Name: user_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: fastapi_taskman
--

ALTER SEQUENCE public.user_user_id_seq OWNED BY public."user".user_id;


--
-- Name: project project_id; Type: DEFAULT; Schema: public; Owner: fastapi_taskman
--

ALTER TABLE ONLY public.project ALTER COLUMN project_id SET DEFAULT nextval('public.project_project_id_seq'::regclass);


--
-- Name: task task_id; Type: DEFAULT; Schema: public; Owner: fastapi_taskman
--

ALTER TABLE ONLY public.task ALTER COLUMN task_id SET DEFAULT nextval('public.task_task_id_seq'::regclass);


--
-- Name: user user_id; Type: DEFAULT; Schema: public; Owner: fastapi_taskman
--

ALTER TABLE ONLY public."user" ALTER COLUMN user_id SET DEFAULT nextval('public.user_user_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: fastapi_taskman
--

COPY public.alembic_version (version_num) FROM stdin;
362837b15fd7
\.


--
-- Data for Name: project; Type: TABLE DATA; Schema: public; Owner: fastapi_taskman
--

COPY public.project (project_id, project_name, project_description) FROM stdin;
\.


--
-- Data for Name: task; Type: TABLE DATA; Schema: public; Owner: fastapi_taskman
--

COPY public.task (task_description, assignee, task_id, due_date, project) FROM stdin;
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: fastapi_taskman
--

COPY public."user" (user_id, email, password, name) FROM stdin;
1	user@example.com	$2b$12$eewaObr9DMszA6BoR/mgwOG8/PtWYpGi.P.44TjfSeRql59yiSLBS	╨Ш╨▓╨░╨╜ ╨Ш╨▓╨░╨╜╨╛╨▓
2	loginov.artem@phystech.ru	$2b$12$kAyqwurLjIUt785WMo6jO.dXkWss/Aw3RlLF0sM5ts1q37xW3cK4e	╨Р╤А╤В╤С╨╝ ╨Ы╨╛╨│╨╕╨╜╨╛╨▓
4	user1@phystech.ru	$2b$12$n4Pe5/IKV/8Fl/QIJSFFSeJMD6vPpLxtUhNCJWDDJPvUhZ/NM0NMi	╨з╨╡╨╗╨╛╨▓╨╡╨║ ╨С╨╡╨╖ ╨б╨╡╨╗╨╡╨╖╤С╨╜╨║╨╕
5	user2@phystech.ru	$2b$12$52AhIHifhhsZRJJrHHgbM.oIyhNyFj0aJ.CH8G9Waadfz.FcqS3uW	╨Р╨╜╤В╨╛╤И╨░ ╨з╨╡╤Е╨╛╨╜╤В╨╡
\.


--
-- Name: project_project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: fastapi_taskman
--

SELECT pg_catalog.setval('public.project_project_id_seq', 1, false);


--
-- Name: task_task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: fastapi_taskman
--

SELECT pg_catalog.setval('public.task_task_id_seq', 1, false);


--
-- Name: user_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: fastapi_taskman
--

SELECT pg_catalog.setval('public.user_user_id_seq', 5, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: fastapi_taskman
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: project project_pkey; Type: CONSTRAINT; Schema: public; Owner: fastapi_taskman
--

ALTER TABLE ONLY public.project
    ADD CONSTRAINT project_pkey PRIMARY KEY (project_id);


--
-- Name: task task_pkey; Type: CONSTRAINT; Schema: public; Owner: fastapi_taskman
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_pkey PRIMARY KEY (task_id);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: fastapi_taskman
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: fastapi_taskman
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (user_id);


--
-- Name: task task_assignee_fkey; Type: FK CONSTRAINT; Schema: public; Owner: fastapi_taskman
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_assignee_fkey FOREIGN KEY (assignee) REFERENCES public."user"(user_id);


--
-- Name: task task_project_fkey; Type: FK CONSTRAINT; Schema: public; Owner: fastapi_taskman
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_project_fkey FOREIGN KEY (project) REFERENCES public.project(project_id);


--
-- PostgreSQL database dump complete
--

