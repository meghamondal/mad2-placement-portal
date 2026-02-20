from flask_restful import Resource, fields, marshal_with, reqparse, request
from flask_security import auth_required, roles_required, current_user
from api.admin.services import AdminService
from datetime import datetime

student_fields = {
  "stud_id": fields.Integer,
  "f_name": fields.String,
  "l_name": fields.String,
  "resume_file": fields.String,
  "dob": fields.DateTime,
  "graduation_year": fields.Integer,
  "cgpa": fields.Float
}

company_fields = {
   "c_id": fields.Integer,
   "c_name": fields.String,
   "hr_contact": fields.String,
   "website": fields.String,
   "approval_status": fields.String
}

pd_fields = {
  "pd_id": fields.Integer,
  "c_id": fields.Integer,
  "job_title": fields.String,
  "job_description": fields.String,
  "eligible_branch": fields.String,
  "min_cgpa": fields.Float,
  "eligible_year": fields.Integer,
  "application_deadline": fields.DateTime,
  "pd_status": fields.String,
  'company_details': fields.Nested(company_fields, attribute='company')
}

app_fields = {
  "app_id": fields.Integer,
  "stud_id": fields.Integer,
  "pd_id": fields.Integer,
  "app_status": fields.String,
  "student_details": fields.Nested(student_fields, attribute='student'),
  "pd_details": fields.Nested(pd_fields, attribute='placement_d')
}

compstatus_parser = reqparse.RequestParser()
compstatus_parser.add_argument("approval_status", type=str, required=True)

pdstatus_parser = reqparse.RequestParser()
pdstatus_parser.add_argument("pd_status", type=str, required=True)

class CountResource(Resource):
  @auth_required("token")
  @roles_required("admin")
  def get(self):
    return{
      "student_count": AdminService.stud_count(),
      "company_count": AdminService.comp_count(),
      "pd_count": AdminService.pd_count()
  }

class AdminStudResource(Resource):
  @auth_required("token")
  @roles_required("admin")
  @marshal_with(student_fields)
  def get(self, stud_id):
    stud_details = AdminService.stud_details(stud_id)
    return stud_details
  
  @auth_required("token")
  @roles_required("admin")
  def delete(self, stud_id):
    AdminService.delete_stud(stud_id)
    return {"message": "Student deleted successfully"}, 200

class AdminStudListResource(Resource):
  @auth_required("token")
  @roles_required("admin")
  @marshal_with(student_fields)
  def get(self):
    return AdminService.get_stud_list()
  
class AdminStudActiveEditResource(Resource):
  @auth_required("token")
  @roles_required("admin")
  def patch(self, stud_id):
    stud_edit = AdminService.edit_stud_active(stud_id)
    return {"message": "Student active status updated successfully..."}, 200
  

  
class AdminCompResource(Resource):
  @auth_required("token")
  @roles_required("admin")
  @marshal_with(company_fields)
  def get(self, c_id):
    comp_details = AdminService.comp_details(c_id)
    return comp_details
  
  @auth_required("token")
  @roles_required("admin")
  def delete(self, c_id):
    AdminService.delete_comp(c_id)
    return {"message": "Company deleted successfully"}, 200
  
class AdminCompListResource(Resource):
  @auth_required("token")
  @roles_required("admin")
  @marshal_with(company_fields)
  def get(self):
    return AdminService.get_comp_list()
  
class AdminCompPendingListResource(Resource):
  @auth_required("token")
  @roles_required("admin")
  @marshal_with(company_fields)
  def get(self):
    return AdminService.get_comp_list_p()
  
class AdminCompEditResource(Resource):
  @auth_required("token")
  @roles_required("admin")
  @marshal_with(company_fields)
  def patch(self, c_id):
    args = compstatus_parser.parse_args()
    args = dict(filter(lambda item: item[1] is not None, args.items()))# removes empty parser values (the one which is having None)
    comp_edit = AdminService.edit_company_status(c_id, args["approval_status"])
    return comp_edit
  
class AdminCompActiveEditResource(Resource):
  @auth_required("token")
  @roles_required("admin")
  def patch(self, c_id):
    comp_edit = AdminService.edit_comp_active(c_id)
    return {"message": "Company active status updated successfully..."}, 200
  
class AdminpdResource(Resource):
  @auth_required("token")
  @roles_required("admin")
  @marshal_with(pd_fields)
  def get(self, pd_id):
    pd_details = AdminService.pd_details(pd_id)
    return pd_details
  
class AdminPdListResource(Resource):
  @auth_required("token")
  @roles_required("admin")
  @marshal_with(pd_fields)
  def get(self):
    return AdminService.get_pd_list()
  
class AdminpdEditResource(Resource):
  @auth_required("token")
  @roles_required("admin")
  @marshal_with(pd_fields)
  def patch(self, pd_id):
    args = pdstatus_parser.parse_args()
    args = dict(filter(lambda item: item[1] is not None, args.items()))# removes empty parser values (the one which is having None)
    pd_edit = AdminService.edit_pd_status(pd_id, args["pd_status"])
    return pd_edit
  
class AdminPdPendingListResource(Resource):
  @auth_required("token")
  @roles_required("admin")
  @marshal_with(pd_fields)
  def get(self):
    return AdminService.get_pd_list_p()
  
class AdminAppListResource(Resource):
  @auth_required("token")
  @roles_required("admin")
  @marshal_with(app_fields)
  def get(self):
    return AdminService.get_app_list()

  
    
  


  
