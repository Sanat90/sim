from odoo import models,fields,api,_
from datetime import datetime

class bank_slip_report_wizard_ant(models.TransientModel):
    _name = "bank.slip.report.wizard.ant"

    def _get_from_date(self):
        return fields.Date.today()

    def _get_payment_method_ids(self):
        payment_method_ids = self.env['account.journal'].search([('type','in',['bank','cash'])])
        return [(6,0,payment_method_ids.ids)]
    
    from_date = fields.Date('From',default=_get_from_date)
    to_date = fields.Date('To', default=_get_from_date)
    user_id = fields.Many2one('res.users','Cashier',required=True)
    payment_method_ids = fields.Many2many('account.journal','wizard_journal_bank_ant','wizard_id','bank_id','Payment Mode',domain=[('type','in',['bank','cash'])])



    def get_report_data(self):
        invoice_obj = self.env['account.invoice']
        domain = [('user_id','=',self.user_id.id),('type','=','out_invoice')]
        if self.from_date:
            domain.append(('date_invoice','>=',self.from_date))
        if self.to_date:
            domain.append(('date_invoice','<=',self.to_date))

        invoice_ids = invoice_obj.search(domain, order="id asc")
        report_data_dict = {}
        count =0
        for invoice in invoice_ids:
            if invoice.payment_ids:
                payment = invoice.payment_ids[0]
                journal_ids = self.payment_method_ids.ids if self.payment_method_ids else self.env[
                    'account.journal'].search(
                    [('type', 'in', ['bank', 'cash'])]).ids
                if payment.journal_id.id in journal_ids:
                    count += 1
                    report_data_dict[count] = {
                        'name' : payment.name,
                        'date' : datetime.strptime(payment.payment_date, "%Y-%m-%d").strftime("%d/%m/%Y"),
                        'state' : payment.state,
                        'mode' : payment.journal_id.name,
                        'reference' : payment.communication,
                        'amount' : payment.amount,
                    }
        return report_data_dict
