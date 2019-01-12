import sys, datetime

if len(sys.argv) != 2:
    sys.exit("Usage: ./run [file.xml]")

filename = sys.argv[1]

import xml.etree.ElementTree as ET
tree = ET.parse(filename)

sys.path.append('..')

from timetable.models import *

root = tree.getroot()

# W xmlu nie ma rozroznienia na rozne rozklady czasu
schedule, _ = Schedule.objects.get_or_create(
    is_default=True,
    defaults={'name': 'Normalne lekcje'}
)

def Id(obj, name='id'):
    # Jakaś dziwna gwiazdka jest w tym xmlu
    return obj.attrib[name].replace('*', '')

schedule.period_set.all().delete()
for p in root.find('periods'):
    a = p.attrib
    obj = Period(number=int(a['period']), begin_time=a['starttime'], \
            end_time=a['endtime'], schedule=schedule)
    obj.clean()
    obj.full_clean()
    obj.save()


Teacher.objects.all().delete()
for t in root.find('teachers'):
    a = t.attrib
    name=a['name'].split(maxsplit=1)
    initials = a['short']
    if len(initials) > 2:
        initials = '??'
    obj = Teacher(pk=Id(t), first_name=name[0],
                  last_name=name[1], initials=initials)
    obj.clean()
    obj.full_clean()
    obj.save()


Subject.objects.all().delete()
for s in root.find('subjects'):
    a = s.attrib
    obj = Subject(pk=Id(s), name=a['name'], short_name=a['short'])
    name_max_len = Subject._meta.get_field('name').max_length
    obj.name = obj.name[:name_max_len]
    short_name_max_len = Subject._meta.get_field('short_name').max_length
    obj.short_name = obj.short_name[:short_name_max_len]
    obj.full_clean()
    obj.save()


Room.objects.all().delete()
for r in root.find('classrooms'):
    a = r.attrib
    obj = Room(pk=Id(r), name=a['name'], short_name=a['short'])
    name_max_len = Room._meta.get_field('name').max_length
    obj.name = obj.name[:name_max_len]
    short_name_max_len = Room._meta.get_field('short_name').max_length
    obj.short_name = obj.short_name[:short_name_max_len]
    obj.full_clean()
    obj.save()


class_names = dict()
Class.objects.all().delete()
for c in root.find('classes'):
    a = c.attrib
    obj = Class(pk=Id(c), name=a['name'])
    class_names[int(Id(c))] = a['name']
    obj.full_clean()
    obj.save()


# W xmlu niektóre nazwy grup nic nie mówią
unspecific = [
    'Chłopcy', 'Dziewczęta', '1. Grupa', '2. Grupa',
    'Cała klasa', 'bez religii'
]

# model for the many to many relationship
GroupClass = Group.classes.through
groupclass_objs = []
groups = []
Group.objects.all().delete()
for g in root.find('groups'):
    a = g.attrib
    obj = Group(Id(g))
    obj.name = a['name']
    if obj.name in unspecific:
        obj.name = class_names[int(Id(g, 'classid'))] + ' ' + obj.name
    if 'Cała klasa' in obj.name:
        obj.link_to_class = True
    groups.append(obj)
    gid = int(Id(g))
    classid = int(Id(g, 'classid'))
    groupclass_objs.append(GroupClass(group_id=gid, class_id=classid))

Group.objects.bulk_create(groups)
GroupClass.objects.bulk_create(groupclass_objs)


# w tym xmlu lekcja ma wiele grup, a grupa nie ma wielu klas
# lekcja u nich to w ogole jakies inne pojecie
# cos pomiedzy Subject a Lesson?

lessons = [dict() for i in range(len(root.find('lessons'))+1)]
for l in root.find('lessons'):
    idx = Id(l)
    idx = int(idx)
    lessons[idx]['subject'] = int(Id(l, 'subjectid'))
    # chyba zawsze jest tylko jeden teacherid (nie ma po przecinku)
    lessons[idx]['teacher'] = int(Id(l, 'teacherids'))
    lessons[idx]['groupids'] = Id(l, 'groupids').split(',')


# obiekty Lesson do zapisania w bazie
tmp = []

for c in root.find('cards'):
    # chyba zawsze jest tylko jeden id
    needle = int(Id(c, 'lessonid'))

    subject = lessons[needle]['subject']
    teacher = lessons[needle]['teacher']
    groupids = lessons[needle]['groupids']
    for groupid in groupids:
        obj = Lesson(group_id=int(groupid), period=int(Id(c, 'period')),
                     room_id=int(Id(c, 'classroomids')))
        obj.subject_id = subject
        obj.teacher_id = teacher
        obj.weekday = Id(c, 'day')
        tmp.append(obj)

Lesson.objects.bulk_create(tmp)

