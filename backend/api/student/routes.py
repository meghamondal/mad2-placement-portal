from flask import Blueprint, request, jsonify
from flask_security.utils import verify_password, hash_password
from models import *
from flask import current_app
import os 
from datetime import datetime
from werkzeug.utils import secure_filename

student = Blueprint("student", __name__, url_prefix="/api/student")

@student.route("/register", methods=['POST'])
def stud_register():

  email = request.form.get("email")
  password = request.form.get("password")
  role = request.form.get("role")
  active = True
  f_name = request.form.get("f_name")
  l_name = request.form.get("l_name")
  resume_file = request.files.get("resume_file")
  dob_s = request.form.get("dob")
  dob = datetime.strptime(dob_s, "%Y-%m-%d").date()
  graduation_year = request.form.get("graduation_year")
  cgpa = request.form.get("cgpa")
  print("Data accepted")

  

  if (not email or not f_name or not l_name or not resume_file or not dob or not graduation_year or not cgpa or not password):
      return jsonify({"message" : "Invalid credentials..."}), 400
  
  existing_user = User.query.filter_by(email=email).first()
  if existing_user:
     return jsonify({"message": "user already exists with this email..."}), 400
  
  allowed_extension=["pdf"]
  file_extension = resume_file.filename.split('.')[-1].lower()

  if file_extension in allowed_extension:
     filename = secure_filename(email + "." +file_extension)
     path = os.path.join("static/resumes", filename)
     resume_file.save(path)
     resume_file_path = path

  if file_extension not in allowed_extension:
     return jsonify({"message": "only .pdf files are allowed"}), 400
  
  
  
  
  

  datastore = current_app.datastore

  
  user = datastore.create_user(email = email, password = hash_password(password), active=active)
  
  db.session.commit()

  role = datastore.find_role("student")
  datastore.add_role_to_user(user, role)

  new_student = Student(stud_id = user.u_id, f_name = f_name, l_name = l_name, resume_file = resume_file_path, dob = dob, graduation_year = graduation_year, cgpa=cgpa)


  db.session.add(new_student)
  print("Student created")
  db.session.commit()


  return jsonify({
    "stud_id" : user.u_id,
    "email" : user.email,
    "message" : "Registration successful..."
    
  }), 201
