# -*- coding: utf-8 -*-
# Part of Accentuate. See LICENSE file for full copyright and licensing details.##
##################################################################################
{
    'name': 'Account Customization',
    'author': 'Accentuate Pte Ltd',
    'version': '10.0.1.1',
    'license': 'AGPL-3',
    'sequence': 1,
    'category': 'account',
    'description': """
      This module account related changes.
    """,
    'depends': [
        'general_template','ant_sim_accounting_custom', 'base' , 'account','account_cancel'
    ],
    'data': [
        'security/ir.model.access.csv',
        'view/account_payment_shortfall.xml',
        'report/cash_register_report_ant.xml',
        'report/invoice_receipt_report_template_ant.xml',
        'report/cash_register_report_template_ant.xml',
        'wizard/cash_register_report_wizard_ant.xml',
        'wizard/bank_slip_report_wizard_ant.xml',
        'wizard/receipt_cashier_report_wizard_ant.xml',
        'wizard/receipt_payment_report_wizard_ant.xml',
        'wizard/receipt_register_report_wizard_ant.xml',
        'wizard/receipt_reversal_report_wizard_ant.xml',
        'wizard/ant_cancel_payment.xml',
        'report/bank_slip_report_template_ant.xml',
        'report/receipt_reversal_report_template_ant.xml',
        'report/receipt_cashier_report_template_ant.xml',
        'report/receipt_register_report_template_ant.xml',
        'report/receipt_payment_report_template_ant.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}

