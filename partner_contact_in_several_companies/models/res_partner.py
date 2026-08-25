# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

# 🚨 19.0: `odoo.osv.expression` е махнат — работата с домейни минава през
# `odoo.fields.Domain`. `Domain(args)` замества `normalize_domain`, а
# `Domain.AND` / `Domain.OR` приемат същите списъци.
from odoo.fields import Domain


class ResPartner(models.Model):
    _inherit = "res.partner"

    # 🔑 ОБИКНОВЕНО поле, НЕ computed. Радиото в диалога го превключва ръчно и
    # стойността persist-ва. Editable computed се проваляше тук: при UI onchange
    # ядрото преизчисляваше computed-а от `contact_id` (празно → standalone) и
    # връщаше ръчния „attached" назад ⇒ връзката пак се скриваше. Инвариантът
    # (attached ⇔ има contact_id) сега се пази в create()/write(). Решение на
    # Росен, 25.08.2026.
    contact_type = fields.Selection(
        [
            ("standalone", "Standalone Contact"),
            ("attached", "Attached to existing Contact"),
        ],
        store=True,
        index=True,
        default="standalone",
    )
    contact_id = fields.Many2one(
        "res.partner",
        string="Main Contact",
        domain=[("is_company", "=", False), ("contact_type", "=", "standalone")],
    )
    other_contact_ids = fields.One2many(
        "res.partner",
        "contact_id",
        string="Others Positions",
    )
    otger_function = fields.Char(
        string="Other Function",
        compute="_compute_otger_function",
    )

    @api.onchange("contact_type")
    def _onchange_contact_type(self):
        # standalone чисти връзката; двете стоят в синхрон и в UI.
        if self.contact_type == "standalone":
            self.contact_id = False

    @api.onchange("contact_id")
    def _onchange_contact_id(self):
        # избран главен контакт ⇒ attached (за UX, ако връзката се сложи първа).
        if self.contact_id:
            self.contact_type = "attached"

    @api.depends("other_contact_ids")
    def _compute_otger_function(self):
        for rec in self:
            rec.otger_function = f"{len(rec.other_contact_ids) if rec.other_contact_ids else ''} other position{len(rec.other_contact_ids) > 0 and 's' or ''}"

    def _basecontact_check_context(self, mode):
        """Remove "search_show_all_positions" for non-search mode.
        Keeping it in context can result in unexpected behavior (ex: reading
        one2many might return the wrong result - i.e. with "attached contact"
        removed even if it"s directly linked to a company).
        Actually, is easier to override a dictionary value to indicate it
        should be ignored...
        """
        if mode != "search" and "search_show_all_positions" in self.env.context:
            result = self.with_context(search_show_all_positions={"is_set": False})
        else:
            result = self
        return result

    @api.model
    def search(self, domain, offset=0, limit=None, order=None):
        # 19.0 преименува първия параметър на `domain`; тялото ползва
        # `args`, затова се пренася веднъж тук
        args = domain
        """Display only standalone contact matching ``args`` or having
        attached contact matching ``args``"""
        ctx = self.env.context
        if (
            ctx.get("search_show_all_positions", {}).get("is_set")
            and not ctx["search_show_all_positions"]["set_value"]
        ):
            args = Domain(args)
            attached_contact_args = Domain.AND(
                [args, [("contact_type", "=", "attached")]]
            )
            attached_contacts = super(ResPartner, self).search(attached_contact_args)
            args = Domain.OR(
                [
                    Domain.AND([[("contact_type", "=", "standalone")], args]),
                    [("other_contact_ids", "in", attached_contacts.ids)],
                ]
            )
        return super(ResPartner, self).search(args, offset=offset, limit=limit, order=order)

    @api.model_create_multi
    def create(self, vals_list):
        """When creating, use a modified self to alter the context (see
        comment in _basecontact_check_context).  Also, we need to ensure
        that the name on an attached contact is the same as the name on the
        contact it is attached to."""
        modified_self = self._basecontact_check_context("create")
        for vals in vals_list:
            if not vals.get("name") and vals.get("contact_id"):
                vals["name"] = modified_self.browse(vals["contact_id"]).name
            # Инвариант (заместя загубения compute): наличен главен контакт ⇒
            # attached. search() и _compute_commercial_partner стъпват на него.
            if vals.get("contact_id"):
                vals["contact_type"] = "attached"
        return super(ResPartner, modified_self).create(vals_list)

    def read(self, fields=None, load="_classic_read"):
        modified_self = self._basecontact_check_context("read")
        return super(ResPartner, modified_self).read(fields=fields, load=load)

    def write(self, vals):
        modified_self = self._basecontact_check_context("write")
        # Държи contact_type в синхрон с contact_id при запис през код
        # (onchange не тича извън UI). `write({"contact_id": False})` ⇒
        # standalone; зададен ⇒ attached.
        if "contact_id" in vals:
            vals = dict(vals)
            vals["contact_type"] = "attached" if vals.get("contact_id") else "standalone"
        return super(ResPartner, modified_self).write(vals)

    def unlink(self):
        modified_self = self._basecontact_check_context("unlink")
        return super(ResPartner, modified_self).unlink()

    def _compute_commercial_partner(self):
        """Returns the partner that is considered the commercial
        entity of this partner. The commercial entity holds the master data
        for all commercial fields (see :py:meth:`~_commercial_fields`)"""
        result = super(ResPartner, self)._compute_commercial_partner()
        for partner in self:
            if partner.contact_type == "attached" and not partner.parent_id:
                partner.commercial_partner_id = partner.contact_id
        return result

    def _contact_fields(self):
        """Returns the list of contact fields that are synced from the parent
        when a partner is attached to him."""
        return ["name", "title"]

    def _contact_sync_from_parent(self):
        """Handle sync of contact fields when a new parent contact entity
        is set, as if they were related fields
        """
        self.ensure_one()
        if self.contact_id:
            contact_fields = self._contact_fields()
            sync_vals = self.contact_id._update_fields_values(contact_fields)
            self.write(sync_vals)

    def update_contact(self, vals):
        if self.env.context.get("__update_contact_lock"):
            return
        contact_fields = self._contact_fields()
        contact_vals = {field: vals[field] for field in contact_fields if field in vals}
        if contact_vals:
            self.with_context(__update_contact_lock=True).write(contact_vals)

    def _fields_sync(self, update_values):
        """Sync commercial fields and address fields from company and to
        children, contact fields from contact and to attached contact
        after create/update, just as if those were all modeled as
        fields.related to the parent
        """
        self.ensure_one()
        res = super(ResPartner, self)._fields_sync(update_values)
        contact_fields = self._contact_fields()
        # 1. From UPSTREAM: sync from parent contact
        if update_values.get("contact_id"):
            self._contact_sync_from_parent()
        # 2. To DOWNSTREAM: sync contact fields to parent or related
        elif any(field in contact_fields for field in update_values):
            update_ids = self.other_contact_ids.filtered(lambda p: not p.is_company)
            if self.contact_id:
                update_ids |= self.contact_id
            update_ids.update_contact(update_values)
        return res

    @api.onchange("contact_id")
    def _onchange_contact_id(self):
        if self.contact_id:
            self.name = self.contact_id.name

    @api.onchange("contact_type")
    def _onchange_contact_type(self):
        if self.contact_type == "standalone":
            self.contact_id = False
