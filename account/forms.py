from .models import User,JobDetails,Applicant
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, forms
from django.contrib.auth import get_user_model, authenticate


class EmployeeRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeRegisterForm, self).__init__(*args, **kwargs)
        self.fields["gender"].required = True
        self.fields["first_name"].label = "First Name"
        self.fields["last_name"].label = "Last Name"
        self.fields["password1"].label = "Password"
        self.fields["password2"].label = "Confirm Password"

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'gender']

    def save(self, commit=True):
        user = super(EmployeeRegisterForm, self).save(commit=False)
        user.role = "employee"
        if commit:
            user.save()

        return user


class EmployerRegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(EmployerRegisterForm, self).__init__(*args, **kwargs)

        self.fields["first_name"].label = "Company Name"
        self.fields["last_name"].label = "Comapny Address"
        self.fields["password1"].label = "Password"
        self.fields["password2"].label = "Confirm Password"

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


    def save(self, commit=True):
        user = super(EmployerRegisterForm, self).save(commit=False)
        user.role = "employer"
        if commit:
            user.save()

        return user



class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user = authenticate(email=email, password=password)

        return super(LoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user


class JobDetailForm(forms.ModelForm):
    class Meta:
        model=JobDetails
        exclude = (
            "user",
            "created_at",
            "company_name",
            "company_address"
        )

    def save(self, commit=True, user=None):
        job = super(JobDetailForm, self).save(commit=False)
        if commit:
            user.save()
           
        return job

class ApplicantForm(forms.ModelForm):
    class Meta:
        model=Applicant
        fields=['resume']

