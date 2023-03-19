from flask import Flask
# from controllers import *
from models import Users, Role
from flask_security import Security, SQLAlchemySessionUserDatastore
from config import *
from database import db
from flask_cors import CORS


app= None
def create_app():
  app = Flask(__name__)
  app.config.from_object(LocalDevelomentConfig)
  db.init_app(app)
  app.app_context().push()
  db.create_all()
  user_datastore = SQLAlchemySessionUserDatastore(db.session,Users,Role)
  security = Security(app,user_datastore)
  return app

app = create_app()
CORS(app)

from controllers import *
#------------------Database init------------------------------------
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///BlogLiteDatabase.sqlite3"
# app.app_context().push()
# db.init_app(app)
# db.create_all()

# user_datastore = SQLAlchemyUserDatastore(db.session,Users)
# security = Security(app,user_datastore)
#---------------------------------------------------------------------



if __name__ == '__main__':
  app.debug = True
  app.run() 