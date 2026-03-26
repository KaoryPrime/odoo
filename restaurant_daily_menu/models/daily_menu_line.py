from odoo import fields, models


class RestaurantDailyMenuLine(models.Model):
    _name = 'restaurant.daily.menu.line'
    _description = 'Ligne de Menu du Jour'
    _order = 'sequence, id'

    menu_id = fields.Many2one(
        comodel_name='restaurant.daily.menu',
        string='Menu',
        required=True,
        ondelete='cascade',
    )
    sequence = fields.Integer(
        string='Séquence',
        default=10,
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Plat',
        required=True,
    )
    category = fields.Selection(
        selection=[
            ('entree', 'Entrée'),
            ('plat', 'Plat'),
            ('dessert', 'Dessert'),
            ('boisson', 'Boisson'),
        ],
        string='Catégorie',
        required=True,
    )
    price = fields.Float(
        string='Prix unitaire',
    )
    is_available = fields.Boolean(
        string='Disponible',
        default=True,
    )
    description = fields.Char(
        string='Description courte',
    )
