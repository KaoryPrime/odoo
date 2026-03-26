from odoo import api, fields, models


class RestaurantWasteLine(models.Model):

    _name = 'restaurant.waste.line'
    _description = 'Ligne de gaspillage restaurant'
    _inherit = ['mail.thread']
    _order = 'waste_date desc, id desc'

    name = fields.Char(
        string='Référence',
        compute='_compute_name',
        store=True,
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Produit',
        required=True,
        index=True,
    )
    category_id = fields.Many2one(
        comodel_name='product.category',
        related='product_id.categ_id',
        store=True,
        string='Catégorie',
    )
    waste_date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.context_today,
    )
    quantity = fields.Float(
        string='Quantité perdue',
        required=True,
    )
    uom_id = fields.Many2one(
        comodel_name='uom.uom',
        string='Unité',
        related='product_id.uom_id',
    )
    estimated_cost = fields.Float(
        string='Coût estimé (€)',
        compute='_compute_estimated_cost',
        store=True,
        digits=(10, 2),
    )
    reason = fields.Selection(
        selection=[
            ('expired', 'Périmé'),
            ('damaged', 'Endommagé'),
            ('overproduction', 'Surproduction'),
            ('preparation', 'Préparation'),
            ('other', 'Autre'),
        ],
        string='Motif',
        required=True,
    )
    responsible_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Responsable',
    )
    note = fields.Text(
        string='Observation',
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Brouillon'),
            ('validated', 'Validé'),
        ],
        string='Statut',
        default='draft',
        required=True,
        tracking=True,
    )
    color = fields.Integer(
        string='Couleur',
        compute='_compute_color',
        store=True,
    )

    @api.depends('product_id', 'waste_date')
    def _compute_name(self):
        for line in self:
            product_name = line.product_id.name if line.product_id else '?'
            date_str = str(line.waste_date) if line.waste_date else '?'
            line.name = f"{product_name} – {date_str}"

    @api.depends('quantity', 'product_id.standard_price')
    def _compute_estimated_cost(self):
        for line in self:
            line.estimated_cost = line.quantity * (line.product_id.standard_price or 0.0)

    @api.depends('reason')
    def _compute_color(self):
        color_map = {
            'expired': 1,
            'damaged': 2,
            'overproduction': 4,
            'preparation': 7,
            'other': 0,
        }
        for line in self:
            line.color = color_map.get(line.reason, 0)

    def action_validate(self):
        for line in self:
            if line.state == 'draft':
                line.state = 'validated'

    def action_reset_draft(self):
        for line in self:
            if line.state == 'validated':
                line.state = 'draft'
