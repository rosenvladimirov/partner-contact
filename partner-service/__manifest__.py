# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Partner Car Services',
    'version': '1.0',
    'category': 'Stock',
    'sequence': 99,
    'description': """
""",
    'depends': [
            'base',
            'base_address_extended',
            'l10n_bg_extend',
            'product',
            'fleet_extend',
            ],
    'data': [
        'security/services_res_partner_security.xml',
        'security/ir.model.access.csv',
        'views/services_res_partner_views.xml',
        'views/base_address_extended.xml',
        'views/service_views.xml',
        'views/service_equipment.xml',

    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
