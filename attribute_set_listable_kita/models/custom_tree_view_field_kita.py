# Copyright 2024 Kıta Yazılım
# License LGPLv3 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import fields, models


class IrUiCustomFieldFilter(models.Model):

    _inherit = "custom.tree.view.field.kita"

    attribute_id = fields.Many2one("attribute.attribute", ondelete="cascade")
