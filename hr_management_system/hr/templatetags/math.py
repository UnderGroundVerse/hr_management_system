from . import register
from django.contrib.auth.models import Group 
from Employees.models import Hrrole, Employee



@register.filter(name='multiply')
def multiply(value, arg):
    return float(value) * float(arg)

@register.filter(name='count_subteam_members')
def count_subteam_members(value):
    return Employee.objects.filter(sub_team=value).count()


@register.filter(name='count_subteam_members_excluding_types')
def count_subteam_members_excluding_types(sub_team):
    excluded_types = ['Alumni', 'Left', 'Dismissed', 'Guest', 'Unknown']
    return Employee.objects.filter(sub_team=sub_team).exclude(user_type__type__in=excluded_types).count()
