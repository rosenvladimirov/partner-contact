#  Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from lxml import etree
from odoo import fields, models, api, _

_logger = logging.getLogger(__name__)


class Users(models.Model):
    _inherit = ['res.users', 'res.transliterate.mixin']
    _name = "res.users"

    name = fields.Char(translate=True)

    @api.depends_context('lang')
    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        lang_order = f'name-->>"{self.env.user.lang}"'
        result = super(Users, self).get_view(
            view_id=view_id, view_type=view_type, **options
        )
        if view_type in ["tree", "kanban"]:
            doc = etree.XML(result["arch"])
            for type_in in ["tree", "kanban"]:
                for node in doc.xpath(f"//{type_in}"):
                    node.set("default_order", lang_order)
            result["arch"] = etree.tostring(doc, encoding="unicode")
        return result
