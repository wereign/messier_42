from django.db import models
from django.core.exceptions import ValidationError

def validate_duration(start_date, end_date):
    if end_date <= start_date:
        raise ValidationError('End date must be after the start date.')

# MAIN MODELS
class User(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True,unique=True,blank=False)
    name = models.CharField(unique=True,blank=False,max_length=20)
    first_name = models.CharField(unique=False,blank=False,max_length=20)
    last_name = models.CharField(unique=False,blank=True,max_length=20)
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

    project_status_choices = [
        ('in progress', 'In Progress'),
        ('not started', 'Not Started'),
        ('completed', 'Completed'),
    ]
    # Define the categorical column using CharField with choices
    approval = models.CharField(choices= project_status_choices, default='not started',max_length=20)
    license = models.CharField(max_length=256,blank=False,unique=False)
    repository_link = models.URLField(unique=False,blank=False)
    demo_link = models.URLField(unique=False,blank=False)
    dataset_link = models.URLField(unique=False,blank=False)

# Connecting models
class PersonSkills(models.Model):
    row_no = models.PositiveIntegerField(primary_key=True)
    person = models.ForeignKey(User,on_delete=models.CASCADE)
    skill = models.ForeignKey(Skills,on_delete=models.CASCADE)
    
    # TODO: add constraints to check that combination of project and domain are unique
    class Meta:
        unique_together = ['person','skill']


class ProjectSkillsReq(models.Model):

    row_no = models.PositiveIntegerField(primary_key=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    skill = models.ForeignKey(Skills,on_delete=models.CASCADE)
    weightage = models.IntegerField(blank=False)

    class Meta:
        unique_together = ['project','skill','weightage']


class PersonsProject(models.Model):

    row_no = models.PositiveIntegerField(primary_key=True)
    person = models.ForeignKey(User,on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    
    approval_choices = [
        ('selected', 'Selected'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
    ]
    # Define the categorical column using CharField with choices
    approval = models.CharField(choices= approval_choices, default='pending',max_length=20)

class ProjectDomain(models.Model):

    row_no = models.PositiveIntegerField(primary_key=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    domain = models.ForeignKey(Domain,on_delete=models.CASCADE)

    # TODO: add constraints to check that combination of project and domain are unique
    class Meta:
        unique_together = ['project','domain']