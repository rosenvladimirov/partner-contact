# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _

class ResourceCalendar(models.Model):

    speedy_work_days = fields.Char('Speedy ServingDays', size=7)
