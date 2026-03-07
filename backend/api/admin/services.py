from models import Student, Company, Placement_drive, Application, User, db
import os



class ServiceError(Exception):
  "base error for service"

class AdminService():

  @staticmethod
  def stud_count():
    total_stud = Student.query.count()
    return total_stud
      
  
  @staticmethod
  def stud_details(stud_id):
    stud = Student.query.filter_by(stud_id = stud_id).all()
    for s in stud:
      user_cred = User.query.filter_by(u_id = s.stud_id).first()
      s.active = user_cred.active
    if not stud:
      raise ServiceError("Student details does not exists...", 404)
    return stud
  
  staticmethod
  def get_stud_list():
    stud = Student.query.all()
    return stud
  
  @staticmethod
  def delete_stud(stud_id):
    stud = Student.query.filter_by(stud_id = stud_id).first()
    user = User.query.get(stud.stud_id)
    if stud is None:
      raise ServiceError("Student details does not exists...", 404)
    app = Application.query.filter_by(stud_id=stud_id).delete()
    if stud.resume_file:
      os.remove(stud.resume_file)
    db.session.delete(stud)
    db.session.delete(user)
    db.session.commit()
    return "Deleted Successfully", 200
  
  @staticmethod
  def edit_stud_active(stud_id):
    user = User.query.get(stud_id)
    if not user:
      raise ServiceError("User not found...", 404)
    user.active = not user.active
    db.session.commit()
    return user


  @staticmethod
  def comp_count():
    total_comp = Company.query.count()
    return total_comp
  
  @staticmethod
  def comp_details(c_id):
    comp = Company.query.filter_by(c_id = c_id).all()
    for c in comp:
      user_cred = User.query.filter_by(u_id = c.c_id).first()
      c.active = user_cred.active
    if not comp:
      raise ServiceError("Company details does not exists...", 404)
    return comp
  
  @staticmethod
  def get_comp_list():
    comp = Company.query.all()
    return comp
  
  @staticmethod
  def get_comp_list_p():
    comp_p = Company.query.filter_by(approval_status="pending").all()
    return comp_p
  
  @staticmethod
  def edit_company_status(c_id, approval_status): 
    comp = Company.query.filter_by(c_id = c_id).first()
    if comp is None:
      raise ServiceError("Company does not exists...", 404)    
    status = ["pending", "approved", "rejected"]
    if approval_status not in status:
      raise ServiceError("Invalid Status", 400)
    
    comp.approval_status = approval_status
    user = User.query.get(c_id)
    if user:
      if approval_status == "approved":
        user.active = True
      else:
        user.active = False

    db.session.commit()
    return comp
  
  @staticmethod
  def delete_comp(c_id):
    # comp = Company.query.filter_by(c_id = c_id).first()
    comp = Company.query.get(c_id)
    user = User.query.get(comp.c_id)
    if comp is None:
      raise ServiceError("Company details does not exists...", 404)
    db.session.delete(comp)
    db.session.delete(user)
    db.session.commit()
    return {"message": "Deleted Successfully"}, 200
  
  @staticmethod
  def edit_comp_active(c_id):
    user = User.query.get(c_id)
    if not user:
      raise ServiceError("User not found...", 404)
    user.active = not user.active
    comp = Company.query.get(c_id)
    if not comp:
      raise ServiceError("Company not found...", 404)
    if user.active is False:
      comp.approval_status = "blocked"
    elif user.active:
      comp.approval_status = "approved"
    db.session.commit()
    return user, comp

 
  @staticmethod
  def pd_count():
    total_pd = Placement_drive.query.count()
    return total_pd
      
  @staticmethod
  def get_pd_list():
    pd = Placement_drive.query.all()
    return pd
  
  @staticmethod
  def pd_details(pd_id):
    pd = Placement_drive.query.filter_by(pd_id = pd_id).all()
    if not pd:
      raise ServiceError("Placement Drive details does not exists...", 404)
    return pd 
  
  @staticmethod
  def edit_pd_status(pd_id, pd_status): 
    pd = Placement_drive.query.filter_by(pd_id = pd_id).first()
    if pd is None:
      raise ServiceError("Placement Drive does not exists...", 404)
    
    status = ["pending", "approved", "rejected"]
    if pd_status not in status:
      raise ServiceError("Invalid Status", 400)
    
    comp = Company.query.get(pd.c_id)
    if not comp:
      raise ServiceError("Company related to this placement drive is not found...", 404)
    
    pd.pd_status = pd_status
    
    if comp.approval_status == "pending":
      pd.pd_status = "pending"
    else:
      pd.pd_status = pd_status
    db.session.commit()
    return pd
  
  @staticmethod
  def get_pd_list_p():
    pd_p = Placement_drive.query.filter_by(pd_status="pending").all()
    return pd_p
  
  @staticmethod
  def get_app_list():
    app = Application.query.all()
    return app
  


