# Copyright <2020> PESOL <info@pesol.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import _, api, fields, models
# from odoo.exceptions import ValidationError


class TierValidation(models.AbstractModel):
    _inherit = "tier.validation"

    def _check_allow_write_under_validation(self, vals):
        """Allow to add exceptions for fields that are allowed to be written
        even when the record is under validation."""

        if self.env.user.has_group('bypass_tier_validation.group_bypass_tier_validation'):
            return True
        exceptions = self._get_under_validation_exceptions()
        for val in vals:
            if val not in exceptions:
                return False
        return True
