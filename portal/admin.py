from django.contrib import admin
from .models import Employee, MedCode, Transactions, EmpLogIn, HRLogIn

@admin.register(MedCode)
class databaseAdmin(admin.ModelAdmin):
	list_display=['med_code','description','category']

@admin.register(Employee)
class databaseAdmin(admin.ModelAdmin):
	list_display=['emp_id','title','gender', 'last_name', 'first_name', 'salary', 'city', 'state']

@admin.register(Transactions)
class databaseAdmin(admin.ModelAdmin):
	list_display=['emp_id','trans_id','procedure_date', 'med_code', 'procedure_price']

@admin.register(EmpLogIn)
class databaseAdmin(admin.ModelAdmin):
	list_display=['emp_id','pswd']

@admin.register(HRLogIn)
class databaseAdmin(admin.ModelAdmin):
	list_display=['emp_id','pswd']


