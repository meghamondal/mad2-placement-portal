from flask_restful import Resource, fields, marshal_with, reqparse
from flask_security import auth_required, roles_required, current_user
from api.company.services import CompanyService
from datetime import datetime

company_fields = {
   "c_id": fields.Integer,
   "c_name": fields.String,
   "hr_contact": fields.String,
   "website": fields.String
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
  "pd_status": fields.String
}

app_fields = {
  "app_id": fields.Integer,
  "pd_id": fields.Integer,
  "app_status": fields.String
}

comp_parser = reqparse.RequestParser()
comp_parser.add_argument("c_name", type=str)
comp_parser.add_argument("hr_contact", type=str)
comp_parser.add_argument("website", type=str)

pd_parser = reqparse.RequestParser()
pd_parser.add_argument("job_title", type=str)
pd_parser.add_argument("job_description", type=str)
pd_parser.add_argument("eligible_branch", type=str)
pd_parser.add_argument("min_cgpa", type=float)
pd_parser.add_argument("eligible_year", type=int)
pd_parser.add_argument("application_deadline", type=lambda x: datetime.strptime(x, "%Y-%m-%d").date())

appstatus_parser = reqparse.RequestParser()
appstatus_parser.add_argument("app_status", type=str, required=True)

class CompanyResource(Resource):
  @auth_required("token")
  @roles_required("company")
  @marshal_with(company_fields)
  def get(self):
    comp = CompanyService.comp_details(current_user.u_id)
    return comp

  @auth_required("token")
  @roles_required("company")
  @marshal_with(company_fields)
  def patch(self):
    args = comp_parser.parse_args()
    args = dict(filter(lambda item: item[1] is not None, args.items()))# removes empty parser values (the one which is having None)
    comp_edit = CompanyService.edit_details(current_user.u_id, args)
    return comp_edit
  
class CompanypdcreateResource(Resource):
  @auth_required("token")
  @roles_required("company")
  @marshal_with(pdrive_fields)
  def post(self):
    args = pd_parser.parse_args()
    args = dict(filter(lambda item: item[1] is not None, args.items()))# removes empty parser values (the one which is having None)
    comp_create = CompanyService.create_placement_drives(current_user.u_id, args)
    return comp_create
  
class CompanypdListResource(Resource):
  @auth_required("token")
  @roles_required("company")
  @marshal_with(pdrive_fields)
  def get(self):
    pd_list = CompanyService.get_app_list(current_user.u_id)
    return pd_list


class CompanyAppListResource(Resource):
  @auth_required("token")
  @roles_required("company")
  @marshal_with(app_fields)
  def get(self, pd_id):
    app_list = CompanyService.get_pd_app(pd_id)
    return app_list
  

class CompanyAppEditResource(Resource):
  @auth_required("token")
  @roles_required("company")
  @marshal_with(app_fields)
  def patch(self, app_id):
    args = appstatus_parser.parse_args()
    args = dict(filter(lambda item: item[1] is not None, args.items()))# removes empty parser values (the one which is having None)
    app_edit = CompanyService.edit_applicants_status(app_id, args["app_status"])
    return app_edit