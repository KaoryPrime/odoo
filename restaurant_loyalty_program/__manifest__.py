{
    'name': 'Restaurant Loyalty Program',
    'version': '18.0.1.0.0',
    'author': 'Kamil',
    'category': 'Restaurant',
    'summary': 'Programme de fidélité client pour restaurant',
    'description': """
        Gestion d'un programme de fidélité avec points et niveaux.
        Compatible Odoo 18 — syntaxe XML stricte (invisible=, readonly=, required=).
    """,
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/loyalty_data.xml',
        'views/loyalty_views.xml',
        'views/loyalty_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
