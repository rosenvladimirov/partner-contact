# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _

class PartnerService(models.Model):
    _name = 'services.res.partner'
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Car Service Partners'


    partner_id = fields.Many2one("res.partner", "Partner", required=True, ondelete='cascade', auto_join=True)

#    lines = fields.One2many("services.equipment", "code")

    service_brand_ids = fields.Many2many("product.brand", string="Service Brand")
    service_equipment_ids = fields.Many2one("services.equipment", string="Available Equipment")
    vehicle_ids = fields.Many2many(comodel_name="fleet.vehicle", relation="rel_fleet_vehicle_to_service_res_partner", column1="vehicle_id", column2="service_id")


    # hack to allow using plain browse record in qweb views, and used in ir.qweb.field.contact
    self = fields.Many2one(comodel_name=_name, compute='_compute_get_ids')

    @api.model
    def _fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        if (not view_id) and (view_type == 'form') and self._context.get('force_email'):
            view_id = self.env.ref('partner.service.service_view_partner_simple_form').id
        res = super(PartnerService, self)._fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            res['arch'] = self.partner_id._fields_view_get_address(res['arch'])
        return res

    @api.one
    def _compute_get_ids(self):
        self.self = self.id

