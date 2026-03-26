{
    'name': 'Employee Calendar Planning',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'author': 'Kamil',
    'license': 'AGPL-3',
    'installable': True,
    'depends': ['hr', 'calendar', 'hr_work_entry'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
        'views/resource_calendar_views.xml',
    ],
    'post_init_hook': 'post_init_hook',
}
