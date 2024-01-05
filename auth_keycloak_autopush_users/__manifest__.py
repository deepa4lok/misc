# -*- coding: utf-8 -*-


{
    "name": "Auto-Push Users to Keycloak",
    "summary": "Auto-push Portal user to Keycloak",
    "version": "16.0.1.0",
    'category': 'Tools',
    'website' : "https://www.tosc.nl/",
    "author": "Deepa, " "The Open Source company (TOSC)",
    "license": "LGPL-3",
    "depends": [
        "auth_signup",
        "auth_keycloak",
    ],
    "data": [
        "views/auth_oauth.xml"
    ],
}