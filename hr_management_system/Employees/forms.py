from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from Employees.models import *



class MemberRegisterForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = ("first_name", "last_name", "email", 'team', 'phone_number',  'profile_picture')

class MemberUpdateForm(UserChangeForm):
    class Meta:
        model = Employee
        fields = (
            "first_name", "last_name",  'phone_number',   'profile_picture'
        )