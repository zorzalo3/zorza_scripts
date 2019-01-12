from timetable.models import Schedule, Period
from datetime import time


periods = [
    {
        'number':       0,
        'begin_time':   time(7, 25),
        'end_time':     time(7, 55)
    },
    {
        'number':       1,
        'begin_time':   time(8, 00),
        'end_time':     time(8, 30)
    },
    {
        'number':       2,
        'begin_time':   time(8, 40),
        'end_time':     time(9, 10)
    },
    {
        'number':       3,
        'begin_time':   time(9, 20),
        'end_time':     time(9, 50)
    },
    {
        'number':       4,
        'begin_time':   time(10, 5),
        'end_time':     time(10, 35)
    },
    {
        'number':       5,
        'begin_time':   time(10, 45),
        'end_time':     time(11, 15)
    },
    {
        'number':       6,
        'begin_time':   time(11, 25),
        'end_time':     time(11, 55)
    },
    {
        'number':       7,
        'begin_time':   time(12, 5),
        'end_time':     time(12, 35)
    },
    {
        'number':       8,
        'begin_time':   time(12, 40),
        'end_time':     time(13, 10)
    },
]

if not Schedule.objects.filter(name='Skrócone lekcje').exists():
    shortened = Schedule(name='Skrócone lekcje', is_default=False)
    shortened.save()
    Period.objects.bulk_create([Period(schedule=shortened, **kwargs) for kwargs in periods])
