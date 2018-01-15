# -*- coding: utf-8 -*-

{
    'name': 'Mass Mail Invoice',
    'summary': 'This module allows sending massive emails of invoices to customers.',
    'category': 'Accounting',
    'version': '1.0',
    'website': 'http://www.magnus.nl',
    'author': 'Magnus - Willem Hulshof',
    'depends': [
        'base',
        'account',
        ],
    'data': [
        "views/mass_mail_view.xml",
        "views/res_partner_view.xml"
    ],
    'installable': True
}