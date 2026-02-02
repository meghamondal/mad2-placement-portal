from flask import Flask
from config import LocalDevelopmentConfig
from dotenv import load_dotenv

def create_app():

  app = Flask(__name__)
  load_dotenv()
  app.config.from_object(LocalDevelopmentConfig)
  from models import db, User, Role
  db.init_app(app)

  from flask_security.datastore import SQLAlchemyUserDatastore
  from extensions import security

  datastore = SQLAlchemyUserDatastore(db, User, Role)
  security.init_app(app, datastore = datastore)#register_blueprint=False

  app.datastore = datastore
  # for trail
  with app.app_context():
    db.create_all()
  return app

app = create_app()

if __name__ == "__main__":
  app.run()