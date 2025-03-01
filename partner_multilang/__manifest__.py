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
    "external_dependencies": {
        "python": [
            "cyrtranslit",
        ]
    },
    "depends": [
        "base",
        "contacts",
    ],
    "data": [
        "views/res_lang_views.xml",
    ],
    "demo": [],
    "installable": True,
    "post_init_hook": "post_init_hook",
    "post_load": "post_load_hook",
}
