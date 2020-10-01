# -*- coding: utf-8 -*-
# Part of Accentuate. See LICENSE file for full copyright and licensing details.##
##################################################################################

{
    'name': 'Models Tracking',
    'author': 'Accentuate Pte Ltd',
    'version': '10.0.1.1',
    'license': 'AGPL-3',
    'sequence': 1,
    'category': 'Mail',
    'description': """
      This module allow to track all fields of model in chatter, based on configuration
    """,
    'depends': [
      'base','mail','sale','purchase','account_accountant','ant_model_tracking_spt'
    ],
    'data': [

     'views/account_move.xml',
     
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
