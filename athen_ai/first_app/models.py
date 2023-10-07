from django.db import models
from django.core.exceptions import ValidationError

def validate_duration(start_date, end_date):
    if end_date <= start_date:
        raise ValidationError('End date must be after the start date.')

# MAIN MODELS
class User(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True,unique=True,blank=False)
    name = models.CharField(unique=True,blank=False)
    first_name = models.CharField(unique=False,blank=False)
    last_name = models.CharField(unique=False,blank=True)
    email = models.EmailField(blank=False)

class Domain(models.Model):
    
    domain_id = models.PositiveIntegerField(primary_key=True,unique=True,blank=False)
    domain_name = models.CharField(max_length=100,blank=False,unique=True)
    domain_info = models.CharField(max_length=1000,blank=True)


class Skills(models.Model):

    skill_id = models.PositiveIntegerField(primary_key=True,unique=True,blank=False)
    skill_name = models.CharField(unique=True,max_length=100,blank=False)

class Project(models.Model):

    project_id = models.PositiveIntegerField(primary_key=True,unique=True,blank=False)
    project_owner = models.ForeignKey(User,on_delete=models.CASCADE)
    
    start_date = models.DateField(blank=False,unique=False)
    end_date = models.DateField(blank=False,unique=False,validators=[validate_duration])


# Connecting models
class PersonSkills(models.Model):

    person = models.ForeignKey(User,on_delete=models.CASCADE)
    skill = models.ForeignKey(Skills,on_delete=models.CASCADE)

    class Meta:

        primary_key = ['person','skill']


class ProjectSkillsReq(models.Model):

    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    skill = models.ForeignKey(Skills,on_delete=models.CASCADE)
    weightage = models.IntegerField(blank=False)

class PersonsProject(models.Model):
    person = models.ForeignKey(User,on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    
    approval_choices = [
        ('selected', 'Selected'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
    ]
    # Define the categorical column using CharField with choices
    approval = models.CharField(choices= approval_choices, default='pending')
    