# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT



class AccountMove(models.Model):
    _inherit = "account.move"

    def create_reversal_moveline_with_query(self, data):
        
        #  Create move
        
        if self.operating_unit_id.id==False:
            operating_unit_id='NULL'
        else:
            operating_unit_id=self.operating_unit_id.id
        
        if self.reversal_id.id==False:
            reversal_id='NULL'
        else:
            reversal_id=self.reversal_id.id
        
        data.update({'name': "/",
         'state': "draft",
         'create_date': datetime.now(),
         'create_uid': self._uid,
         'write_date': datetime.now(),
         'write_uid': self._uid,
         'company_id': self.env.user.company_id.id,
         'currency_id': self.env.user.company_id.currency_id and self.env.user.company_id.currency_id.id,
         'matched_percentage': 0.0,
         'to_be_reversed': False,
         'operating_unit_id':operating_unit_id,
         'reversal_id':reversal_id,
         'move_type':'other'       
         })

        cr = self._cr
        sql = "INSERT INTO account_move (ref,narration,operating_unit_id," \
              "reversal_id, date,journal_id, name, state, create_date, create_uid, write_date, write_uid," \
              " company_id, currency_id,move_type,matched_percentage, to_be_reversed) " \
              "VALUES ('%(ref)s','%(narration)s',%(operating_unit_id)s,%(reversal_id)s,'%(date)s'::date," \
              "%(journal_id)s,'%(name)s', '%(state)s', '%(create_date)s', %(create_uid)s, '%(write_date)s', %(write_uid)s," \
              " %(company_id)s, %(currency_id)s,'%(move_type)s',%(matched_percentage)s, %(to_be_reversed)s);" % data
        cr.execute(sql)
        sql = 'select id from account_move order by id desc limit 1'
        cr.execute(sql)
        move_id = cr.fetchone()[0]
        move=self.env['account.move'].browse([move_id])[0]
        
       
        # Create move line       
        
        sql_query = ("""
                    INSERT INTO account_move_line (
                            create_date,
                            partner_bank_id,
                            partner_id,
                            ref,
                            user_type_id,
                            journal_id,
                            currency_id,
                            date_maturity,
                            blocked,
                            analytic_account_id,
                            payment_mode_id,
                            l10n_nl_date_invoice,
                            start_date,
                            end_date,
                            operating_unit_id,
                            product_id,
                            tax_line_id,
                            product_uom_id,
                            create_uid,                            
                            credit,
                            account_id,
                            invoice_id,
                            bank_payment_line_id,                            
                            tax_exigible,
                            credit_cash_basis,
                            debit_cash_basis,
                            balance_cash_basis,
                            write_date,
                            date,
                            write_uid,
                            move_id,
                            name,
                            debit,
                            amount_currency,
                            quantity,
                            company_currency_id,
                            balance,
                            company_id
                            )
                    SELECT
                            create_date,
                            partner_bank_id,
                            ref,
                            user_type_id,
                            journal_id,
                            currency_id,
                            date_maturity,
                            blocked,
                            analytic_account_id,
                            payment_mode_id,
                            l10n_nl_date_invoice,
                            start_date,
                            end_date,                            
                            operating_unit_id,
                            product_id,
                            tax_line_id,
                            product_uom_id,
                            create_uid,                        
                            debit,
                            account_id,
                            invoice_id,
                            bank_payment_line_id,
                            tax_exigible,
                            credit_cash_basis,
                            debit_cash_basis,
                            balance_cash_basis,
                            write_date,
                            date,
                            write_uid,
                            {0} AS move_id,
                            name,
                            credit,
                            amount_currency,
                            quantity,
                            company_currency_id,
                            balance,
                            company_id
                    FROM account_move_line
                    WHERE move_id={1} AND NOT (debit=0 AND credit=0);
        """.format(                 
                   move_id,
                   self.id                 
                   ))
        cr.execute(sql_query)
        return move
    
    
    def create_reversals(self, date=False, journal=False, move_prefix=False,
                         line_prefix=False, reconcile=False):
        
        moves = self.env['account.move']
        
        for orig in self:
            data = orig._move_reverse_prepare(
                date=date, journal=journal, move_prefix=move_prefix)
            data = orig._move_lines_reverse_prepare(
                data, date=date, journal=journal, line_prefix=line_prefix)
            if self.env.user.company_id.reversal_via_sql:
                # Create account move and lines using query
                reversal_move = self.create_reversal_moveline_with_query(data)
            else: 
                # Create account move and lines using ORM           
                reversal_move = self.create(data)
            moves |= reversal_move
            orig.write({
                'reversal_id': reversal_move.id,
                'to_be_reversed': False,
            })
        if moves:
            moves._post_validate()
            moves.post()
            if reconcile:
                orig.move_reverse_reconcile()
        return moves
    
   
