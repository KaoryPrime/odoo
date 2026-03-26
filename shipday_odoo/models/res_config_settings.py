from odoo import _, api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    shipday_api_key = fields.Char(
        string='Clé API Shipday',
        config_parameter='shipday_odoo.api_key',
        help="Clé API Shipday (disponible dans votre tableau de bord Shipday → Settings → API).",
    )

    shipday_restaurant_name = fields.Char(
        string='Nom du restaurant',
        config_parameter='shipday_odoo.restaurant_name',
        default='Mon Restaurant',
    )
    shipday_restaurant_address = fields.Char(
        string='Adresse du restaurant',
        config_parameter='shipday_odoo.restaurant_address',
    )
    shipday_restaurant_phone = fields.Char(
        string='Téléphone du restaurant',
        config_parameter='shipday_odoo.restaurant_phone',
    )

    shipday_default_delivery_delay = fields.Integer(
        string='Délai de livraison par défaut (minutes)',
        config_parameter='shipday_odoo.delivery_delay',
        default=30,
        help="Nombre de minutes après l'heure de pickup pour estimer la livraison.",
    )
