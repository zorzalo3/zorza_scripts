#!/usr/bin/env python3
import os, django, sys, datetime

if len(sys.argv) != 2:
    sys.exit("Usage: ./import [file.xml]")

filename = sys.argv[1]

import xml.etree.ElementTree as ET
tree = ET.parse(filename)

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zorza.settings')
django.setup()

from timetable.models import *

root = tree.getroot()

sincet = datetime.datetime.now()

def since():
    """profiling"""
    global sincet
    diff = datetime.datetime.now() - sincet
    print(diff.seconds * 1000000 + diff.microseconds)
    sincet = datetime.datetime.now()

# na librusie nie ma rozroznienia na rozne rozklady czasu
try:
    schedule = Schedule.objects.get(pk=1)
except:
    schedule = Schedule(name='Normalne lekcje', is_default=True)
    schedule.save()

def Id(obj, name='id'):
    return obj.attrib[name].strip('*') #jakas dziwna gwiazdka jest w tym xmlu

Period.objects.all().delete()
for p in root.find('periods'):
    a = p.attrib
    obj = Period(number=int(a['period']), begin_time=a['starttime'], \
            end_time=a['endtime'], schedule=schedule)
    obj.clean()
    obj.full_clean()
    obj.save()

since()

Teacher.objects.all().delete()
for t in root.find('teachers'):
    a = t.attrib
    name=a['name'].split(maxsplit=1)
    initials = a['short']
    if len(initials) > 2:
        initials = '??'
    obj = Teacher(pk=Id(t), first_name=name[0], last_name=name[1], initials=initials)
    obj.clean()
    obj.full_clean()
    obj.save()

since()

Subject.objects.all().delete()
for s in root.find('subjects'):
    a = s.attrib
    obj = Subject(pk=Id(s), name=a['name'], short_name=a['short'])
    obj.clean()
    try:
        obj.full_clean()
    except:
        obj.name=obj.name[:Subject._meta.get_field('name').max_length]
        obj.short_name=obj.short_name[:Subject._meta.get_field('short_name').max_length]
        obj.full_clean()
    obj.save()

since()

Room.objects.all().delete()
for r in root.find('classrooms'):
    a = r.attrib
    obj = Room(pk=Id(r), name=a['name'], short_name=a['short'])
    obj.clean()
    try:
        obj.full_clean()
    except:
        obj.name=obj.name[:Room._meta.get_field('name').max_length]
        obj.short_name=obj.short_name[:Room._meta.get_field('short_name').max_length]
        obj.full_clean()
    obj.save()

since()

class_names = dict()
Class.objects.all().delete()
for c in root.find('classes'):
    a = c.attrib
    obj = Class(pk=Id(c), name=a['name'])
    class_names[int(Id(c))] = a['name']
    obj.full_clean()
    obj.save()

since()

# W xmlu niektóre nazwy grup nic nie mówią
unspecific = [
    'Chłopcy', 'Dziewczęta', '1. Grupa', '2. Grupa',
    'Cała klasa', 'bez religii'
]

Group.objects.all().delete()
for g in root.find('groups'):
    a = g.attrib
    obj = Group(Id(g))
    obj.name = a['name']
    if obj.name in unspecific:
        obj.name = class_names[int(Id(g, 'classid'))] + ' ' + obj.name
    obj.save()
    # bulk_create nie dziala z ManyToMany więc to najwolniejsza część skryptu
    obj.classes.add(Id(g, 'classid'))

since()

# w tym xmlu lekcja ma wiele grup, a grupa nie ma wielu klas
# lekcja u nich to w ogole jakies inne pojecie
# cos pomiedzy Subject a Lesson?

lessons = [dict() for i in range(len(root.find('lessons'))+1)]
lessons[0]['a'] = 2
for l in root.find('lessons'):
    idx = Id(l)
    idx = int(idx)
    lessons[idx]['subject'] = int(Id(l, 'subjectid'))
    # chyba zawsze jest tylko jeden teacherid (nie ma po przecinku)
    lessons[idx]['teacher'] = int(Id(l, 'teacherids'))
    lessons[idx]['groupids'] = Id(l, 'groupids').replace('*', '').split(',')

since()

# obiekty Lesson do zapisania w bazie
tmp = []

for c in root.find('cards'):
    # chyba zawsze jest tylko jeden id
    needle = int(Id(c, 'lessonid'))

    subject = lessons[needle]['subject']
    teacher = lessons[needle]['teacher']
    groupids = lessons[needle]['groupids']
    for groupid in groupids:
        obj = Lesson(group_id=int(groupid), period=int(Id(c, 'period')), room_id=int(Id(c, 'classroomids')))
        obj.subject_id = subject
        obj.teacher_id = teacher
        obj.weekday = Id(c,'day')
        tmp.append(obj)

Lesson.objects.bulk_create(tmp)

since()
