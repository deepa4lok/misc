# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2018 Magnus (<http://magnus.nl>).
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
    'name': 'import provinces not installed by l10n_nl_postcodeapi',
    'images': [],
    'summary': 'Import Provinces used by PostcodeApi.nu',
    'version': '10.0.0.1.0',
    'author': 'TOSC',
    'category': 'Localization',
    'website': 'https://github.com/magnuscolors/misc',
    'license': 'AGPL-3',
    'depends': ['l10n_nl_postcodeapi'],
    'data': [
        # 'data/res.country.state.csv',
        ],
    'external_dependencies': {
    },
    'installable': True,
}
