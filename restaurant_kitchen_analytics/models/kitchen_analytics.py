from odoo import _, api, fields, models

class KitchenAnalyticsLine(models.Model):
    """
    Ligne analytique cuisine.

    Chaque enregistrement représente un plat issu d'une commande de vente,
    avec le suivi du temps de préparation (commandé → livré) et de l'écart
    entre la quantité commandée et la quantité réellement servie.
    """

    _name = 'kitchen.analytics.line'
    _description = 'Ligne Analytique Cuisine'
    _order = 'order_datetime desc'

    name = fields.Char(
        string='Référence',
        compute='_compute_name',
        store=True,
        help="Identifiant lisible : numéro de commande + nom du plat.",
    )

    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Commande',
        required=True,
        ondelete='cascade',
        index=True,
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Plat',
        required=True,
        index=True,
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        related='sale_order_id.partner_id',
        store=True,
        string='Client',
    )
    order_date = fields.Date(
        related='sale_order_id.date_order',
        store=True,
        string='Date commande',
    )

    order_datetime = fields.Datetime(
        string='Heure de commande',
        required=True,
        default=fields.Datetime.now,
        help="Moment où le plat a été commandé.",
    )
    delivery_datetime = fields.Datetime(
        string='Heure de livraison',
        help="Moment où le plat a été remis au client.",
    )

    preparation_time = fields.Float(
        string='Temps de préparation (min)',
        compute='_compute_preparation_time',
        store=True,
        digits=(10, 2),
        help="Durée exacte entre la commande et la livraison du plat, en minutes.",
    )
    preparation_time_display = fields.Char(
        string='Durée',
        compute='_compute_preparation_time',
        store=True,
        help="Durée formatée (ex. : 25 min, 1h05).",
    )
    qty_ordered = fields.Float(
        string='Qté commandée',
        default=1.0,
    )
    qty_delivered = fields.Float(
        string='Qté livrée',
        default=0.0,
    )
    qty_variance = fields.Float(
        string='Écart de quantité',
        compute='_compute_qty_variance',
        store=True,
        help="Différence entre la quantité livrée et la quantité commandée."
             " Valeur positive = surplus ; valeur négative = manque.",
    )
    color = fields.Integer(
        string='Couleur',
        compute='_compute_color',
        store=True,
    )

    state = fields.Selection(
        selection=[
            ('pending', 'En attente'),
            ('in_progress', 'En préparation'),
            ('done', 'Livré'),
            ('cancelled', 'Annulé'),
        ],
        string='Statut',
        default='pending',
        required=True,
    )

    @api.depends('sale_order_id', 'product_id')
    def _compute_name(self):
        for line in self:
            order_ref = line.sale_order_id.name if line.sale_order_id else '?'
            product_name = line.product_id.name if line.product_id else '?'
            line.name = f"{order_ref} – {product_name}"

    @api.depends('order_datetime', 'delivery_datetime')
    def _compute_preparation_time(self):
        for line in self:
            if (
                line.order_datetime
                and line.delivery_datetime
                and line.delivery_datetime > line.order_datetime
            ):
                delta_seconds = (
                    line.delivery_datetime - line.order_datetime
                ).total_seconds()
                minutes = delta_seconds / 60
                line.preparation_time = minutes
                h = int(minutes // 60)
                m = int(minutes % 60)
                line.preparation_time_display = (
                    f"{h}h{m:02d}" if h else f"{m} min"
                )
            else:
                line.preparation_time = 0.0
                line.preparation_time_display = '—'

    @api.depends('qty_ordered', 'qty_delivered')
    def _compute_qty_variance(self):
        for line in self:
            line.qty_variance = line.qty_delivered - line.qty_ordered

    @api.depends('state')
    def _compute_color(self):
        color_map = {
            'pending': 0,
            'in_progress': 4,
            'done': 10,
            'cancelled': 1,
        }
        for line in self:
            line.color = color_map.get(line.state, 0)

    def action_start(self):
        """Passer le plat à l'état 'En préparation'."""
        for line in self:
            if line.state == 'pending':
                line.state = 'in_progress'

    def action_deliver(self):
        """Marquer le plat comme livré et enregistrer l'heure de livraison."""
        now = fields.Datetime.now()
        for line in self:
            if line.state == 'in_progress':
                line.state = 'done'
                if not line.delivery_datetime:
                    line.delivery_datetime = now
                if line.qty_delivered == 0.0:
                    line.qty_delivered = line.qty_ordered

    def action_cancel(self):
        """Annuler le plat."""
        for line in self:
            if line.state in ('pending', 'in_progress'):
                line.state = 'cancelled'

    def action_reset_pending(self):
        """Remettre le plat en attente."""
        for line in self:
            if line.state == 'cancelled':
                line.state = 'pending'
