{
    'name': 'HR Shift Custom',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Gestion des shifts avec règles RH configurables',
    'description': """
        Ce module permet de gérer les shifts des employés avec des règles RH :
        - Pause minimale configurable entre deux shifts
        - Durée maximale de travail par jour configurable
        - Durée minimale et maximale par shift configurable
        - Vue calendrier des shifts
        - Tableau de bord avec statistiques
        - Suivi complet via chatter
    """,
    'author': 'Kamil',
    'depends': ['hr', 'mail'],
    'data': [
        'security/hr_shift_groups.xml',
        'security/ir.model.access.csv',
        'data/hr_shift_config_data.xml',
        'views/hr_shift_config_views.xml',
        'views/hr_shift_view.xml',
        'views/hr_shift_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}