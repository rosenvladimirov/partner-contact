#  Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from lxml import etree
from polyglot.transliteration import Transliterator

from odoo import api, models
from polyglot.text import Text

_logger = logging.getLogger(__name__)


def partner_name_translate(name, lang, transliterate):
    if lang != "en_US" and transliterate:
        transliterator = Transliterator(source_lang=lang[:2], target_lang="en")
        text_to_letters = list(name)
        text_from_letters = []
        for letter in text_to_letters:
            if ' ' in letter:
                text_from_letters.append(letter)
                continue
            letter_transliterate = transliterator.transliterate(letter)
            text_from_letters.append(letter.isupper() and letter_transliterate.upper() or letter_transliterate)
        return "".join(text_from_letters)
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
        if view_type in ["tree", "kanban"]:
            doc = etree.XML(result["arch"])
            for type_in in ["tree", "kanban"]:
                for node in doc.xpath(f"//{type_in}"):
                    node.set("default_order", lang_order)
            result["arch"] = etree.tostring(doc, encoding="unicode")
        return result

    def _get_transliterate_languages(self):
        return self.env['res.lang'].with_context(active_test=False).search([('transliterate', '=', True)])

    def _check_lang(self, text):
        current_lang = lang = self.env.user.lang
        installed_langs = self._get_transliterate_languages()
        transliterate = installed_langs.filtered(lambda r: r.code == lang)
        if text and lang == 'en_US':
            text_text = Text(text)
            lang_detect = text_text.language.code
            langs = installed_langs.filtered(lambda r: r.code.startswith(lang_detect))

            if len(langs) > 0:
                transliterate = True
                lang = langs[0].code
        _logger.info(f"LANG: {lang} {current_lang} {text} {self.name}")
        return lang, current_lang, transliterate

    @api.depends_context('lang')
    def _force_multilanguage(self, vals, new_record=False):
        if vals.get("city") and new_record:
            lang, current_lang, transliterate = self._check_lang(vals["city"])
            if lang != "en_US":
                if current_lang != lang:
                    record = self.with_context(**dict(self._context, lang=lang))
                    record.city = vals['city']
                record = self.with_context(**dict(self._context, lang="en_US"))
                record.city = partner_name_translate(vals["city"], lang, transliterate)
        if vals.get("street") and new_record:
            lang, current_lang, transliterate = self._check_lang(vals["street"])
            if lang != "en_US":
                if current_lang != lang:
                    record = self.with_context(**dict(self._context, lang=lang))
                    record.street = vals["street"]
                record = self.with_context(**dict(self._context, lang="en_US"))
                record.street = partner_name_translate(vals["street"], lang, transliterate)
        if vals.get("name") and new_record:
            lang, current_lang, transliterate = self._check_lang(vals["name"])
            if lang != "en_US":
                if current_lang != lang:
                    record = self.with_context(**dict(self._context, lang=lang))
                    record.name = vals["name"]
                record = self.with_context(**dict(self._context, lang="en_US"))
                record.name = partner_name_translate(vals["name"], lang, transliterate)
        if vals.get("company_name") and new_record:
            lang, current_lang, transliterate = self._check_lang(vals["company_name"])
            if lang != "en_US":
                if current_lang != lang:
                    record = self.with_context(**dict(self._context, lang=lang))
                    record.company_name = vals["company_name"]
                record = self.with_context(**dict(self._context, lang="en_US"))
                record.company_name = partner_name_translate(vals["company_name"], lang, transliterate)

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for record, vals in zip(res, vals_list):
            record._force_multilanguage(vals, new_record=True)
        return res
