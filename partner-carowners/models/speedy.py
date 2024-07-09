# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from .speedy_parcer import *

class SeedyOffices(models.Model):
    _name = 'speedy.res.partner.offices'
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Speedy offices by country'


    partner_id = fields.Many2one("res.partner", "Partner", required=True, ondelete='cascade', auto_join=True)
    #display_name = fields.Char(compute='_compute_display_name', search='_name_search_ext', store=False, index=False)

    #customer = fields.Boolean(string='Is a Customer', related="partner_id.customer",
    #                           help="Check this box if this contact is a customer.")
    #supplier = fields.Boolean(string='Is a Vendor', related="partner_id.supplier",
    #                           help="Check this box if this contact is a vendor. "
    #                           "If it's not checked, purchase people will not see it when encoding a purchase order.")

    speedy_office_id = fields.Integer("Office ID")
    nearbyOfficeId = fields.Integer("Nearby office ID")

    typeid = fields.Integer("Courier service type ID")
    officeType = fields.Integer("Office type: 0 - Speedy office, 3 - APT")

    #name = fields.Char("Courier service name")
    siteId = fields.Integer("Serving site ID")
    allowanceFixedTimeDelivery = fields.Selection(COMPLEMENTARYSERVICEALLOWANCE, string="Fixed time for delivery", help="Specifies if the complementary service 'Fixed time for delivery' is banned, allowed or required")
    allowanceCashOnDelivery = fields.Selection(COMPLEMENTARYSERVICEALLOWANCE, string="Cash On Delivery", help="Specifies if the complementary service 'COD' is banned, allowed or required")
    allowanceInsurance = fields.Selection(COMPLEMENTARYSERVICEALLOWANCE, string="Insurance", help="Specifies if the complementary service 'Insurance' is banned, allowed or required")
    allowanceBackDocumentsRequest = fields.Selection(COMPLEMENTARYSERVICEALLOWANCE, string="Return Documents", speedy="Specifies if the complementary service 'Return documents' is banned, allowed or required")
    allowanceBackReceiptRequest = fields.Selection(COMPLEMENTARYSERVICEALLOWANCE, string="Return Receipt", help="Specifies if the complementary service 'Return receipt' is banned, allowed or required")
    allowanceToBeCalled = fields.Selection(COMPLEMENTARYSERVICEALLOWANCE, string="To be called", help="Specifies if the complementary service 'To be called' is banned, allowed or required")
    allowanceDeliveryToFloor = fields.Selection(COMPLEMENTARYSERVICEALLOWANCE, string="Delivery to floor", help="Specifies if the complementary service 'Delivery to floor' is banned, allowed or required")
    allowanceOptionsBeforePayment = fields.Selection(COMPLEMENTARYSERVICEALLOWANCE, string="Options before payment", help="Specifies if the complementary service 'Options Before Payment' is banned, allowed or required")
    allowanceReturnVoucher = fields.Selection(COMPLEMENTARYSERVICEALLOWANCE, string="Return Voucher", help="Specifies if the complementary service 'Return Voucher' is banned, allowed or required")

    deliveryDeadline = fields.Datetime("The deadline for shipment delivery")

    cargoType = fields.Selection(CARGOTYPE, size=1, string="Cargo Type (1 - CARGO_TYPE_PARCEL, 2 - CARGO_TYPE_PALLET)")

    maxParcelDimensions = fields.Many2one("speedy.parcel.dimensions", string="Max parcel dimensions")
    maxParcelWeight = fields.Integer("Max parcel weight for office")

    workingTimeSchedule = fields.Many2one("resource.calendar", string="Working time schedule for the office")

    requireParcelsData = fields.Boolean("Shows if parcels require weight and size description")

    # hack to allow using plain browse record in qweb views, and used in ir.qweb.field.contact
    self = fields.Many2one(comodel_name=_name, compute='_compute_get_ids')

    #@api.one
    #def _name_search_ext(self, operator, value):
    #    return self.partner_id._name_search_ext(operator, value)

    #@api.one
    #@api.depends('is_company', 'name', 'parent_id.name', 'type', 'company_name')
    #def _compute_display_name(self):
    #    self.partner_id._compute_display_name()

    @api.model
    def _fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        if (not view_id) and (view_type == 'form') and self._context.get('force_email'):
            view_id = self.env.ref('delivery_speedy.speedy_view_partner_simple_form').id
        res = super(SeedyOffices, self)._fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            res['arch'] = self.partner_id._fields_view_get_address(res['arch'])
        return res

    @api.one
    def _compute_get_ids(self):
        self.self = self.id

class SpeedyParcelDimension(models.Model):
    _name = 'speedy.parcel.dimensions'
    _description = 'Speedy Max Parcel Dimensions'

    width = fields.Integer("Width (cm)")
    height = fields.Integer("Height (cm)")
    dept = fields.Integer("Dept (cm)")

#class SpeedyWorkingTime(model.Models):
#    _name = 'speedy.working.time'
#    _description = 'Speedy Office Working Time'
#
#    date = fields.Date("Working time date")
#    workingTimeException = fields.bool("Shows whether the office working time is overriden")
#    workingTimeFrom = fields.Integer("Working time - FROM")
#    workingTimeTo = fields.Integer("Working time - TO")

