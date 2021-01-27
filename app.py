from flask import Flask, render_template
import blackboard
import vuz1c


app = Flask('portfolio_service')

@app.route('/portfolio', strict_slashes=False)
def portfolio_service() -> str:
    vuz = vuz1c.Vuz1C()
    users = vuz.get_users()
    return render_template(
        'userslist.html', 
        title='Портфолио это сладкое слово вер. 0.2', 
        users = users
        )
@app.route('/portfolio/<user_id>', methods=['GET'], strict_slashes=False)
def portfolio_user_info(user_id: str) -> str:
    pfl = blackboard.BlackBoard()
    userinfo = pfl.get_user_info(user_id)
    return render_template(
        'userinfo.html', 
        title=userinfo['login'], 
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
    app.run(host='0.0.0.0',port=8000)