#  Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, SUPERUSER_ID
from polyglot.downloader import downloader


def _get_lang_sorted(lang):
    return


def pre_init_hook(env):
    downloader.download("TASK:transliteration2", quiet=True)


def post_init_hook(env):
    languages = downloader._packages
    for lang in env['res.lang'].search([]):
        if f"transliteration2.{lang.code[:2]}" in languages:
            lang.transliterate = True

    languages = env['res.lang'].with_context(active_test=False).search([('code', '!=', 'en_US')])
    for partner_id in env['res.partner'].search([]):
        for lang in languages:
            partner_id.with_context(**dict(partner_id._context, lang=lang)). \
                _force_multilanguage(partner_id, {'name': partner_id.name}, new_record=True)
