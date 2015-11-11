from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .models import Temperature
import operator

# Create your views here.

def home(request):
    last_hour_data = Chartdata.load_last_hour()

    chart1 = {"renderTo": 'chart_1', "type": 'line', "height": 300,}
    title1 = {"text": 'Last Hour Temperature'}
    xAxis1 = {"title": {"text": 'Date'}, "categories": last_hour_data['measured'], "reversed": 'true'}
    yAxis1 = {"title": {"text": 'Temperature [C]'}}
    series1 = [
        {"name": 'Temperature [C]', "data": last_hour_data['temperature']},
        ]

    last_month_data = Chartdata.load_last_month()

    chart2 = {"renderTo": 'chart_2', "type": 'line', "height": 300,}
    title2 = {"text": 'Last 30 Days Temperature'}
    xAxis2 = {"title": {"text": 'Date'}, "categories": last_month_data['date'], "reversed": 'true'}
    yAxis2 = {"title": {"text": 'Temperature [C]'}}
    series2 = [
        {"name": 'Temperature [C]', "data": last_month_data['avg_temperature']},
        ]

    last_day_data = Chartdata.load_last_day()

    chart3 = {"renderTo": 'chart_3', "type": 'line', "height": 300,}
    title3 = {"text": 'Last 24 Hours Temperature'}
    xAxis3 = {"title": {"text": 'Date'}, "categories": last_day_data['date'], "reversed": 'true'}
    yAxis3 = {"title": {"text": 'Temperature [C]'}}
    series3 = [
        {"name": 'Temperature [C]', "data": last_day_data['avg_temperature']},
        ]

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
        'yAxis3': yAxis3
    }

    return render(request, 'home.html', chart)



class Chartdata(object):
    # def load_data():
    #     data = {'temperature': [], 'measured': [], 'incorrect': 0}
    #     data_last_30_days = {'day': [], 'avg_temp': []}
    #     values = Temperature.objects.all()
    #
    #     for x in values:
    #         print('pobieram: ' + str(x.correctness) + ' ' + str(x.measured) + ' ' + str(x.temperature))
    #         if x.correctness is not False:
    #             data['temperature'].append(x.temperature)
    #             data['measured'].append(x.measured)
    #         else:
    #             data['incorrect'] += 1
    #     return data

    def load_last_hour():
        last_hour_data = {'temperature': [], 'measured': []}
        values = Temperature.objects.raw('SELECT * FROM temperatures_temperature WHERE correctness = 1 ORDER BY id DESC LIMIT 6')

        for x in values:
            last_hour_data['temperature'].append(x.temperature)
            last_hour_data['measured'].append('%02d:%02d' % (x.measured.hour,x.measured.minute))
        return last_hour_data

    def load_last_day():
        last_day_data = {'avg_temperature': [], 'date': []}
        values = Temperature.objects.raw('SELECT AVG(temperatures_temperature.temperature) AS "avg_temperature",'
                                         ' STRFTIME("%H", measured) AS "id" FROM temperatures_temperature'
                                         ' WHERE correctness = 1 GROUP BY STRFTIME("%Y-%m-%d-%H", measured)'
                                         ' ORDER BY measured DESC LIMIT 24')
        for x in values:
            last_day_data['avg_temperature'].append(round(x.avg_temperature,2))
            last_day_data['date'].append('%s:00' % x.id)
        index, value = max(enumerate(last_day_data['avg_temperature']), key=operator.itemgetter(1))
        index2, value2 = min(enumerate(last_day_data['avg_temperature']), key=operator.itemgetter(1))
        last_day_data['avg_temperature'][index] = "{\"y\": %s, \"marker\": {\"symbol\": \"url(https://www.highcharts.com/samples/graphics/sun.png)\"}}" % value
        last_day_data['avg_temperature'][index2] = "{\"y\": %s, \"marker\": {\"symbol\": \"url(https://www.highcharts.com/samples/graphics/snow.png)\"}}" % value2

        return last_day_data

    def load_last_month():
        last_month_data = {'avg_temperature': [], 'date': []}
        values = Temperature.objects.raw('SELECT AVG(temperatures_temperature.temperature) as "avg_temperature", '
                                         'STRFTIME("%d-%m", measured) as "id" FROM temperatures_temperature '
                                         'WHERE correctness = 1 GROUP BY STRFTIME("%Y-%m-%d", measured) '
                                         'ORDER BY STRFTIME("%Y-%m-%d", measured) DESC LIMIT 30')
        for x in values:
            last_month_data['avg_temperature'].append(round(x.avg_temperature,2))
            last_month_data['date'].append(x.id)
        return last_month_data