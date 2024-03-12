# Copyright 2024 Kıta Yazılım
# License LGPLv3 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import _, api, fields, models


class CustomTreeViewFieldKita(models.Model):

    _name = "custom.tree.view.field.kita"
    _description = "Özelleştirilebilir tree view field"  # TODO
    _order = "model_id, sequence, id"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer()
    model_id = fields.Many2one(
        comodel_name="ir.model", required=True, ondelete="cascade"
    )
    field_id = fields.Many2one(
        comodel_name="ir.model.fields",
        domain="[('model_id', '=', model_id)]",
        required=True,
        ondelete="cascade",
    )
    model_name = fields.Char(
        related="model_id.model",
        store=True,
        readonly=True,
        index=True,
        string="Model name",
    )
    optional = fields.Selection(
        selection=[
            ("hide", "Gizle"),
            ("show", "Göster"),
        ],
        string="Görünebilirlik",
        default="hide",
    )
    position_after = fields.Char(
        help="Optional field name for putting the filter after that one. "
        "If empty or not found, it will be put at the end.",
    )

    def _get_related_field(self):
        """Determine the chain of fields."""
        self.ensure_one()
        related = self.field_id
        target = self.env[self.model_name]
        for name in related:
            field = target._fields[name]
            target = target[name]
        return field
