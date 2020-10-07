from odoo import api, fields, models, tools, SUPERUSER_ID, _

class ANTAccountInvoice(models.Model):
    _inherit = "account.invoice"

    supplier_invoice_date = fields.Date("Supplier Invoice Date", track_visibility='onchange')