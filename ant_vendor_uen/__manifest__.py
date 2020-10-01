# -*- coding: utf-8 -*-
# Part of ANT. See LICENSE file for full copyright and licensing details.
{
    'name': 'Vendor UEN',
    'version': '2.1',
    'category': 'Partner',
    'summary': 'Vendor UEN',
    'description': """
This module is used to expose uen field in partner form.
    """,
    'depends': ['base','account'],
    'author': "Accentuate Pte. Ltd.",
    'website': "accentuate.com.sg",
    'data': [
        'views/nmt_res_partner.xml',
        'views/nmt_account_invoice.xml',
        'views/nmt_product_template.xml',
    ],
    'installable': True,
    'auto_install': False
}