# Copyright 2024 Kıta Yazılım
# License LGPLv3 or later (https://www.gnu.org/licenses/lgpl-3.0).

from lxml import etree
from odoo import _, api, fields, models


class Base(models.AbstractModel):

    _inherit = "base"

    @api.model
    def _add_custom_field_on_tree(self, res, custom_fields):
        arch = etree.fromstring(res["arch"])
        for custom_field in custom_fields:
            node = False
            if custom_field.position_after:
                node = arch.xpath("//field[@name='%s']" % custom_field.position_after)
            if not node:
                node = arch.xpath("//field[last()]")
            if node:
                elem = etree.Element(
                    "field",
                    {
                        "name": custom_field.field_id.name,
                        "string": custom_field.name,
                        "optional": custom_field.optional,
                    },
                )
                node[0].addnext(elem)
        res["arch"] = etree.tostring(arch)
        return res

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        """Inject fields field in tree views."""
        res = super().get_view(view_id, view_type, **options)
        if view_type == "tree":
            custom_fields = self.env["custom.tree.view.field.kita"].search(
                [("model_name", "=", res.get("model"))]
            )
            if custom_fields:
                res = self._add_custom_field_on_tree(res, custom_fields)
        return res

    # @api.model
    # def get_views(self, views, options=None):
    #     """Inject fake field definition for having custom fields available."""
    #     res = super().get_views(views, options)
    #     custom_fields = self.env["custom.tree.view.field.kita"].search(
    #         [("model_name", "=", self._name)]
    #     )
    #     for custom_field in custom_fields:
    #        field = custom_field.field_id
    #        field_name = custom_field.field_id.name
    #        res["models"][self._name][field_name] = field.field_description
    #        force this for avoiding to appear on the rest of the UI
    #        if "selectable" in res["models"][self._name][field_name]:
    #            res["models"][self._name][field_name]["selectable"] = False
    #        if "sortable" in res["models"][self._name][field_name]:
    #            res["models"][self._name][field_name]["sortable"] = False
    #        if "store" in res["models"][self._name][field_name]:
    #            res["models"][self._name][field_name]["store"] = False
    #     return res
