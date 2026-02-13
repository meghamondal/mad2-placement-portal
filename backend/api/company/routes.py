from flask import Blueprint, request, jsonify
from flask_security.utils import verify_password, hash_password
from models import *
from flask import current_app

company = Blueprint("company", __name__, url_prefix="/api/company")

@company.route("/register", methods=['POST'])
def comp_register():
  data = request.get_json()
  email = data.get("email")
  password = data.get("password")
  role = data.get("role")
  active = False
  c_name = data.get("c_name")
  hr_contact = data.get("hr_contact")
  website = data.get("website")
  approval_status = "pending"
  print("Data accepted")
  

  if (not email or not c_name or not hr_contact or not website or not approval_status or not password):
      return jsonify({"message" : "Invalid credentials..."}), 400
  

  datastore = current_app.datastore

  existing_user = User.query.filter_by(email = email).first()

  if existing_user:
    existing_company = User.query.get(existing_user.u_id)
    if existing_company:
       return jsonify({"message" : "Company already exists..."}), 400
  
  user = datastore.create_user(email = email, password = hash_password(password), active=active)
  
  db.session.commit()

  role = datastore.find_role("company")
  datastore.add_role_to_user(user, role)

  new_company = Company(c_id = user.u_id, c_name = c_name, hr_contact = hr_contact, website = website, approval_status = approval_status)


  db.session.add(new_company)
  print("Company created")
  db.session.commit()


  return jsonify({
    "c_id" : user.u_id,
    "email" : user.email,
    "message" : "Registration successful..."
    
  }), 201
