# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class account_payment(models.Model):
    _inherit = 'account.payment'
    
    enable_reason = fields.Boolean(string='Short Fall', help="Enable Shortage / Excess Payment Reason", default=False)
    shortfall_reason = fields.Char(string='Shortage/Excess Reason', help="Fill in reason for Shortage/Excess Payments")
    reversal_by = fields.Many2one('res.users',string='Reversal By', help="Person Who Reverse the payment",default=lambda self: self.env.user)
    cancel_date = fields.Date(string='Cancelled Date', copy=False)
    reversal_remark = fields.Char(string='Reversal Remarks', help="Remarks on Reversal")


    @api.multi
    def action_custom_cancel(self):
        res_id = self.env['ant.cancel.payment.wizard'].create({'payment_id':self.id})
        return {
            'name': ('Cancel Payment'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('ant_account_customization.ant_cancel_payment_wizard_form_view').id,
            'res_model': 'ant.cancel.payment.wizard',
            'type': 'ir.actions.act_window',            
            'res_id':res_id.id,
            'target':'new'
        }
