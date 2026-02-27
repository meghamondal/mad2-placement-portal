from flask import Flask
from config import LocalDevelopmentConfig
from dotenv import load_dotenv
from api.auth import auth
from api.student import student, stud_api, stud_api_bp
from api.company import company, comp_api_bp
from api.admin import admin_api_bp
from flask_cors import CORS
from datetime import datetime
from flask_caching import Cache
from extensions import cache


def create_app():

  app = Flask(__name__)
  load_dotenv()
  app.config.from_object(LocalDevelopmentConfig)
  from models import db, User, Role
  db.init_app(app)
  CORS(app)

  from flask_security.datastore import SQLAlchemyUserDatastore
  from extensions import security, cache

  datastore = SQLAlchemyUserDatastore(db, User, Role)
  security.init_app(app, datastore = datastore)#register_blueprint=False

  app.datastore = datastore

  app.register_blueprint(auth)
  app.register_blueprint(student)
  app.register_blueprint(company)

  app.register_blueprint(stud_api_bp)
  app.register_blueprint(comp_api_bp)
  app.register_blueprint(admin_api_bp)

  cache.init_app(app)

  @app.route('/cache')
  @cache.cached(timeout=1)
  def cache():
      print("function executed")
      return {"date" : str(datetime.utcnow())}



  # for trail
  with app.app_context():
    db.create_all()
  return app

app = create_app()

# from datetime import time

if __name__ == "__main__":
  app.run()