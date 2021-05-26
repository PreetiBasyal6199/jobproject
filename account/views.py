from xml.dom.minidom import Document

from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.urls import reverse_lazy
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
            return HttpResponseRedirect('/login/')

        else:
            form=EmployeeRegisterForm

    return render(request, 'register.xhtml', {'form': form})




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
            return HttpResponseRedirect('/login/')
        else:

            return HttpResponse("Please enter valid data")
            form=CompanyRegisterForm

    return render(request, 'companyregister.xhtml', {'form': form})


def LoginView(request):
    fm=LoginForm()

    if request.method == 'POST':
        fm = LoginForm(data=request.POST)
        if fm.is_valid():
            username=fm.cleaned_data['email']
            pswrd=fm.cleaned_data['password']

            user=authenticate(username=username,password=pswrd)
            if user:

                login(request,user)
                if user.role =="employee":

                    return HttpResponseRedirect('/view-job-employee/')
                else:
                    return HttpResponseRedirect('/post-job/')
            else:
                return HttpResponse("The user is not registered yet")

    else:
        fm = LoginForm()

    return render(request, 'companylogin.xhtml', {'form': fm})


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
    return render(request,'jobform.xhtml',{'form':form})

@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def ViewJobByCompany(request):
    obj=JobDetails.objects.filter(user_id=request.user.id)


    return render(request,'ViewAllJobCom.html',{'obj':obj})


@login_required(login_url=reverse_lazy('/login/'))
@user_is_employee
def ViewJobByEmployee(request):
    obj=JobDetails.objects.all()
    return render(request,'ViewAllJob.html',{'obj':obj})


def ApplyJobView(request,id):
    form = ApplicantForm(request.POST, request.FILES)
    user = get_object_or_404(User, id=request.user.id)
    qs=JobDetails.objects.get(pk=id)

    applicant=Applicant.objects.filter(user=user,job=qs.position,company=qs.company_name)
    if not applicant:
        if request.method=="POST":

            if form.is_valid():

                obj=form.save(commit=False)
                obj.user=user
                obj.resume=request.FILES['resume']
                obj.job=qs.position
                obj.company=qs.company_name
                obj.applied="True"
                obj.save()
                return HttpResponseRedirect('/view-ajob-employee/')
        pi = JobDetails.objects.get(pk=id)
        form = ApplicantForm(instance=pi)
        return render(request, 'applyjob.xhtml', {'form': form})

    else:
        return HttpResponse("Already applied for this job")

@login_required
@user_is_employee
def view_job_employee(request):
    user = get_object_or_404(User, id=request.user.id)
    job=Applicant.objects.filter(user=user)
    return render(request, 'viewappliedjobbyemp.html', {'job': job})


def view_applied_jobs(request,id):
    user=get_object_or_404(User,id=request.user.id)
    qs=Applicant.objects.filter(company=user.first_name)
    return render(request,'ViewApplicant.html',{'qs':qs})








