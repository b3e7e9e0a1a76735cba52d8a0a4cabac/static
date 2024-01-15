from subprocess import check_output
from flask import Blueprint, render_template, request, jsonify

vuln = Blueprint('vuln', __name__)


@vuln.route('/', methods=['GET'])
def root():
    return render_template('index.html')


@vuln.route('/api/<type>', methods=['GET'])
def hex_digit(type):
    match type:
        case 'hex':
            value = request.args.get("value")
            black_list = ['ls', 'dir', 'whoami', 'id', 'python', 'who', 'echo', 'last', 'ping', 'nslookup', 'uname', 'ps', ';', '&', ' ']
            for q in black_list:
                value = value.replace(q, '')
            cmd = f'python3 -c "print(hex({value}))"'
            print(cmd)
            try:
                result = check_output(cmd, shell=True, timeout=5).decode()
                return f'Hex-представление: {result}'
            except:
                return 'Ошибка преобразования числа в hex!'