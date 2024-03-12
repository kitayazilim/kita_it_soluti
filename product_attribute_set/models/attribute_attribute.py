from odoo import models


class AttributeAttribute(models.Model):
    _inherit = "attribute.attribute"

    def _create_custom_filter(self):
        res = super()._create_custom_filter()
        if res.model_name == "product.template":
            product_product_model = self.env["ir.model"].search(
                [("model", "=", "product.product")]
            )
            data = {
                "model_id": product_product_model.id,
                "name": self.field_description,
                "expression": self.name,
                "sequence": self.sequence,
                "attribute_id": self.id,
            }
            self.env["ir.ui.custom.field.filter"].create(data)

    def _update_custom_filter(self, custom_filter):
        self.ensure_one()
        for item in custom_filter:
            data = {}
            if item.name != self.field_description:
                data.update({"name": self.field_description})
            if item.expression != self.name:
                data.update({"expression": self.name})
            if item.sequence != self.sequence:
                data.update({"sequence": self.sequence})
            if data:
                item.write(data)
