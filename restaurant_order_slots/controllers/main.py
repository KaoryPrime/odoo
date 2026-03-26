# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import logging

from odoo.http import request, route
from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)

# Valeurs autorisées pour validation côté serveur
ALLOWED_ORDER_TYPES = ('pickup', 'delivery')
ALLOWED_PICKUP_DATES = ('today', 'tomorrow', 'after_tomorrow')
ALLOWED_DELIVERY_SLOTS = (
    '11h-12h', '12h-13h', '13h-14h',
    '19h-20h', '20h-21h', '21h-22h',
)


class RestaurantWebsiteSale(WebsiteSale):
    """
    Surcharge du contrôleur website_sale pour sauvegarder les créneaux
    restaurant sur la commande lors du passage en paiement.

    Odoo 18 : request.website.sale_get_order() est remplacé par
    request.cart (accès direct au panier courant).
    """

    @route(
        ['/shop/payment'],
        type='http',
        auth='public',
        website=True,
        methods=['GET', 'POST'],
        sitemap=False,
    )
    def shop_payment(self, **post):
        # Appel du parent en premier
        res = super().shop_payment(**post)

        # Odoo 18 : request.cart est le panier courant
        order = getattr(request, 'cart', None)

        if not order:
            return res

        order_type = post.get('order_type')
        delivery_slot = post.get('delivery_slot')
        pickup_date = post.get('pickup_date')

        # Validation des valeurs reçues (sécurité : on n'écrit que des valeurs connues)
        vals = {}
        if order_type and order_type in ALLOWED_ORDER_TYPES:
            vals['order_type'] = order_type
        if pickup_date and pickup_date in ALLOWED_PICKUP_DATES:
            vals['pickup_date'] = pickup_date
        if delivery_slot and delivery_slot in ALLOWED_DELIVERY_SLOTS:
            vals['delivery_slot'] = delivery_slot

        if vals:
            try:
                order.sudo().write(vals)
                _logger.info(
                    "restaurant_order_slots: créneau mis à jour sur commande %s → %s",
                    order.name, vals,
                )
            except Exception as e:
                _logger.error(
                    "restaurant_order_slots: erreur écriture créneau sur commande %s — %s",
                    order.name, e,
                )

        return res
