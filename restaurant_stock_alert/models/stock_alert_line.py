from odoo import api, fields, models


class RestaurantStockAlertLine(models.Model):
    _name = 'restaurant.stock.alert.line'
    _description = 'Ligne d\'alerte de stock'
    _order = 'alert_date desc'

    ALERT_STATE_SELECTION = [
        ('new', 'Nouveau'),
        ('acknowledged', 'Acquitté'),
        ('ordered', 'Commandé'),
        ('resolved', 'Résolu'),
    ]

    name = fields.Char(
        string='Nom',
        compute='_compute_name',
        store=True,
    )
    rule_id = fields.Many2one(
        comodel_name='restaurant.stock.alert.rule',
        string='Règle',
        required=True,
        ondelete='cascade',
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        related='rule_id.product_id',
        store=True,
        string='Produit',
    )
    alert_date = fields.Datetime(
        string='Date alerte',
        default=fields.Datetime.now,
    )
    current_quantity = fields.Float(
        string="Stock au moment de l'alerte",
    )
    min_quantity = fields.Float(
        related='rule_id.min_quantity',
        string='Seuil minimum',
    )
    suggested_order = fields.Float(
        string='Quantité suggérée',
    )
    state = fields.Selection(
        selection=ALERT_STATE_SELECTION,
        string='Statut',
        default='new',
        required=True,
    )
    color = fields.Integer(
        string='Couleur',
        compute='_compute_color',
    )

    @api.depends('rule_id', 'alert_date')
    def _compute_name(self):
        for line in self:
            product_name = line.rule_id.product_id.name if line.rule_id and line.rule_id.product_id else '?'
            date_str = fields.Datetime.to_string(line.alert_date) if line.alert_date else ''
            line.name = f"Alerte {product_name} – {date_str}"

    @api.depends('state')
    def _compute_color(self):
        color_map = {
            'new': 1,
            'acknowledged': 4,
            'ordered': 2,
            'resolved': 10,
        }
        for line in self:
            line.color = color_map.get(line.state, 0)

    def action_acknowledge(self):
        for line in self:
            if line.state == 'new':
                line.state = 'acknowledged'

    def action_mark_ordered(self):
        for line in self:
            if line.state in ('new', 'acknowledged'):
                line.state = 'ordered'

    def action_resolve(self):
        for line in self:
            if line.state != 'resolved':
                line.state = 'resolved'
