from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class RestaurantHappyHour(models.Model):

    _name = 'restaurant.happy.hour'
    _description = 'Happy Hour'
    _order = 'day_of_week, time_start'

    name = fields.Char(
        string='Nom de la promotion',
        required=True,
    )
    day_of_week = fields.Selection(
        selection=[
            ('0', 'Lundi'),
            ('1', 'Mardi'),
            ('2', 'Mercredi'),
            ('3', 'Jeudi'),
            ('4', 'Vendredi'),
            ('5', 'Samedi'),
            ('6', 'Dimanche'),
        ],
        string='Jour de la semaine',
        required=True,
    )
    time_start = fields.Float(
        string='Heure de début',
        required=True,
        help="Heure de début au format heures:minutes",
    )
    time_end = fields.Float(
        string='Heure de fin',
        required=True,
        help="Heure de fin au format heures:minutes",
    )
    discount_type = fields.Selection(
        selection=[
            ('percentage', 'Pourcentage'),
            ('fixed', 'Montant fixe'),
        ],
        string='Type de remise',
        required=True,
        default='percentage',
    )
    discount_value = fields.Float(
        string='Valeur de remise',
        required=True,
    )
    line_ids = fields.One2many(
        comodel_name='restaurant.happy.hour.line',
        inverse_name='happy_hour_id',
        string='Produits concernés',
    )
    active = fields.Boolean(
        default=True,
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Brouillon'),
            ('active', 'Actif'),
            ('expired', 'Expiré'),
        ],
        string='Statut',
        default='draft',
        required=True,
    )
    date_start = fields.Date(
        string='Valide à partir du',
    )
    date_end = fields.Date(
        string='Valide jusqu au',
    )
    description = fields.Text(
        string='Description',
    )
    product_count = fields.Integer(
        string='Produits',
        compute='_compute_product_count',
    )
    color = fields.Integer(
        string='Couleur',
        compute='_compute_color',
    )

    @api.depends('line_ids')
    def _compute_product_count(self):
        for record in self:
            record.product_count = len(record.line_ids)

    @api.depends('state')
    def _compute_color(self):
        color_map = {
            'draft': 0,
            'active': 10,
            'expired': 1,
        }
        for record in self:
            record.color = color_map.get(record.state, 0)

    @api.constrains('time_start', 'time_end')
    def _check_time_range(self):
        for record in self:
            if record.time_start >= record.time_end:
                raise ValidationError(
                    _("L'heure de début doit être inférieure à l'heure de fin.")
                )

    @api.constrains('date_start', 'date_end')
    def _check_date_range(self):
        for record in self:
            if record.date_start and record.date_end and record.date_start > record.date_end:
                raise ValidationError(
                    _("La date de début doit être antérieure ou égale à la date de fin.")
                )

    def action_activate(self):
        for record in self:
            if record.state == 'draft':
                record.state = 'active'

    def action_expire(self):
        for record in self:
            if record.state == 'active':
                record.state = 'expired'

    def action_reset_draft(self):
        for record in self:
            if record.state in ('active', 'expired'):
                record.state = 'draft'

    def is_currently_active(self):
        self.ensure_one()
        if self.state != 'active':
            return False
        now = fields.Datetime.now()
        today = now.date()
        if self.date_start and today < self.date_start:
            return False
        if self.date_end and today > self.date_end:
            return False
        current_day = str(today.weekday())
        if self.day_of_week != current_day:
            return False
        current_time = now.hour + now.minute / 60.0
        if current_time < self.time_start or current_time > self.time_end:
            return False
        return True

    def get_discount_for_product(self, product_id):
        self.ensure_one()
        if not self.is_currently_active():
            return 0.0
        line = self.line_ids.filtered(lambda l: l.product_id.id == product_id)
        if not line:
            return 0.0
        return self.discount_value
