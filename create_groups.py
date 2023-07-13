from timetable.models import *

"""Tworzy nową grupę jeśli nauczyciel ma lekcje z kilkoma klasami.
Tak jest w przypadku np. BO"""

def merge_names(names):
    """Łączy nazwy klas tak:
        ['1A', '2A', '3A'] => '123A'
        ['2A', '2B'] => '2AB'
	['1Bg','1Dg'] => '1BgDg'
	#TODO handle ambigous groups like:
		['1A','2A','2B'] should give '1A2AB' not '12AB'
    """
    firsts = sorted({name[0] for name in names})
    seconds = sorted({name[1:] for name in names})
    return "".join(firsts+seconds)

name_cutoff = Group._meta.get_field('name').max_length

for lesson in Lesson.objects.all():
    similar = Lesson.objects.filter(teacher=lesson.teacher, room=lesson.room,
        period=lesson.period, weekday=lesson.weekday)
    if similar.count() > 1:
        values = similar.values('id', 'group__name', 'group__classes')
        common = values[0]['group__name'].replace('/',' ').split(' ', 1)[1]
        class_names = []
        class_ids = []
        for obj in values:
            klass = obj['group__name'].split(' ')[0]
            class_ids.append(obj['group__classes'])
            class_names.append(klass)
        new_name = merge_names(class_names)+' '+common
        new, created = Group.objects.get_or_create(name=new_name[:name_cutoff])
        if created:
            new.classes.set(class_ids)
        similar.delete()
        lesson.group = new
        lesson.save()

Group.objects.create(name="Konsultacje", link_to_class=False)
