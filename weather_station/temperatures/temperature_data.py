from django.conf import settings
from .models import Temperature
import operator


class Chartdata(object):
    @staticmethod
    def load_last_hour():
        last_hour_data = {'temperature': [], 'measured': []}
        values = Temperature.objects.filter(correctness=1).order_by('-id')[:6:1]
        for x in values:
            last_hour_data['temperature'].append(x.temperature)
            last_hour_data['measured'].append('%02d:%02d' % (x.measured.hour, x.measured.minute))
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
        if last_day_data['avg_temperature']:
            index_max, value_max = max(enumerate(last_day_data['avg_temperature']), key=operator.itemgetter(1))
            index_min, value_min = min(enumerate(last_day_data['avg_temperature']), key=operator.itemgetter(1))
            last_day_data['avg_temperature'][index_max] = "{\"y\": %s, \"marker\": {\"symbol\": \"url(%ssun.png)\"}}" \
                                                          % (value_max, settings.STATIC_URL)
            last_day_data['avg_temperature'][index_min] = "{\"y\": %s, \"marker\": {\"symbol\": \"url(%ssnow.png)\"}}" \
                                                          % (value_min, settings.STATIC_URL)

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
