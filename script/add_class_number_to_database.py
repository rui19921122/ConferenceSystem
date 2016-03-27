import datetime
import sys, os

path = os.path.realpath(os.getcwd())
sys.path.append(r'C:\Users\Administrator\Desktop\ConferenceSystem')
os.environ['DJANGO_SETTINGS_MODULE'] = 'ConferenceSystem.settings'
from django.conf import settings
import django

django.setup()

from call_over.models import CallOverNumber

today = datetime.date(year=2016, day=25, month=3)
timedelta = datetime.timedelta(days=1)
today_day = 3
today_night = 2
for num in range(0, 10000):
    date = today + num * timedelta
    number = num % 4
    if number == 0:
        CallOverNumber.objects.create(day_number=1, class_number=3, date=date)
        CallOverNumber.objects.create(day_number=2, class_number=2, date=date)
    elif number == 1:
        CallOverNumber.objects.create(day_number=1, class_number=4, date=date)
        CallOverNumber.objects.create(day_number=2, class_number=3, date=date)
    elif number == 2:
        CallOverNumber.objects.create(day_number=1, class_number=1, date=date)
        CallOverNumber.objects.create(day_number=2, class_number=4, date=date)
    elif number == 3:
        CallOverNumber.objects.create(day_number=1, class_number=2, date=date)
        CallOverNumber.objects.create(day_number=2, class_number=1, date=date)