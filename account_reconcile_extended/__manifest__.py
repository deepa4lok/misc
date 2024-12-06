# -*- coding: utf-8 -*-
{
    'name': "account_reconcile_extended",

    'summary': """
        Account Reconcile Extended""",

    'description': """
        Account Reconcile Extended
    """,

    'author': "K.Sushma-TOSC",
    'website': "https://www.tosc.nl",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '16.0.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['account','account_reconcile_oca'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
