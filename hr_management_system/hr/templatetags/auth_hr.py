from . import register
from django.contrib.auth.models import Group 
from Employees.models import Hrrole



@register.filter(name='has_hrRole')
def has_hrRole(user):
    return Hrrole.objects.filter(member=user).exists()

