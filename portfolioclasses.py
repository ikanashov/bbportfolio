import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class VuzStudent:
    faculty: str
    group: str
    full_name: str
    kod_fl: str
    login: str
    email: str


@dataclass
class PSQLFaculty:
    id: uuid.UUID
    name: str
    updated: datetime


@dataclass 
class PSQLGroup:
    id: uuid.UUID
    name: str
    updated: datetime


@dataclass
class PSQLStudent:
    id: uuid.UUID
    fio: str
    kod_fl: str
    login: str
    e_mail: str
    updated: datetime


@dataclass
class PSQLFacultyGroup:
    id: uuid.UUID
    faculty_id: uuid.UUID
    group_id: uuid.UUID
    created: datetime


@dataclass
class PSQLGroupStudent:
    id: uuid.UUID
    group_id: uuid.UUID
    student_id: uuid.UUID
    created: datetime
