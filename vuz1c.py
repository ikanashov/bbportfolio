import csv
import io
import os 
import uuid
from datetime import datetime, timezone

from requests import Session
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from zeep import Client
from zeep.transports import Transport
from dotenv import load_dotenv

import psycopg2

from portfolioclasses import VuzStudent, PSQLFaculty, PSQLGroup, PSQLStudent, PSQLFacultyGroup, PSQLGroupStudent


class Vuz1CSoap:
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
            SOAP1CLINK = os.getenv('SOAP1CLINK')
            SOAP1CUSER = os.getenv('SOAP1CUSER')
            SOAP1CPASSWORD = os.getenv('SOAP1CPASSWORD')
        else:
            SOAP1CLINK = ''
            SOAP1CUSER = ''
            SOAP1CPASSWORD = ''
        
        try:
            session = Session()
            session.auth = HTTPBasicAuth(SOAP1CUSER, SOAP1CPASSWORD)
            client1c = Client(SOAP1CLINK, transport=Transport(session=session))
            #print(client1c.service.GetGroups(''))
            #print(client1c.service.GetDataByLogin('aebagaturov'))
            #print(client1c.service.GetDataByLogin('mesalmin'))
            #print(client1c.service.GetDataByLogin('kuznecovaa'))
        except:
            print('Ошибка при подключении к SOAP сервису 1С')
    

class Vuz1C:
    """Class to read data from csv 1C Vuz Dekanat"""
    
    def __init__(self):
        try:
            f = open ("db/1clogins.csv",'r')
            self.users = []
            for line in f:
                splitline = line.rstrip().split(';')
                self.users.append(splitline)
            #from yandex praktikum data.sort(key=lambda row: row[1], reverse=True)
            self.users.sort(key=lambda row: row[2])
            self.users.sort(key=lambda row: row[1])
            self.users.sort(key=lambda row: row[0])
            # А это не испольузется по SOLID надо удалить!
            self.groups = set(list(zip(*self.users))[1])
            # Это просто необходимо исправить list set list не смешно!
            self.filials = list(set(list(zip(*self.users))[0]))
            self.filials.sort(key=lambda row: row[0])
        finally:
            f.close()
    
    def get_users(self) -> list:
        users = [
            {
                'faculty': row[0],
                'group': row[1],
                'full_name': row[2],
                'login': row[4],
            }
        for row in self.users
        ]
        return users
    
    def get_faculty(self) -> list:
        return self.filials

    def get_groups(self, faculty_name: str) -> list:
        groups = [row[1] for row in self.users if row[0] == faculty_name]
        # Это мне тоже очень не нравиться надо переделать
        groups = list(set(groups))
        groups.sort()
        groups = [
            {
                'faculty': faculty_name,
                'group': group
            }
        for group in groups
        ]
        return groups

    def get_users_in_group(self, group_name: str) -> list:
        users = [
            {
                'faculty': row[0],
                'group': row[1],
                'full_name': row[2],
                'login': row[4],
            }
        for row in self.users if row[1] == group_name
        ]
        return users

