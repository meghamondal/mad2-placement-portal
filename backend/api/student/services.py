from models import Student, Placement_drive, Application, db, User
from flask_security import current_user
from datetime import datetime

class ServiceError(Exception):
  pass

class StudentService():

  #get student details
  @staticmethod
  def stud_details(stud_id):
    stud = Student.query.filter_by(stud_id = stud_id).first()
    if not stud:
      raise ServiceError("Student details does not exists...", 404)
    return stud
  
  #edit student details
  @staticmethod
  def edit_details(stud_id, data):
    stud = Student.query.filter_by(stud_id=stud_id).first()
    if not stud:
      raise ServiceError("Student details does not exists...", 404)
    
    editable_fields = ["f_name", "l_name", "cgpa", "resume_file", "dob", "graduation_year"]
    for key, value in data.items():
      if key in editable_fields and value is not None:
        setattr(stud, key, value)
    db.session.commit()
    print("new data", data)
    return stud
  
  
  #get placement drives
  @staticmethod
  def get_placement_drives(stud_id):
    stud = Student.query.get(stud_id)
    pdrives = Placement_drive.query.filter(Placement_drive.pd_status=="Approved", Placement_drive.min_cgpa<=stud.cgpa).all()
    return pdrives
  
  #apply to pdrive
  @staticmethod
  def apply_to_pdrive(stud_id, pd_id):
    drive = Placement_drive.query.get(pd_id)
    if drive is None:
      raise ServiceError("Drive details does not exists...", 404)
    if drive.application_deadline < datetime.now():
      raise ServiceError("Application deadline passed...", 400)
    #chercking for duplicates
    existing = Application.query.filter_by(stud_id = stud_id, pd_id = pd_id).first()
    if existing:
      raise ServiceError("Already applied...", 400)
    app = Application(stud_id = stud_id, pd_id = pd_id, app_status = "applied")

    db.session.add(app)
    db.session.commit()
    return app
  
  #get application history
  @staticmethod
  def get_app_history(stud_id):
    app = Application.query.filter_by(stud_id = stud_id).all()
    return app