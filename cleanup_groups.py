from timetable.models import *

# Clean up
for group in Group.objects.all():
    lessons = Lesson.objects.filter(group=group)
    if (lessons.count() == 0):
        group.delete()
