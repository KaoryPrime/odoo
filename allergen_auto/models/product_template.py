from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    allergen_ids = fields.Many2many(
        comodel_name='allergen.allergen',
        relation='product_template_allergen_rel',
        column1='product_tmpl_id',
        column2='allergen_id',
        string='Allergènes',
        compute='_compute_allergens',
        store=True,
        readonly=False,
        help="Allergènes présents dans ce produit. "
             "Calculé automatiquement depuis la nomenclature (BoM) si elle existe. "
             "Modifiable manuellement pour les matières premières sans BoM.",
    )

    allergen_computed = fields.Boolean(
        string='Allergènes calculés automatiquement',
        compute='_compute_allergen_computed',
        store=False,
    )

    @api.depends('bom_ids')
    def _compute_allergen_computed(self):
        """Indique si les allergènes sont gérés automatiquement (produit avec BoM)."""
        for product in self:
            product.allergen_computed = bool(product.bom_ids)

    @api.depends(
        'bom_ids',
        'bom_ids.bom_line_ids',
        'bom_ids.bom_line_ids.product_id',
        'bom_ids.bom_line_ids.product_id.product_tmpl_id.allergen_ids',
    )
    def _compute_allergens(self):
        """
        Calcule les allergènes d'un produit fini en agrégeant ceux de tous
        ses composants définis dans la nomenclature (BoM).
        Si le produit n'a pas de BoM, la valeur stockée est conservée
        (gestion manuelle par l'utilisateur).
        """
        for product in self:
            if product.bom_ids:
                # Produit avec BoM → calcul automatique depuis les composants
                allergens = self.env['allergen.allergen']
                for bom in product.bom_ids:
                    for line in bom.bom_line_ids:
                        allergens |= line.product_id.product_tmpl_id.allergen_ids
                product.allergen_ids = allergens
            # Pas de BoM → on ne touche pas (saisie manuelle, champ store=True conserve la valeur)
