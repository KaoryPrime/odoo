from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    loyalty_card_id = fields.Many2one(
        'restaurant.loyalty.card',
        string='Carte fidélité',
    )
    loyalty_points = fields.Float(
        related='loyalty_card_id.points_balance',
        string='Points fidélité',
    )
    loyalty_tier = fields.Selection(
        related='loyalty_card_id.tier',
        string='Niveau fidélité',
    )
