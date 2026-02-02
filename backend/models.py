from extensions import db
from datetime import datetime
from flask_security.core import UserMixin, RoleMixin


class User(db.Model, UserMixin):
  __tablename__="user"
  u_id=db.Column(db.Integer, primary_key=True)
  name=db.Column(db.String, nullable = False)
  email=db.Column(db.String, nullable= False, unique=True)
  password=db.Column(db.String, nullable=False, unique=True)
  fs_uniquifier = db.Column(db.String, unique = True, nullable = False)
  active=db.Column(db.Boolean, default = True)
  roles=db.Relationship('Role', backref = 'bearers', secondary='user_roles')

class Role(db.Model, RoleMixin):
  __tablename__="role"
  r_id = db.Column(db.Integer, primary_key = True)
  name=db.Column(db.String, unique=True, nullable=False)
  description=db.Column(db.String, nullable=False)

class UserRoles(db.Model):
  __tablename__ ="user_roles"
  ur_id=db.Column(db.Integer, primary_key = True)
  u_id=db.Column(db.Integer, db.ForeignKey('user.u_id'))
  r_id=db.Column(db.Integer, db.ForeignKey('role.r_id'))

class Student(db.Model):
  __tablename__="student"
  stud_id=db.Column(db.Integer, db.ForeignKey('user.u_id'), primary_key=True)
  f_name=db.Column(db.String, nullable=False)
  l_name=db.Column(db.String, nullable=False)
  resume_file=db.Column(db.String, nullable = False)
  dob=db.Column(db.DateTime, nullable=False)
  graduation_year = db.Column(db.Integer, nullable=False)
  cgpa=db.Column(db.Float, nullable=False)
  applications=db.relationship("Application", cascade="all,delete", backref="student", lazy=True)

class Company(db.Model):
  __tablename__="company"
  c_id=db.Column(db.Integer, db.ForeignKey('user.u_id'), primary_key=True)
  c_name=db.Column(db.String, nullable=False)
  hr_contact=db.Column(db.String, nullable=False)
  website=db.Column(db.String, nullable=False)
  approval_status=db.Column(db.Enum("pending", "approved", "rejected"), default="pending")
  p_drives=db.relationship("Placement_drive", cascade="all,delete", backref="company", lazy=True)

class Placement_drive(db.Model):
  __tablename__="placement_d"
  pd_id=db.Column(db.Integer, primary_key = True)
  c_id=db.Column(db.Integer, db.ForeignKey('company.c_id'))
  job_title=db.Column(db.String, nullable=False)
  job_description=db.Column(db.Text, nullable=False)
  eligible_branch=db.Column(db.String)
  min_cgpa=db.Column(db.Float, nullable=False)
  eligible_year=db.Column(db.Integer)
  application_deadline=db.Column(db.DateTime, nullable=False)
  pd_status=db.Column(db.Enum("pending", "approved", "rejected"), default="pending")
  applications=db.relationship("Application", cascade="all,delete", backref="placement_d", lazy=True)

class Application(db.Model):
  __tablename__="application"
  app_id=db.Column(db.Integer, primary_key = True)
  pd_id=db.Column(db.Integer, db.ForeignKey('placement_d.pd_id'))
  stud_id=db.Column(db.Integer, db.ForeignKey('student.stud_id'))
  app_date=db.Column(db.DateTime, nullable=False, default=datetime.now())
  app_status=db.Column(db.Enum("applied", "shortlisted", "selected", "rejected"), default="applied")

