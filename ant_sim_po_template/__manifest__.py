# -*- coding: utf-8 -*-
# Part of ANT. See LICENSE file for full copyright and licensing details.
{
    'name': 'Purchase Order Email Template',
    'category': 'Approval',
    'summary': 'Purchase Order Email Template',
    'description': """
This module is used to add custom Purchase Order Email Template.
""",
    'depends': ['base','purchase'],
    'author': "Accentuate Pte Ltd.",
    'website': "accentuate.com.sg",
    'data': [
        'data/email_templates.xml'
    ],  
    'installable': True,
}
