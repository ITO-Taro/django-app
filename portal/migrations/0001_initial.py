# Generated by Django 4.0.4 on 2022-05-07 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmpLogIn',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('emp_id', models.CharField(max_length=30)),
                ('pswd', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'emplogin',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('emp_id', models.CharField(db_column='emp_id', max_length=30)),
                ('title', models.CharField(max_length=20)),
                ('gender', models.CharField(max_length=10)),
                ('last_name', models.CharField(max_length=30)),
                ('first_name', models.CharField(max_length=30)),
                ('salary', models.IntegerField()),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=15)),
            ],
            options={
                'verbose_name_plural': 'EMPloyees',
                'db_table': 'employee',
            },
        ),
        migrations.CreateModel(
            name='HRLogIn',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('emp_id', models.CharField(max_length=30)),
                ('pswd', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'hrlogin',
            },
        ),
        migrations.CreateModel(
            name='MedCode',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('med_code', models.CharField(db_column='CODE', max_length=30)),
                ('description', models.CharField(max_length=30)),
                ('category', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'MEDcodes',
                'db_table': 'medcode',
            },
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('emp_id', models.CharField(db_column='emp_id', max_length=30)),
                ('trans_id', models.CharField(max_length=30)),
                ('procedure_date', models.DateTimeField(verbose_name='proc_date')),
                ('med_code', models.CharField(db_column='medical_code', max_length=30)),
                ('procedure_price', models.FloatField()),
            ],
            options={
                'verbose_name_plural': 'TRansactions',
                'db_table': 'transactions',
            },
        ),
    ]
