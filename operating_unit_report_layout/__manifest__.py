# Copyright 2018 Willem Hulshof TOSC (www.tosc.nl).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "Operating Unit Report Layout",

    'summary': "This module creates basic layouts for reports.",

    'author': "TOSC",
    'website': "http://www.tosc.nl",
    'category': 'accounts',
    'version': '16.0.1.0.0',
    'depends': ['operating_unit'],

    'data': [
        'views/operating_unit_view.xml',
        'data/report_paperformat.xml',
    ],
    
    'assets': {
        'web.report_assets_common': [
            '/operating_unit_report_layout/static/src/css/operating_unit_report_layout.scss',
        ],
    }
}
