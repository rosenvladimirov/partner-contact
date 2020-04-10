# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Delivery Carrier-Speedy Bulgaria',
    'version': '1.0',
    'category': 'Stock',
    'sequence': 5,
    'description': """
""",
    'depends': [
            'base',
            'delivery',
            'base_address_extended',
            'l10n_bg_extend',
            ],
    'data': [
        'data/speedy_res_partner_data.xml',
        'security/delivery_speedy_security.xml',
        'security/ir.model.access.csv',
        'views/delivery_speedy_view.xml',
        'views/base_address_extended.xml',
        'views/speedy_views.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
