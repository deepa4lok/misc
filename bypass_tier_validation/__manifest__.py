# -*- coding: utf-8 -*-
{
    'name': "By-Pass Tier Validation",

    'summary': """
        By-Pass Tier Validation for account move""",

    'description': """
        By-Pass Tier Validation for account move
    """,

    'author': "K.Sushma, " "The Open Source company (TOSC)",
    'website': "https://tosc.nl",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    "version": "14.0.0.0.0",
    "license": "AGPL-3",

    # any module necessary for this one to work correctly
    'depends': ['account_move_tier_validation'],

    # always loaded
    'data': [
        'security/groups.xml',
        # 'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
