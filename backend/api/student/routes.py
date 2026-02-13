from flask import Blueprint, request, jsonify
from flask_security.utils import verify_password, hash_password
from models import *
from flask import current_app

student = Blueprint("student", __name__, url_prefix="/api/student")

@student.route("/register", methods=['POST'])
def stud_register():
  data = request.get_json()
  email = data.get("email")
  password = data.get("password")
  role = data.get("role")
  active = True
  f_name = data.get("f_name")
  l_name = data.get("l_name")
  resume_file = data.get("resume_file")
  dob_s = data.get("dob")
  dob = datetime.strptime(dob_s, "%Y-%m-%d").date()
  graduation_year = data.get("graduation_year")
  cgpa = data.get("cgpa")
  print("Data accepted")
  

  if (not email or not f_name or not l_name or not resume_file or not dob or not graduation_year or not cgpa or not password):
      return jsonify({"message" : "Invalid credentials..."}), 400
  

  datastore = current_app.datastore

  existing_user = User.query.filter_by(email = email).first()

  if existing_user:
    return jsonify({"message" : "User already exists..."}), 400
  
  user = datastore.create_user(email = email, password = hash_password(password), active=active)
  
  db.session.commit()

  role = datastore.find_role("student")
  datastore.add_role_to_user(user, role)

  new_student = Student(stud_id = user.u_id, f_name = f_name, l_name = l_name, resume_file = resume_file, dob = dob, graduation_year = graduation_year, cgpa=cgpa)


  db.session.add(new_student)
  print("Student created")
  db.session.commit()


  return jsonify({
    "stud_id" : user.u_id,
    "email" : user.email,
    "message" : "Registration successful..."
    
  }), 201
