# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, an open source suite of business apps
#    This module copyright (C) 2013-2015 Therp BV (<http://therp.nl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Street name, number and extension',
    'summary': 'Introduces separate field for extension after street and number.',
    'version': '10.0.1.0.0',
    'author': 'TOSC,Odoo Community Association (OCA)',
    'website': 'https://github.com/magnuscolors/misc',
    'category': 'Tools',
    'depends': [
        'base',
        'web',
        # 'partner_street_number'
        ],
    'data': [
        'views/res_partner.xml',
        # 'views/assets.xml',
        ],
    'installable': True,
    'license': 'AGPL-3',
#    'post_init_hook': 'post_init_hook',
}
