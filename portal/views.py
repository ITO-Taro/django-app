from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .weather_app_functions import Weather, FindCoordinates as coor
from .models import Employee, MedCode, HRLogIn, EmpLogIn, Transactions

SEARCH_LIMIT = 30


def portal_home(request):
    return render(request, "portal/index.html")


class LogIn:

    @csrf_protect
    def emp_login(request):

        if request.method == "POST":
            input_id = request.POST['user_id']
            input_pswd = request.POST['password']
            
            pswd = str(EmpLogIn.objects.filter(emp_id=input_id).values("pswd")[0]["pswd"])

            if input_pswd == pswd:
                HttpResponseRedirect("/portal/emp-portal")

                res = dict()
                
                res['emp'] = Employee.objects.filter(emp_id=input_id)[0]

                medicals = Transactions.objects.filter(emp_id=res['emp'].emp_id).order_by("procedure_date")

                res['med'] = dict()

                for indx, med in enumerate(medicals):
                    indx = str(indx)
                    code_info = MedCode.objects.filter(med_code=med.med_code)[0]
                    res['med'][indx] = {"date": med.procedure_date.date, "code": med.med_code, "decsript": code_info.description, "price": med.procedure_price, "t_id": med.trans_id}
                    


                return render(request, "portal/emp_portal.html", {'res': res})
                # return render(request, "portal/test.html", {'res': res})
            else:
                return render(request, "portal/emp_login.html", {"message": "Wrong Employee ID or Password"})

        else:
            return render(request, "portal/emp_login.html", {"message": ""})

    @csrf_protect
    def hr_login(request):

        if request.method == "POST":
            input_id = request.POST['user_id']
            input_pswd = request.POST['password']
            
            pswd = str(HRLogIn.objects.filter(emp_id=input_id).values("pswd")[0]["pswd"])

            if input_pswd == pswd:
                return HttpResponseRedirect("/portal/hr-portal")
            else:
                return render(request, "portal/hr_login.html", {"message": "Wrong Employee ID or Password"})

        else:
            return render(request, "portal/hr_login.html", {"message": ""})

class HrPortal:

    def home(request):
        return render(request, "portal/hr_portal.html")

    def emp_search_last(request):
        return render(request, "portal/hr_emp_search_last.html", {"search_limit": SEARCH_LIMIT})

    @csrf_protect
    def emp_search_last_res(request):
        template = "portal/hr_emp_search_last_result.html"
        name = HrPortal.__get_form(request).upper()

        res = Employee.objects.filter(last_name__contains=name)

        total_match = len(res)

        if res:
            res = res[:SEARCH_LIMIT]

        return render(request, template, {"res": res, "search_limit": SEARCH_LIMIT, "total_match":total_match})

    def __get_form(request):
        input = request.POST
        return input['key_word']

class EmpPortal:

    def home(request):
        return render(request, "portal/emp_portal.html")

    def emp_search_last(request):
        return render(request, "portal/emp_emp_search_last.html", {"search_limit": SEARCH_LIMIT})

    @csrf_protect
    def emp_search_last_res(request):
        template = "portal/emp_emp_emp_search_last_result.html"
        input_id = EmpPortal.__get_form(request).upper()

        res = Employee.objects.filter(emp_id=input_id)



        return render(request, template, {"res": res})

    def __get_form(request):
        input = request.POST
        return input['emp_id']

class WeatherForecast:

    def coordinates_and_weather(request):

        if request.method == "POST":
            curr_location = coor().current_location(request)

            loc_data = coor().your_coordinates(request, curr_location)

            data = Weather(loc_data).weather_forecast()

            data['current']['sunrise'] = data['current']['sunrise'].split()[1]
            data['current']['sunset'] = data['current']['sunset'].split()[1]

            HttpResponseRedirect("/portal/weather-forecast")

            return render(request, "portal/coordinates&weather_result.html", {"data":data})
            
        else:
            return render(request, "portal/coordinates&weather.html")