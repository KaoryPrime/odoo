# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import logging
from datetime import datetime, timedelta

import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

# Délai de timeout pour les appels API (secondes)
SHIPDAY_TIMEOUT = 10


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # ── Champs de traçabilité ──────────────────────────────────────────────────

    shipday_sent = fields.Boolean(
        string='Envoyé à Shipday',
        default=False,
        copy=False,
        tracking=True,
    )
    shipday_order_id = fields.Char(
        string='ID Shipday',
        readonly=True,
        copy=False,
        help="Identifiant de la commande dans Shipday après envoi.",
    )
    shipday_last_error = fields.Text(
        string='Dernière erreur Shipday',
        readonly=True,
        copy=False,
    )

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _get_shipday_api_key(self):
        """Récupère la clé API depuis les paramètres système."""
        key = self.env['ir.config_parameter'].sudo().get_param('shipday_odoo.api_key')
        if not key or key.strip() == '':
            raise UserError(_(
                "Clé API Shipday non configurée.\n"
                "Allez dans Paramètres → Shipday pour renseigner votre clé API."
            ))
        return key.strip()

    def _get_shipday_restaurant_info(self):
        """Récupère les infos restaurant depuis les paramètres système."""
        get = self.env['ir.config_parameter'].sudo().get_param
        return {
            'name': get('shipday_odoo.restaurant_name') or 'Mon Restaurant',
            'address': get('shipday_odoo.restaurant_address') or '',
            'phone': get('shipday_odoo.restaurant_phone') or '',
        }

    def _get_shipday_delivery_delay(self):
        """Retourne le délai de livraison configuré (en minutes)."""
        delay = self.env['ir.config_parameter'].sudo().get_param(
            'shipday_odoo.delivery_delay', default='30'
        )
        try:
            return int(delay)
        except (ValueError, TypeError):
            return 30

    def _build_customer_address(self, partner):
        """Construit l'adresse complète du client."""
        parts = [
            partner.street or '',
            partner.street2 or '',
            partner.zip or '',
            partner.city or '',
            partner.state_id.name if partner.state_id else '',
            partner.country_id.name if partner.country_id else '',
        ]
        return ', '.join(p for p in parts if p)

    def _resolve_delivery_date(self):
        """
        Calcule la date de livraison attendue.
        Compatible avec restaurant_order_slots si présent,
        avec fallback sur aujourd'hui si le module est absent.
        """
        today = fields.Date.today()

        # Compatibilité optionnelle avec restaurant_order_slots
        if hasattr(self, 'pickup_date') and self.pickup_date:
            pickup = self.pickup_date
            if pickup == 'today':
                return today
            elif pickup == 'tomorrow':
                return today + timedelta(days=1)
            elif pickup == 'after_tomorrow':
                return today + timedelta(days=2)

        return today

    def _resolve_pickup_time(self, delivery_date):
        """
        Calcule l'heure de pickup depuis le créneau de livraison.
        Compatible avec restaurant_order_slots si présent.
        """
        # Compatibilité optionnelle avec restaurant_order_slots
        if hasattr(self, 'delivery_slot') and self.delivery_slot:
            slot = self.delivery_slot
            try:
                slot_start = slot.split('-')[0].strip().replace('h', ':00')
                # Valider le format HH:MM:SS
                datetime.strptime(
                    f"{delivery_date.strftime('%Y-%m-%d')} {slot_start}",
                    "%Y-%m-%d %H:%M:%S"
                )
                return slot_start
            except Exception:
                _logger.warning("shipday_odoo: format de créneau invalide '%s'", slot)

        # Fallback : heure courante arrondie à la demi-heure
        now = datetime.now()
        rounded = now.replace(minute=0 if now.minute < 30 else 30, second=0, microsecond=0)
        return rounded.strftime('%H:%M:%S')

    def _build_shipday_payload(self):
        """Construit le payload JSON pour l'API Shipday."""
        self.ensure_one()
        partner = self.partner_shipping_id or self.partner_id
        restaurant = self._get_shipday_restaurant_info()
        delivery_date = self._resolve_delivery_date()
        pickup_time = self._resolve_pickup_time(delivery_date)
        delay = self._get_shipday_delivery_delay()

        # Calcul de l'heure de livraison estimée
        date_str = delivery_date.strftime('%Y-%m-%d')
        try:
            pickup_dt = datetime.strptime(f"{date_str} {pickup_time}", "%Y-%m-%d %H:%M:%S")
            delivery_time = (pickup_dt + timedelta(minutes=delay)).strftime('%H:%M:%S')
        except Exception:
            delivery_time = pickup_time

        return {
            "orderNumber": self.name,
            "customerName": partner.name or '',
            "customerAddress": self._build_customer_address(partner),
            "customerEmail": partner.email or '',
            "customerPhoneNumber": partner.phone or partner.mobile or '',
            "restaurantName": restaurant['name'],
            "restaurantAddress": restaurant['address'],
            "restaurantPhoneNumber": restaurant['phone'],
            "totalOrderCost": self.amount_total,
            "deliveryInstruction": self.note or '',
            "orderSource": "Odoo",
            "additionalId": str(self.id),
            "expectedDeliveryDate": delivery_date.isoformat(),
            "expectedPickupTime": pickup_time,
            "expectedDeliveryTime": delivery_time,
        }

    # ── Action principale ─────────────────────────────────────────────────────

    def action_send_to_shipday(self):
        """Envoie la commande vers Shipday via l'API REST."""
        for order in self:
            api_key = order._get_shipday_api_key()

            headers = {
                'Accept': 'application/json',
                'Authorization': f'Basic {api_key}',
                'Content-Type': 'application/json',
            }

            payload = order._build_shipday_payload()

            _logger.info(
                "shipday_odoo: envoi commande %s vers Shipday (client: %s)",
                order.name, order.partner_id.name,
            )

            try:
                response = requests.post(
                    'https://api.shipday.com/orders',
                    headers=headers,
                    json=payload,
                    timeout=SHIPDAY_TIMEOUT,
                )
            except requests.exceptions.Timeout:
                error_msg = _("Timeout : Shipday n'a pas répondu dans les %d secondes.") % SHIPDAY_TIMEOUT
                order.shipday_last_error = error_msg
                raise UserError(error_msg)
            except requests.exceptions.ConnectionError:
                error_msg = _("Impossible de joindre l'API Shipday. Vérifiez votre connexion internet.")
                order.shipday_last_error = error_msg
                raise UserError(error_msg)

            if response.status_code in (200, 201):
                order.shipday_sent = True
                order.shipday_last_error = False
                # Récupérer l'ID Shipday si présent dans la réponse
                try:
                    resp_data = response.json()
                    if isinstance(resp_data, dict):
                        order.shipday_order_id = str(
                            resp_data.get('orderId') or resp_data.get('id') or ''
                        )
                except Exception:
                    pass
                order.message_post(
                    body=_("✅ Commande envoyée à Shipday avec succès. ID Shipday : %s")
                    % (order.shipday_order_id or 'N/A'),
                )
                _logger.info(
                    "shipday_odoo: commande %s envoyée avec succès (HTTP %s)",
                    order.name, response.status_code,
                )
            else:
                error_msg = _("Erreur Shipday (HTTP %s) : %s") % (
                    response.status_code, response.text[:500]
                )
                order.shipday_last_error = error_msg
                order.message_post(body=f"❌ {error_msg}")
                _logger.error(
                    "shipday_odoo: erreur envoi commande %s — HTTP %s — %s",
                    order.name, response.status_code, response.text[:200],
                )
                raise UserError(error_msg)

    def action_reset_shipday(self):
        """Remet à zéro le statut Shipday pour permettre un renvoi."""
        for order in self:
            order.shipday_sent = False
            order.shipday_order_id = False
            order.shipday_last_error = False
            order.message_post(body=_("🔄 Statut Shipday réinitialisé manuellement."))