class ETL1cToPostgres():
    """Class to load data from csv to postgress base"""
    vuzfaculties: dict = {}
    vuzgroups: dict = {}
    vuzstudents: dict = {}
    vuzfacultygroups: dict = {}
    vuzgroupstudents: dict = {}
    
    def __init__(self, users: list, envfile='.env'):
        self.users = [VuzStudent(user[0], user[1], user[2], user[3], user[4], user[5]) for user in users]

        dotenv_path = os.path.join(os.path.dirname(__file__), envfile)
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)

        self.conn = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB', 'postgres'),
            user=os.getenv('POSTGRES_USER', 'postgres'),
            password=os.getenv('POSTGRES_PASSWORD', ''),
            host=os.getenv('POSTGRES_HOST', 'localhost'),
            port=int(os.getenv('POSTGRES_PORT', '5432')),
            options='-c search_path=' + os.getenv('POSTGRES_SCHEMA', 'public'),
        )

    def copy_to_table_from_csv(self, tablename: str, csvtable: io.StringIO):
        with self.conn as conn, conn.cursor() as cur:
            cur.copy_from(csvtable, tablename, sep='|')
    
    def get_or_add_vuz_faculty(self, faculty: str) -> PSQLFaculty:
        try:
            vuzfaculty = self.vuzfaculties[faculty]
        except KeyError:
            now = datetime.now(timezone.utc)
            vuzfaculty = (str(uuid.uuid4()), faculty, now)
            self.vuzfaculties[faculty] = vuzfaculty
        finally:
            return PSQLFaculty(*vuzfaculty)

    def get_or_add_vuz_group(self, group: str) -> PSQLGroup:
        try:
            vuzgroup = self.vuzgroups[group]
        except KeyError:
            now = datetime.now(timezone.utc)
            vuzgroup = (str(uuid.uuid4()), group, now)
            self.vuzgroups[group] = vuzgroup
        finally:
            return PSQLGroup(*vuzgroup)

    def get_or_add_vuz_student(self, student: VuzStudent) -> PSQLStudent:
        try:
            vuzstudent = self.vuzstudents[student.login]
        except KeyError:
            now = datetime.now(timezone.utc)
            id = str(uuid.uuid4())
            if student.email:
                email = student.email
            else:
                email = '\\N'
            vuzstudent = (id, student.full_name, student.kod_fl, student.login, email, now)
            self.vuzstudents[student.login] = vuzstudent
        finally:
            return PSQLStudent(*vuzstudent)
    
    def get_or_add_faculty_group(self, faculty_id: str, group_id: str) -> PSQLFacultyGroup:
        try:
            vuzfacultygroup = self.vuzfacultygroups[faculty_id+group_id]
        except KeyError:
            now = datetime.now(timezone.utc)
            id = str(uuid.uuid4())
            vuzfacultygroup = (id, faculty_id, group_id, now)
            self.vuzfacultygroups[faculty_id+group_id] = vuzfacultygroup
        finally:
            return PSQLFacultyGroup(*vuzfacultygroup)
    
    def get_or_add_student_group(self, group_id: str, student_id: str) -> PSQLGroupStudent:
        try:
            vuzgroupstudent = self.vuzgroupstudents[group_id+student_id]
        except KeyError:
            now = datetime.now(timezone.utc)
            id = str(uuid.uuid4())
            vuzgroupstudent = (id, group_id, student_id, now)
            self.vuzgroupstudents[group_id+student_id] = vuzgroupstudent
        finally:
            return PSQLGroupStudent(*vuzgroupstudent)

    def get_users(self):
        for user in self.users:
            if user.login:
                faculty = self.get_or_add_vuz_faculty(user.faculty)
                group = self.get_or_add_vuz_group(user.group)
                student = self.get_or_add_vuz_student(user)
                faculty_group = self.get_or_add_faculty_group(faculty.id, group.id)
                student_group = self.get_or_add_student_group(group.id, student.id)
            else:
                print('empty_login', user.faculty, user.group, user.full_name, user.kod_fl, user.email)

    def generate_csv(self, tabledict: dict) -> io.StringIO:
        csvtable = io.StringIO()
        tablewriter = csv.writer(csvtable, delimiter='|',)
        for key in tabledict:
            tablewriter.writerow(tabledict[key])
        csvtable.seek(0)
        return csvtable

if __name__ == "__main__":
    pass
     #x = Vuz1C()
     #print(x.get_users())
     #Vuz1CSoap()
     #
     #etl = ETL1cToPostgres(Vuz1C().users)
     #etl.get_users()
     #vuzfaculties = etl.generate_csv(etl.vuzfaculties)
     #vuzgroups = etl.generate_csv(etl.vuzgroups)
     #vuzstudents = etl.generate_csv(etl.vuzstudents)
     #vuzfacultygroups = etl.generate_csv(etl.vuzfacultygroups)
     #vuzgroupstudents = etl.generate_csv(etl.vuzgroupstudents)
     
     #etl.copy_to_table_from_csv('vuz_faculties', vuzfaculties)
     #etl.copy_to_table_from_csv('vuz_groups', vuzgroups)
     #etl.copy_to_table_from_csv('vuz_students', vuzstudents)
     #etl.copy_to_table_from_csv('vuz_facult_group', vuzfacultygroups)
     #etl.copy_to_table_from_csv('vuz_group_student', vuzgroupstudents)
     
     #print(len(etl.users))
     #print(len(etl.vuzfaculties))
     #print(len(etl.vuzgroups))
     #print(len(etl.vuzstudents))
     #print(len(etl.vuzfacultygroups))
     #print(len(etl.vuzgroupstudents))
