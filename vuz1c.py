import os 
import uuid
from datetime import datetime, timezone

from requests import Session
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from zeep import Client
from zeep.transports import Transport
from dotenv import load_dotenv

from portfolioclasses import VuzStudent, PSQLFaculty, PSQLGroup, PSQLStudent


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
            self.groups = set(list(zip(*self.users))[1])
            self.filials = set(list(zip(*self.users))[0])
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
        for row in self.users]
        return users


class ETL1cToPostgres():
    """Class to load data from csv to postgress base"""
    vuzfaculties: dict = {}
    vuzgroups: dict = {}
    vuzstudents: dict = {}
    vuzfacultygroups: dict = {}
    vuzgroupstuednts: dict = {}

    def __init__(self, users: list):
        self.users = [VuzStudent(user[0], user[1], user[2], user[3], user[4], user[5]) for user in users]
    
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

    def add_vuz_student(self, student: VuzStudent) -> PSQLStudent:
        now = datetime.now(timezone.utc)
        id = str(uuid.uuid4())
        if student.email:
            email = student.email
        else:
            email = '\\N'
        vuzstudent = (id, student.full_name, student.kod_fl, student.login, email, now)
        self.vuzstudents[student.login] = vuzstudent
        return PSQLStudent(*vuzstudent)

    def get_users(self):
        for user in self.users:
            self.get_or_add_vuz_faculty(user.faculty)
            self.get_or_add_vuz_group(user.group)
            self.add_vuz_student(user)


if __name__ == "__main__":
     #x = Vuz1C()
     #print(x.get_users())
     #Vuz1CSoap()
     etl = ETL1cToPostgres(Vuz1C().users)
     etl.get_users()
     print(etl.vuzfaculties)
     print(etl.vuzgroups)
     print(len(etl.vuzstudents))
     


#zipusers = list(zip(*users))
#print (filials)
#print (groups)
#course = input ("Введитие ИД курса : ")
#group = input ("Введите название групп(ы) через пробел : ")
#try:
    #f = open ('_bb_zachislil_'+course+'_'+group+'.csv','w')
    #group = group.split(' ')
#    for user in users:
#        if user[1] in group:
#            print (course+','+user[4]+',S')
#            f.write(course+','+user[4]+',S'+'\n')
#finally:
#    f.close()