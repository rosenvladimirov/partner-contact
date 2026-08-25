# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class PartnerContactInSeveralCompaniesCase(common.TransactionCase):
    def setUp(self):
        """*****setUp*****"""
        super(PartnerContactInSeveralCompaniesCase, self).setUp()
        self.partner = self.env["res.partner"]
        self.action = self.env["ir.actions.act_window"]
        current_module = "partner_contact_in_several_companies"
        # Get test records reference
        self.main_partner = self.env.ref("base.main_partner")
        self.bob_contact = self.env.ref("%s.res_partner_contact1" % current_module)
        self.bob_job1 = self.env.ref(
            "%s.res_partner_contact1_work_position1" % current_module
        )
        self.roger_contact = self.env.ref("base.res_partner_main2")
        self.roger_job2 = self.env.ref(
            "%s.res_partner_main2_position_consultant" % current_module
        )

    def test_00_show_only_standalone_contact(self):
        """Check that only standalone contact are shown if context
        explicitly state to not display all positions
        """
        ctx = {"search_show_all_positions": {"is_set": True, "set_value": False}}
        partner_ids = self.partner.with_context(**ctx).search([])
        self.assertTrue(self.bob_job1 not in partner_ids)
        self.assertTrue(self.roger_job2 not in partner_ids)

    def test_01_show_all_positions(self):
        """Check that all contact are show if context is empty or
        explicitly state to display all positions or the "is_set"
        value has been set to False.
        """

        partner_ids = self.partner.search([])
        self.assertTrue(self.bob_job1 in partner_ids)
        self.assertTrue(self.roger_job2 in partner_ids)

        ctx = {"search_show_all_positions": {"is_set": False}}
        partner_ids = self.partner.with_context(**ctx).search([])
        self.assertTrue(self.bob_job1 in partner_ids)
        self.assertTrue(self.roger_job2 in partner_ids)

        ctx = {"search_show_all_positions": {"is_set": True, "set_value": True}}
        partner_ids = self.partner.with_context(**ctx).search([])
        self.assertTrue(self.bob_job1 in partner_ids)
        self.assertTrue(self.roger_job2 in partner_ids)

    def test_02_reading_other_contact_one2many_show_all_positions(self):
        """Check that readonly partner's ``other_contact_ids`` return
        all values whatever the context
        """

        ctx = {}
        self.assertEqual(
            self.bob_job1, self.bob_contact.with_context(**ctx).other_contact_ids
        )
        ctx = {"search_show_all_positions": {"is_set": False}}
        self.assertEqual(
            self.bob_job1, self.bob_contact.with_context(**ctx).other_contact_ids
        )
        ctx = {"search_show_all_positions": {"is_set": True, "set_value": False}}
        self.assertEqual(
            self.bob_job1, self.bob_contact.with_context(**ctx).other_contact_ids
        )
        ctx = {"search_show_all_positions": {"is_set": True, "set_value": True}}
        self.assertEqual(
            self.bob_job1, self.bob_contact.with_context(**ctx).other_contact_ids
        )

        ctx = {}
        self.assertIn(self.bob_job1, self.main_partner.with_context(**ctx).child_ids)
        ctx = {"search_show_all_positions": {"is_set": False}}
        self.assertIn(self.bob_job1, self.main_partner.with_context(**ctx).child_ids)
        ctx = {"search_show_all_positions": {"is_set": True, "set_value": False}}
        self.assertIn(self.bob_job1, self.main_partner.with_context(**ctx).child_ids)
        ctx = {"search_show_all_positions": {"is_set": True, "set_value": True}}
        self.assertIn(self.bob_job1, self.main_partner.with_context(**ctx).child_ids)

    def test_03_search_match_attached_contacts(self):
        """Check that searching partner also return partners having
        attached contacts matching search criteria
        """
        # Bob's contact has one other position which is related to
        # 'YourCompany'
        # so search for all contacts working for 'YourCompany'
        # should contain Bob position.
        partner_ids = self.partner.search([("parent_id", "ilike", "YourCompany")])
        self.assertTrue(self.bob_job1 in partner_ids)

        # but when searching without 'all positions',
        # we should get the position standalone contact instead.
        ctx = {"search_show_all_positions": {"is_set": True, "set_value": False}}
        partner_ids = self.partner.with_context(**ctx).search(
            [("parent_id", "ilike", "YourCompany")]
        )
        self.assertTrue(self.bob_contact in partner_ids)

    def test_04_contact_creation(self):
        """Check that we're begin to create a contact"""

        # Create a contact using only name
        new_contact = self.partner.create({"name": "Bob Egnops"})
        self.assertEqual(new_contact.contact_type, "standalone")

        # Create a contact with only contact_id
        new_contact = self.partner.create({"contact_id": self.bob_contact.id})
        self.assertEqual(new_contact.name, "Bob Egnops")
        self.assertEqual(new_contact.contact_type, "attached")

        # Create a contact with both contact_id and name;
        # contact's name should override provided value in that case
        new_contact = self.partner.create(
            {"contact_id": self.bob_contact.id, "name": "Rob Egnops"}
        )
        self.assertEqual(new_contact.name, "Bob Egnops")

        # Reset contact to standalone
        new_contact.write({"contact_id": False})
        self.assertEqual(new_contact.contact_type, "standalone")

        # Reset contact to attached, and ensure only it is unlinked (i.e.
        # context is ignored).
        new_contact.write({"contact_id": self.bob_contact.id})
        ctx = {"search_show_all_positions": {"is_set": True, "set_value": True}}
        new_contact.with_context(**ctx).unlink()
        partner_ids = self.partner.with_context(**ctx).search(
            [("id", "in", [new_contact.id, self.bob_contact.id])]
        )
        self.assertIn(self.bob_contact, partner_ids)
        self.assertNotIn(new_contact, partner_ids)

    def test_05_contact_fields_sync(self):
        """Check that contact's fields are correctly synced between
        parent contact or related contacts
        """

        # Test DOWNSTREAM sync
        self.bob_contact.write({"name": "Rob Egnops"})
        self.assertEqual(self.bob_job1.name, "Rob Egnops")

        # Test UPSTREAM sync
        self.bob_job1.write({"name": "Bob Egnops"})
        self.assertEqual(
            self.bob_contact.name,
            "Bob Egnops",
        )

    def test_06_ir_action(self):
        """Check ir_action context is auto updated."""

        new_context_val = (
            "'search_show_all_positions': " "{'is_set': True, 'set_value': False}"
        )

        xmlid = "base.action_partner_form"
        details = self.env["ir.actions.act_window"]._for_xml_id(xmlid)

        self.assertIn(
            new_context_val,
            details["context"],
            msg="Default actions not updated with new context",
        )

        xmlid = "partner_contact_in_several_companies.action_partner_form"
        details = self.env["ir.actions.act_window"]._for_xml_id(xmlid)

        self.assertNotIn(
            new_context_val,
            details["context"],
            msg="Custom actions incorrectly updated with new context",
        )

    def test_07_onchange(self):
        """Check onchange method"""

        new_contact = self.partner.create({"name": "Bob before onchange"})
        new_contact.write({"contact_id": self.bob_contact.id})
        new_contact._onchange_contact_id()
        self.assertEqual(new_contact.name, "Bob Egnops")

        new_contact.write({"contact_type": "standalone"})
        new_contact._onchange_contact_type()
        self.assertEqual(new_contact.contact_id, self.partner)

    def test_08_commercial_partner_compute(self):
        new_contact = self.partner.create({"name": "Bob before onchange"})
        new_contact.write({"contact_id": self.bob_contact.id, "parent_id": False})
        new_contact._compute_commercial_partner()
        self.assertEqual(
            new_contact.commercial_partner_id,
            self.bob_contact,
        )

    def test_09_contact_type_is_manually_editable(self):
        """Радиото Standalone/Attached трябва да е editable в диалога.

        Дефектът (erp3, 25.08.2026): `contact_type` беше computed БЕЗ
        `readonly=False` ⇒ readonly в UI ⇒ юзърът не можеше да превключи на
        „attached", а без това полето с връзката (`contact_id`) стоеше вечно
        скрито. Този assert пада на стария код и минава на поправения.
        """
        field = self.partner._fields["contact_type"]
        self.assertFalse(
            field.readonly,
            "contact_type трябва да е editable (readonly=False), за да работи "
            "радиото в диалога за добавяне на контакт",
        )

    def test_10_standalone_clears_the_link(self):
        """Ръчното превключване на standalone чисти висящата връзка.

        Пази инварианта, на който стъпва `_compute_commercial_partner`:
        standalone контакт няма главен контакт.
        """
        rec = self.partner.new({"contact_id": self.bob_contact.id})
        self.assertEqual(rec.contact_type, "attached")
        rec.contact_type = "standalone"
        rec._onchange_contact_type()
        self.assertFalse(
            rec.contact_id,
            "standalone трябва да изчисти contact_id, за да не остане висяща "
            "връзка",
        )

    def test_11_create_attached_syncs_without_crash(self):
        """Създаване на attached контакт не гърми и пренася името.

        Заварен o19 дефект (erp3, 25.08.2026): `_contact_sync_from_parent`
        викаше `_update_fields_values` (махнат в o19) и `_contact_fields`
        връщаше `title` (махнато от res.partner в o19) ⇒ всеки attached контакт
        хвърляше AttributeError още при запис. Никой не стигаше дотам, защото
        връзката не се показваше в диалога.
        """
        child = self.partner.create(
            {"contact_id": self.bob_contact.id, "type": "contact"}
        )
        self.assertEqual(child.contact_type, "attached")
        self.assertEqual(child.name, self.bob_contact.name)
        # синхронът чете само реално съществуващи полета
        self.assertNotIn("title", child._contact_fields())
