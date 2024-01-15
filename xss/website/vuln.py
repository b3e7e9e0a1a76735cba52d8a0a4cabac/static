import mysql.connector
import hashlib
from flask import Blueprint, render_template, request, make_response, redirect
from apscheduler.schedulers.background import BackgroundScheduler
from selenium import webdriver
from urllib.parse import urlparse


vuln = Blueprint('vuln', __name__)


def sql_query(query, json=False):
    irp_db = mysql.connector.connect(
        host="172.16.0.104",
        user="sql",
        password="sql",
        database="lab_xss"
    )
    db_cursor = irp_db.cursor(dictionary=json)
    result = db_cursor.execute(query)
    content = db_cursor.fetchall()
    irp_db.commit()
    irp_db.close()
    return result, content


def admin_check_url():
    table = "appeals"
    result, urls = sql_query(f"SELECT text FROM {table}", True)

    op = webdriver.ChromeOptions()
    op.add_argument('--headless')
    op.add_argument('--disable-dev-shm-usage')
    op.add_argument("--no-sandbox");

    driver = webdriver.Chrome(options=op)

    admin_cookie = 'c2a5d79fc4fe27badf027b35cb4b312d'

    for url in urls:
        vuln = url['text']
        vuln = vuln.replace('+', '%2b')
        u = urlparse(vuln)
        u = u.scheme + '://' + u.netloc
        print(u)
        driver.get(u)
        driver.add_cookie({'name': 'session_cookie', 'value': admin_cookie, 'path': '/'})
        driver.get(vuln)
    driver.close()
    sql_query(f"DELETE FROM {table} WHERE email='None'", True)


@vuln.route('/ask', methods=['GET'])
def password():
    if request.method == 'GET':
        text = request.args.get('text')
        if text:
            table = 'appeals'
            email = request.cookies.get('email')
            content = f"Ваш вопрос: <b>{text}</b><br>" \
                   "Обращение принято в работу. Ответ поступит на указанный электронный адрес вашего аккаунта."

            query = f'INSERT INTO {table} VALUES ("{email}", "{text}")'
            sql_query(query)

            resp = make_response(render_template('ask.html', content=content))
            return resp
        else:
            return render_template('ask.html')


@vuln.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        table = "users"
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        query = f"SELECT email, password FROM {table} WHERE email = '{email}'"
        result, credentials = sql_query(query, json=True)

        if credentials:
            if hashlib.md5(password.encode()).hexdigest() == credentials[0]['password']:
                session_cookie = f"{email}:{credentials[0]['password']}"
                session_cookie = hashlib.md5(session_cookie.encode()).hexdigest()
                query = f"UPDATE {table} SET cookie='{session_cookie}' WHERE email='{email}';"
                sql_query(query)
                resp = make_response('1')
                resp.set_cookie('session_cookie', session_cookie)
                resp.set_cookie('email', email)
                return resp
            else:
                return '2'
        else:
            return '3'


@vuln.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        table = "users"
        first_name = request.form['inputFirstName']
        last_name = request.form['inputLastName']
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        query = f"SELECT email FROM {table} WHERE email = '{email}'"
        result, check_user = sql_query(query)

        if not check_user:
            query = f"INSERT INTO {table} VALUES ('{email}', '{first_name}', '{last_name}', '{hashlib.md5(password.encode()).hexdigest()}', '', 0)"
            try:
                sql_query(query, False)
                return '1'
            except:
                return '3'
        else:
            return '2'


@vuln.route('/', methods=['GET'])
def root():
    email = request.cookies.get('email')
    session_cookie = request.cookies.get('session_cookie')

    table = "users"
    query = f"SELECT cookie, is_admin FROM {table} WHERE email = '{email}'"
    result, cookie = sql_query(query, json=True)
    if cookie:
        if session_cookie == cookie[0]['cookie']:
            if cookie[0]['is_admin']:
                return render_template('success.html')
            return render_template('404.html')
        else:
            return make_response(redirect('/login', code=302))
    else:
        return make_response(redirect('/login', code=302))


scheduler = BackgroundScheduler()
scheduler.add_job(admin_check_url, 'interval', seconds=60, id='my_job_id')
scheduler.start()

