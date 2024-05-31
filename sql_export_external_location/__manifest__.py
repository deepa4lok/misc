# -*- coding: utf-8 -*-
{
    'name': "SQL Export - External Location",

    'summary': """
        Sends Report exported from SQL Extract via FTP Server
                """,

    'description': """
        Sends Report exported from SQL Extract Module via FTP Server
    """,

    'author'  : "TOSC",
    'website' : "https://www.tosc.nl/",
    'license' : "LGPL-3", 
    'category': 'SQL Export',
    'version' : '10.0.3',
    'depends' : ['sql_export'
                ],
    'data'    : [
                 'security/ir.model.access.csv',
                 'views/ftp_config.xml'
                ],
    'demo'    : [
                ],
}