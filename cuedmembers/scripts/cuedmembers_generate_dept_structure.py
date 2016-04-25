"""
Create research groups and divisions for fixture.

Run via:

    manage.py runscript cuedmembers_generate_dept_structure

"""

from cuedmembers.models import ResearchGroup, Division

DIVISIONS = {
    'A': 'Energy, Fluids and Turbomachinery',
    'B': 'Electrical Engineering',
    'C': 'Mechanics, Materials and Design',
    'D': 'Civil Engineering',
    'E': 'Manufacturing and Management',
    'F': 'Information Engineering',
}

RESEARCH_GROUPS = {
    'A': ['Energy Group', 'Fluids Group', 'Turbomachinery Group'],
    'B': ['Electronics, Power and Energy Conversion Group',
          'Photonics Group',
          'Solid State Electronics and Nanoscale Science Group'],
    'C': ['Applied Mechanics', 'Biomechanics', 'Engineering Design',
          'Materials Engineering'],
    'D': ['Construction Engineering Group',
          'Geotechnical and Environmental Group',
          'Structures Group', 'Sustainable Development Group'],
    'E': ['Manufacturing Systems', 'Production Processes',
          'Strategy and Policy'],
    'F': ['Computational and Biological Learning Laboratory',
          'Control Group', 'Machine Intelligence Laboratory',
          'Signal Processing and Communications Laboratory'],
}

def run():
    for l, n in DIVISIONS.items():
        Division.objects.get_or_create(letter=l, name=n)

    for d, groups in RESEARCH_GROUPS.items():
        division = Division.objects.get(letter=d)
        for g in groups:
            ResearchGroup.objects.get_or_create(division=division, name=g)

