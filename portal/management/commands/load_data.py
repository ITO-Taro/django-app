from django.core.management import BaseCommand, call_command
from portal.models import *
from sqlalchemy import create_engine
import pandas as pd


path = "./data/"

DB = "sqlite:///health-care-portal.db"

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""

class Command(BaseCommand):

    help = "Loads data from files in data/"

    @classmethod
    def handle():
        if not MedCode.objects.exists():
            Command.med_code()
        
        if not Employee.objects.exists():
            Command.emp_info()
        
        if not Transactions.objects.exists():
            Command.transactions_table()

    def med_code(self):
        df = pd.read_excel(path+"2021_medical_codes.xlsx", index_col=False, usecols=["CODE","DESCRIPTION","CATEGORY"])
        for col in ["CODE", "DESCRIPTION", "CATEGORY"]:
            if col == "CODE":
                df[col] = df[col].apply(lambda x: str(x).strip(" "))
            else:
                df[col] = df[col].apply(lambda x: "".join([i for i in x.lower() if ord(i) in range(97, 123) or ord(i) in range(47, 58) or i == " "]).title())
        engine = create_engine(DB, echo=False)
        df.to_sql("MedCode", con=engine, if_exists="replace")
        # for num in df.index:
        #     med_code = MedCode(code = df.loc[num, "CODE"], description = df.loc[num, "DESCRIPTION"], category = df.loc[num, "CATEGORY"])
        #     med_code.save()
        # return

    def emp_info(self):
        df = pd.read_csv(path+"patient_accounts.txt", index_col=False, names=["emp_id", "title", "gender", "last_name", "first_name", "salary", "city", "state"])
        df = df.fillna("")
        for col in df.columns:
            df[col] = df[col].apply(lambda x: "".join([i for i in x if ord(i.lower()) in range(97, 123) or ord(i) in range(48, 58) or i == "%" or i == " " or i == "-"]))
            if col == "salary":
                df[col] = df[col].astype(int)
            elif col == "city":
                df[col] = df[col].apply(lambda x: x.replace("%", " ").title())
            elif col == "first_name":
                df[col] = df[col].apply(lambda x: x.strip(" ").title())
        engine = create_engine(DB, echo=False)
        df.to_sql("Employee", con=engine, if_exists="replace")
        # for num in df.index:
        #     emp = Employee(emp_id=df.loc[num, "emp_id"], title=df.loc[num, "title"], \
        #         gender=df.loc[num, "gender"], last_name=df.loc[num, "last_name"], first_name=df.loc[num, "first_name"],\
        #             salary=df.loc[num, "salary"], city=df.loc[num, "city"], state=df.loc[num, "state"])
        #     emp.save()
        # return

    def transactions_table(self):

        df = pd.read_csv(path+"patient_transactions.csv", names=["emp_id", "trans_id", "procedure_date", "medical_code", "procedure_price"], converters={"procedure_price": float}, parse_dates=["procedure_date"])

        for col in ["emp_id", "trans_id", "medical_code"]:
            df[col] = df[col].apply(lambda x: "".join([i for i in x if ord(i) in range(48, 58) or ord(i.lower()) in range(97, 123) or i == "-"]))
        engine = create_engine(DB, echo=False)
        df.to_sql("Transactions", con=engine, if_exists="replace")
        # for num in df.index:
        #     transaction = Transactions(emp_id=df.loc[num, "emp_id"], trans_id=df.loc[num, "trans_id"],\
        #         procedure_date=df.loc[num, "procedure_date"], medical_code=df.loc[num, "medical_code"], procedure_price=df.loc[num, "procedure_price"])
        #     transaction.save()
        # return
    


