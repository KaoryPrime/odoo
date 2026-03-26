from odoo import _, api, fields, models

DELIVERY_SLOT_SELECTION = [
    ('11h-12h', '11h – 12h'),
    ('12h-13h', '12h – 13h'),
    ('13h-14h', '13h – 14h'),
    ('19h-20h', '19h – 20h'),
    ('20h-21h', '20h – 21h'),
    ('21h-22h', '21h – 22h'),
]

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    pickup_date = fields.Selection(
        selection=[
            ('today', "Aujourd'hui"),
            ('tomorrow', 'Demain'),
            ('after_tomorrow', 'Après-demain'),
        ],
        string="Jour de retrait/livraison",
        default='today',
        tracking=True,
    )

    order_type = fields.Selection(
        selection=[
            ('pickup', 'À emporter'),
            ('delivery', 'Livraison'),
        ],
        string="Type de commande",
        default='pickup',
        tracking=True,
    )

    delivery_slot = fields.Selection(
        selection=DELIVERY_SLOT_SELECTION,
        string="Créneau horaire",
        default='12h-13h',
        tracking=True,
    )

    order_slot_summary = fields.Char(
        string='Résumé créneau',
        compute='_compute_order_slot_summary',
        store=True,
        help="Résumé lisible du créneau pour affichage rapide.",
    )

    @api.depends('pickup_date', 'order_type', 'delivery_slot')
    def _compute_order_slot_summary(self):
        pickup_labels = dict(self._fields['pickup_date'].selection)
        type_labels = dict(self._fields['order_type'].selection)
        slot_labels = dict(self._fields['delivery_slot'].selection)
        for order in self:
            parts = []
            if order.order_type:
                parts.append(type_labels.get(order.order_type, ''))
            if order.pickup_date:
                parts.append(pickup_labels.get(order.pickup_date, ''))
            if order.delivery_slot:
                parts.append(slot_labels.get(order.delivery_slot, ''))
            order.order_slot_summary = ' — '.join(p for p in parts if p) or False
