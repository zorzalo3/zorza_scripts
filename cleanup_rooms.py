# TODO
from timetable.models import *

# Clean up
for room in Room.objects.all():
    lesson = Lesson.objects.filter(room=room)
    if (lesson.count() == 0):
        room.delete()