{
    'name': 'Allergènes Automatiques',
    'version': '18.0.1.0.0',
    'depends': ['product', 'mrp', 'website_sale'],
    'author': 'Kamil',
    'category': 'Product',
    'summary': 'Calcul automatique des allergènes pour les recettes selon la BoM',
    'description': """
        Ce module permet de :
        - Définir des allergènes réglementaires sur les matières premières
        - Calculer automatiquement les allergènes des produits finis via leur nomenclature (BoM)
        - Afficher les allergènes sur la fiche produit du site e-commerce
    """,
    'data': [
        'security/ir.model.access.csv',
        'data/allergen_data.xml',
        'views/allergen_views.xml',
        'views/product_template_views.xml',
        'views/product_allergen_website.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
