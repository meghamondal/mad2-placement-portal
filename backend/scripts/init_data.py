from app import app
from models import db
from models import *
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import hash_password

with app.app_context():
  db.drop_all()
  db.create_all()
  datastore : SQLAlchemyUserDatastore = app.datastore

  admin_r = datastore.find_or_create_role(name = "admin", description = "super user")
  student_r = datastore.find_or_create_role(name = "student", description = "applies for jobs")
  company_r = datastore.find_or_create_role(name = "company", description = "provides job oppurnities and hires students")

  if not datastore.find_user(email = "admin@example.com"):
    datastore.create_user(email = "admin@example.com",  password = hash_password("password"), roles=['admin'])
  if not datastore.find_user(email = "testcompany@example.com"):
    datastore.create_user(email = "testcompany@example.com", password = hash_password("password"), roles=['company'])
  if not datastore.find_user(email = "rahul@example.com"):
    datastore.create_user(email = "rahul@example.com", password = hash_password("password"), roles=['student'])
  try:
    db.session.commit()
  except:
    db.session.rollback()
    print("Error Found")


  if User.query.filter_by(email = "rahul@example.com").first():
    stud_data = User.query.filter_by(email = "rahul@example.com").first()
    stud_dob = datetime(day=17, month=6, year=2001)
    new_stud=Student(stud_id = stud_data.u_id, f_name = 'Rahul', l_name = 'Kumar', resume_file = "static/resumes/rahulexample.com.pdf" , graduation_year = '2027', cgpa ='8.01', dob = stud_dob) #needs to changde the logic to make it url safe for resume file
    db.session.add(new_stud)
    db.session.commit()

  if User.query.filter_by(email= "testcompany@example.com").first():
    comp_data = User.query.filter_by(email= "testcompany@example.com").first()
    new_comp=Company(c_id=comp_data.u_id, c_name = "testcompany", hr_contact="hr@testcompany.com", website="www.testcompany.com", industry="Technology & IT", approval_status = 'approved')
    db.session.add(new_comp)
    db.session.commit()

  comp_e = User.query.filter_by(email= "testcompany@example.com").first()
  if comp_e:
    comp_d = Company.query.filter_by(c_id=comp_e.u_id).first()
    if comp_d:
      place_drive = Placement_drive.query.filter_by(job_title = "Data Analyst", c_id = comp_d.c_id).first()
      if not place_drive:
        new_pd = Placement_drive(c_id = comp_d.c_id, job_title = "Data Analyst", job_description = "Collecting, cleaning and analyzing data",
                                    eligible_branch = "CSE, IT, Data Science, AI&ML", min_cgpa = "6.50", eligible_year = "2024",
                                    application_deadline = datetime(day=17, month=3, year=2026))
        db.session.add(new_pd)
        db.session.commit()

  place_drive = Placement_drive.query.filter_by(job_title = "Data Analyst", c_id = comp_d.c_id).first()
  stud_user = User.query.filter_by(email = "rahul@example.com").first()
  stud_data = Student.query.filter_by(stud_id = stud_user.u_id).first()

  application = Application.query.filter_by(pd_id = place_drive.pd_id, stud_id = stud_data.stud_id).first()

  if not application:
    new_app = Application(pd_id = place_drive.pd_id, stud_id = stud_data.stud_id, app_date = datetime(day=17, month=3, year=2026))
    db.session.add(new_app)
    db.session.commit()