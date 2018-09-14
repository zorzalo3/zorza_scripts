#!/usr/bin/env python3
import os, django, sys
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zorza.settings')
django.setup()
# użyć po imporcie z xml

replaces = {
    'cl_hour' : 'Class hour',
    'spa' : 'Spanish',
    'ger' : 'German',
    'eng' : 'English',
    'eng_ea' : 'English extra',
    'pol_ed' : 'English extended',
    'rel' : 'Religion',
    'it' : 'IT',
    'it_ed' : 'IT extended',
    'PE' : 'Physical Education',
    'eco' : 'Economics',
    'art' : 'Art',
    'music' : 'Music',
    'bio' : 'Biology',
    'bio_ea' : 'Biology extra',
    'bio_ed' : 'Biology ',
    'che' : 'Chemistry',
    'che_ed' : 'Chemistry extended',
    'phi' : 'Physics',
    'phy_ed' : 'Physics extended',
    'phy_ea' : 'Physics extra',
    'geo' : 'Geography',
    'geo_ed' : 'Geography extended',
    'his' : 'History',
    'his_r' : 'History extended',
    'soc' : 'Politics',
    'mat' : 'Maths',
    'mat_b' : 'Maths basic',
    'mat_ea' : 'Maths extra',
    'mat_ed' : 'Maths extended',
    'kas' : 'Knowledge about society',
    'kas_r' : 'Knowledge about society extended',
    'se' : 'Safety education',
    'CaD' : 'Color and design',
    'kae' : 'Knowledge about enviroment',
    'hoc' : 'History of culture',
    'EEL' : 'Extra Extended lessons'
}

from timetable.models import *

for subject in Subject.objects.all():
    try:
        subject.short_name = replaces[subject.short_name]
        subject.save()
    except KeyError:
        print("No entry {} in the dictionary".format(subject.short_name))
