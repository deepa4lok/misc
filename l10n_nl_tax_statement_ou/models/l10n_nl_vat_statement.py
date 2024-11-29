from odoo import api, fields, models, _

class VatStatement(models.Model):
    _inherit = 'l10n.nl.vat.statement'

    operating_unit_id = fields.Many2one(
        'operating.unit', 'Operating Unit',
        default=lambda self: self.env['res.users'].operating_unit_default_get(),
    )

    def _with_ou_domain(self, domain):
        """
        Add an OU clause if an operating unit is set
        """
        return domain + ([
            '|',
            ('operating_unit_id', '=', self.operating_unit_id.id),
            ('operating_unit_id', '=', False),
        ] if self.operating_unit_id else [])

    def _init_move_line_domain(self):
        return self._with_ou_domain(super()._init_move_line_domain())

    def _get_unreported_move_domain(self):
        return self._with_ou_domain(super()._get_unreported_move_domain())

    def _domain_check_prev_open_statements(self):
        return self._with_ou_domain(super()._domain_check_prev_open_statements())

    def _get_move_lines_domain(self):
        return self._with_ou_domain(super()._get_move_lines_domain())
