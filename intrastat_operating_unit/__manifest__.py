# -*- coding: utf-8 -*-
{
    'name': "Intra-Community transactions declaration (ICP)-Operating Unit",

    'summary': """
        Operating Unit for ICP""",

    'description': """
        Operating Unit for ICP
    """,

    'author': "Willem Hulshof",
    'website': "www.tosc.nl",

    'category': 'Accounting',
    'version': '0.1',

    'depends': ['l10n_nl_tax_statement_icp'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/l10n_nl_intrastat.xml',
        'views/l10n_nl_intrastat.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable':True,

    # l10n_nl_intrastat is not available in odoo12
}