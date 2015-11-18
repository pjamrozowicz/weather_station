from django.conf import settings
from django.shortcuts import render
from .forms import NewsletterForm
from .models import Temperature
import operator

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


class Chartdata(object):
    @staticmethod
    def load_last_hour():
        last_hour_data = {'temperature': [], 'measured': []}
        values = Temperature.objects.raw('SELECT * FROM temperatures_temperature '
                                         'WHERE correctness = 1 ORDER BY id DESC LIMIT 6')

        for x in values:
            last_hour_data['temperature'].append(x.temperature)
            last_hour_data['measured'].append('%02d:%02d' % (x.measured.hour,x.measured.minute))
        return last_hour_data

    @staticmethod
    def load_last_day():
        last_day_data = {'avg_temperature': [], 'date': []}
        values = Temperature.objects.raw('SELECT AVG(temperatures_temperature.temperature) AS "avg_temperature",'
                                         ' STRFTIME("%H", measured) AS "id" FROM temperatures_temperature'
                                         ' WHERE correctness = 1 GROUP BY STRFTIME("%Y-%m-%d-%H", measured)'
                                         ' ORDER BY measured DESC LIMIT 24')
        for x in values:
            last_day_data['avg_temperature'].append(round(x.avg_temperature,2))
            last_day_data['date'].append('%s:00' % x.id)
        index_max, value_max = max(enumerate(last_day_data['avg_temperature']), key=operator.itemgetter(1))
        index_min, value_min = min(enumerate(last_day_data['avg_temperature']), key=operator.itemgetter(1))
        last_day_data['avg_temperature'][index_max] = "{\"y\": %s, \"marker\":" \
                                                   " {\"symbol\": \"url(%ssun.png)\"}" \
                                                      "}" % (value_max, settings.STATIC_URL)
        last_day_data['avg_temperature'][index_min] = "{\"y\": %s, \"marker\":" \
                                                   " {\"symbol\": \"url(%ssnow.png)\"}" \
                                                      "}" % (value_min, settings.STATIC_URL)

        return last_day_data

    @staticmethod
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

    @staticmethod
    def load_last_year():
        last_year_data = {'avg_temperature': [], 'month': []}
        list_of_months = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June',
                          '07': 'July', '08': 'August', '09': 'September', '10': 'October',
                          '11': 'November', '12': 'December'}
        values = Temperature.objects.raw('SELECT AVG(temperatures_temperature.temperature) AS "avg_temperature",'
                                         ' STRFTIME("%m", measured) as "id" FROM temperatures_temperature'
                                         ' GROUP BY STRFTIME("%Y-%m", measured) '
                                         'ORDER BY STRFTIME("%Y-%m", measured) DESC LIMIT 12')
        for x in values:
            last_year_data['avg_temperature'].append(round(x.avg_temperature,2))
            last_year_data['month'].append(list_of_months[x.id])
        return last_year_data
