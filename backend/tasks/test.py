from celery import shared_task
import datetime
from models import Application
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

@shared_task(ignore_results = False, name="monthly_report")
def monthly_report():
  return "Monthly reports sent"

@shared_task(ignore_results = False, name="daily_remainder")
def daily_remainder():
  return "Delivery is sent to user"