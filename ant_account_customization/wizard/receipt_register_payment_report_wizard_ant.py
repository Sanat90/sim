from odoo import models, fields, api, _
from collections import OrderedDict, defaultdict
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta
from datetime import datetime

class receipt_payment_report_wizard_ant(models.TransientModel):
    _name = "receipt.payment.report.wizard.ant"

    def _get_from_date(self):
        return fields.Date.today()

    def _get_payment_method_ids(self):
        payment_method_ids = self.env['account.journal'].search([('type', 'in', ['bank', 'cash'])])
        return [(6, 0, payment_method_ids.ids)]

    from_date = fields.Date('From', default=_get_from_date)
    to_date = fields.Date('To', default=_get_from_date)
    user_id = fields.Many2one('res.users', 'Cashier', required=True)
    payment_method_ids = fields.Many2many('account.journal', 'wizard_journal_bank_ant', 'wizard_id', 'bank_id',
                                          'Payment Mode', domain=[('type', 'in', ['bank', 'cash'])])
    report_type = fields.Selection(string="Type", selection=[('amount', 'Amount'), ('count', 'Count')],
                                   required=True, default="amount")

    def get_report_data(self):
        def get_month_day_range(date):
            last_day = date + relativedelta(day=1, months=+1, days=-1)
            first_day = date + relativedelta(day=1)
            return first_day, last_day

        invoice_obj = self.env['account.invoice']
        domain = [('user_id', '=', self.user_id.id), ('type', '=', 'out_invoice')]
        if self.from_date:
            domain.append(('date_invoice', '>=', self.from_date))
        if self.to_date:
            domain.append(('date_invoice', '<=', self.to_date))

        invoice_ids = invoice_obj.search(domain)
        journal_ids = self.env['account.journal'].search([('type', 'in', ['bank', 'cash'])]).ids
        mode_result = defaultdict(list)
        for invoice in invoice_ids:
            if invoice.payment_ids:
                for payment in invoice.payment_ids:
                    if payment.journal_id.id in journal_ids and payment.payment_type == "inbound":
                        if self.report_type == "amount":
                            mode_result[str(payment.journal_id.name)] += [payment.amount]
                        elif self.report_type == "count":
                            mode_result[str(payment.journal_id.name)] += [1]
        employee_header_lis = []
        employee_data_lis = []
        input_from_date = datetime.strptime(self.from_date, "%Y-%m-%d")
        input_to_date = datetime.strptime(self.to_date, "%Y-%m-%d")
        from_date = datetime.strptime(self.from_date, "%Y-%m-%d")
        month_domain = {}
        while from_date < input_to_date:
            new_domain = [('user_id', '=', self.user_id.id), ('type', '=', 'out_invoice')]
            if from_date == input_from_date:
                from_date, to_date = get_month_day_range(from_date)
                month_domain.update(
                    {from_date: new_domain + [("date_invoice", ">=", input_from_date.strftime("%Y-%m-%d")),
                                              ("date_invoice", "<", to_date.strftime("%Y-%m-%d"))]})
                from_date = to_date + relativedelta(days=1)
            else:
                from_date, to_date = get_month_day_range(from_date)
                if to_date.month == input_to_date.month:
                    to_date = input_to_date
                month_domain.update(
                    {from_date: new_domain + [("date_invoice", ">=", input_from_date.strftime("%Y-%m-%d")),
                                              ("date_invoice", "<=", to_date.strftime("%Y-%m-%d"))]})
                from_date = to_date + relativedelta(days=1)
        mode_result = OrderedDict(sorted(mode_result.items()))
        for item, amounts in mode_result.items():
            employee_header_lis.append(item)
            employee_data_lis.append(sum(amounts))
        month_header = []
        month_data = []
        for month, m_domain in month_domain.items():
            data_set = [month.strftime("%B") + " " + month.strftime("%Y")]
            for journal in self.env['account.journal'].search([('type', 'in', ['bank', 'cash'])], order='name'):
                if journal.name not in month_header:
                    month_header.append(journal.name)
                invoice_ids = invoice_obj.search(m_domain)
                total = 0.0
                for invoice in invoice_ids:
                    if invoice.payment_ids:
                        for payment in invoice.payment_ids:
                            if journal.id == payment.journal_id.id and payment.payment_type == "inbound":
                                if self.report_type == "amount":
                                    total += payment.amount
                                elif self.report_type == "count":
                                    total += 1
                data_set.append(total)
            month_data.append(data_set)
        zero_list = [0 for item in month_header]
        return {"header_list": employee_header_lis if employee_header_lis else month_header,
                "total_list": employee_data_lis if employee_data_lis else zero_list,
                "month_header": month_header, "month_data": month_data}
