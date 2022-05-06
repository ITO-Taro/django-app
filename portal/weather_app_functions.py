from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
import pandas as pd
import csv, json
from matplotlib.figure import Figure
import io, base64, time, datetime, os
import requests
from health_care_portal.settings import LOCATION_TOKEN, WEATHER_TOKEN

GEO_URL = "https://us1.locationiq.com/v1/search.php"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=imperial"
WEATHER_HIST_URL = "https://history.openweathermap.org/data/3.0/history/timemachine?lat=%s&lon=%s&dt=%s&appid=%s"
STATES = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}


class FindCoordinates:

    def __init__(self):
        self.coordinates = None

    def your_coordinates(self, request, address):
        
        if self.__validate_address_input(address):
        #Your unique private_token should replace value of the private_token variable.
        #To know how to obtain a unique private_token please refer the README file for this script.

            phys_address = " ".join([i for i in address.values()])
            data = {
                'key': LOCATION_TOKEN,
                'q': phys_address,
                'format': 'json'
            }

            response = requests.get(GEO_URL, params=data)

            latitude = response.json()[0]['lat']
            longitude = response.json()[0]['lon']

            res = {"location": address, "latitude": latitude, "longitude": longitude}
            # self.coordinates = res
            
            return res
            # return render_template("geolocation_result.html", coordinates=res)
        
        else:
            return False
    
    
    def __validate_address_input(self, address):
        st_num = address["street_number"].split()
        st_name = address["street_name"].split()
        city = address["city"].split()

        if all([[i.isnumeric() for i in st_num],\
            [i.isalpha() for i in st_name],\
                [i.isalpha() for i in city],\
                    (address["state"] in STATES.keys() or address["state"] in STATES.values()),\
                        self.__valid_zip(address["zip"])]):
                        return True
        else:
            return False
    
    def __valid_zip(self, zip):
        res = None
        if len(zip) < 5:
            res = False
        else:
            if len(zip) == 5 and zip.isnumeric():
                res = True
            else:
                if len(zip) > 5 and '-' in zip:
                    zip = zip.split('-')
                    if all([len(zip[0]) == 5, zip[0].isnumeric(), zip[1].isnumeric()]):
                        res = True
                    else:
                        res = False
                else:
                    res = False
        return res
    
    def current_location(self, request):
        curr_location = {
            "street_number": request.POST["st_number"],
            "street_name": request.POST["st_name"],
            "unit": request.POST["unit"],
            "city": request.POST["city"],
            "state": request.POST["state"],
            "zip": request.POST["zip"]
        }

        return curr_location
        

class Weather(FindCoordinates):

    today = datetime.datetime.today().strftime("%Y-%m-%d")

    def __init__(self, location_data):
        self.loc_data = location_data
        self.basic = self.__setup_api()

    def weather_forecast(self):

        data = self.basic

        url = WEATHER_URL % (data['lat'], data['lon'], data['key'])

        response = requests.get(url)

        res = json.loads(response.text)

        offset = res['timezone_offset']

        res = self.normalize_dt(res, offset)

        temp_data = dict()
        res["today_max"] = 0
        res["today_min"] = 100

        
        for dict_obj in res['hourly']:
            '''
            create dictionaries for all dates as the key
            '''
            date_ = dict_obj['dt'].split()[0]
            temp_data[date_] = self.hourly_temp_dict()
        
        for dict_obj in res['hourly']:
            '''
            update the dictionaries created above
            abbreviated time = keys, temp = values
            seperated this for-loop to use date as the key as opposed to date&time as key
            '''
            date_, time = dict_obj['dt'].split()
            temperature = float(dict_obj["temp"])
            temp_data[date_][time[:2]] = temperature


            if date_ == self.today:
                if temperature > res['today_max']:
                    res['today_max'] = temperature
                elif temperature < res["today_min"]:
                    res["today_min"] = temperature
        
        # Need to convert dict.keys() object into a type-list so that each element may work with dict methods (e.g, '.keys()')
        temp_data["groups"] = list(temp_data.keys())
            
        chart_url = self.__plot_chart(temp_data, "Temperature Hourly")

        res['chart_url'] = chart_url

        res["today_date"] = self.today

        return res
    
    def normalize_dt(self, data, offset):

        if isinstance(data, str):
            return
        
        if isinstance(data, dict):

            for key in data.keys():
                if (key == 'dt' or key =='sunrise' or key == 'sunset'):
                    data[key] = self.__unix_to_time(data[key], offset)
                else:
                    self.normalize_dt(data[key], offset)
        
        if isinstance(data, list):

            for item in data:
                self.normalize_dt(item, offset)
        
        return data
    
    '''
    historical data are available only to paid subscribers.
    Function out of order for now.
    '''

    def __setup_api(self):
        res = {
            "key": WEATHER_TOKEN,
            "lat": self.loc_data['latitude'],
            "lon": self.loc_data['longitude'],
            "address": self.loc_data['location']
        }

        return res
        
    def __unix_to_time(self, timestamp, offset):
        res = datetime.datetime.utcfromtimestamp(int(timestamp)+int(offset)).strftime('%Y-%m-%d %H:%M:%S')
        return res

    def __to_unix(self, date_time):
        _time = date_time.split()[0].split("-")
        _time = list(map(int, _time))
        date_ = datetime.datetime(_time[0], _time[1], _time[2], 0, 0)
        res = time.mktime(date_.timetuple())
        return res
    
    def hourly_temp_dict(self):
        res = dict()
        for num in range(24):
            if num < 10:
                num = f"0{num}"
            res[str(num)] = None
        
        return res

    def __plot_chart(self, data, title):
        fig = Figure(figsize=(9, 5))
        ax = fig.add_subplot(1,1,1)
        fig.patch.set_color("none")
        ax.set_facecolor("none")
        ax.tick_params(axis="x", colors="white", labelsize=10)
        ax.tick_params(axis="y", colors="white")
        ax.set_title(label=title, fontdict={'color':'white', 'fontsize':20})
        ax.spines["top"].set_color("white")
        ax.spines["right"].set_color("white")
        ax.spines["bottom"].set_color("white")
        ax.spines["left"].set_color("white")

        for group in data["groups"]:
            ax.plot(data[group].keys(), data[group].values(), label=group, linewidth=5)
            ax.legend(labelcolor="white", facecolor="none", edgecolor="none")
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            url = base64.b64encode(buf.getbuffer()).decode("ascii")
            res = f"data:image/png;base64,{url}"
            
        return res




