from flask_restful import Api
from flask import Blueprint
from api.company.routes import company
comp_api_bp = Blueprint("comp_api", __name__, url_prefix="/comp_api")

comp_api = Api(comp_api_bp)

from .resources import CompanyResource, CompanypdcreateResource, CompanypdEditResource,CompanypdListResource, CompanypdResource, CompanyAppListResource, CompanyAppEditResource, CompCountResource

comp_api.add_resource(CompanyResource, "/comp_details")
comp_api.add_resource(CompanypdcreateResource, "/comp_pdcreate")
comp_api.add_resource(CompanypdEditResource, "/comp_pdedit/<int:pd_id>")
comp_api.add_resource(CompanypdListResource, "/comp_pdlist")
comp_api.add_resource(CompanypdResource, "/comp_pd_details/<int:pd_id>")
comp_api.add_resource(CompanyAppListResource, "/comp_applist/<int:pd_id>")
comp_api.add_resource(CompanyAppEditResource, "/comp_editastatus/<int:app_id>")
comp_api.add_resource( CompCountResource, "/comp_counts")
