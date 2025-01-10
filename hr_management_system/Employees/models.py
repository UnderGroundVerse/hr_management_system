from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from .managers import EmployeeManager
from django.db.models.signals import *


class Employee(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField(blank=True, null=True)
    is_staff = models.IntegerField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    date_joined = models.DateTimeField(blank=True, null=True)
    first_name = models.CharField(max_length=25, blank=True, null=True)
    last_name = models.CharField(max_length=25, blank=True, null=True)
    full_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(unique=True, max_length=254)
    profile_picture = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(unique=True, max_length=11)
    sub_team = models.ForeignKey('Subteam', models.DO_NOTHING, blank=True, null=True)
    team = models.ForeignKey('Team', models.DO_NOTHING, blank=True, null=True)
    
    objects = EmployeeManager()
    
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
   
    class Meta:
        managed = True
        db_table = 'employee'


class Hrrole(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    member = models.OneToOneField(Employee, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'hrrole'


class HrroleTeams(models.Model):
    hrrole = models.OneToOneField(Hrrole, models.DO_NOTHING, primary_key=True)  # The composite primary key (hrrole_id, team_id) found, that is not supported. The first column is selected.
    team = models.ForeignKey('Team', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'hrrole_teams'
        unique_together = (('hrrole', 'team'),)


class Meeting(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    scheduled_at = models.DateTimeField()
    required_to_attend = models.IntegerField(default=0)
    evaluated = models.IntegerField(default=0)
    created_by = models.ForeignKey(Employee, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'meeting'


# class MeetingSubTeams(models.Model):
#     meeting = models.OneToOneField(Meeting, models.DO_NOTHING, primary_key=True)  # The composite primary key (meeting_id, subteam_id) found, that is not supported. The first column is selected.
#     subteam = models.ForeignKey('Subteam', models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'meeting_sub_teams'
#         unique_together = (('meeting', 'subteam'),)


# class MeetingTeams(models.Model):
#     meeting = models.OneToOneField(Meeting, models.DO_NOTHING, primary_key=True)  # The composite primary key (meeting_id, team_id) found, that is not supported. The first column is selected.
#     team = models.ForeignKey('Team', models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'meeting_teams'
#         unique_together = (('meeting', 'team'),)


class Meetingevaluation(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attendance = models.CharField(max_length=2)
    task = models.SmallIntegerField()
    performance = models.SmallIntegerField()
    interaction = models.SmallIntegerField()
    behavior = models.SmallIntegerField()
    bonus = models.IntegerField()
    total = models.SmallIntegerField()
    comment = models.CharField(max_length=500)
    created_by = models.ForeignKey(Employee, models.DO_NOTHING, blank=True, null=True)
    meeting = models.ForeignKey(Meeting, models.DO_NOTHING)
    member = models.ForeignKey(Employee, models.DO_NOTHING, related_name='meetingevaluation_member_set')
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.total = self.task + self.performance + self.behavior + self.interaction + self.bonus 
        return super().save(force_insert, force_update, using, update_fields)

    class Meta:
        managed = False
        db_table = 'meetingevaluation'


class Rating(models.Model):
    id = models.BigAutoField(primary_key=True)
    task = models.SmallIntegerField(default=0)
    performance = models.SmallIntegerField(default=0)
    interaction = models.SmallIntegerField(default=0)
    behavior = models.SmallIntegerField(default=0)
    bonus = models.SmallIntegerField(default=0)
    total = models.SmallIntegerField(default=0)
    attended_meetings = models.SmallIntegerField(default=0)
    unattended_meetings = models.SmallIntegerField(default=0)
    employee = models.OneToOneField(Employee, models.DO_NOTHING)

    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.total = self.task + self.performance + self.behavior + self.interaction + self.bonus 
        return super().save(force_insert, force_update, using, update_fields)
    class Meta:
        managed = False
        db_table = 'rating'


class Subteam(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    team = models.ForeignKey('Team', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'subteam'
        unique_together = (('team', 'name'),)


class Team(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'team'
        
        
        
class Warnings(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_official = models.IntegerField()
    warning_type = models.CharField(max_length=20)
    notes = models.TextField(blank=True, null=True)
    employee = models.ForeignKey(Employee, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'warnings'
        
        
        
        
        
def update_rating(sender, instance, **kwargs):
    member = instance.member
    rating = Rating.objects.raw(f'''
     SELECT *
    FROM rating 
    WHERE rating.employee_id = {member.id};
                                ''')[0]
    if not rating:
        rating = Rating.objects.create(employee=member)
    meetings = Meeting.objects.raw('''
    SELECT * 
    FROM meeting 
    WHERE (meeting.evaluated = 1 AND meeting.required_to_attend = 1);                               
    ''')
    evaluations = Meetingevaluation.objects.raw(f'''
    SELECT *
    FROM meetingevaluation 
    WHERE (meetingevaluation.meeting_id IN (5) AND meetingevaluation.member_id = {member.id});

                                                ''')
    avg_behavior = 0
    avg_task = 0
    avg_performance = 0
    avg_interaction = 0
    avg_bonus = 0
    avg_total = 0
    attended_meetings_num = 0
    unattended_meetings_num = 0
    for evaluation in evaluations:
        avg_behavior += evaluation.behavior
        avg_task += evaluation.task
        avg_performance += evaluation.performance
        avg_interaction += evaluation.interaction
        avg_bonus += evaluation.bonus
        avg_total += evaluation.total
        if evaluation.attendance  == 'A':
            attended_meetings_num += 1
        elif evaluation.attendance == 'M':
            unattended_meetings_num += 1
    if len(evaluations) > 0:
        avg_behavior /= len(evaluations)
        avg_task /= len(evaluations)
        avg_performance /= len(evaluations)
        avg_interaction /= len(evaluations)
        avg_bonus /= len(evaluations)
        avg_total /= len(evaluations)
    else:
        avg_behavior = 0
        avg_task = 0
        avg_performance = 0
        avg_interaction = 0
        avg_bonus = 0
        avg_total = 0
    
    rating.behavior = int(avg_behavior)
    rating.task = int(avg_task)
    rating.performance = int(avg_performance)
    rating.interaction = int(avg_interaction)
    rating.bonus = int(avg_bonus)
    rating.total = int(avg_total)
    rating.attended_meetings = attended_meetings_num
    rating.unattended_meetings = unattended_meetings_num
    rating.save()



post_save.connect(update_rating, Meetingevaluation)

post_delete.connect(update_rating, Meetingevaluation)