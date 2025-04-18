#  Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

import cyrtranslit
from langdetect import detect
from lxml import etree

from odoo import api, models

_logger = logging.getLogger(__name__)
TRANSLITERATE_FIELDS = ['name', 'company_name',
                        'city', 'street', 'street2',
                        'private_city', 'private_street', 'private_street2']

def partner_name_translate(name, lang, transliterate):
    if lang not in ["en", "en_US"] and transliterate:
        return cyrtranslit.to_latin(name, lang[:2])
    return name


class ResTransliterate(models.AbstractModel):
    _name = "res.transliterate.mixin"
    _description = "Names transliterate mixin"

    @api.depends_context('lang')
    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        lang_order = f"name->>'{self.env.user.lang}'"
        result = super(ResTransliterate, self).get_view(
            view_id=view_id, view_type=view_type, **options
        )
        value_fields = self.fields_get()
        if value_fields.get('name') and value_fields['name']['type'] == 'char' \
                and not value_fields['name'].get('related') and view_type in ["tree", "kanban"]:
            doc = etree.XML(result["arch"])
            for type_in in ["tree", "kanban"]:
                for node in doc.xpath(f"//{type_in}"):
                    node.set("default_order", lang_order)
            result["arch"] = etree.tostring(doc, encoding="unicode")
        return result

    def _get_transliterate_languages(self):
        return self.env['res.lang'].search([('transliterate', '=', True)])

    def _get_code_lang(self, code):
        return self.env['res.lang'].search([('iso_code', '=', code)])

    def _check_lang(self, text):
        current_lang = lang = self.env.user.lang
        installed_langs = self._get_transliterate_languages()
        transliterate = installed_langs.filtered(lambda r: r.code == lang)
        # if text and lang == 'en_US':
        #     detect_lang = detect(text)
        #     lang = self._get_code_lang(detect_lang).code
        #     if not lang:
        #         lang = current_lang
        # _logger.info(f"LANG: {lang} {current_lang} {text} {self.name}")
        return current_lang, transliterate

    @api.depends_context('lang')
    def _force_multilanguage(self, vals, new_record=False):
        for field_name in [x for x in TRANSLITERATE_FIELDS if x in self._fields.keys()]:
            if field_name not in self._fields.keys():
                continue
            if vals.get(field_name) and new_record:
                current_lang, transliterate = self._check_lang(vals[field_name])
                # Save in user lang
                record = self.with_context(**dict(self._context, lang=current_lang, update_lang=True))
                record.write({
                  field_name: vals[field_name],
                })
                # if transliterate save transliterated
                if transliterate and current_lang != "en_US":
                    record = self.with_context(**dict(self._context, lang="en_US", update_lang=True))
                    record.write({
                        field_name: partner_name_translate(vals[field_name], current_lang, transliterate)
                    })

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for record, vals in zip(res, vals_list):
            record._force_multilanguage(vals, new_record=True)
        return res

    def write(self, vals):
        res = super().write(vals)
        if not self._context.get('update_lang', False):
            for record in self:
                for field_name in [x for x in TRANSLITERATE_FIELDS if x in self._fields.keys()]:
                    if not getattr(record, field_name):
                        record._force_multilanguage(vals, True)
        return res
