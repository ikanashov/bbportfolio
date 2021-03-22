import datetime
import pyodbc 


class BlackBoard:
    """Class to connect to BlackBoard sql server"""
    
    sql_query_user_courses = """
    SELECT 
        users.pk1 user_pk1
        ,users.user_id ,users.lastname ,users.firstname 
        ,course_users.pk1 course_user_id, course_users.crsmain_pk1
        ,courses.course_id, courses.course_name
    FROM users
        JOIN course_users on course_users.users_pk1=users.pk1
        JOIN course_main courses on courses.pk1=course_users.crsmain_pk1
    WHERE user_id = ?
    ORDER BY courses.course_id
    """
    sql_query_user_activity_in_system = """
    SELECT
        cm.course_id, cm.course_name 
        ,aa.course_pk1, aa.event_type, aa.user_pk1
        ,u.user_id, aa.data, aa.timestamp
        FROM [BBLEARN_stats].[dbo].[activity_accumulator] aa
        JOIN [BBLEARN_stats].[dbo].[users] u ON aa.user_pk1=u.pk1
        JOIN [BBLEARN_stats].[dbo].[course_main] cm ON cm.pk1=aa.course_pk1
    WHERE user_id= ?
    ORDER BY timestamp DESC;
    """
    sql_query_user_info = """
    SELECT
        pk1 user_pk, system_role, user_id, student_id, 
        lastname, firstname, 
        email, suffix
    FROM users
    WHERE user_id = ?
    """
    sql_query_user_grade_on_course = """
    SELECT
       gsa.pk1, gsa.gradebook_main_pk1,
       gsa.attempt_pk1, gsa.attempt_grade, 
       gsa.last_attempt_date, gsa.last_graded_date,
       gsa.attempt_feedback,
       cc.title
       --,fn.FILE_NAME
    FROM gb2_score_and_attempt_vw gsa
        join gradebook_main gm ON gm.pk1=gsa.gradebook_main_pk1
        join course_contents cc ON cc.pk1=gm.course_contents_pk1
        --left join cms_resource_link crl ON crl.parent_pk1=gsa.attempt_pk1 and crl.crsmain_pk1=gsa.book_pk1
        --left join [BBLEARN_cms_doc].[dbo].[XYF_URLS] fn ON fn.FILE_ID=REPLACE(crl.resource_id,'_1','')        
    WHERE course_users_pk1 = ? AND gsa.attempt_grade IS NOT NULL
    """
    sql_query_course_by_course_users_id = """
    SELECT
        course_main.pk1, course_main.course_id, course_main.course_name
    FROM course_main
        JOIN course_users on course_users.crsmain_pk1=course_main.pk1
    WHERE course_users.pk1 = ?
    """
    sql_query_file_by_attempt_id = """
    SELECT 
        --af.pk1, af.attempt_pk1, 
        af.files_pk1,f.file_name
	FROM attempt_files af
        JOIN files f on f.pk1=af.files_pk1
    WHERE af.attempt_pk1 = ?
    """

    def __init__(self):
        dsn = 'BBSQLMSSQLServerDatabase' 
        database = 'BBLEARN' 
        username = '***REMOVED***' 
        password = '***REMOVED***' 
        cnxn = pyodbc.connect('DSN='+dsn+';DATABASE='+database+';UID='+username+';PWD='+ password)
        self.cursor = cnxn.cursor()
    
    def get_user_courses(self, user_id: str) -> list:
        self.cursor.execute(BlackBoard.sql_query_user_courses, (user_id,))
        rows = self.cursor.fetchall()
        usercourses: list = [{
                'course_id': row[6],
                'course_name': row[7],
                'course_user_id': row[4],
            } for row in rows]
        return usercourses

    def get_user_activity(self, user_id: str) -> list:
        self.cursor.execute(BlackBoard.sql_query_user_activity_in_system, (user_id,))
        rows = self.cursor.fetchall()
        useractivity: list = [{
                'course_id': row[0],
                'course_name': row[1],
                'activity_type': row[3],
                'activity_data': row[6],
                'activity_datetime': row[7].strftime('%d.%m.%Y %H:%M:%S'),
            } for row in rows]
        return useractivity

    def get_user_info(self, user_id: str) -> dict:
        self.cursor.execute(BlackBoard.sql_query_user_info, (user_id,))
        row = self.cursor.fetchone()
        userinfo: dict = { 
            'login': row[2],
            'id': row[3],
            'lastname': row[4],
            'firstname': row[5],
            'email': row[6]
            }
        return userinfo
    
    def get_course_by_course_users_id(self, user_id_on_curse: str) -> dict:
        self.cursor.execute(BlackBoard.sql_query_course_by_course_users_id, 
                            (user_id_on_curse,))
        row = self.cursor.fetchone()
        courseinfo: dict = { 
            'course_pk1': row[0],
            'course_id': row[1],
            'course_name': row[2],
            }
        return courseinfo

    def get_files_by_attempt_id(self, attempt_id: str) -> list:
        self.cursor.execute(BlackBoard.sql_query_file_by_attempt_id, (attempt_id,))
        rows = self.cursor.fetchall()
        attempt_files: list = [{
                'file_id': row[0],
                'file_name': row[1],
            } for row in rows]
        return attempt_files

    def get_user_grade_on_course(self, user_id_on_curse: str) -> list:
        self.cursor.execute(BlackBoard.sql_query_user_grade_on_course, (user_id_on_curse,))
        rows = self.cursor.fetchall()        
        user_grade_in_course = [{
            'attempt_id': row[2],
            'grade': row[3],
            'attempt_date': row[4].strftime('%d.%m.%Y %H:%M:%S'),
            'grade_date': row[5].strftime('%d.%m.%Y %H:%M:%S'),
            'attempt_feedback': row[6],
            'grade_title': row[7],
            'attempt_files': self.get_files_by_attempt_id(row[2]),
        } for row in rows]
        return user_grade_in_course

if __name__ == "__main__":
     x = BlackBoard()
     print(x.get_course_by_course_users_id('233613'))
     print(x.get_user_grade_on_course('233613'))
