from odoo import models, fields, api, _
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta
from datetime import datetime
from collections import OrderedDict

class receipt_cashier_report_wizard_ant(models.TransientModel):
    _name = "receipt.cashier.report.wizard.ant"

    def _get_from_date(self):
        return fields.Date.today()

    def _get_payment_method_ids(self):
        payment_method_ids = self.env['account.journal'].search([('type', 'in', ['bank', 'cash'])])
        return [(6, 0, payment_method_ids.ids)]

    from_date = fields.Date('From', default=_get_from_date)
    to_date = fields.Date('To', default=_get_from_date)
    user_id = fields.Many2one('res.users', 'Cashier', required=True)
    payment_method_ids = fields.Many2many('account.journal', 'wizard_journal_receipt_cashier_ant', 'wizard_id',
                                          'bank_id', 'Payment Mode',
                                          domain=[('type', 'in', ['bank', 'cash'])])
    period = fields.Selection(string="Period",
                              selection=[('day', 'Day'), ('week', 'Week'), ('month', 'Month')],
                              required=True)

    def get_report_data(self):
        def get_month_day_range(date):
            last_day = date + relativedelta(day=1, months=+1, days=-1)
            first_day = date + relativedelta(day=1)
            return first_day, last_day
        if self.period == "day":
            domains = OrderedDict()
            if self.from_date:
                from_date = datetime.strptime(self.from_date, "%Y-%m-%d")
            else:
                from_date = datetime.strptime(self._get_from_date(), "%Y-%m-%d") - relativedelta(days=7)
            for count in range(10):
                domain = [('user_id', '=', self.user_id.id), ('type', '=', 'out_invoice')]
                from_date = from_date + relativedelta(days=1 if count > 0 else 0)
                domains.update({from_date: domain + [("date_invoice", "=", from_date.strftime("%Y-%m-%d"))]})

            invoice_obj = self.env['account.invoice']
            header_list = []
            total_dict = []
            for item, value in domains.items():
                invoice_ids = invoice_obj.search(value)
                count = 0
                journal_ids = self.payment_method_ids.ids if self.payment_method_ids else self.env[
                    'account.journal'].search(
                    [('type', 'in', ['bank', 'cash'])]).ids
                total_amount = 0.0
                for invoice in invoice_ids:
                    if invoice.payment_ids:
                        for payment in invoice.payment_ids:
                            if payment.journal_id.id in journal_ids and payment.payment_type == "inbound":
                                total_amount += payment.amount
                header_list+=[item.strftime("%d/%m/%Y")]
                total_dict+=[total_amount]
            return {"header_list": header_list, "total_list": total_dict}
        elif self.period == "week":
            domains = OrderedDict()
            if self.from_date:
                from_date = datetime.strptime(self.from_date, "%Y-%m-%d")
            else:
                from_date = datetime.strptime(self._get_from_date(), "%Y-%m-%d") - relativedelta(days=7)
            for count in range(10):
                domain = [('user_id', '=', self.user_id.id), ('type', '=', 'out_invoice')]
                from_date = from_date
                to_date = from_date + relativedelta(days=7)
                domains.update({from_date: domain + [("date_invoice", ">=", from_date.strftime("%Y-%m-%d")),
                                                     ("date_invoice", "<", to_date.strftime("%Y-%m-%d"))]})
                from_date = to_date

            invoice_obj = self.env['account.invoice']
            header_list = []
            total_dict = []
            for item, value in domains.items():
                invoice_ids = invoice_obj.search(value)
                journal_ids = self.payment_method_ids.ids if self.payment_method_ids else self.env[
                    'account.journal'].search(
                    [('type', 'in', ['bank', 'cash'])]).ids
                total_amount = 0.0
                for invoice in invoice_ids:
                    if invoice.payment_ids:
                        for payment in invoice.payment_ids:
                            if payment.journal_id.id in journal_ids and payment.payment_type == "inbound":
                                total_amount += payment.amount
                header_list+=[ "Week of " + item.strftime("%d/%m/%Y")]
                total_dict+=[total_amount]
            return {"header_list": header_list, "total_list": total_dict}
        elif self.period == "month":
            domains = OrderedDict()
            if self.from_date:
                from_date = datetime.strptime(self.from_date, "%Y-%m-%d")
            else:
                from_date = datetime.strptime(self._get_from_date(), "%Y-%m-%d") - relativedelta(days=7)
            for count in range(10):
                domain = [('user_id', '=', self.user_id.id), ('type', '=', 'out_invoice')]
                from_date, to_date = get_month_day_range(from_date)
                domains.update({from_date: domain + [("date_invoice", ">=", from_date.strftime("%Y-%m-%d")),
                                                     ("date_invoice", "<", to_date.strftime("%Y-%m-%d"))]})
                from_date = to_date + relativedelta(days=1)

            invoice_obj = self.env['account.invoice']
            header_list = []
            total_dict = []
            for item, value in domains.items():
                invoice_ids = invoice_obj.search(value)
                journal_ids = self.payment_method_ids.ids if self.payment_method_ids else self.env[
                    'account.journal'].search(
                    [('type', 'in', ['bank', 'cash'])]).ids
                total_amount = 0.0
                for invoice in invoice_ids:
                    if invoice.payment_ids:
                        for payment in invoice.payment_ids:
                            if payment.journal_id.id in journal_ids and payment.payment_type == "inbound":
                                total_amount += payment.amount
                header_list+=[item.strftime("%B") + " " + item.strftime("%Y")]
                total_dict+=[total_amount]
            return {"header_list": header_list, "total_list": total_dict}

# receipt_no = "account.payment number as Receipt number"
# receipt_paid_date = "Date where this Payment is registered and Paid"
# cashier_name = "res.partner , Person / account who registered the payment"
# cancelled_date_date = "which the payment is cancelled in the system (Need to create field in account.payment)"
# reversal = "By Account/User who cancelled the payment in the system (Need to create field in account.payment)"
# payment_mode = "Mode of payment used by customer to make this payment (Payment Journal)"
# payment_amount = "Amount paid for this paid Transaction (payment amount from account.payment)"
# amount = "Amount before GST/VAT Taxes (Please Pull From Invoice)"
# gst = "GST Tax amount calculated (Please Pull From Invoice)"
# total = "amount_total of the Invoice"
# customer_no = "membership_number from res.partner field"
# customer_name = "Customer name from Res.partner"
# reversal = "Remark"
