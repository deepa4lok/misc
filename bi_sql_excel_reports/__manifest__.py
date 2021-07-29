# -*- coding: utf-8 -*-
# Copyright (C) 2021 - Today: Magnus (http://www.magnus.nl)
# @author: Vincent Verheul (v.verheul@magnus.nl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "BI SQL Excel Reports",
    "summary": "Pull SQL reports, defined in Odoo from within Excel, using the Excel add-in and this module to define the pivot layout.",
    "version": "10.0.1.1.0",
    "author": "Magnus",
    "website": "https://www.magnus.nl/",
    "license": "AGPL-3",
    "category": "Reporting",
    "depends": [
        "bi_sql_editor"
    ],
    "data": [
	    'views/view_bi_excel_report.xml', 
    ],
    'installable': True,
    'external_dependencies': {
        'python': [
        ],
    },
}
