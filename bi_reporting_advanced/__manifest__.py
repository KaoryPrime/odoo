{
    'name': 'BI Reporting Advanced',
    'version': '18.0.1.0.0',
    'category': 'Reporting',
    'summary': 'Rapports avancés et automatisation (ventes, facturation, stocks)',
    'depends': ['base', 'sale', 'account', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_report_views.xml',
        'views/invoice_report_views.xml',
        'views/stock_report_views.xml',
        'views/menu_items.xml',
        'data/cron_jobs.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}