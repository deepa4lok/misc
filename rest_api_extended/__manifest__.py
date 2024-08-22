# -*- coding: utf-8 -*-
# Copyright (C) 2024 The Open Source Company (<https://www.tosc.nl>)

{
    "name": "Rest API - Extended",
    "version": "10.0.2.0",
    "author": "Deepa Venkatesh (DK), The Open Source Company (TOSC)",
    "license": "AGPL-3",
    "website": "www.tosc.nl",
    "summary": "This app supports accepting of Analytic Ref ",
    "description": '''
Description
-----------
This app accepts Analytic Account Code/Ref sent as 'account_analytic_code', & then finds & updates with Analytic Account 'account_analytic_id'.
''',
    "category": "Other",
    "depends": [
        'rest_api',
    ],
    "data": [],
    "qweb":[],
    "auto_install": False,
    "installable": True,
    "application": False,
    "external_dependencies": {
        'python': [],
    },
}
