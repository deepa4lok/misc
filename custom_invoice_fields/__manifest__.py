{
    'name': 'Custom Invoice Fields',
    'version': '1.0',
    'summary': 'Add Mileage and License Plate fields to invoices',
    'category': 'Accounting',
    'author': 'Your Name',
    'depends': ['account'],
    'data': [
        'views/account_move_views.xml',
        'report/account_invoice_report.xml',
    ],
    'installable': True,
    'application': False,
}
