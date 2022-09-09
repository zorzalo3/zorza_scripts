from timetable.models import *

# Clean up
for teacher in Teacher.objects.all():
    lesson = Lesson.objects.filter(teacher=teacher)
    if (lesson.count() == 0):
        teacher.delete()