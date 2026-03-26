from odoo import models, fields, api, Command
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_employee_discount_applied = fields.Boolean(
        string='Remise employé appliquée',
        default=False,
        copy=False,
        help="Indique si la remise employé a été appliquée sur cette commande.",
    )
    x_employee_discount_status = fields.Char(
        string='Statut remise employé',
        copy=False,
        readonly=True,
        help="Détail du résultat du calcul de remise employé.",
    )

    def _get_employee_tag_name(self):
        """Retourne le nom du tag employé, configurable via les paramètres système."""
        return self.env['ir.config_parameter'].sudo().get_param(
            'employee_order_discount.tag_name', default='Employé'
        )

    def _get_or_create_discount_product(self):
        """
        Retourne le produit de remise. Le crée automatiquement s'il n'existe pas.
        Utilise un XML ID pour éviter les doublons entre installations.
        """
        product = self.env.ref(
            'employee_order_discount.product_employee_discount',
            raise_if_not_found=False,
        )
        if product:
            return product.with_context(active_test=False)

        product = self.env['product.product'].sudo().search(
            [('name', '=', 'Remise Employé'), ('active', 'in', [True, False])],
            limit=1,
        )
        if product:
            return product

        _logger.info("employee_order_discount: création automatique du produit 'Remise Employé'")
        product = self.env['product.product'].sudo().create({
            'name': 'Remise Employé',
            'type': 'service',
            'sale_ok': True,
            'purchase_ok': False,
            'invoice_policy': 'order',
            'taxes_id': [Command.set([])],
            'description_sale': 'Remise accordée aux employés (commande gratuite)',
        })
        return product

    def _apply_employee_discount(self):
        """
        Applique une remise totale (ligne négative) si :
        - Le client possède le tag employé configuré
        - Il a passé moins de 2 commandes confirmées ce mois-ci
        - Aucune remise n'a déjà été appliquée sur cette commande
        """
        self.ensure_one()

        if self.x_employee_discount_applied:
            return

        tag_name = self._get_employee_tag_name()

        is_employe = any(tag.name == tag_name for tag in self.partner_id.category_id)
        if not is_employe:
            self.x_employee_discount_status = f"Client sans tag '{tag_name}' — remise non applicable."
            return

        if self.date_order:
            order_date = self.date_order.date()
        else:
            order_date = fields.Date.context_today(self)

        first_day = order_date.replace(day=1)
        last_day = first_day + relativedelta(months=1, days=-1)

        orders_in_month = self.search_count([
            ('partner_id', '=', self.partner_id.id),
            ('date_order', '>=', fields.Datetime.to_datetime(first_day)),
            ('date_order', '<=', fields.Datetime.to_datetime(last_day).replace(
                hour=23, minute=59, second=59
            )),
            ('state', 'not in', ['cancel', 'draft']),
            ('id', '!=', self.id),
        ])

        if orders_in_month >= 2:
            self.x_employee_discount_status = (
                f"Remise non appliquée : {orders_in_month} commande(s) déjà passée(s) "
                f"ce mois-ci (limite : 2)."
            )
            return

        lines_to_discount = self.order_line.filtered(
            lambda l: l.product_id and l.price_subtotal > 0
        )
        if not lines_to_discount:
            self.x_employee_discount_status = "Aucune ligne facturable — remise non appliquée."
            return

        discount_product = self._get_or_create_discount_product()
        already_discounted = self.order_line.filtered(
            lambda l: l.product_id == discount_product
        )
        if already_discounted:
            self.x_employee_discount_applied = True
            self.x_employee_discount_status = "Remise déjà présente sur la commande."
            return

        total_ht_to_discount = sum(lines_to_discount.mapped('price_subtotal'))

        if total_ht_to_discount <= 0:
            self.x_employee_discount_status = "Montant HT nul — remise non appliquée."
            return

        self.order_line = [Command.create({
            'product_id': discount_product.id,
            'name': f'Commande gratuite employé ({tag_name})',
            'product_uom_qty': 1,
            'price_unit': -total_ht_to_discount,
            'tax_id': [Command.set([])],
            'sequence': 999,
        })]

        self.x_employee_discount_applied = True
        self.x_employee_discount_status = (
            f"✅ Remise appliquée : -{total_ht_to_discount:.2f} € HT "
            f"({orders_in_month} commande(s) ce mois-ci)."
        )
        _logger.info(
            "employee_order_discount: remise de %.2f€ HT appliquée sur commande %s (client: %s)",
            total_ht_to_discount, self.name, self.partner_id.name,
        )

    @api.model_create_multi
    def create(self, vals_list):
        """
        Odoo 18 : create() prend une liste de vals (model_create_multi).
        On applique la remise après création pour chaque commande.
        """
        orders = super().create(vals_list)
        for order in orders:
            order._apply_employee_discount()
        return orders

    def action_confirm(self):
        """
        Applique la remise au moment de la confirmation si elle n'a pas encore
        été appliquée (ex : commande créée en brouillon, tag ajouté après).
        """
        result = super().action_confirm()
        for order in self:
            order._apply_employee_discount()
        return result

    def action_reset_employee_discount(self):
        """
        Action manuelle : supprime la ligne de remise et réinitialise les flags,
        permettant de recalculer la remise si nécessaire.
        """
        self.ensure_one()
        discount_product = self._get_or_create_discount_product()
        discount_lines = self.order_line.filtered(
            lambda l: l.product_id == discount_product
        )
        discount_lines.unlink()
        self.x_employee_discount_applied = False
        self.x_employee_discount_status = "Remise réinitialisée manuellement."
        self._apply_employee_discount()
