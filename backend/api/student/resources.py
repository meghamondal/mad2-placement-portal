from flask import request
from flask_restful import Resource, fields, marshal_with, reqparse
from flask_security import auth_required, roles_required, current_user
from api.student.services import StudentService
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from extensions import cache

# marshal fields

student_fields = {
  "stud_id": fields.Integer,
  "f_name": fields.String,
  "l_name": fields.String,
  "resume_file": fields.String,
  "dob": fields.DateTime,
  "graduation_year": fields.Integer,
  "cgpa": fields.Float,
}

company_fields = {
   "c_id": fields.Integer,
   "c_name": fields.String,
   "hr_contact": fields.String,
   "website": fields.String,
   "industry": fields.String,
}

pdrive_fields = {
  "pd_id": fields.Integer,
  "c_id": fields.Integer,
  "job_title": fields.String,
  "job_description": fields.String,
  "eligible_branch": fields.String,
  "min_cgpa": fields.Float,
  "eligible_year": fields.Integer,
  "application_deadline": fields.DateTime,
  'company_details': fields.Nested(company_fields, attribute='company')
}

intw_fields = {
  "intw_id": fields.Integer,
  "scheduled": fields.DateTime,
  "intw_status": fields.String,
  "remarks": fields.String
}

app_fields = {
  "app_id": fields.Integer,
  "pd_id": fields.Integer,
  "app_status": fields.String,
  "pd_details": fields.Nested(pdrive_fields, attribute='placement_d'),
  "intw_details": fields.List(fields.Nested(intw_fields), attribute='interviews'),
  "company_name": fields.String(attribute='placement_d.company.c_name')
}



# parser fields

stud_parser = reqparse.RequestParser()
stud_parser.add_argument("f_name", type=str)
stud_parser.add_argument("l_name", type=str)
stud_parser.add_argument("resume_file", type=str)
stud_parser.add_argument("dob", type=lambda x: datetime.strptime(x, "%Y-%m-%d").date())
stud_parser.add_argument("graduation_year", type=int)
stud_parser.add_argument("cgpa", type=float)

pd_parser = reqparser = reqparse.RequestParser()
pd_parser.add_argument("pd_id", type=int, required=True)

class StudentResource(Resource):
  @auth_required("token")
  @roles_required("student")
  @cache.cached(key_prefix="get_stud_details")
  @marshal_with(student_fields)
  def get(self):
    stud = StudentService.stud_details(current_user.u_id)
    return stud
  

  @auth_required("token")
  @roles_required("student")
  @marshal_with(student_fields)
  def patch(self):
    data = request.form.to_dict()
    resume_file = request.files.get("resume_file")
    allowed_extension=["pdf"]
    if resume_file:
      file_extension = resume_file.filename.split('.')[-1].lower()
      if file_extension not in allowed_extension:
        return {"message": "Only pdf files are allowed"}, 400
      filename = secure_filename(current_user.email + "." +file_extension)
      path = os.path.join("static/resumes", filename)
      resume_file.save(path)
      data["resume_file"] = path
    if "dob" in data and data["dob"]:
      data["dob"] = datetime.strptime(data["dob"], "%Y-%m-%d").date()
    data = {k: v for k, v in data.items() if v != ""}
    stud_edit = StudentService.edit_details(current_user.u_id, data)
    cache.delete_memoized(StudentResource.gety)

    return stud_edit
  

class StudentpdListResource(Resource):
  @auth_required("token")
  @roles_required("student")
  @cache.cached(key_prefix="get_stud_pdlist")
  @marshal_with(pdrive_fields)
  def get(self):
    pd_list = StudentService.get_placement_drives(current_user.u_id)
    print("db is called for pd list")
    return pd_list
  
class StudentpdResource(Resource):
  @auth_required("token")
  @roles_required("student")
  @cache.memoize(timeout=60)
  @marshal_with(pdrive_fields)
  def get(self, pd_id):
    pd_details = StudentService.pd_details(pd_id)
    print("caching is used")
    return pd_details
  
class StudentpdApplyResource(Resource):
  @auth_required("token")
  @roles_required("student")
  def post(self, pd_id):
    # pd_id = pd_parser.parse_args()["pd_id"]

    output = StudentService.apply_to_pdrive(current_user.u_id, pd_id)
    cache.delete_memoized(StudentpdListResource.get)
    cache.delete_memoized(StudentAppHistoryResource.get)

    # if output == "Already applied...":
    #   return {"message": "You have already applied "}, 400
    return {"message": "Submission Successful..."}, 201
  
class StudentAppHistoryResource(Resource):
  @auth_required("token")
  @roles_required("student")
  @cache.cached(key_prefix="get_stud_apphistory")
  @marshal_with(app_fields)
  def get(self):
    app_history = StudentService.get_app_history(current_user.u_id)
    return app_history


class StudOfferLetterResource(Resource):
  @auth_required("token")
  @roles_required("student")
  def get(self, app_id):
    offer_letter = StudentService.offer_letter(current_user.u_id, app_id)
    return {"offer_letter": offer_letter}, 200

  
