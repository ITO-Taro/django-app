import datetime
from tabnanny import verbose

from django.db import models
from django.utils import timezone
from .management.commands.load_data import Command as com





class MedCode(models.Model):

    id = models.AutoField(primary_key=True)
    med_code = models.CharField(max_length=30, db_column="CODE")
    description = models.CharField(max_length=30)
    category = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "MEDcodes"
        db_table = "medcode"


class Employee(models.Model):

    id = models.AutoField(primary_key=True)
    emp_id = models.CharField(max_length=30, db_column="emp_id")
    title = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    salary = models.IntegerField()
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=15)

    class Meta:
        verbose_name_plural = "EMPloyees"
        db_table = "employee"


class Transactions(models.Model):

    id = models.AutoField(primary_key=True)
    emp_id = models.CharField(max_length=30, db_column="emp_id")
    trans_id = models.CharField(max_length=30)
    procedure_date =models.DateTimeField("proc_date")
    med_code = models.CharField(max_length=30, db_column="medical_code")
    procedure_price = models.FloatField()

    class Meta:
        verbose_name_plural = "TRansactions"
        db_table = "transactions"



class HRLogIn(models.Model):
    
    id = models.AutoField(primary_key=True)
    emp_id = models.CharField(max_length=30)
    pswd = models.CharField(max_length=30)

    class Meta:
        db_table = "hrlogin"

class EmpLogIn(models.Model):

    id = models.AutoField(primary_key=True)
    emp_id = models.CharField(max_length=30)
    pswd = models.CharField(max_length=30)

    class Meta:
        db_table = "emplogin"

