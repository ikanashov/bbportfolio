from flask import Flask, render_template

import blackboard
import vuz1c


vuz = vuz1c.Vuz1C()

app = Flask('portfolio_service')

@app.route('/portfolio/allusers', strict_slashes=False)
def portfolio_service() -> str:
    users = vuz.get_users()
    return render_template(
        'userslist.html', 
        title = 'Портфолио студента "Уральский Государственный университет путей сообщения"', 
        users = users
        )

@app.route('/portfolio', strict_slashes=False)
def portfolio_groups() -> str:
    faculties = vuz.get_faculty()
    return render_template(
        'facultylist.html',
        title = 'Портфолио студента "Уральский Государственный университет путей сообщения"',
        faculties = faculties
    )

@app.route('/portfolio/faculty/<faculty_name>', methods=['GET'], strict_slashes=False)
def porfolio_faculty_groups(faculty_name: str) -> str:
    groups = vuz.get_groups(faculty_name)
    return render_template(
        'grouplist.html',
        title = 'Группы факультета — ' + faculty_name,
        groups = groups
    )

@app.route('/portfolio/group/<group_name>', methods=['GET'], strict_slashes=False)
def portfolio_users_in_group(group_name: str) -> str:
    users = vuz.get_users_in_group(group_name)
    return render_template(
        'userslist.html', 
        title = 'Портфолио студентов группы — ' + group_name, 
        users = users
        )


@app.route('/portfolio/<user_id>', methods=['GET'], strict_slashes=False)
def portfolio_user_info(user_id: str) -> str:
    pfl = blackboard.BlackBoard()
    userinfo = pfl.get_user_info(user_id)
    return render_template(
        'userinfo.html', 
        title = userinfo['login'], 
        userinfo = userinfo
        )

@app.route('/portfolio/<user_id>/activity', methods=['GET'], strict_slashes=False)
def portfolio_user_activity(user_id: str) -> str:
    pfl = blackboard.BlackBoard()
    userinfo = pfl.get_user_info(user_id)
    useractivity = pfl.get_user_activity(user_id)
    return render_template(
        'useractivity.html', 
        title=userinfo['login'], 
        userinfo = userinfo, 
        useractivity = useractivity,
        )

@app.route('/portfolio/<user_id>/courses', methods=['GET'], strict_slashes=False)
def portfolio_user_courses(user_id: str) -> str:
    pfl = blackboard.BlackBoard()
    userinfo = pfl.get_user_info(user_id)
    usercourses = pfl.get_user_courses(user_id)
    return render_template(
        'usercourses.html', 
        title=userinfo['login'], 
        userinfo = userinfo, 
        usercourses = usercourses,
        )

@app.route('/portfolio/<user_id>/courses/<course_user_id>', methods=['GET'], strict_slashes=False)
def portfolio_user_grade_in_course(user_id: str, course_user_id: str) -> str:
    pfl = blackboard.BlackBoard()
    userinfo = pfl.get_user_info(user_id)
    courseinfo = pfl.get_course_by_course_users_id(course_user_id)
    usergrades = pfl.get_user_grade_on_course(course_user_id)
    return render_template(
        'usergrade.html', 
        title=userinfo['login'], 
        userinfo = userinfo,
        courseinfo = courseinfo,
        usergrades = usergrades, 
        )


@app.route('/', methods=['GET'])
def movies_deafault() -> str:
    #Страница по умолчанию
    return 'Enjoy the silence'


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8001)