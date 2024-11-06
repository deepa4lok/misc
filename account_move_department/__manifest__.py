{
    'name': 'Account Move Department',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Adds department field to account move form',
    'depends': ['account', 'hr'],
    'data': [
        'views/account_move_view.xml',
    ],
    'installable': True,
    'application': False,
}
