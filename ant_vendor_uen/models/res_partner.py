from odoo import api, fields, models, tools, SUPERUSER_ID, _

class ANTResPartner(models.Model):
    _inherit = "res.partner"

    vendor_uen = fields.Char('UEN', track_visibility='always')
    