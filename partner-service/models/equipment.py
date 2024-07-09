# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _

class ServiceEquipment(models.Model):
    _name = 'services.equipment'
    _description = 'Equipment'

    name = fields.Char("Name")
    code = fields.Char("Code")
    description = fields.Text("Description")

    product_id = fields.Many2one("product.product", "Product")
    partner_id = fields.Many2one(comodel_name="services.res.partner")
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('services.equipment'))
