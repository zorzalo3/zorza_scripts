replaces = {
    'GDDW': 'GDDW',
    'ang': 'Angielski',
    'niem': 'Niemiecki',
    'pol': 'Polski',
    'pol_d': 'Polski D',
    'pol_r': 'Polski R',
    'rel': 'Religia',
    'inf': 'Informatyka',
    'inf_r': 'Informatyka R',
    'WF': 'WF',
    'przeds': 'Przeds.',
    'war_plas': 'W. Plastyczne',
    'war_teatr': 'W. Teatralne',
    'bio': 'Biologia',
    'bio_d': 'Biologia D',
    'bio_r': 'Biologia R',
    'che': 'Chemia',
    'che_r': 'Chemia R',
    'fiz': 'Fizyka',
    'fiz_r': 'Fizyka R',
    'fiz_d': 'Fizyka D',
    'geo': 'Geografia',
    'geo_r': 'Geografia R',
    'his': 'Historia',
    'his_r': 'Historia R',
    'HiS': 'Hist. i społ.',
    'mat': 'Matematyka',
    'mat': 'Matematyka',
    'mat_d': 'Matematyka D',
    'mat_r': 'Matematyka R',
    'wos': 'WOS',
    'wos_r': 'WOS R',
    'edu_b': 'EDB',
    'HS/HD': 'HS/HD',
    'prz': 'Przyroda',
    'WOK': 'WOK',
    'BO': 'BO',
    'E': 'Etyka',
    'BOF': 'BO Finaliści',
    'mat_zdw': 'Matematyka',
    'fiz_zdw': 'Fizyka',
    'pol_zdw': 'Polski',
    'mat_z': 'Matematyka',
    'fiz_z': 'Fizyka',
    'pol_z': 'Polski',
}

from timetable.models import *

for subject in Subject.objects.all():
    try:
        subject.short_name = replaces[subject.short_name]
        subject.save()
    except KeyError:
        print("No entry {} in the dictionary".format(subject.short_name))
