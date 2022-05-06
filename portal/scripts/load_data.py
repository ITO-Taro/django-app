from django.core.management import BaseCommand, call_command
from portal.models import *
from sqlalchemy import create_engine
import pandas as pd
import string

PATH = "./data/"

DB = "sqlite:///health-care-portal.db"

MEDICAL_CODE = "2021_medical_codes.xlsx"

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""

ALPHA_NUM = string.ascii_letters + string.digits
EXCEPTIONS =  ["%", " ", "-"]

class DataUpload:

    help = "Loads data from files in data/"


    def handle(self):
        if not MedCode.objects.exists():
            self.med_code()
            print("MedCode: Data Insertion Success")
        
        if not Employee.objects.exists() or not EmpLogIn.objects.exists():
            self.emp_info()
            print("Employee: Data Insertion Success")

        if not Transactions.objects.exists():
            self.transactions_table()
            print("Transactions: Data Insertion Success")
        
        if not HRLogIn.objects.exists():
            self.hr_login()
            print("HRLogIn: Data Insertion Success")
        


    def med_code(self):
        df = pd.read_excel(PATH+MEDICAL_CODE, usecols=["CODE","DESCRIPTION","CATEGORY"], index_col=False)
        for col in ["CODE", "DESCRIPTION", "CATEGORY"]:
            if col == "CODE":
                df[col] = df[col].apply(lambda x: str(x).strip(" "))
            else:
                df[col] = df[col].apply(lambda x: "".join([i for i in x.lower() if i in ALPHA_NUM or i == " "]).title())
        
        self.__to_sql(df, "medcode")

        # df.reset_index(inplace=True)
        # df.rename(columns={"index":"id"}, inplace=True)
        
        # engine = create_engine(DB, echo=False)
        # df.to_sql("MedCode", con=engine, if_exists="replace")


    def emp_info(self):
        df = pd.read_csv(PATH+"patient_accounts.txt", names=["emp_id", "title", "gender", "last_name", "first_name", "salary", "city", "state"], index_col=False)
        df = df.fillna("")
        for col in df.columns:
            df[col] = df[col].apply(lambda x: "".join([i for i in x if i.lower() in ALPHA_NUM or i in EXCEPTIONS]))
            if col == "salary":
                df[col] = df[col].astype(int)
            elif col == "city":
                df[col] = df[col].apply(lambda x: x.replace("%", " ").title())
            elif col == "first_name":
                df[col] = df[col].apply(lambda x: x.strip(" ").title())
        
        emp_auth = self.__create_emp_auth(df)

        self.__to_sql(df, "employee")
        self.__to_sql(emp_auth, "emplogin")

        # df.reset_index(inplace=True)
        # df.rename(columns={"index":"id"}, inplace=True)
        
        # engine = create_engine(DB, echo=False)
        # df.to_sql("Employee", con=engine, if_exists="replace")


    def transactions_table(self):

        df = pd.read_csv(PATH+"patient_transactions.csv", names=["emp_id", "trans_id", "procedure_date", "medical_code", "procedure_price"], converters={"procedure_price": float}, parse_dates=["procedure_date"], index_col=False)

        for col in ["emp_id", "trans_id", "medical_code"]:
            df[col] = df[col].apply(lambda x: "".join([i for i in x if ord(i) in range(48, 58) or ord(i.lower()) in range(97, 123) or i == "-"]))
        
        self.__to_sql(df, "transactions")

        # df.reset_index(inplace=True)
        # df.rename(columns={"index":"id"}, inplace=True)
        
        # engine = create_engine(DB, echo=False)
        # df.to_sql("Transactions", con=engine, if_exists="replace")
    
    def hr_login(self):
        
        df = pd.read_csv(PATH+"admin_auth.txt", names=["emp_id", "pswd"])

        self.__to_sql(df, "hrlogin")

        # df.reset_index(inplace=True)
        # df.rename(columns={"index":"id"}, inplace=True)
        
        # engine = create_engine(DB, echo=False)
        # df.to_sql("HRLogIn", con=engine, if_exists="replace")


    def __create_emp_auth(self, data):
        all_id = pd.DataFrame(data['emp_id'])

        for num in all_id.index:
            all_id.loc[num, 'pswd'] = '1111'
        
        return all_id
        
    
    def __to_sql(self, data, table_name):
        data.reset_index(inplace=True)
        data.rename(columns={"index":"id"}, inplace=True)
        
        engine = create_engine(DB, echo=False)
        data.to_sql(table_name, con=engine, if_exists="replace")


