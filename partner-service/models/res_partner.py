# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _

import logging
_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = 'res.partner'

    def _get_hiden_category_ids(self):
        return [self.env.ref('partner-service.res_partner_services').id]

    hide_category = fields.Boolean("Is Car Service", compute="_compute_service_partner", search="_value_search")

    @api.one
    @api.depends('category_id')
    def _compute_service_partner(self):
        self.hide_category = self.category_id in self._get_hiden_category_ids()

    @api.multi
    def _value_search(self, operator, value):
        if operator == "=" and value:
            operator = "in"
        elif operator == "=" and not value:
            operator = "not in"
        return [('category_id', operator, self._get_hiden_category_ids())]

