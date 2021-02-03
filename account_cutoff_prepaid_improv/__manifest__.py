# -*- coding: utf-8 -*-
# © 2013-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# © 2018 Magnus (Willem Hulshof <w.hulshof@magnus.nl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Cut-off Prepaid SQL',
    'version': '10.0.1.0.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Prepaid Expense, Prepaid Revenue',
    'author': 'Magnus',
    'website': 'http://www.magnus.nl',
    'depends': [
        'account_cutoff_prepaid',
        'account',
        'account_cutoff_base_operating_unit',
        'queue_job'
        ],
    'data': [
        'views/account_config_settings.xml'
    ],
    'images': [
        ],
    'installable': True,
}
