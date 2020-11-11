from odoo import models,fields,api,_
from datetime import datetime

class ant_cancel_payment_wizard(models.TransientModel):
    _name = "ant.cancel.payment.wizard"
    
    payment_id = fields.Many2one('account.payment')
    reversal_by = fields.Many2one('res.users',string='Reversal By', help="Person Who Reverse the payment",default=lambda self: self.env.user)
    cancel_date = fields.Date(string='Cancelled Date', copy=False)
    reversal_remark = fields.Char(string='Reversal Remarks', help="Remarks on Reversal")
    
    def execute_cancel(self):
        self.payment_id.write({'reversal_by':self.reversal_by.id,'cancel_date':self.cancel_date,'reversal_remark':self.reversal_remark})
        self.payment_id.cancel()