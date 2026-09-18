@echo off

cd /d "C:\Users\Vishal Gautam\Desktop\SarkariJobs"

call venv\Scripts\activate.bat

python manage.py auto_update >> automation_log.txt 2>&1