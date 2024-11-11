{
    'name': 'Account Move Department',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Adds sales team field to account move form',
    'depends': ['account', 'sales_team'],
    'data': [
        'views/account_move_view.xml',
    ],
    'installable': True,
    'application': False,
}
