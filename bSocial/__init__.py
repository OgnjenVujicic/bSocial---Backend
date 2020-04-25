from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_argon2 import Argon2
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = '4321628bb0b13ce0c676dfjf280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JSON_SORT_KEYS'] = False
db = SQLAlchemy(app)
argon2 = Argon2(app)
CORS(app)

#enables foregin key in sqlite
if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
    def _fk_pragma_on_connect(dbapi_con, con_record): 
        dbapi_con.execute('pragma foreign_keys=ON')

    with app.app_context():
        from sqlalchemy import event
        event.listen(db.engine, 'connect', _fk_pragma_on_connect)

from bSocial import routes