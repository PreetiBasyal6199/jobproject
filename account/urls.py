from django.urls import path
from rest_framework import views
from .views import ViewJobByEmployee,ApplyJobView,ViewJobByEmployee,view_job_employee,view_applied_jobs
from .views import EmployeeRegisterView,EmployeeProfile,CompanyProfile,LoginView,EmployerRegisterView,PostJobView,ViewJobByCompany
urlpatterns=[
    path('employee/register/',EmployeeRegisterView),
    path('login/',LoginView),
    path('employee/profile/',EmployeeProfile),
    path('company/register/',EmployerRegisterView),
    path('company/profile/', CompanyProfile),
    path('post-job/',PostJobView),
    path('view-job-company/', ViewJobByCompany),
    path('view-job-employee/', ViewJobByEmployee),
    path('apply-job/<int:id>/',ApplyJobView,name="apply"),
    path('view-ajob-employee/',view_job_employee),
    path('view-ajob-company/<int:id>/',view_applied_jobs),


]