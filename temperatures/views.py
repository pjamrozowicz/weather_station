from django.shortcuts import render
from .forms import NewsletterForm
from .temperature_data import *
from .sun import *

# Create your views here.


def home(request):
    last_hour_data = Chartdata.load_last_hour()

    chart1 = {"renderTo": 'chart_1', "type": 'line', "height": 300}
    title1 = {"text": 'Last Hour Temperature'}
    xAxis1 = {"title": {"text": 'Date'}, "categories": last_hour_data['measured'], "reversed": 'true'}
    yAxis1 = {"title": {"text": 'Temperature [C]'}}
    series1 = [{"name": 'Temperature [C]', "data": last_hour_data['temperature']}]

    last_month_data = Chartdata.load_last_month()

    chart2 = {"renderTo": 'chart_2', "type": 'line', "height": 300}
    title2 = {"text": 'Last 30 Days Temperature'}
    xAxis2 = {"title": {"text": 'Date'}, "categories": last_month_data['date'], "reversed": 'true'}
    yAxis2 = {"title": {"text": 'Temperature [C]'}}
    series2 = [{"name": 'Temperature [C]', "data": last_month_data['avg_temperature']}]

    last_day_data = Chartdata.load_last_day()

    chart3 = {"renderTo": 'chart_3', "type": 'line', "height": 300}
    title3 = {"text": 'Last 24 Hours Temperature'}
    xAxis3 = {"title": {"text": 'Date'}, "categories": last_day_data['date'], "reversed": 'true'}
    yAxis3 = {"title": {"text": 'Temperature [C]'}}
    series3 = [{"name": 'Temperature [C]', "data": last_day_data['avg_temperature']}]

    last_year_data = Chartdata.load_last_year()

    chart4 = {"renderTo": 'chart_4', "type": 'line', "height": 300}
    title4 = {"text": 'Last 12 Months Temperature'}
    xAxis4 = {"title": {"text": 'Date'}, "categories": last_year_data['month'], "reversed": 'true'}
    yAxis4 = {"title": {"text": 'Temperature [C]'}}
    series4 = [{"name": 'Temperature [C]', "data": last_year_data['avg_temperature']}]

    sun = Sun('50.05', '19.93')  # Coordinates for Cracow
    sunrise = sun.next_rising()
    sunset = sun.next_sunset()

    form = NewsletterForm(request.POST or None)
    if form.is_valid():
        form.save()

    chart = {
        'chartID1': 'chart_1',
        'chart1': chart1,
        'series1': series1,
        'title1': title1,
        'xAxis1': xAxis1,
        'yAxis1': yAxis1,
        'chartID2': 'chart_2',
        'chart2': chart2,
        'series2': series2,
        'title2': title2,
        'xAxis2': xAxis2,
        'yAxis2': yAxis2,
        'chartID3': 'chart_3',
        'chart3': chart3,
        'series3': series3,
        'title3': title3,
        'xAxis3': xAxis3,
        'yAxis3': yAxis3,
        'chartID4': 'chart_4',
        'chart4': chart4,
        'series4': series4,
        'title4': title4,
        'xAxis4': xAxis4,
        'yAxis4': yAxis4,
        'form': form
    }

    return render(request, 'home.html', chart)
