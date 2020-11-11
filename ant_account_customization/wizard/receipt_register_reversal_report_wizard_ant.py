from odoo import models,fields,api,_
from datetime import datetime

class receipt_reversal_report_wizard_ant(models.TransientModel):
    _name = "receipt.reversal.report.wizard.ant"

    def _get_from_date(self):
        return fields.Date.today()

    def _get_payment_method_ids(self):
        payment_method_ids = self.env['account.journal'].search([('type','in',['bank','cash'])])
        return [(6,0,payment_method_ids.ids)]
    
    from_date = fields.Date('From',default=_get_from_date)
    to_date = fields.Date('To', default=_get_from_date)
    user_id = fields.Many2one('res.users','Cashier',required=True)
    payment_method_ids = fields.Many2many('account.journal','wizard_journal_reversal_ant','wizard_id','bank_id','Payment Mode',domain=[('type','in',['bank','cash'])])



    def get_report_data(self):
        payment_obj = self.env['account.payment']
        domain = [('state', '=', 'draft')]
        if self.from_date:
            domain.append(('payment_date', '>=', self.from_date))
        if self.to_date:
            domain.append(('payment_date', '<=', self.to_date))

        payment_invoice_ids = payment_obj.search(domain, order="id asc")
        report_data_dict = {}
        count = 0



        for payment in payment_invoice_ids:
            invoice_obj = self.env['account.invoice']
            inv_domain = [('id', '=', payment.invoice_ids.id)]
            invoice_obj_ids = invoice_obj.search(inv_domain)
            for invoice in invoice_obj_ids:
                    count += 1
                    report_data_dict[count] = {
                        'receipt_no': payment.name,
                        'receipt_paid_date': datetime.strptime(payment.payment_date, "%Y-%m-%d").strftime("%d/%m/%Y"),
                        'customer_name': payment.partner_id.name,
                        'customer_no': payment.partner_id.name,
                        'payment_mode': payment.journal_id.name,
                        'payment_amount': payment.amount,
                        'amount': invoice.amount_untaxed,
                        'gst': invoice.amount_tax,
                        'type': "",
                        'type_description': "",
                        'cashier_name': payment.create_uid.name,
                        'total_amount': payment.amount,
                        'status': invoice.state,
                        'company': payment.company_id.name,
                        'reversal_remark': payment.communication,
                    }
        return report_data_dict

