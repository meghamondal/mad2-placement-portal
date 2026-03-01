from flask_restful import Api
from flask import Blueprint
from api.student.routes import student
stud_api_bp = Blueprint("api", __name__, url_prefix="/api")

stud_api = Api(stud_api_bp)

from .resources import StudentResource, StudentpdListResource, StudentpdApplyResource, StudentAppHistoryResource, StudentpdResource, StudOfferLetterResource, StudExportResource, StudExportStatus

stud_api.add_resource(StudentResource, "/stud_details")
stud_api.add_resource(StudentpdListResource, "/stud_pdlist")
stud_api.add_resource(StudentpdResource, "/stud_pddetails/<int:pd_id>")
stud_api.add_resource(StudentpdApplyResource, "/stud_apply/<int:pd_id>")
stud_api.add_resource(StudentAppHistoryResource, "/stud_apps")
stud_api.add_resource(StudOfferLetterResource, "/stud_offer/<int:app_id>")

stud_api.add_resource(StudExportResource, "/export_csv/<int:stud_id>")
stud_api.add_resource(StudExportStatus, "/export_status/<string:task_id>")