from xml.dom.minidom import Document

from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.urls import reverse_lazy
from rest_framework import serializers
from django.core import serializers

from .forms import EmployeeRegisterForm,LoginForm,EmployerRegisterForm,JobDetailForm,ApplicantForm
# Create your views here.
from .models import User,JobDetails,Applicant
from .decorators import user_is_employer,user_is_employee


def EmployeeRegisterView(request):
    form=EmployeeRegisterForm
    if request.method =='POST':
        form = EmployeeRegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            password=form.cleaned_data.get('password1')
            user.set_password(password)

            user.save()
            return HttpResponseRedirect('/employeelogin/')

        else:
            form=EmployeeRegisterForm

    return render(request, 'FirstProject/employeeregister.html', {'form': form})




def EmployeeProfile(request):
    return render(request,'profile.xhtml',{})


def EmployerRegisterView(request):
    form =EmployerRegisterForm
    if request.method=="POST":

        form=EmployerRegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            password=form.cleaned_data.get('password1')
            user.set_password(password)

            user.save()
            return HttpResponseRedirect('/employerlogin/')
        else:

            return HttpResponse("Please enter valid data")
            form=CompanyRegisterForm

    return render(request, 'FirstProject/companyregister.html', {'form': form})


def EmployerLoginView(request):
    fm=LoginForm()

    if request.method == 'POST':
        fm = LoginForm(data=request.POST)
        if fm.is_valid():
            username=fm.cleaned_data['email']
            pswrd=fm.cleaned_data['password']

            user=authenticate(username=username,password=pswrd)
            if user:
                if user.role =="employer":

                  login(request,user)

                  return HttpResponseRedirect('/aftercom-dash/')
            else:
                return HttpResponse("The user is not registered as Employer")

    else:
        fm = LoginForm()

    return render(request, 'FirstProject/EmployerLogin.html', {'form': fm})

def EmployeeLoginView(request):
    fm=LoginForm()

    if request.method == 'POST':
        fm = LoginForm(data=request.POST)
        if fm.is_valid():
            username=fm.cleaned_data['email']
            pswrd=fm.cleaned_data['password']

            user=authenticate(username=username,password=pswrd)
            if user:
                if user.role =="employee":

                  login(request,user)

                  return HttpResponseRedirect('/afteremp-dash')
            else:
                return HttpResponse("The user is not registered as Employee")

    else:
        fm = LoginForm()

    return render(request, 'FirstProject/EmployeeLogin.html', {'form': fm})


def CompanyProfile(request):
    return render(request,'cprofile.xhtml',{})


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def PostJobView(request):

    form=JobDetailForm()
    if request.method=="POST":

        #form=JobDetailForm(company_name=name)
        form=JobDetailForm(data=request.POST)

        user = get_object_or_404(User, id=request.user.id)
        qs = User.objects.get(id=request.user.id)
        name = qs.first_name
        address=qs.last_name
        if form.is_valid():
            obj=form.save(commit=False)
            obj.user=user
            obj.company_name=name
            obj.company_address=address
            obj.save()
            return HttpResponseRedirect('/view-job-company/')


        form=JobDetailForm()
    return render(request,'FirstProject/postjob.html',{'form':form})

@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def ViewJobByCompany(request):
    obj=JobDetails.objects.filter(user_id=request.user.id)


    return render(request,'FirstProject/ViewAllJobCom.html',{'obj':obj})


@login_required(login_url=reverse_lazy('/login/'))
@user_is_employee
def ViewJobByEmployee(request):
    obj=JobDetails.objects.all()
    return render(request,'FirstProject/ViewAllJob.html',{'obj':obj})


def ApplyJobView(request,id):
    form = ApplicantForm(request.POST, request.FILES)

    qs=JobDetails.objects.get(pk=id)
    user = get_object_or_404(User, id=request.user.id)

    applicant=Applicant.objects.filter(user=user,job=qs.position,company=qs.company_name)
    if not applicant:
        if request.method=="POST":

            if form.is_valid():

                obj=form.save(commit=False)
                obj.user=user
                obj.resume=request.FILES['resume']

                obj.job=qs.position
                obj.company=qs.company_name
                obj.applied=="True"
                obj.save()
                return HttpResponseRedirect('/view-ajob-employee/')

        form = ApplicantForm(instance=qs)
        return render(request, 'FirstProject/jobform.html', {'form': form})

    else:
        return HttpResponse("Already applied for this job")

@login_required
@user_is_employee
def view_job_employee(request):
    user = get_object_or_404(User, id=request.user.id)
    job=Applicant.objects.filter(user=user)
    return render(request, 'FirstProject/viewappliedjobbyemp.html', {'job': job})


def view_applied_jobs(request):
    user=get_object_or_404(User,id=request.user.id)
    qs=Applicant.objects.filter(company=user.first_name)
    return render(request,'FirstProject/ViewApplicant.html',{'qs':qs})

def Home(request):
    return render(request,'FirstProject/index.html')


def Employee_Click(request):
    return render(request,'FirstProject/employeeclick.html')

def Employer_Click(request):
    return render(request,'FirstProject/EmployerClick.html')

def Employee_Dash(request):
    return render(request,'FirstProject/employeeafterlogin.html')

def Employer_Dash(request):
    return render(request,'FirstProject/employerafterlogin.html')

def aboutus_view(request):
    return render(request,'FirstProject/aboutus.html')






