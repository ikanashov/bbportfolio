from functools import wraps

from flask import Flask, render_template, flash, redirect, request, Request, make_response

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, length

from core.config import config
from service.blackboard import BlackBoard
from service.vuz1c import Vuz1C


class SearchForm(FlaskForm):
    search_lastname = StringField(
        label = 'Поиск по фамилии', 
        description = 'Введите фамилию',
        render_kw = {"placeholder": "Введите фамилию"},
        validators = [DataRequired(), length(min=2, max=20)]
    )
    submit = SubmitField(label = 'Найти')


# Наивная проверка на авторизацию в ББ,
# если пользователь авторизован то у него стоит cookies web_client_cache_guid
# в принтах идеи для дальнейшей проверки действительно ли пользователь залогинен
# но пока пойдет и так
def authrequired(target):
    @wraps(target)
    def _is_auth(*args, **kwargs):
        if request.cookies.get('web_client_cache_guid') != None:
            print(request.cookies.get('web_client_cache_guid'))
            print(request.user_agent.string)
            print(request.remote_addr)
            print(request.access_route[0])
            return target(*args, **kwargs)
        flash('Для получения доступа к портфолио необходимо войти в систему BlackBoard')
        response = make_response(render_template('authrequired.html'), 401)
        # return response
        return target(*args, **kwargs)
    return _is_auth


vuz = Vuz1C()

app = Flask('portfolio_service')
app.config['SECRET_KEY'] = config.FLASK_SECRET_KEY


@app.route('/portfolio', strict_slashes=False)
@app.route('/portfolio/faculty', strict_slashes=False)
@authrequired
def portfolio_groups() -> str:
    form = SearchForm()
    faculties = vuz.get_faculty()
    return render_template(
        'facultylist.html',
        title = 'Портфолио студента "Уральский Государственный университет путей сообщения"',
        faculties = faculties,
        form = form
    )

@app.route('/portfolio/faculty/<faculty_name>', methods=['GET'], strict_slashes=False)
@authrequired
def porfolio_faculty_groups(faculty_name: str) -> str:
    groups = vuz.get_groups(faculty_name)
    return render_template(
        'grouplist.html',
        title = 'Группы факультета — ' + faculty_name,
        groups = groups,
        faculty_name = faculty_name,
        backbutton = {'link': '/portfolio/', 'text': 'Вернуться назад'}
    )

@app.route('/portfolio/faculty/<faculty_name>/group/<group_name>', methods=['GET'], strict_slashes=False)
@authrequired
def portfolio_users_in_group(faculty_name: str, group_name: str) -> str:
    users = vuz.get_users_in_group(group_name)
    return render_template(
        'usersingroup.html', 
        title = 'Портфолио студентов группы — ' + group_name, 
        users = users,
        faculty_name =  faculty_name,
        group_name = group_name,
        backbutton = {'link': '/portfolio/faculty/' + faculty_name, 'text': 'Вернуться назад'}
        )

@app.route('/portfolio/faculty/<faculty_name>/group/<group_name>/<user_id>', methods=['GET'], strict_slashes=False)
@app.route('/portfolio/<user_id>', methods=['GET'], strict_slashes=False)
@authrequired
def portfolio_user_info(user_id: str, faculty_name: str = None, group_name: str = None) -> str:
    pfl = BlackBoard()
    backurl = '/portfolio/faculty/' + faculty_name + '/group/' + group_name if (faculty_name and group_name) else '/portfolio/'
    userinfo = pfl.get_user_info(user_id)
    return render_template(
        'userinfo.html', 
        title = userinfo['login'], 
        userinfo = userinfo,
        backbutton = {'link': backurl, 'text': 'Вернуться назад'}
        )

@app.route('/portfolio/faculty/<faculty_name>/group/<group_name>/<user_id>/activity', methods=['GET'], strict_slashes=False)
@app.route('/portfolio/<user_id>/activity', methods=['GET'], strict_slashes=False)
@authrequired
def portfolio_user_activity(user_id: str, faculty_name: str = None, group_name: str = None) -> str:
    pfl = BlackBoard()
    backurl = '/portfolio/faculty/' + faculty_name + '/group/' + group_name + '/' + user_id if (faculty_name and group_name) else '/portfolio/' + user_id
    userinfo = pfl.get_user_info(user_id)
    useractivity = pfl.get_user_activity(user_id)
    return render_template(
        'useractivity.html', 
        title=userinfo['login'], 
        userinfo = userinfo, 
        useractivity = useractivity,
        backbutton = {'link': backurl, 'text': 'Вернуться назад'}
        )

@app.route('/portfolio/faculty/<faculty_name>/group/<group_name>/<user_id>/courses', methods=['GET'], strict_slashes=False)
@app.route('/portfolio/<user_id>/courses', methods=['GET'], strict_slashes=False)
@authrequired
def portfolio_user_courses(user_id: str, faculty_name: str = None, group_name: str = None) -> str:
    pfl = BlackBoard()
    backurl = '/portfolio/faculty/' + faculty_name + '/group/' + group_name + '/' + user_id if (faculty_name and group_name) else '/portfolio/' + user_id
    userinfo = pfl.get_user_info(user_id)
    usercourses = pfl.get_user_courses(user_id)
    return render_template(
        'usercourses.html', 
        title=userinfo['login'], 
        userinfo = userinfo, 
        usercourses = usercourses,
        backbutton = {'link': backurl, 'text': 'Вернуться назад'}
        )

@app.route('/portfolio/faculty/<faculty_name>/group/<group_name>/<user_id>/courses/<course_user_id>', methods=['GET'], strict_slashes=False)
@app.route('/portfolio/<user_id>/courses/<course_user_id>', methods=['GET'], strict_slashes=False)
@authrequired
def portfolio_user_grade_in_course(user_id: str, course_user_id: str, faculty_name: str = None, group_name: str = None) -> str:
    pfl = BlackBoard()
    backurl = '/portfolio/faculty/' + faculty_name + '/group/' + group_name + '/' + user_id + '/courses' if (faculty_name and group_name) else '/portfolio/' + user_id + '/courses'
    userinfo = pfl.get_user_info(user_id)
    courseinfo = pfl.get_course_by_course_users_id(course_user_id)
    usergrades = pfl.get_user_grade_on_course(course_user_id)
    return render_template(
        'usergrade.html', 
        title=userinfo['login'], 
        userinfo = userinfo,
        courseinfo = courseinfo,
        usergrades = usergrades,
        backbutton = {'link': backurl, 'text': 'Вернуться назад'}
        )

@app.route('/portfolio/search', methods=['POST'], strict_slashes=False)
@authrequired
def portfolio_search_users() -> str:
    form = SearchForm()
    if form.validate_on_submit():
        users = vuz.search_users(form.search_lastname.data)
        return render_template(
            'userssearch.html', 
            title = 'Результат поиска студентов по фамилии — ' + form.search_lastname.data, 
            users = users,
            backbutton = {'link': '/portfolio/', 'text': 'Вернуться назад'}
            )
    flash('Необходимо ввести фамилию студента (min - 2 символа, max - 20 символов)')
    return redirect('/portfolio')

@app.route('/', methods=['GET'])
def movies_deafault() -> str:
    #Страница по умолчанию
    return 'Enjoy the silence'


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8001)