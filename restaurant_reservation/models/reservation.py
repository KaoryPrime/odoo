from odoo import api, fields, models


class RestaurantTable(models.Model):

    _name = 'restaurant.table'
    _description = 'Table de Restaurant'
    _order = 'name'

    name = fields.Char(
        string='Nom',
        required=True,
    )
    capacity = fields.Integer(
        string='Capacité',
        default=4,
    )
    zone = fields.Selection(
        selection=[
            ('salle', 'Salle'),
            ('terrasse', 'Terrasse'),
            ('bar', 'Bar'),
            ('privee', 'Privée'),
        ],
        string='Zone',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )


class RestaurantReservation(models.Model):

    _name = 'restaurant.reservation'
    _description = 'Réservation Restaurant'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'reservation_date desc, reservation_time'

    name = fields.Char(
        string='Référence',
        compute='_compute_name',
        store=True,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Client',
        required=True,
        index=True,
    )
    reservation_date = fields.Date(
        string='Date',
        required=True,
    )
    reservation_time = fields.Selection(
        selection=[
            ('11:00', '11:00'),
            ('11:30', '11:30'),
            ('12:00', '12:00'),
            ('12:30', '12:30'),
            ('13:00', '13:00'),
            ('13:30', '13:30'),
            ('14:00', '14:00'),
            ('14:30', '14:30'),
            ('15:00', '15:00'),
            ('15:30', '15:30'),
            ('16:00', '16:00'),
            ('16:30', '16:30'),
            ('17:00', '17:00'),
            ('17:30', '17:30'),
            ('18:00', '18:00'),
            ('18:30', '18:30'),
            ('19:00', '19:00'),
            ('19:30', '19:30'),
            ('20:00', '20:00'),
            ('20:30', '20:30'),
            ('21:00', '21:00'),
            ('21:30', '21:30'),
            ('22:00', '22:00'),
        ],
        string='Heure',
    )
    nb_guests = fields.Integer(
        string='Nombre de couverts',
        required=True,
        default=2,
    )
    table_id = fields.Many2one(
        comodel_name='restaurant.table',
        string='Table',
    )
    note = fields.Text(
        string='Notes',
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Brouillon'),
            ('confirmed', 'Confirmé'),
            ('seated', 'Installé'),
            ('done', 'Terminé'),
            ('cancelled', 'Annulé'),
        ],
        string='Statut',
        default='draft',
        required=True,
        tracking=True,
    )
    phone = fields.Char(
        string='Téléphone',
        related='partner_id.phone',
        store=True,
    )
    email = fields.Char(
        string='Email',
        related='partner_id.email',
        store=True,
    )
    duration = fields.Float(
        string='Durée estimée (h)',
        default=1.5,
    )
    color = fields.Integer(
        string='Couleur',
        compute='_compute_color',
        store=True,
    )

    @api.depends('partner_id', 'reservation_date')
    def _compute_name(self):
        for rec in self:
            partner_name = rec.partner_id.name if rec.partner_id else '?'
            date_str = str(rec.reservation_date) if rec.reservation_date else '?'
            rec.name = f"{partner_name} – {date_str}"

    @api.depends('state')
    def _compute_color(self):
        color_map = {
            'draft': 0,
            'confirmed': 4,
            'seated': 7,
            'done': 10,
            'cancelled': 1,
        }
        for rec in self:
            rec.color = color_map.get(rec.state, 0)

    def action_confirm(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'confirmed'

    def action_seat(self):
        for rec in self:
            if rec.state == 'confirmed':
                rec.state = 'seated'

    def action_done(self):
        for rec in self:
            if rec.state == 'seated':
                rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            if rec.state in ('draft', 'confirmed', 'seated'):
                rec.state = 'cancelled'

    def action_reset_draft(self):
        for rec in self:
            if rec.state == 'cancelled':
                rec.state = 'draft'
