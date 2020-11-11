# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError



class account_payment(models.Model):
    _inherit = 'account.payment'
    enable_reason = fields.Boolean(string='Enable Reason', help="Enable Shortage / Excess Payment Reason", default=False)
    shortfall_reason = fields.Char(string='Shortage/Excess Reason', help="Fill in reason for Shortage/Excess Payments")
    reversal_by = fields.Char(string='Reversal By', help="Person Who Reverse the payment")
    cancel_date = fields.Date(string='Cancelled Date', default=fields.Date.context_today, required=True, copy=False)
    reversal_remark = fields.Char(string='Reversal Remarks', help="Remarks on Reversal")


    @api.multi
    def cancel(self):
        for rec in self:
            for move in rec.move_line_ids.mapped('move_id'):
                if rec.invoice_ids:
                    move.line_ids.remove_move_reconcile()
                move.button_cancel()
                move.unlink()
            rec.state = 'draft'
