#  Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from polyglot.downloader import downloader

from odoo import models
from .models.res_transliterate import partner_name_translate

from .odoo.models import regex_order

_logger = logging.getLogger(__name__)


def pre_init_hook(env):
    downloader.download("TASK:transliteration2", quiet=True)


def post_init_hook(env):
    languages = downloader._packages
    for lang in env['res.lang'].with_context(active_test=False).search([]):
        if f"transliteration2.{lang.code[:2]}" in languages:
            lang.transliterate = True

    languages = env['res.lang'].search([('code', '!=', 'en_US')])
    partners = env['res.partner'].search([])
    for partner_id in partners:
        text = partner_id.name
        if not text:
            continue

        for lang in languages:
            _logger.info(f"Partner {text} to {lang.code}")
            partner_id.with_context(lang=lang.code).name = text
            partner_id.with_context(lang="en_US").name = partner_name_translate(text, lang.code[:2], lang.transliterate)


def post_load_hook():
    models.regex_order = regex_order
