# -*- coding: utf-8 -*-
# Part of ANT. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, SUPERUSER_ID, _

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
    partner_ref = fields.Char('Quote Ref', copy=False,\
        help="Reference of the sales order or bid sent by the vendor. "
             "It's used to do the matching when you receive the "
             "products as this reference is usually written on the "
             "delivery order sent by your vendor.")