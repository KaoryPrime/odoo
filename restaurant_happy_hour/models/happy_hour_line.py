from odoo import api, fields, models


class RestaurantHappyHourLine(models.Model):

    _name = 'restaurant.happy.hour.line'
    _description = 'Ligne Happy Hour'

    happy_hour_id = fields.Many2one(
        comodel_name='restaurant.happy.hour',
        string='Happy Hour',
        required=True,
        ondelete='cascade',
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Produit',
        required=True,
    )
    original_price = fields.Float(
        related='product_id.list_price',
        string='Prix original',
    )
    discounted_price = fields.Float(
        string='Prix remisé',
        compute='_compute_discounted_price',
        store=True,
    )

    @api.depends('original_price', 'happy_hour_id.discount_type', 'happy_hour_id.discount_value')
    def _compute_discounted_price(self):
        for line in self:
            if line.happy_hour_id.discount_type == 'percentage':
                line.discounted_price = line.original_price * (1 - line.happy_hour_id.discount_value / 100)
            elif line.happy_hour_id.discount_type == 'fixed':
                line.discounted_price = max(0.0, line.original_price - line.happy_hour_id.discount_value)
            else:
                line.discounted_price = line.original_price
