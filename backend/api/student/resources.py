from flask import request
from flask_restful import Resource, fields, marshal_with, reqparse
from flask_security import auth_required, roles_required, current_user
from api.student.services import StudentService
from datetime import datetime

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

pdrive_fields = {
  "pd_id": fields.Integer,
  "job_title": fields.String,
  "job_description": fields.String,
  "eligible_branch": fields.String,
  "min_cgpa": fields.Float,
  "eligible_year": fields.Integer,
  "application_deadline": fields.DateTime
}

app_fields = {
  "app_id": fields.Integer,
  "pd_id": fields.Integer,
  "app_status": fields.String
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
  @marshal_with(student_fields)
  def get(self):
    stud = StudentService.stud_details(current_user.u_id)
    return stud
  

  @auth_required("token")
  @roles_required("student")
  @marshal_with(student_fields)
  def patch(self):
    args = stud_parser.parse_args()
    args = dict(filter(lambda item: item[1] is not None, args.items()))# removes empty parser values (the one which is having None)
    stud_edit = StudentService.edit_details(current_user.u_id, args)
    return stud_edit
  

class StudentpdListResource(Resource):
  @auth_required("token")
  @roles_required("student")
  @marshal_with(pdrive_fields)
  def get(self):
    pd_list = StudentService.get_placement_drives(current_user.u_id)
    return pd_list
  
class StudentpdApplyResource(Resource):
  @auth_required("token")
  @roles_required("student")
  def post(self):
    pd_id = pd_parser.parse_args()["pd_id"]

    output = StudentService.apply_to_pdrive(current_user.u_id, pd_id)

    if output == "Already applied...":
      return {"message": "You have already applied "}, 400
    return {"message": "Submission Successful..."}, 201
  
class StudentAppHistoryResource(Resource):
  @auth_required("token")
  @roles_required("student")
  @marshal_with(app_fields)
  def get(self):
    app_history = StudentService.get_app_history(current_user.u_id)
    return app_history




  
