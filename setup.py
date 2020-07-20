from __init__ import app
from config import config_data

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=config_data['application']["server"]["port"],
        debug=False
    )
