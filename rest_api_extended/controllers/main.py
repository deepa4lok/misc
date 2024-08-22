# -*- coding: utf-8 -*-
# Copyright (C) 2024 The Open Source Company (<https://www.tosc.nl>)

import odoo
from odoo.addons.rest_api.controllers import main
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)


def get_analytic_accountID(aa_code):
    aaObj = request.env['account.analytic.account']
    aaID = aaObj.sudo().search([('code', '=', aa_code)], limit=1)
    aaID = aaID and aaID.id or False
    return aaID


def convert_values_from_jdata_to_vals1(modelname, jdata, creating=True):
    cr, uid = request.cr, request.session.uid
    Model = request.env(cr, uid)[modelname]

    x2m_fields = [f for f in jdata if type(jdata[f]) == list]
    f_props = Model.fields_get(x2m_fields)

    vals = {}
    for field in jdata:
        val = jdata[field]
        if type(val) != list:
            if field == 'account_analytic_code':
                vals['account_analytic_id'] = get_analytic_accountID(val)
            else:
                vals[field] = val
        else:
            # x2many
            #
            # Sample for One2many field:
            # 'bank_ids': [{'acc_number': '12345', 'bank_bic': '6789'}, {'acc_number': '54321', 'bank_bic': '9876'}]
            vals[field] = []
            field_type = f_props[field]['type']
            # if updating of 'many2many'
            if (not creating) and (field_type == 'many2many'):
                # unlink all previous 'ids'
                vals[field].append((5,))

            for jrec in val:
                rec = {}
                for f in jrec:
                    if f == 'account_analytic_code':
                        rec['account_analytic_id'] = get_analytic_accountID(jrec[f])
                    else:
                        rec[f] = jrec[f]

                if field_type == 'one2many':
                    if creating:
                        vals[field].append((0, 0, rec))
                    else:
                        if 'id' in rec:
                            id = rec['id']
                            del rec['id']
                            if len(rec):
                                # update record
                                vals[field].append((1, id, rec))
                            else:
                                # remove record
                                vals[field].append((2, id))
                        else:
                            # create record
                            vals[field].append((0, 0, rec))

                elif field_type == 'many2many':
                    # link current existing 'id'
                    vals[field].append((4, rec['id']))
    return vals

#Overridden:
main.convert_values_from_jdata_to_vals = convert_values_from_jdata_to_vals1

