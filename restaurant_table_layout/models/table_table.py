from odoo import api, fields, models


class RestaurantTableLayout(models.Model):
    _name = 'restaurant.table.layout'
    _description = 'Table de restaurant'
    _inherit = ['mail.thread']
    _order = 'zone_id, name'

    name = fields.Char(
        string='Numéro de table',
        required=True,
        tracking=True,
    )
    zone_id = fields.Many2one(
        comodel_name='restaurant.zone',
        string='Zone',
        required=True,
        ondelete='restrict',
        index=True,
        tracking=True,
    )
    capacity = fields.Integer(
        string='Nombre de places',
        required=True,
        default=4,
    )
    shape = fields.Selection(
        selection=[
            ('round', 'Ronde'),
            ('square', 'Carrée'),
            ('rectangle', 'Rectangulaire'),
        ],
        string='Forme',
        default='square',
    )
    state = fields.Selection(
        selection=[
            ('free', 'Libre'),
            ('occupied', 'Occupée'),
            ('reserved', 'Réservée'),
            ('maintenance', 'Maintenance'),
        ],
        string='Statut',
        default='free',
        required=True,
        tracking=True,
    )
    current_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Commande en cours',
    )
    current_guests = fields.Integer(
        string='Couverts actuels',
    )
    waiter_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Serveur assigné',
        tracking=True,
    )
    note = fields.Text(
        string='Notes',
    )
    color = fields.Integer(
        string='Couleur',
        compute='_compute_color',
        store=True,
    )

    @api.depends('state')
    def _compute_color(self):
        color_map = {
            'free': 10,
            'occupied': 1,
            'reserved': 4,
            'maintenance': 0,
        }
        for table in self:
            table.color = color_map.get(table.state, 0)

    def action_set_free(self):
        for table in self:
            table.state = 'free'

    def action_set_occupied(self):
        for table in self:
            table.state = 'occupied'

    def action_set_reserved(self):
        for table in self:
            table.state = 'reserved'

    def action_set_maintenance(self):
        for table in self:
            table.state = 'maintenance'

    def action_open_order(self):
        self.ensure_one()
        if not self.current_order_id:
            return False
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': self.current_order_id.id,
            'target': 'current',
        }
