#!/usr/bin/env python3
import os, django, sys, itertools, operator
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zorza.settings')
django.setup()

from timetable.models import *

# Clean up
for group in Group.objects.all():
    lessons = Lesson.objects.filter(group=group)
    if (lessons.count() == 0):
        group.delete()
