# Copyright 2024 Kıta Yazılım
# License LGPLv3 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import api, fields, models


class AttributeAttribute(models.Model):

    _inherit = "attribute.attribute"

    listable = fields.Boolean(
        default=False,
        string="Listele",
        help="Modelin Tree viewlarında listelemek için işaretlemeniz yeterli",
    )

    def _get_custom_field(self):
        self.ensure_one()
        return self.env["custom.tree.view.field.kita"].search(
            [("attribute_id", "=", self.id)]
        )

    def _prepare_create_custom_field(self):
        self.ensure_one()
        model_id = self.attribute_group_id.model_id
        field_id = self.env["ir.model.fields"].search(
            [("model_id", "=", model_id.id), ("name", "=", self.name)]
        )
        return {
            "model_id": model_id.id,
            "field_id": field_id.id,
            "name": self.field_description,
            "optional": "show",
            "sequence": self.sequence,
            "attribute_id": self.id,
        }

    def _create_custom_field(self):
        data = self._prepare_create_custom_field()
        obj = self.env["custom.tree.view.field.kita"].create(data)
        if obj.model_name == "product.template":
            product_product_model = self.env["ir.model"].search(
                [("model", "=", "product.product")]
            )
            field_id = self.env["ir.model.fields"].search(
                [("model_id", "=", product_product_model.id), ("name", "=", self.name)]
            )
            new_data = {
                "model_id": product_product_model.id,
                "field_id": field_id.id,
                "name": obj.name,
                "optional": obj.optional,
                "sequence": self.sequence,
                "attribute_id": self.id,
            }
            self.env["custom.tree.view.field.kita"].create(new_data)

        return obj

    def _update_custom_field(self, custom_field):
        for field in custom_field:
            self.ensure_one()
            data = {}
            if field.name != self.field_description:
                data.update({"name": self.field_description})
            if field.sequence != self.sequence:
                data.update({"sequence": self.sequence})
            if data:
                field.write(data)

    def write(self, vals):
        res = super(AttributeAttribute, self).write(vals)
        for attribute in self:
            custom_field = self._get_custom_field()
            if attribute.listable:
                if not custom_field:
                    self._create_custom_field()
                else:
                    self._update_custom_field(custom_field)
            elif custom_field:
                custom_field.unlink()
        return res

    @api.model_create_multi
    @api.returns("self", lambda value: value.id)
    def create(self, vals_list):
        attributes = super(AttributeAttribute, self).create(vals_list)
        list_attributes = attributes.filtered(lambda att: att.listable)
        for attribute in list_attributes:
            attribute._create_custom_field()
        return attributes
