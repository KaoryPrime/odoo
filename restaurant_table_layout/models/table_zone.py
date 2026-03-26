from odoo import api, fields, models


class RestaurantZone(models.Model):
    _name = 'restaurant.zone'
    _description = 'Zone de restaurant'
    _order = 'sequence, name'

    name = fields.Char(
        string='Nom de la zone',
        required=True,
    )
    zone_type = fields.Selection(
        selection=[
            ('indoor', 'Intérieur'),
            ('outdoor', 'Terrasse'),
            ('bar', 'Bar'),
            ('vip', 'VIP'),
            ('private', 'Privé'),
        ],
        string='Type',
        required=True,
    )
    capacity = fields.Integer(
        string='Capacité totale',
        compute='_compute_capacity',
        store=True,
    )
    table_ids = fields.One2many(
        comodel_name='restaurant.table.layout',
        inverse_name='zone_id',
        string='Tables',
    )
    table_count = fields.Integer(
        string='Nombre de tables',
        compute='_compute_table_stats',
    )
    available_count = fields.Integer(
        string='Tables disponibles',
        compute='_compute_table_stats',
    )
    active = fields.Boolean(
        default=True,
    )
    sequence = fields.Integer(
        default=10,
    )
    color = fields.Integer(
        string='Couleur',
        compute='_compute_color',
    )

    @api.depends('table_ids.capacity')
    def _compute_capacity(self):
        for zone in self:
            zone.capacity = sum(zone.table_ids.mapped('capacity'))

    @api.depends('table_ids.state')
    def _compute_table_stats(self):
        for zone in self:
            tables = zone.table_ids
            zone.table_count = len(tables)
            zone.available_count = len(tables.filtered(lambda t: t.state == 'free'))

    @api.depends('table_ids.state')
    def _compute_color(self):
        for zone in self:
            if not zone.table_count:
                zone.color = 0
            else:
                ratio = zone.available_count / zone.table_count
                if ratio >= 0.5:
                    zone.color = 10
                elif ratio > 0:
                    zone.color = 4
                else:
                    zone.color = 1
