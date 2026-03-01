from flask_restful import Resource, fields, marshal_with, reqparse
from flask_security import auth_required, roles_required, current_user
from api.company.services import CompanyService
from datetime import datetime
from extensions import cache


student_fields = {
  "stud_id": fields.Integer,
  "f_name": fields.String,
  "l_name": fields.String,
  "resume_file": fields.String,
  "dob": fields.DateTime,
  "graduation_year": fields.Integer,
  "cgpa": fields.Float,
  "active": fields.Boolean
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
  "pd_status": fields.String,
  'company_details': fields.Nested(company_fields, attribute='company')
}

app_fields = {
  "app_id": fields.Integer,
  "pd_id": fields.Integer,
  "app_status": fields.String,
  "student_details": fields.Nested(student_fields, attribute='student'),
  "pd_details": fields.Nested(pdrive_fields, attribute='placement_d')
}

intw_fields = {
  "intw_id": fields.Integer,
  "app_id": fields.Integer,
  "scheduled": fields.DateTime,
  "intw_status": fields.String,
  "remarks": fields.String
}

intw_parser = reqparse.RequestParser()
intw_parser.add_argument("scheduled", type=lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"), required=True)
intw_parser.add_argument("remarks", type=str)
intw_parser.add_argument("intw_status", type=str)

comp_parser = reqparse.RequestParser()
comp_parser.add_argument("c_name", type=str)
comp_parser.add_argument("hr_contact", type=str)
comp_parser.add_argument("website", type=str)
comp_parser.add_argument("industry", type=str)

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
  @cache.cached(key_prefix="get_compdetails")
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
    cache.delete("get_compdetails")
    return comp_edit
  
class CompanypdcreateResource(Resource):
  @auth_required("token")
  @roles_required("company")
  @marshal_with(pdrive_fields)
  def post(self):
    args = pd_parser.parse_args()
    args = dict(filter(lambda item: item[1] is not None, args.items()))# removes empty parser values (the one which is having None)
    comp_create = CompanyService.create_placement_drives(current_user.u_id, args)
    cache.delete("get_comppdlist")
    cache.delete("get_compcount")
    return comp_create
  
class CompanypdEditResource(Resource):
  @auth_required("token")
  @roles_required("company")
  @marshal_with(pdrive_fields)
  def patch(self, pd_id):
    args = pd_parser.parse_args()
    args = dict(filter(lambda item: item[1] is not None, args.items()))# removes empty parser values (the one which is having None)
    pd_edit = CompanyService.edit_pddetails(current_user.u_id, pd_id, args)
    cache.delete("get_comppdlist")
    cache.delete_memoized(CompanypdResource.get, CompanypdResource, pd_id)
    cache.delete("get_compcount")
    return pd_edit, 200
  

class CompanypdListResource(Resource):
  @auth_required("token")
  @roles_required("company")
  @cache.cached(key_prefix="get_comppdlist")
  @marshal_with(pdrive_fields)
  def get(self):
    pd_list = CompanyService.get_pd_list(current_user.u_id)
    return pd_list
  
class CompanypdResource(Resource):
  @auth_required("token")
  @roles_required("company")
  @cache.memoize(timeout=60)
  @marshal_with(pdrive_fields)
  def get(self, pd_id):
    pd_details = CompanyService.pd_details(pd_id)
    return pd_details


class CompanyAppListResource(Resource):
  @auth_required("token")
  @roles_required("company")
  @cache.memoize(timeout=60)
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
    cache.delete_memoized(CompanyAppListResource.get, CompanyAppListResource, app_edit.pd_id)
    cache.delete("get_compapplist")
    cache.delete("get_compcount")
    return app_edit
  
class CompCountResource(Resource):
  @auth_required("token")
  @roles_required("company")
  @cache.cached(key_prefix="get_compcount")
  def get(self):
    c_id = current_user.u_id
    return{
      "pd_count": CompanyService.pd_count(c_id),
      "active_pd_count": CompanyService.active_pd_count(c_id),
      "app_count": CompanyService.app_count(c_id),
      "short_app_count": CompanyService.short_app_count(c_id)
  }, 200

class CompAppShortlistedResource(Resource):
  @auth_required("token")
  @roles_required("company")
  @cache.cached(key_prefix="get_compapplist")
  @marshal_with(app_fields)
  def get(self):
    comp_id = current_user.u_id
    return CompanyService.short_app_list(comp_id)
  
class CompanyScheduleIntwResource(Resource):
  @auth_required("token")
  @roles_required("company")
  @marshal_with(intw_fields)
  def post(self, app_id):
    args = intw_parser.parse_args()
    args = dict(filter(lambda item: item[1] is not None, args.items()))# removes empty parser values (the one which is having None)
    schedule_intw = CompanyService.schedule_interview(app_id, args)
    cache.delete_memoized(CompanyAppListResource.get, CompanyAppListResource, schedule_intw.application.pd_id)
    cache.delete("get_compcount")
    return schedule_intw
  
class CompanyIntwPassStatusResource(Resource):
  @auth_required("token")
  @roles_required("company")
  @marshal_with(intw_fields)
  def patch(self, app_id):
    intw_pass = CompanyService.edit_intw_pass(app_id)
    pd_id = intw_pass.pd_id
    cache.delete_memoized(CompanyAppListResource.get, CompanyAppListResource, pd_id)
    cache.delete("get_compapplist")
    cache.delete("get_compcount")
    return intw_pass
  
class CompanyIntwFailStatusResource(Resource):
  @auth_required("token")
  @roles_required("company")
  @marshal_with(intw_fields)
  def patch(self, app_id):
    intw_fail = CompanyService.edit_intw_fail(app_id)
    pd_id = intw_fail.pd_id
    cache.delete_memoized(CompanyAppListResource.get, CompanyAppListResource, pd_id)
    cache.delete("get_compapplist")
    cache.delete("get_compcount")
    return intw_fail
  
from tasks.test import compcsv_report
import time

class CompExportResource(Resource):
  # @auth_required("token")
  # @roles_required("company")
  def post(self,c_id):
    result = compcsv_report.delay(c_id)
    return {
      "task_id": result.id,
      "result": result.result,
      "message": "Export started"
    }
from celery.result import AsyncResult
from flask import send_from_directory, redirect

class CompExportStatus(Resource):
  # @auth_required("token")
  # @roles_required("company") 
  def get(self, task_id):
    res = AsyncResult(task_id)
    while not res.ready():
      time.sleep(1)
      filename = res.result
      return redirect(f"/static/{filename}")
    return send_from_directory('static', res.result)
