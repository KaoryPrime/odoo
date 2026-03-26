from odoo import models, fields


class Allergen(models.Model):
    _name = 'allergen.allergen'
    _description = 'Allergène réglementaire'
    _order = 'sequence, name'

    name = fields.Char(
        string='Nom',
        required=True,
        translate=True,
    )
    code = fields.Char(
        string='Code réglementaire',
        help="Identifiant réglementaire de l'allergène (ex: gluten, crustaces, lait…)",
    )
    icon = fields.Char(
        string='Icône (emoji)',
        help="Emoji représentant l'allergène pour l'affichage web (ex: 🌾, 🥛, 🥚)",
        size=10,
    )
    description = fields.Text(
        string='Description',
        translate=True,
        help="Détails sur cet allergène et les aliments qui le contiennent",
    )
    color = fields.Integer(
        string='Couleur',
        default=0,
    )
    sequence = fields.Integer(
        string='Séquence',
        default=10,
    )
    active = fields.Boolean(
        string='Actif',
        default=True,
    )
    product_count = fields.Integer(
        string='Nb produits',
        compute='_compute_product_count',
    )

    def _compute_product_count(self):
        for allergen in self:
            allergen.product_count = self.env['product.template'].search_count(
                [('allergen_ids', 'in', allergen.id)]
            )

    def action_view_products(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Produits contenant {self.name}',
            'res_model': 'product.template',
            'view_mode': 'list,form',
            'domain': [('allergen_ids', 'in', self.id)],
        }
