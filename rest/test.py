from flask import Blueprint

app = Blueprint('test', __name__, url_prefix='/test')


@app.route('/test', methods=['POST'])
def test():
    pass
