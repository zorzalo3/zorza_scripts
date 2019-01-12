#!/usr/bin/env python3
import os, django, sys, itertools, operator
import calendar
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zorza.settings')
django.setup()

from timetable.models import *

"""Oddziela BO od klas"""

day_names = ['Pn', 'Wt', 'Śr', 'Cz', 'Pt', 'So', 'Nd']

to_split = ['BO', 'BOF']

subjects = Subject.objects.filter(short_name__in=to_split)

lessons = Lesson.objects.filter(subject__in=subjects)
for l in lessons:
    new_name = '{} {} {} {}'.format(
        l.group.name.split()[0],
        l.teacher.initials,
        l.subject.short_name,
        day_names[l.weekday])
    if new_name == l.group.name:
        continue
    new_group = Group(name=new_name)
    new_group.save()
    new_group.classes.add(*l.group.classes.all())
    similar = Lesson.objects.filter(subject=l.subject, teacher=l.teacher,
                                    weekday=l.weekday, group=l.group)
    similar.update(group=new_group)
