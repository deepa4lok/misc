{
    'name': 'Helpdesk SLA',
    'version': '1.0',
    'summary': 'Add ticket priority field to helpdesk tickets and manage SLAs',
    'description': 'This module adds a priority field to helpdesk tickets and provides a way to manage SLAs.',
    'author': 'The Open Source Company',
    'category': 'Helpdesk',
    'depends': ['helpdesk_mgmt'],
    'data': [
        'views/menuitem.xml',
        'views/helpdesk_ticket_views.xml',
        'views/helpdesk_sla_views.xml',
        'views/sla_line_views.xml',
        'data/ir_cron_data.xml',
    ],
    'installable': True,
    'application': False,
}
