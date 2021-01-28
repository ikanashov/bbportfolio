-- Схема для обмена данными с информацией в 1С ВУЗ
CREATE SCHEMA IF NOT EXISTS bb;

CREATE TABLE IF NOT EXISTS bb.vuz_faculties (
    id uuid PRIMARY KEY,
    name character varying(255) NOT NULL,
    updated timestamp with time zone NOT NULL,
    UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS bb.vuz_groups (
    id uuid PRIMARY KEY,
    name character varying(255) NOT NULL,
    updated timestamp with time zone NOT NULL,
    UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS bb.vuz_students (
    id uuid PRIMARY KEY,
    full_name character varying(255) NOT NULL,
    kod_fl character varying(8) NOT NULL,
    login character varying(100) NOT NULL,
    email character varying(100) NULL,
    updated timestamp with time zone NOT NULL,
    UNIQUE (login)
);

-- m2m-таблица для связывания групп и факультетов
CREATE TABLE IF NOT EXISTS bb.vuz_facult_group (
    id uuid PRIMARY KEY,
    faculty_id uuid NOT NULL,
    group_id uuid NOT NULL,
    created timestamp with time zone,
    FOREIGN KEY (faculty_id) REFERENCES bb.vuz_faculties (id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES bb.vuz_groups (id) ON DELETE CASCADE
);

-- Уникальность связки групп и факультетов
CREATE UNIQUE INDEX vuz_group_facult_ind ON bb.vuz_facult_group (faculty_id, group_id);


-- m2m-таблица для связывания групп и студентов
CREATE TABLE IF NOT EXISTS bb.vuz_group_student (
    id uuid PRIMARY KEY,
    group_id uuid NOT NULL,
    student_id uuid NOT NULL,
    created timestamp with time zone,
    FOREIGN KEY (student_id) REFERENCES bb.vuz_students (id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES bb.vuz_groups (id) ON DELETE CASCADE
);
CREATE UNIQUE INDEX vuz_student_group_ind ON bb.vuz_group_student (group_id, student_id);
