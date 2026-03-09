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
from celery_setup import celery_init_app
from celery.schedules import crontab
from tasks.test import monthly_report, comp_monthly_report, daily_remainder
from flask import jsonify



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
  security.init_app(app, datastore = datastore)

  app.datastore = datastore

  app.register_blueprint(auth)
  app.register_blueprint(student)
  app.register_blueprint(company)

  app.register_blueprint(stud_api_bp)
  app.register_blueprint(comp_api_bp)
  app.register_blueprint(admin_api_bp)

  cache.init_app(app)


  # celery config
  app.config.from_mapping(
     CELERY=dict(
        broker_url="redis://localhost:6379/0",
        result_backend="redis://localhost:6379/1",
        timezone = 'Asia/Kolkata'
      ),
  )
  celery = celery_init_app(app)
  celery.autodiscover_tasks()

  # @app.route('/cache')
  # @cache.cached(timeout=1)
  # def cache():
  #     print("function executed")
  #     return {"date" : str(datetime.utcnow())}


  with app.app_context():
    db.create_all()
  return app, celery

app, celery = create_app()


from tasks.test import add
@app.route("/celery-tasks")
def task():
  add.delay(1,2)
  return {"message": "task started"}

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
  sender.add_periodic_task(
    crontab(hour=10, minute=31, day_of_month=1),
    # crontab(minute='*/2'),
    monthly_report.s(),
    )
  
  sender.add_periodic_task(
    crontab(hour=10, minute=31, day_of_month=1),
    # crontab(minute='*/2'),
    comp_monthly_report.s(),
    )
  
  sender.add_periodic_task(
    crontab(hour=10, minute=30, day_of_week="*"),
    # crontab(minute='*/2'),
    daily_remainder.s(),
    )

if __name__ == "__main__":
  app.run()