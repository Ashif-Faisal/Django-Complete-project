from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class userprofile(models.Model):

    sr_name = models.CharField(max_length=30, null=True)
    work_stream = models.CharField(max_length=30, null=True)
    task = models.CharField(max_length=300, null=True)
    value_hml = models.CharField(max_length=30, null=True)
    urgent_yn = models.BooleanField(max_length=30, null=True)
    # request_date = models.CharField(max_length=30, null=True)
    request_date = models.DateTimeField(null=True)
    needed_date = models.DateTimeField(max_length=30, null=True)
    etd = models.DateTimeField(max_length=30,null=True)
    acd = models.DateTimeField(max_length=30, null=True)
    request_by_actor = models.CharField(max_length=30, null=True)
    status = models.CharField(max_length=30, null=True)
    maker1 = models.CharField(max_length=30, null= True)
    maker2 = models.CharField(max_length=30, null=True)
    checker = models.CharField(max_length=30, null=True)
    outside_office_time = models.CharField(max_length=30, null=True)
    url = models.CharField(max_length=100, null=True)
    add_to_google = models.DateTimeField(max_length=30, null=True)
    employee_id = models.CharField(max_length=30, null=True)
    comment = models.CharField(max_length=400, null=True)
    attachment = models.FileField(max_length=100, null=True)
    approval = models.CharField(max_length=50, null=True)
    team = models.CharField(max_length=50, null=True)
    #attachment = models.FileField(upload_to='media/')
    #attachment = models.ImageField(upload_to='media',null=True)
    application_project_name = models.CharField(max_length=150, null=True)
    access_environtment = models.CharField(max_length=50, null=True)
    access_privilege_type = models.CharField(max_length=200, null=True)
    access_Duaration = models.CharField(max_length=50, null=True)
    why_access_needed = models.CharField(max_length=200, null=True)
    approved_by = models.CharField(max_length=50, null=True)
    latest_update = models.CharField(max_length=500, null=True)
    Updated_task_id = models.CharField(max_length=50, null=True)
    update_date = models.DateTimeField(max_length=50, null=True)
    company_id = models.IntegerField(max_length=50, null=True)


    def __str__(self):
        return self.sr_name


class infoUpdate(models.Model):
    latest_update = models.CharField(max_length=500, null=True)
    task_id = models.CharField(max_length=50, null=True)
    update_date = models.DateTimeField(max_length=50, null=True)
    def __str__(self):
        return self.latest_update


class companyinfo(models.Model):
    company_name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=50, null=True)
    phonenumber = models.CharField(max_length=16, null=True)
    # comp_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comp_user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True)




    def __str__(self):
        return self.comp_user_id.id



class userReg(models.Model):
    username = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=50, null=True)
    password1 = models.CharField(max_length=128, null=True)
    password2 = models.CharField(max_length=16, null=True)
    first_name = models.CharField(max_length=16, null=True)
    last_name = models.CharField(max_length=16, null=True)
    is_superuser = models.CharField(max_length=16, null=True)
    is_staff = models.CharField(max_length=16, null=True)
    comp_user_id = models.CharField(max_length=16, null=True)


class User(models.Model):
    username = models.CharField(max_length=100, null=True)
    password1 = models.CharField(max_length=128, null=True)
    password2 = models.CharField(max_length=16, null=True)

    email = models.EmailField(unique=True, max_length=255, blank=False)
    first_name = models.CharField('first name', max_length=150, blank=True)
    last_name = models.CharField('last name', max_length=150, blank=True)
    mobile = models.PositiveBigIntegerField('mobile', null=True, blank=True)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=False)
    is_superuser = models.BooleanField('superuser', default=False)
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    comp_user_id = models.CharField(max_length=16, null=True)


    def __str__(self):
        return self.email

    def full_name(self):
        return self.first_name + " " + self.last_name