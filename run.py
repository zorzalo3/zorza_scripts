#!/usr/bin/env python3
import os, django, sys
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zorza.settings')
django.setup()

with django.db.transaction.atomic():

    # Importuje plan lekcji z .xml
    import import_xml

    # Łączy grupy z planu o tej samej nazwie w jedną (np. językowe)
    import merge_groups

    # Oddziela np. BO od całych klas
    import split_groups

    # Łączy grupy mające lekcję z tym samym nauczycielem w tym samym czasie
    import create_groups

    # Usuwa pozostałości po porzednich skryptach
    import cleanup_groups

    # Usuwa nauczycieli, którzy nie mają żadnych lekcji
    import cleanup_teachers

    # Usuwa sale, w których nie ma lekcji
    import cleanup_rooms

    # Zmienia wyświetlane nazwy na bardziej stosowne do wyświetlania
    import rename_subjects

    # Dodaje skrócone lekcje jeśli ich jeszcze nie ma
    import add_shortened_periods
