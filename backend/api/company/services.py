from models import Company, Placement_drive, Application, Student, db
from datetime import datetime

class ServiceError(Exception):
  pass

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
    
    editable_fields = ["c_name", "hr_contact", "website", "approval_status"]
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
  
  #get placement drives associated with respective company id
  @staticmethod
  def get_app_list(c_id):
    comp_pd = Placement_drive.query.filter_by(c_id = c_id).all()
    return comp_pd
  
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
    