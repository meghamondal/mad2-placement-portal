from celery import shared_task
import datetime
from models import Application, Placement_drive, User, Company, Role
from render_utils import render_report
from mail import send_email
import csv

@shared_task()
def add(x,y):
  return x+y

@shared_task(ignore_results=False, name="csv_report")
def csv_report(stud_id):
  app = Application.query.filter_by(stud_id=stud_id).all()
  csv_filename = f"applications_{stud_id}_{datetime.datetime.now().strftime('%f')}.csv"
  with open(f'static/{csv_filename}', 'w', newline = "") as csvfile:
    s_no = 1
    app_csv = csv.writer(csvfile, delimiter = ',')
    app_csv.writerow(['S No.', 'Student ID', 'Company Name', 'Job Title', 'Application Status', 'Applied Date'])
    for a in app:
      this_app = [s_no, a.stud_id, a.placement_d.company.c_name, a.placement_d.job_title, a.app_status, a.app_date]
      app_csv.writerow(this_app)
      s_no += 1

  return csv_filename

@shared_task(ignore_results=False, name="compcsv_report")
def compcsv_report(c_id):
  pd = Placement_drive.query.filter_by(c_id=c_id).all()
  csv_filename = f"pdrives_{c_id}_{datetime.datetime.now().strftime('%f')}.csv"
  with open(f'static/{csv_filename}', 'w', newline = "") as csvfile:
    s_no = 1
    pd_csv = csv.writer(csvfile, delimiter = ',')
    pd_csv.writerow(['S No.', 'Company ID', 'Company Name', 'Job Title', 'Application Status', 'Student ID' ,'Student Name'])
    for p in pd:
      for a in p.applications:
        this_pd = [s_no, p.c_id, p.company.c_name, p.job_title, a.app_status, a.student.stud_id ,f"{a.student.f_name} {a.student.l_name}"]
        pd_csv.writerow(this_pd)
        s_no += 1

  return csv_filename

@shared_task(ignore_results = False, name="monthly_report")
def monthly_report():
  total_pd = Placement_drive.query.count()
  total_app = Application.query.count()
  total_selected_app = Application.query.filter_by(app_status="selected").count()
  pd_rate = 0
  if total_app > 0:
    pd_rate = round((total_selected_app/total_app)*100, 2)
  selection_density = 0
  if total_pd > 0:
    selection_density = round((total_selected_app/total_pd), 2)
  monthly_report_data = {
    "total_pd": total_pd,
    "total_app": total_app,
    "total_selected_app": total_selected_app,
    "pd_rate": pd_rate,
    "selection_density": selection_density
  }
  message = render_report("monthly_admin_report.html", monthly_report_data)
  send_email("admin@example.com", subject = "Monthly Placement Activity Report", message=message)

  return "Monthly reports sent"


@shared_task(ignore_results = False, name="comp_monthly_report")
def comp_monthly_report():
  users = User.query.join(User.roles).filter(Role.name == "company").all()
  for u in users:
    company = Company.query.filter_by(c_id=u.u_id).first()
    comp_pds = Placement_drive.query.filter_by(c_id=company.c_id).all()
    total_pds = len(comp_pds)
    total_apps = 0
    total_selected = 0
    for pd in comp_pds:
      pd_apps = Application.query.filter_by(pd_id=pd.pd_id).all()
      total_apps += len(pd_apps)
      total_pd_selected = Application.query.filter_by(pd_id=pd.pd_id, app_status="selected").count()
      total_selected += total_pd_selected
    pd_rate = 0 
    if total_apps > 0:
      pd_rate = round((total_selected/total_apps)*100, 2)

    comp_monthly_report_data = {
      "company_name": company.c_name,
      "total_pds": total_pds,
      "total_apps": total_apps,
      "total_selected": total_selected,
      "pd_rate": pd_rate
    }
    message = render_report("monthly_company_report.html", comp_monthly_report_data)
    send_email(u.email, subject = "Monthly Activity Report for the Company", message=message)

  return "Monthly reports sent"

@shared_task(ignore_results = False, name="daily_remainder")
def daily_remainder():
  return "Delivery is sent to user"