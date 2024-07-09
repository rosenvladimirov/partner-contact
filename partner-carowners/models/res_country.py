# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from .seedy_parcer import ADDRESS_1

class CountryState(models.Model):
    _inherit = 'res.country'

    post_require = fields.Boolean("Post code is required")
    speedy_nom = fields.Selection(ADDRESS_1.speedy_nom[2], string=ADDRESS_1.speedy_nom[0], help=ADDRESS_1.speedy_nom[1])


