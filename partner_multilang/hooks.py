#  Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import cyrtranslit

from odoo import models
from .models.res_transliterate import partner_name_translate

from .odoo.models import regex_order

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    languages = cyrtranslit.supported()
    for lang in env['res.lang'].with_context(active_test=False).search([]):
        if f"{lang.code[:2]}" in languages:
            lang.transliterate = True

    languages = env['res.lang'].search([('code', '!=', 'en_US')])
    partners = env['res.partner'].search([])
    for partner_id in partners:
        text = partner_id.name
        if not text:
            continue

        for lang in languages:
            if lang.code == 'en_US':
                continue
            transliterate_lang = partner_name_translate(text, lang.code[:2], lang.transliterate)
            _logger.info(f"Partner {text} => {transliterate_lang} The {lang.code} and is a transliterate language: {lang.transliterate}")
            # partner_id.with_context(lang=lang.code).name = text
            partner_id.with_context(lang="en_US").name = transliterate_lang


def post_load_hook():
    models.regex_order = regex_order
