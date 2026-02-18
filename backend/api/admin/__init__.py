from flask_restful import Api
from flask import Blueprint
admin_api_bp = Blueprint("admin_api", __name__, url_prefix="/admin_api")

admin_api = Api(admin_api_bp)

from .resources import CountResource, AdminStudResource, AdminStudListResource, AdminCompResource, AdminCompListResource, AdminCompEditResource, AdminpdResource, AdminpdEditResource, AdminAppListResource, AdminCompPendingListResource

admin_api.add_resource(CountResource, "/counts")
admin_api.add_resource(AdminStudResource, "/stud_details/<int:stud_id>")
admin_api.add_resource(AdminStudListResource, "/stud_list")
admin_api.add_resource(AdminCompResource, "/comp_details/<int:c_id>")
admin_api.add_resource(AdminCompListResource, "/comp_list")
admin_api.add_resource(AdminCompPendingListResource, "/comp_plist")
admin_api.add_resource(AdminCompEditResource, "/comp_status/<int:c_id>")
admin_api.add_resource(AdminpdResource, "/pd_details/<int:pd_id>")
admin_api.add_resource(AdminpdEditResource, "/pd_status/<int:pd_id>")
admin_api.add_resource(AdminAppListResource, "/app_list")