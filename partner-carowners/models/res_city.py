# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class City(models.Model):
    _inherit = 'res.city'

    speedy_site_id = fields.Integer("Speedy Cite ID")
    speedy_nom = fields.Selection([('0', 'Speedy has no site nomenclature for this country.'),
             ('1', 'Speedy has full site nomenclature for this country.'),
             ('2', 'Speedy has partial site nomenclature for this country.'),]
                string="Speedy Type Service")
    speedy_service_office_id = fields.Integer('Speedy Service ID')
    speedy_hub_office_id =  fields.Integer('Speedy Hub ID')
    speedy_resource_calendar_id = fields.Many2one('resource.calendar', 'Working Schedule')

    def _get_speedy_data(self):
        #background-image: url('https://www.speedy.bg/web/images/logo.png');
        #background-size: contain;


class StreetCity(models.Model):
    _inherit = 'res.city.street'


    speedy_site_id = fields.Integer("Speedy Cite ID")
    speedy_street_id = fields.Integer("Speedy Cite ID", index=True)

