from odoo import api, fields, models


class RestaurantDailyMenu(models.Model):
    _name = 'restaurant.daily.menu'
    _description = 'Menu du Jour'
    _inherit = ['mail.thread']
    _order = 'date desc'

    MENU_TYPE_SELECTION = [
        ('midi', 'Midi'),
        ('soir', 'Soir'),
        ('brunch', 'Brunch'),
        ('special', 'Spécial'),
    ]

    name = fields.Char(
        string='Nom',
        compute='_compute_name',
        store=True,
    )
    date = fields.Date(
        string='Date du menu',
        required=True,
    )
    menu_type = fields.Selection(
        selection=MENU_TYPE_SELECTION,
        string='Service',
        required=True,
        default='midi',
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Brouillon'),
            ('active', 'Actif'),
            ('archived', 'Archivé'),
        ],
        string='Statut',
        default='draft',
        required=True,
        tracking=True,
    )
    line_ids = fields.One2many(
        comodel_name='restaurant.daily.menu.line',
        inverse_name='menu_id',
        string='Plats',
    )
    total_price = fields.Float(
        string='Prix total menu',
        compute='_compute_total_price',
        store=True,
    )
    menu_price = fields.Float(
        string='Prix menu fixe (€)',
    )
    note = fields.Text(
        string='Notes',
    )
    responsible_id = fields.Many2one(
        comodel_name='res.users',
        string='Responsable',
        default=lambda self: self.env.user,
    )
    color = fields.Integer(
        string='Couleur',
        compute='_compute_color',
    )
    line_count = fields.Integer(
        string='Nombre de plats',
        compute='_compute_line_count',
    )

    @api.depends('date', 'menu_type')
    def _compute_name(self):
        type_labels = dict(self.MENU_TYPE_SELECTION)
        for menu in self:
            label = type_labels.get(menu.menu_type, '')
            date_str = menu.date or ''
            menu.name = f"Menu {label} – {date_str}"

    @api.depends('line_ids.price')
    def _compute_total_price(self):
        for menu in self:
            menu.total_price = sum(menu.line_ids.mapped('price'))

    @api.depends('state')
    def _compute_color(self):
        color_map = {
            'draft': 0,
            'active': 10,
            'archived': 1,
        }
        for menu in self:
            menu.color = color_map.get(menu.state, 0)

    @api.depends('line_ids')
    def _compute_line_count(self):
        for menu in self:
            menu.line_count = len(menu.line_ids)

    def action_activate(self):
        for menu in self:
            if menu.state == 'draft':
                menu.state = 'active'

    def action_archive_menu(self):
        for menu in self:
            if menu.state == 'active':
                menu.state = 'archived'

    def action_reset_draft(self):
        for menu in self:
            if menu.state in ('active', 'archived'):
                menu.state = 'draft'
