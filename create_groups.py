#!/usr/bin/env python3
import os, django, sys, itertools, operator
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zorza.settings')
django.setup()

from timetable.models import *

"""Tworzy nową grupę jeśli nauczyciel ma lekcje z kilkoma klasami.
Tak jest w przypadku np. BO"""

def merge_names(names):
    """Łączy nazwy klas tak:
        ['1A', '2A', '3A'] => '123A'
        ['2A', '2B'] => '2AB'
    """
    firsts = sorted({name[0] for name in names})
    seconds = sorted({name[1] for name in names})
    return "".join(firsts+seconds)


for lesson in Lesson.objects.all():
    similar = Lesson.objects.filter(teacher=lesson.teacher, room=lesson.room,
        period=lesson.period, weekday=lesson.weekday)
    if similar.count() > 1:
        values = similar.values('id', 'group__name', 'group__classes')
        common = values[0]['group__name'].split(' ', 1)[1]
        class_names = []
        class_ids = []
        for obj in values:
            klass = obj['group__name'][:2]
            class_ids.append(obj['group__classes'])
            class_names.append(klass)
        new_name = merge_names(class_names)+' '+common
        try:
            new = Group.objects.get(name=new_name[:15])
        except:
            new = Group(name = new_name[:15])
            new.save()
            new.classes.set(class_ids)
        similar.exclude(pk=lesson.pk)
        similar.delete()
        lesson.group = new
        lesson.save()

