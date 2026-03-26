import base64
import io

from odoo import api, fields, models

try:
    import qrcode
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False


class RestaurantQrcodeMenu(models.Model):
    _name = 'restaurant.qrcode.menu'
    _description = 'QR Code Menu Restaurant'

    name = fields.Char(string='Nom / Table', required=True)
    table_number = fields.Char(string='Numéro de table')
    menu_url = fields.Char(string='URL du menu', required=True)
    qr_code_image = fields.Binary(
        string='QR Code',
        compute='_compute_qr_code',
        store=True,
        attachment=True,
    )
    description = fields.Text(string='Description')
    active = fields.Boolean(default=True)
    scan_count = fields.Integer(string='Nombre de scans', default=0)
    last_scan_date = fields.Datetime(string='Dernier scan')
    color = fields.Integer(default=0)

    @api.depends('menu_url')
    def _compute_qr_code(self):
        for record in self:
            if record.menu_url and HAS_QRCODE:
                try:
                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4,
                    )
                    qr.add_data(record.menu_url)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    buffer = io.BytesIO()
                    img.save(buffer, format="PNG")
                    record.qr_code_image = base64.b64encode(buffer.getvalue())
                except Exception:
                    record.qr_code_image = False
            else:
                record.qr_code_image = False

    def action_reset_scan_count(self):
        for record in self:
            record.scan_count = 0
            record.last_scan_date = False

    def action_increment_scan(self):
        for record in self:
            record.scan_count += 1
            record.last_scan_date = fields.Datetime.now()
