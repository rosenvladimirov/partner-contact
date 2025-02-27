#  Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import os
import shutil

from polyglot.downloader import downloader

from odoo import models, addons
from odoo.tools import config
from .models.res_transliterate import partner_name_translate

from .odoo.models import regex_order

_logger = logging.getLogger(__name__)


def pre_init_hook(env):
    try:
        downloader.download("TASK:transliteration2", quiet=True)
    except Exception as e:
        _logger.info(f"An error occurred while download transliteration2: {e}")
        module = __name__.split("addons.")[1].split(".")[0]
        module_path = ""
        for adp in addons.__path__:
            module_path = adp + os.sep + module
            if os.path.isdir(module_path):
                break
        module_path += os.sep + "lib"
        module_path += os.sep + "polyglot_data"
        data_dir = config.get('data_dir', '/var/lib/odoo')
        data_dir = os.path.join(data_dir, 'polyglot_data')
        try:
            shutil.copytree(module_path, data_dir)
            _logger.info(f"Successfully copied folder: {module_path} -> {data_dir}")
        except FileExistsError:
            _logger.warning(f"Error: The target folder '{data_dir}' already exists.")
        except Exception as e:
            print(f"An error occurred while copying: {e}")


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
