{
    'name': 'Employee Discount (Webshop Compatible)',
    'version': '18.0.1.0.0',
    'depends': ['sale', 'contacts', 'website_sale'],
    'author': 'Kamil',
    'category': 'Sales',
    'summary': "Remise automatique pour les clients 'Employé' : gratuit si moins de 2 commandes dans le mois (compatible webshop)",
    'description': """
        Ce module applique automatiquement une remise totale (commande gratuite) aux clients
        ayant le tag configuré (par défaut "Employé"), à condition qu'ils aient passé
        moins de 2 commandes dans le mois en cours.

        Fonctionnalités :
        - Compatible commandes backend ET webshop (website_sale)
        - Tag employé configurable dans les paramètres système
        - Création automatique du produit de remise s'il n'existe pas
        - Traçabilité : champ indiquant si la remise a été appliquée et pourquoi
        - Bandeau informatif sur la fiche commande
    """,
    'data': [
        'security/ir.model.access.csv',
        'data/discount_product_data.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
