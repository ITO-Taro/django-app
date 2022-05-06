from django.urls import path
from . import views

app_name = "portal"

urlpatterns = [
    path("", views.portal_home, name='home'),
    path("hr-login/", views.LogIn.hr_login, name='hr-login'),
    path("hr-portal", views.HrPortal.home, name="hr-home"),
    path("emp-login/", views.LogIn.emp_login, name='emp-login'),
    path("emp-portal", views.EmpPortal.home, name="emp-home"),
    path('emp-search-last/', views.HrPortal.emp_search_last, name='emp-search'),
    path('emp-search-last/res/', views.HrPortal.emp_search_last_res, name='emp-search-res'),
    path("weather-forecast/", views.WeatherForecast.coordinates_and_weather, name="weather-app")
    # path('emp-search-salary/', views.ResultsView.as_view(), name='emp-search-salary'),
    # path('hr-portal/', views.vote, name='hr-portal'),
]