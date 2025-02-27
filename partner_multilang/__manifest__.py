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
    "description": """
        Multilang partner names.
    """,
    'external_dependencies': {
        'python': [
            'polyglot',
            'numpy==1.24.4',
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
    "post_load": "post_load_hook",  # Reported with PR https://github.com/odoo/odoo/pull/174499
}
