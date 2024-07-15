{
    'name': 'Helpdesk SLA',
    'version': '1.0',
    'summary': 'Add ticket priority field to helpdesk tickets and manage SLAs',
    'description': 'This module provides a way to manage SLAs for helpdesk tickets.',
    'author': 'The Open Source Company',
    'category': 'Helpdesk',
    'depends': ['helpdesk_mgmt'],
    'data': [
        'views/helpdesk_ticket_views.xml',
        'views/helpdesk_sla_views.xml',
        'views/sla_line_views.xml',
        'data/ir_cron_data.xml',
    ],
    'installable': True,
    'application': False,
}
