# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, SUPERUSER_ID, _


class account_payment(models.Model):
    _name = 'account.payment'
    _inherit = ['account.payment','mail.thread', 'ir.needaction_mixin']