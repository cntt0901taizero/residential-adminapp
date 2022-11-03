from builtins import print

from odoo import models, fields


class tb_feekind(models.Model):
    _name = 'tb_feekind'
    _description = 'Danh mục loại phí'

    code = fields.Char(string='Mã loại phí', required=True, copy=False)
    name = fields.Char(string='Tên loại phí', required=True, copy=False)
    note = fields.Text(string='Ghi chú', copy=False, help='Ghi rõ ràng các khoản phí (nếu có)')
    is_active = fields.Boolean(string='Trạng thái', default=True)

    def set_status_active(self):
        self.is_active = True




