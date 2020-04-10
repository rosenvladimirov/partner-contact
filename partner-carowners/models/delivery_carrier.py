# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import psycopg2

from odoo import api, fields, models, registry, SUPERUSER_ID, _

_logger = logging.getLogger(__name__)

from .speedy_request import SpeedyRequest
from .speedy_parcer import *

class DeliveryCarrierBGSpeedy(models.Model):
    _inherit = 'delivery.carrier'
    _description = "Carrier Speedy Bulgaria"

    ''' A Shipping Provider

    In order to add your own external provider, follow these steps:

    1. Create your model MyProvider that _inherit 'delivery.carrier'
    2. Extend the selection of the field "delivery_type" with a pair
       ('<my_provider>', 'My Provider')
    3. Add your methods:
       <my_provider>_rate_shipment
       <my_provider>_send_shipping
       <my_provider>_get_tracking_link
       <my_provider>_cancel_shipment
       (they are documented hereunder)
    '''

    delivery_type = fields.Selection(selection_add=[('bgspeedy', 'Speedy Bulgaria')])
    bgspeedy_account_number = fields.Char("User name", help="""
To get a test account please send us an e-mail to eps.registration@speedy.bg and provide the following info:

    Name
    Company name
    Direct Phone number
    Skype Name (if available)

        """,
        groups="base.group_system")
    bgspeedy_password = fields.Char("Password for Access", groups="base.group_system")
    bgspeedy_client_id = fields.Integer("Client ID in Speedy", help="Fill your client id from the speedy information system.")

    def bgspeedy_rate_shipment(self):
        pass

    def bgspeedy_send_shipping(self):
        pass

    def bgspeedy_get_tracking_link(self):
        pass

    def bgseepdy_cancel_shipment(self):
        pass
