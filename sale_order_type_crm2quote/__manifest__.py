# -*- coding: utf-8 -*-
# Copyright (C) 2024 The Open Source Company (<https://www.tosc.nl>)

{
    "name": "Sale Order Type Crm2Quote",
    "version": "16.0.0.0",
    "author": "Deepa Venkatesh (DK), The Open Source Company (TOSC)",
    "license": "AGPL-3",
    "website": "www.tosc.nl",
    "summary": "This app prompts the user to choose Sale Order type during conversion of Lead to Quotation.",
    "description": '''
Description
-----------
This app prompts the user to choose Sale Order type during conversion of Lead to Quotation.

USAGE
============
* configure corresponding Action in Sale Order Type form (Sales > Configuration > Sale Order Types).

''',
    "category": "CRM",
    "depends": [
        'sale_order_type',
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/crm_lead_to_quote_view.xml",
    ],
    "qweb":[],
    "auto_install": False,
    "installable": True,
    "application": False,
    "external_dependencies": {
        'python': [],
    },
}
