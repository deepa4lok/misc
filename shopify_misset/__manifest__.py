# -*- coding: utf-8 -*-


{
    "name": "Shopify for Misset",
    "summary": "Shopify improvements for Misset",
    "version": "10.0.3.5",
    'category': 'Tools',
    'website' : "https://www.tosc.nl/",
    "author": "Deepa, " "The Open Source company (TOSC)",
    "license": "LGPL-3",
    "depends": [
        "shopify_odoo_bridge",
        "odoo_multi_channel_sale",
        "account_payment_partner", "account",
        "sale", "sale_operating_unit", "account_payment_sale",
    ],
    "data": [
        "views/multi_channel_sale.xml",
        "views/sale_order.xml",
    ],
}

