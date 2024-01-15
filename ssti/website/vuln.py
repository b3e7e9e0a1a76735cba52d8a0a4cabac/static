from flask import Blueprint, render_template, request, make_response, redirect, render_template_string, abort

vuln = Blueprint('vuln', __name__)


@vuln.route('/', methods=['GET'])
def root():
    return render_template('index.html')


@vuln.route('/search', methods=['GET'])
def search():
    q = request.args.get('q')
    black_list = ["self", "config", "import", "class", "subclasses", "bultins", "getitem", "application", "read"]
    for v in black_list:
        q = q.replace(v, '')
    if q:
        try:
            query = render_template_string(q)
            content = f'По вашему запросу {query} ничего не найдено'
            return render_template('search.html', content=content)
        except:
            content = 'Ошибка запроса'
            return render_template('search.html', content=content)
    else:
        return abort(403)

