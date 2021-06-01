from django.urls import path
from rest_framework import views
from .views import ViewJobByEmployee, ApplyJobView, ViewJobByEmployee, view_job_employee, view_applied_jobs, Home, \
    Employee_Click, Employer_Click,EmployeeLoginView,Employer_Dash,Employee_Dash,aboutus_view

from .views import EmployeeRegisterView,EmployeeProfile,CompanyProfile,EmployerLoginView,EmployerRegisterView,PostJobView,ViewJobByCompany
urlpatterns=[
    path('',Home),
    path('employee/register/',EmployeeRegisterView),
    path('employerlogin/',EmployerLoginView),
    path('employeelogin/',EmployeeLoginView),
    path('employee/profile/',EmployeeProfile),
    path('company/register/',EmployerRegisterView),
    path('company/profile/', CompanyProfile),
    path('post-job/',PostJobView),
    path('view-job-company/', ViewJobByCompany),
    path('view-job-employee/', ViewJobByEmployee),
    path('apply-job/<int:id>/',ApplyJobView,name="apply"),
    path('view-ajob-employee/',view_job_employee),
    path('view-ajob-company/',view_applied_jobs),
    path('emp-dash/',Employee_Click),
    path('com-dash/',Employer_Click),
    path('aftercom-dash/',Employer_Dash),
    path('afteremp-dash/',Employee_Dash),
    path('logout/',Home),
    path('aboutus/',aboutus_view),

]