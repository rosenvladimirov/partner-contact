# Copyright 2023 Rosen Vladimirov
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Partner Multilang",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "category": "Localization",
    "complexity": "normal",
    "author": "Rosen Vladimirov,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    'external_dependencies': {
        'python': [
            'polyglot',
            'numpy',
            'pycld2',
            'morfessor',
            'pyicu',
        ]
    },
    "depends": [
        "base",
    ],
    "data": [
        'views/res_lang_views.xml',
    ],
    "demo": [],
    "installable": True,
    "pre_init_hook": "pre_init_hook",
    "post_init_hook": "post_init_hook",
}
