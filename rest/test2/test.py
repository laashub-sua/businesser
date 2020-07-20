from flask import Blueprint

app = Blueprint('test2.test', __name__, url_prefix='/test2/test')


@app.route('/test', methods=['POST'])
def test():
    pass
