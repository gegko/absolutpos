--
-- PostgreSQL database dump
--

-- Dumped from database version 16.0 (Debian 16.0-1.pgdg120+1)
-- Dumped by pg_dump version 16.0 (Debian 16.0-1.pgdg120+1)

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
-- Name: answer; Type: TABLE; Schema: public; Owner: absolutpos
--

CREATE TABLE public.answer (
    text character varying NOT NULL,
    business_id uuid NOT NULL,
    question_id uuid NOT NULL,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.answer OWNER TO absolutpos;

--
-- Name: business; Type: TABLE; Schema: public; Owner: absolutpos
--

CREATE TABLE public.business (
    name character varying NOT NULL,
    city character varying NOT NULL,
    address character varying NOT NULL,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    businesstype_id uuid,
    businessarea_id uuid
);


ALTER TABLE public.business OWNER TO absolutpos;

--
-- Name: businessarea; Type: TABLE; Schema: public; Owner: absolutpos
--

CREATE TABLE public.businessarea (
    name character varying NOT NULL,
    businesstype_id uuid NOT NULL,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.businessarea OWNER TO absolutpos;

--
-- Name: businessareaquestionlink; Type: TABLE; Schema: public; Owner: absolutpos
--

CREATE TABLE public.businessareaquestionlink (
    businessarea_id uuid NOT NULL,
    question_id uuid NOT NULL
);


ALTER TABLE public.businessareaquestionlink OWNER TO absolutpos;

--
-- Name: businesstype; Type: TABLE; Schema: public; Owner: absolutpos
--

CREATE TABLE public.businesstype (
    name character varying NOT NULL,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.businesstype OWNER TO absolutpos;

--
-- Name: question; Type: TABLE; Schema: public; Owner: absolutpos
--

CREATE TABLE public.question (
    text character varying NOT NULL,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.question OWNER TO absolutpos;

--
-- Data for Name: answer; Type: TABLE DATA; Schema: public; Owner: absolutpos
--

COPY public.answer (text, business_id, question_id, id, created_at) FROM stdin;
\.


--
-- Data for Name: business; Type: TABLE DATA; Schema: public; Owner: absolutpos
--

COPY public.business (name, city, address, id, created_at, businesstype_id, businessarea_id) FROM stdin;
moi novii bizik	piter	sovetskaya 1	96d80800-1885-4e51-87bd-c003064a08ef	2024-02-24 21:19:04.045728	9d63ba8a-3e92-4784-bdfa-36c128042212	b5bde420-1fbe-44a4-a7ff-98e5681d7828
moi osnovnoi bizik	moscow	arbat 12	b975e661-4edf-4d60-be77-6fa02c967a87	2024-02-24 21:13:28.44597	0b7acf2d-e93c-43ac-882e-a3994d4c943d	fdf828c0-ca26-45a7-b611-f9fd7a18daaf
\.


--
-- Data for Name: businessarea; Type: TABLE DATA; Schema: public; Owner: absolutpos
--

COPY public.businessarea (name, businesstype_id, id, created_at) FROM stdin;
Ресторан	9d63ba8a-3e92-4784-bdfa-36c128042212	f3748f92-1b68-478a-a529-af5384ed2de3	2024-02-23 23:43:47.399969
Бар	9d63ba8a-3e92-4784-bdfa-36c128042212	b5bde420-1fbe-44a4-a7ff-98e5681d7828	2024-02-23 23:43:50.042779
Кафе	9d63ba8a-3e92-4784-bdfa-36c128042212	70e5357e-92b6-4a33-853b-68d088ec0c0f	2024-02-23 23:43:54.380263
Магазин	0b7acf2d-e93c-43ac-882e-a3994d4c943d	26373ba9-14f6-4a8d-8084-008b98818bb0	2024-02-23 23:44:00.113752
Киоск	0b7acf2d-e93c-43ac-882e-a3994d4c943d	fdf828c0-ca26-45a7-b611-f9fd7a18daaf	2024-02-23 23:44:05.199754
DRAFT	0870f0bc-0976-49ce-a81c-62e586d006ab	7e599f9f-e004-4ab5-b06b-120b8c9e738b	2024-02-23 23:50:07.447741
\.


--
-- Data for Name: businessareaquestionlink; Type: TABLE DATA; Schema: public; Owner: absolutpos
--

COPY public.businessareaquestionlink (businessarea_id, question_id) FROM stdin;
f3748f92-1b68-478a-a529-af5384ed2de3	c874ae9d-a403-4a0e-b782-9b6ce582765d
b5bde420-1fbe-44a4-a7ff-98e5681d7828	c874ae9d-a403-4a0e-b782-9b6ce582765d
70e5357e-92b6-4a33-853b-68d088ec0c0f	c874ae9d-a403-4a0e-b782-9b6ce582765d
f3748f92-1b68-478a-a529-af5384ed2de3	3c076b8a-cb9b-4365-8042-caae5b19dd78
f3748f92-1b68-478a-a529-af5384ed2de3	477bc67e-83af-4dfc-9e38-97dc8fd9a8b1
70e5357e-92b6-4a33-853b-68d088ec0c0f	477bc67e-83af-4dfc-9e38-97dc8fd9a8b1
7e599f9f-e004-4ab5-b06b-120b8c9e738b	d9dfb614-b11e-49b1-8ad3-4cfec0fea65b
7e599f9f-e004-4ab5-b06b-120b8c9e738b	42e49a17-0c8e-454c-8355-274ce6c95ed0
26373ba9-14f6-4a8d-8084-008b98818bb0	10197439-e1d7-4c2b-9817-1f3ed43434c5
f3748f92-1b68-478a-a529-af5384ed2de3	10197439-e1d7-4c2b-9817-1f3ed43434c5
b5bde420-1fbe-44a4-a7ff-98e5681d7828	10197439-e1d7-4c2b-9817-1f3ed43434c5
70e5357e-92b6-4a33-853b-68d088ec0c0f	10197439-e1d7-4c2b-9817-1f3ed43434c5
fdf828c0-ca26-45a7-b611-f9fd7a18daaf	10197439-e1d7-4c2b-9817-1f3ed43434c5
fdf828c0-ca26-45a7-b611-f9fd7a18daaf	d39e9e03-496e-4d9b-bfa8-41a12e4d2721
b5bde420-1fbe-44a4-a7ff-98e5681d7828	d39e9e03-496e-4d9b-bfa8-41a12e4d2721
26373ba9-14f6-4a8d-8084-008b98818bb0	a70ae79c-b129-4420-8625-c8115b62ca43
7e599f9f-e004-4ab5-b06b-120b8c9e738b	b30c51ea-7675-4d28-aaae-f559655c5fda
7e599f9f-e004-4ab5-b06b-120b8c9e738b	1e3f7f5c-fab1-46cd-be8b-b93a3265ca9b
f3748f92-1b68-478a-a529-af5384ed2de3	1e3f7f5c-fab1-46cd-be8b-b93a3265ca9b
b5bde420-1fbe-44a4-a7ff-98e5681d7828	1e3f7f5c-fab1-46cd-be8b-b93a3265ca9b
70e5357e-92b6-4a33-853b-68d088ec0c0f	1e3f7f5c-fab1-46cd-be8b-b93a3265ca9b
26373ba9-14f6-4a8d-8084-008b98818bb0	1e3f7f5c-fab1-46cd-be8b-b93a3265ca9b
fdf828c0-ca26-45a7-b611-f9fd7a18daaf	1e3f7f5c-fab1-46cd-be8b-b93a3265ca9b
\.


--
-- Data for Name: businesstype; Type: TABLE DATA; Schema: public; Owner: absolutpos
--

COPY public.businesstype (name, id, created_at) FROM stdin;
Ритейл	0b7acf2d-e93c-43ac-882e-a3994d4c943d	2024-02-23 23:43:33.324024
Общепит	9d63ba8a-3e92-4784-bdfa-36c128042212	2024-02-23 23:43:37.621785
DRAFT	0870f0bc-0976-49ce-a81c-62e586d006ab	2024-02-23 23:50:01.38838
\.


--
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: absolutpos
--

COPY public.question (text, id, created_at) FROM stdin;
Самый магазинный вопрос	a70ae79c-b129-4420-8625-c8115b62ca43	2024-02-24 17:57:06.555672
Ещё один вопрос для всех	1e3f7f5c-fab1-46cd-be8b-b93a3265ca9b	2024-02-24 18:00:45.937823
Вопрос для всех	10197439-e1d7-4c2b-9817-1f3ed43434c5	2024-02-24 17:55:29.520167
Черновик вопроса для ресторана	d9dfb614-b11e-49b1-8ad3-4cfec0fea65b	2024-02-23 23:50:19.710016
Вопрос для ресторана	3c076b8a-cb9b-4365-8042-caae5b19dd78	2024-02-23 23:44:50.937384
Вопрос для общепита	c874ae9d-a403-4a0e-b782-9b6ce582765d	2024-02-23 23:44:28.342512
Ресторан или кафе?	477bc67e-83af-4dfc-9e38-97dc8fd9a8b1	2024-02-23 23:45:04.354479
Старый вопрос для киосков	42e49a17-0c8e-454c-8355-274ce6c95ed0	2024-02-23 23:50:43.342719
Вопрос, который не подошёл ритейлу и общепиту	b30c51ea-7675-4d28-aaae-f559655c5fda	2024-02-24 17:58:06.303588
Назовите 3 цифры на обороте карты	d39e9e03-496e-4d9b-bfa8-41a12e4d2721	2024-02-24 17:56:04.589821
\.


--
-- Name: answer answer_pkey; Type: CONSTRAINT; Schema: public; Owner: absolutpos
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT answer_pkey PRIMARY KEY (id);


--
-- Name: business business_pkey; Type: CONSTRAINT; Schema: public; Owner: absolutpos
--

ALTER TABLE ONLY public.business
    ADD CONSTRAINT business_pkey PRIMARY KEY (id);


--
-- Name: businessarea businessarea_pkey; Type: CONSTRAINT; Schema: public; Owner: absolutpos
--

ALTER TABLE ONLY public.businessarea
    ADD CONSTRAINT businessarea_pkey PRIMARY KEY (id);


--
-- Name: businessareaquestionlink businessareaquestionlink_pkey; Type: CONSTRAINT; Schema: public; Owner: absolutpos
--

ALTER TABLE ONLY public.businessareaquestionlink
    ADD CONSTRAINT businessareaquestionlink_pkey PRIMARY KEY (businessarea_id, question_id);


--
-- Name: businesstype businesstype_pkey; Type: CONSTRAINT; Schema: public; Owner: absolutpos
--

ALTER TABLE ONLY public.businesstype
    ADD CONSTRAINT businesstype_pkey PRIMARY KEY (id);


--
-- Name: question question_pkey; Type: CONSTRAINT; Schema: public; Owner: absolutpos
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT question_pkey PRIMARY KEY (id);


--
-- Name: answer answer_business_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: absolutpos
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT answer_business_id_fkey FOREIGN KEY (business_id) REFERENCES public.business(id);


--
-- Name: answer answer_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: absolutpos
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT answer_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: business business_businessarea_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: absolutpos
--

ALTER TABLE ONLY public.business
    ADD CONSTRAINT business_businessarea_id_fkey FOREIGN KEY (businessarea_id) REFERENCES public.businessarea(id);


--
-- Name: business business_businesstype_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: absolutpos
--

ALTER TABLE ONLY public.business
    ADD CONSTRAINT business_businesstype_id_fkey FOREIGN KEY (businesstype_id) REFERENCES public.businesstype(id);


--
-- Name: businessarea businessarea_businesstype_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: absolutpos
--

ALTER TABLE ONLY public.businessarea
    ADD CONSTRAINT businessarea_businesstype_id_fkey FOREIGN KEY (businesstype_id) REFERENCES public.businesstype(id);


--
-- Name: businessareaquestionlink businessareaquestionlink_businessarea_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: absolutpos
--

ALTER TABLE ONLY public.businessareaquestionlink
    ADD CONSTRAINT businessareaquestionlink_businessarea_id_fkey FOREIGN KEY (businessarea_id) REFERENCES public.businessarea(id);


--
-- Name: businessareaquestionlink businessareaquestionlink_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: absolutpos
--

ALTER TABLE ONLY public.businessareaquestionlink
    ADD CONSTRAINT businessareaquestionlink_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- PostgreSQL database dump complete
--

