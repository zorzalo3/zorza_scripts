import itertools, operator

from timetable.models import *

"""Łączy grupy o tej samej nazwie w jedną"""

# https://stackoverflow.com/questions/4724515/django-how-can-i-select-objects-with-the-same-field-values
def group_objects_by_attr(queryset, attr_name):
    all_instances = queryset.order_by(attr_name)
    keyfunc = operator.attrgetter(attr_name)
    return {k: list(g) for k, g in itertools.groupby(all_instances, keyfunc)}

all_groups = Group.objects.all()
grouped_by_name = group_objects_by_attr(all_groups, 'name')


for name, groups in grouped_by_name.items():
    first = groups[0]
    for group in groups[1:]:
        first.classes.add(*group.classes.all())
        Lesson.objects.filter(group=group).delete()
        group.delete()
