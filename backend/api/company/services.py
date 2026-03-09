from models import Company, Placement_drive, Application, Student, Interview, db, User
from sqlalchemy import or_
from datetime import datetime


class ServiceError(Exception):
  "base error for service"


class CompanyService():

  #get company details
  @staticmethod
  def comp_details(c_id):
    comp = Company.query.filter_by(c_id = c_id).first()
    if not comp:
      raise ServiceError("Company details does not exists...", 404)
    return comp
  
  #edit company details
  @staticmethod
  def edit_details(c_id, data):
    comp = Company.query.filter_by(c_id=c_id).first()
    if not comp:
      raise ServiceError("Company details does not exists...", 404)
    
    editable_fields = ["c_name", "hr_contact", "website", "industry"]
    for key, value in data.items():
      if key in editable_fields and value is not None:
        setattr(comp, key, value)
    db.session.commit()
    print("new data", data)
    return comp
  
  #create placement drives
  @staticmethod
  def create_placement_drives(c_id, data):
    comp = Company.query.get(c_id)
    if comp is None:
      raise ServiceError("Company does not exists...", 404)
    if comp.approval_status != "approved":
      raise ServiceError("Company is not approved by the admin...", 403)
    if comp.approval_status == "rejected":
      raise ServiceError("Company is  rejected by the admin...", 403)
    
    pd = Placement_drive(
      c_id = c_id,
      job_title=data.get("job_title"),
      job_description=data.get("job_description"),
      eligible_branch=data.get("eligible_branch"),
      min_cgpa=data.get("min_cgpa"),
      eligible_year=data.get("eligible_year"),
      application_deadline=data.get("application_deadline"),
      pd_status=data.get("pd_status")
    )
    db.session.add(pd)
    db.session.commit()
    return pd
  
  #edit p_drives details
  @staticmethod
  def edit_pddetails(c_id, pd_id,data):
    pd = Placement_drive.query.filter_by(pd_id=pd_id).first()
    if not pd:
      raise ServiceError("Placement Drive details does not exists...", 404)
    
    if pd.c_id != c_id:
      raise ServiceError("Placement Drive details cannot be accessed...", 403)
    
    editable_fields = ["job_title", "job_description", "eligible_branch", "min_cgpa", "eligible_year", "application_deadline"]
    for key, value in data.items():
      if key in editable_fields and value is not None:
        setattr(pd, key, value)
    db.session.commit()
    print("new data", data)
    return pd
  

  #get placement drives associated with respective company id
  @staticmethod
  def get_pd_list(c_id):
    comp_pd = Placement_drive.query.filter_by(c_id = c_id).all()
    return comp_pd
  
  @staticmethod
  def pd_details(pd_id):
    pd = Placement_drive.query.filter_by(pd_id = pd_id).all()
    if not pd:
      raise ServiceError("Placement Drive details does not exists...", 404)
    return pd 
  
  #list of all the application(applicants)  associated to a particular placement drive
  @staticmethod
  def get_pd_app(pd_id):
    pd = Placement_drive.query.get(pd_id)
    if pd is None:
      raise ServiceError("pd_Drive not found...")
    applicants = Application.query.filter_by(pd_id=pd_id).all()
    return applicants
  
  #edit the status of the application
  @staticmethod
  def edit_applicants_status(app_id, app_status): 
    app = Application.query.filter_by(app_id = app_id).first()
    if app is None:
      raise ServiceError("Applicant does not exists...", 404)
    pd = Placement_drive.query.get(app.pd_id)
    if pd is None:
      raise ServiceError("pd_Drive not found...", 404)
    
    status = ["applied", "shortlisted", "selected", "rejected"]
    if app_status not in status:
      raise ServiceError("Invalid Status", 400)
    
    app.app_status = app_status
    db.session.commit()
    return app
  
  @staticmethod
  def pd_count(c_id):
    total_pd = Placement_drive.query.filter_by(c_id=c_id).count()
    return total_pd
  
  @staticmethod
  def active_pd_count(c_id):
    atotal_pd = Placement_drive.query.filter(Placement_drive.c_id==c_id, Placement_drive.application_deadline > datetime.now()).count()
    return atotal_pd
  
  @staticmethod
  def app_count(c_id):
    total_app = Application.query.join(Placement_drive).filter(Placement_drive.c_id==c_id).count()
    return total_app
  
  @staticmethod
  def short_app_count(c_id):
    total_short_app = Application.query.join(Placement_drive).filter(Placement_drive.c_id==c_id, Application.app_status == "shortlisted").count()
    return total_short_app
  
  @staticmethod
  def short_app_list(comp_id):
    short_app = Application.query.join(Placement_drive).filter(Placement_drive.c_id == comp_id,or_(Application.app_status == "shortlisted", Application.app_status == "interview scheduled")).all()
    return short_app
  
  @staticmethod
  def schedule_interview(app_id, data):
    app = Application.query.get(app_id)
    if app is None:
      raise ServiceError("Application does not exists...", 404)
    if app.app_status != "shortlisted":
      raise ServiceError("Application is not shortlisted by the company...", 403)
    if app.app_status == "rejected":
      raise ServiceError("application is  rejected by the company...", 403)
    stud = Student.query.get(app.stud_id)
    if stud is None:
      raise ServiceError("Student is deleted by the admin", 404)
    user = User.query.get(stud.stud_id)
    if not user.active:
      raise ServiceError("Student account is deactivated by the admin", 403)
    
    intw = Interview(
      app_id = app_id,
      scheduled=data.get("scheduled"),
      intw_status="scheduled",
      remarks=data.get("remarks"),
    )
    app.app_status = "interview scheduled"
    db.session.add(intw)
    db.session.add(app)
    db.session.commit()
    return intw
  
  @staticmethod
  def edit_intw_pass(app_id):
    app = Application.query.filter_by(app_id = app_id).first()
    if not app:
      raise ServiceError("Application not found...", 404)
    if app.app_status != "interview scheduled":
      raise ServiceError("Interview is not scheduled for this application...", 400)
    intw = Interview.query.filter_by(app_id=app_id).first()
    if not intw:
      raise ServiceError("Interview related to this application id not found...", 404)
    if intw.scheduled > datetime.now():
      raise ServiceError("Interview is not completed yet...", 400)
    intw.intw_status = "passed"
    app.app_status = "selected"

    db.session.commit()
    return app
  
  @staticmethod
  def edit_intw_fail(app_id):
    app = Application.query.filter_by(app_id = app_id).first()
    if not app:
      raise ServiceError("Application not found...", 404)
    if app.app_status != "interview scheduled":
      raise ServiceError("Interview is not scheduled for this application...", 400)
    intw = Interview.query.filter_by(app_id=app_id).first()
    if not intw:
      raise ServiceError("Interview related to this application id not found...", 404)
    if intw.scheduled > datetime.now():
      raise ServiceError("Interview is not completed yet...", 400)
    intw.intw_status = "failed"
    app.app_status = "rejected"

    db.session.commit()
    return app