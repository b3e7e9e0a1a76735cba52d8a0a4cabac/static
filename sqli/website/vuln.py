import uuid

import mysql.connector
from flask import Blueprint, render_template, request, jsonify


def sql_query(query, json=False):
    irp_db = mysql.connector.connect(
        host="172.16.0.104",
        user="sql",
        password="sql",
        database="lab_sqli"
    )
    db_cursor = irp_db.cursor(dictionary=json)
    result = db_cursor.execute(query)
    content = db_cursor.fetchall()
    irp_db.commit()
    irp_db.close()
    return result, content


vuln = Blueprint('vuln', __name__)


@vuln.route('/', methods=['GET'])
def root():
    return render_template('index.html')


@vuln.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        table = 'users'
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        query = f"SELECT email, password FROM {table} WHERE email = '{email}'"
        try:
            result, credentials = sql_query(query, json=True)

            if credentials:
                if password == credentials[0]['password'] and email == credentials[0]['email']:
                    return 'FLAG'
                else:
                    return render_template('login.html')
            else:
                return render_template('login.html')
        except:
            return render_template('login.html')


@vuln.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')


@vuln.route('/api/<type>', methods=['GET', 'POST'])
def xss_func(type):
    match type:
        case 'orders':
            id = request.args.get("id")
            table = 'orders'
            query = f"SELECT id, source, destination, status, info, recipient FROM {table} WHERE id = ('{id}')"
            try:
                result, responses = sql_query(query, json=True)
                if responses:
                    output = ""
                    for response in responses:
                        output += f"<h5>Заказ: {response['id']}<br>" \
                                 f"Путь: {response['source']} - {response['destination']}<br>" \
                                 f"Статус: {response['status']}<br>" \
                                 f"Содержимое: {response['info']}<br>" \
                                 f"Получатель: {response['recipient']}<br><br><h5>"
                    return output
                else:
                    return 'Заказ не найден, проверьте корректность ввода'
            except:
                return 'Заказ не найден, проверьте корректность ввода'

        case 'ticket':
            if request.method == 'POST':
                uid = str(uuid.uuid4())
                status = 'В работе'
                name = request.form['name']
                email = request.form['email']
                subject = request.form['subject']
                text = request.form['text']

                table = 'tickets'
                query = f"INSERT INTO {table} VALUES ('{uid}', '{status}', '{name}', '{email}', '{subject}', '{text}')"
                try:
                    sql_query(query, False)
                    return f'Ваша заявка <b>{uid}</b> была отправлена! Проверить статус заявки можно по форме ниже'
                except Exception as e:
                    return 'Ошибка отправки заявки, повторите попытку позже'
            else:
                id = request.args.get('id')

                black_list = ['-- -', '--', '/*', '*/', '#']

                for q in black_list:
                    id = id.replace(q, '')

                table = 'tickets'
                query = f"SELECT status FROM {table} WHERE uid = ('{id}')"

                try:
                    result, content = sql_query(query, True)
                    content = content[0]['status']
                except:
                    return 'Заявка с данным ID не найдена'

                if content is not None:
                    return f'Статус вашей заявки: <b>{content}</b>'
                else:
                    return 'Заявка с данным ID не найдена'






